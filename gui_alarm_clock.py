import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time
import threading
import os
import json
import subprocess
import sys

# Try pygame for sound (optional). If it's not available, we'll fall back to macOS tools.
try:
    import pygame
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False

ALARM_STORE = "alarms.json"       # alarms persistence
SETTINGS_STORE = "settings.json"  # UI/theme persistence


def mac_fallback_alert(seconds: int = 3):
    """
    macOS fallback: try 'afplay' on a system sound; else 'say'; else terminal bell.
    """
    system_sounds = [
        "/System/Library/Sounds/Glass.aiff",
        "/System/Library/Sounds/Ping.aiff",
        "/System/Library/Sounds/Pop.aiff",
        "/System/Library/Sounds/Blow.aiff",
    ]

    def _afplay(path):
        try:
            subprocess.Popen(["afplay", path])
            time.sleep(seconds)
            return True
        except Exception:
            return False

    for s in system_sounds:
        if os.path.exists(s) and _afplay(s):
            return

    try:
        subprocess.call(["say", "Alarm ringing"])
        return
    except Exception:
        pass

    for _ in range(3):
        print("\a", end="", flush=True)
        time.sleep(0.25)


def play_alert(sound_file: str | None = None, duration_seconds: int = 3):
    """
    Master alert for macOS:
    - Use pygame if available and a file is provided
    - Else use macOS 'afplay'/'say'
    - Else terminal bell
    """
    if HAS_PYGAME:
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            if sound_file and os.path.exists(sound_file):
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
                time.sleep(duration_seconds)
                pygame.mixer.music.stop()
                return
        except Exception:
            pass

    mac_fallback_alert(duration_seconds)


def is_valid_hhmm(s: str) -> bool:
    """Return True if s is a valid 24-hour 'HH:MM' time string."""
    try:
        time.strptime(s, "%H:%M")
        return True
    except ValueError:
        return False


def _detect_macos_dark_mode() -> bool:
    """Best-effort macOS dark-mode detection (used on first run only)."""
    if sys.platform != "darwin":
        return False
    try:
        # Returns 'Dark' when dark mode is enabled, non-zero exit code otherwise
        out = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True,
        )
        return "Dark" in out.stdout
    except Exception:
        return False


class AlarmClock:
    """
    Stores alarms as dicts:
    {
        "time": "HH:MM",
        "label": "Wake up",
        "repeat": "daily" | "none",
        "enabled": True
    }
    """

    # Treeview column sizing weights (sum ≈ 1.0)
    COL_WEIGHTS = (0.14, 0.18, 0.54, 0.14)  # enabled, time, label, repeat

    def __init__(self, sound_file: str | None = None):
        # Window
        self.window = tk.Tk()
        self.window.title("Capstone Alarm Clock")
        self.window.minsize(520, 380)

        # HiDPI scaling for macOS Retina (tweak if text feels too small/large)
        try:
            if sys.platform == "darwin":
                self.window.tk.call("tk", "scaling", 1.4)
        except Exception:
            pass

        # Data
        self.sound_file = sound_file
        self.alarms: list[dict] = self._load_alarms()
        self.settings = self._load_settings()
        self.is_dark = self.settings.get("dark_mode", _detect_macos_dark_mode())

        self._stop_event = threading.Event()
        self._checker_thread = threading.Thread(target=self._check_loop, daemon=True)
        self._last_rung_keys = set()  # to avoid ringing multiple times within the same minute

        # Theme + UI
        self._init_style()
        self._apply_theme(self.is_dark)
        self._build_ui()

        # Start background checker
        self._checker_thread.start()

        # Clean shutdown
        self.window.protocol("WM_DELETE_WINDOW", self._on_close)

    # ---------- Persistence ----------
    def _load_alarms(self) -> list[dict]:
        if os.path.exists(ALARM_STORE):
            try:
                with open(ALARM_STORE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                out = []
                for a in data:
                    if isinstance(a, dict) and "time" in a and is_valid_hhmm(a["time"]):
                        out.append({
                            "time": a.get("time", "07:30"),
                            "label": a.get("label", "Alarm"),
                            "repeat": a.get("repeat", "none"),
                            "enabled": bool(a.get("enabled", True)),
                        })
                return out
            except Exception:
                return []
        return []

    def _save_alarms(self):
        try:
            with open(ALARM_STORE, "w", encoding="utf-8") as f:
                json.dump(self.alarms, f, indent=2)
        except Exception:
            pass  # non-fatal

    def _load_settings(self) -> dict:
        if os.path.exists(SETTINGS_STORE):
            try:
                with open(SETTINGS_STORE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_settings(self):
        try:
            with open(SETTINGS_STORE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass

    # ---------- Theme / Style ----------
    def _init_style(self):
        self.style = ttk.Style(self.window)
        # Use a ttk theme that accepts color overrides (clam works well cross-platform)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

    def _apply_theme(self, dark: bool):
        """Apply dark or light palette to ttk widgets and base window."""
        # Palette
        if dark:
            bg = "#1f2430"
            surface = "#2a2f3a"
            fg = "#e6e6e6"
            subtle = "#9aa4b2"
            accent = "#3d7eff"
            danger = "#ff5c5c"
            entry_bg = "#303645"
            sel_bg = "#44506a"
        else:
            bg = "#f7f7f9"
            surface = "#ffffff"
            fg = "#1a1a1a"
            subtle = "#606770"
            accent = "#2f6fed"
            danger = "#c83e3e"
            entry_bg = "#ffffff"
            sel_bg = "#d9e2ff"

        # Root window
        self.window.configure(bg=bg)

        # Frame/Label/Button
        self.style.configure("TFrame", background=bg)
        self.style.configure("Surface.TFrame", background=surface)
        self.style.configure("TLabel", background=bg, foreground=fg)
        self.style.configure("Subtle.TLabel", foreground=subtle, background=bg)

        self.style.configure("TButton", background=surface, foreground=fg)
        self.style.map("TButton",
                       background=[("active", sel_bg)],
                       foreground=[("disabled", subtle)])

        self.style.configure("Accent.TButton", background=accent, foreground="#ffffff")
        self.style.map("Accent.TButton",
                       background=[("active", accent)],
                       foreground=[("disabled", "#dddddd")])

        self.style.configure("Danger.TButton", background=danger, foreground="#ffffff")

        # Entry / Checkbutton
        self.style.configure("TEntry", fieldbackground=entry_bg, foreground=fg, insertcolor=fg)
        self.style.configure("TCheckbutton", background=bg, foreground=fg)

        # Treeview
        self.style.configure(
            "Treeview",
            background=surface,
            fieldbackground=surface,
            foreground=fg,
            rowheight=24,
            bordercolor=bg,
            lightcolor=bg,
            darkcolor=bg,
        )
        self.style.configure("Treeview.Heading", background=surface, foreground=fg)
        self.style.map("Treeview", background=[("selected", sel_bg)], foreground=[("selected", "#ffffff")])

        # Save & remember
        self.is_dark = dark
        self.settings["dark_mode"] = bool(dark)
        self._save_settings()

    # ---------- UI ----------
    def _build_ui(self):
        # Layout grid: 4 rows (header, add-form, list, footer)
        for r, w in ((0, 0), (1, 0), (2, 1), (3, 0)):
            self.window.rowconfigure(r, weight=w)
        self.window.columnconfigure(0, weight=1)

        # Header
        header = ttk.Frame(self.window, padding=(12, 10))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        self.current_time_label = ttk.Label(header, text="Current Time: ", font=("Arial", 12))
        self.current_time_label.grid(row=0, column=0, sticky="w")
        self._tick_clock()

        # Add form
        add_frame = ttk.Frame(self.window, padding=(12, 6))
        add_frame.grid(row=1, column=0, sticky="ew")
        for c in range(6):
            add_frame.columnconfigure(c, weight=1 if c in (1, 3) else 0)

        ttk.Label(add_frame, text="Time (HH:MM):").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
        self.time_entry = ttk.Entry(add_frame, justify="center", width=10)
        self.time_entry.insert(0, "07:30")
        self.time_entry.grid(row=0, column=1, sticky="ew", pady=4)

        ttk.Label(add_frame, text="Label:").grid(row=0, column=2, sticky="w", padx=(12, 8), pady=4)
        self.label_entry = ttk.Entry(add_frame)
        self.label_entry.insert(0, "Alarm")
        self.label_entry.grid(row=0, column=3, sticky="ew", pady=4)

        self.repeat_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(add_frame, text="Repeat daily", variable=self.repeat_var).grid(
            row=0, column=4, sticky="w", padx=(12, 8), pady=4
        )

        ttk.Button(add_frame, text="Add Alarm", style="Accent.TButton", command=self._add_alarm).grid(
            row=0, column=5, sticky="e", pady=4
        )

        # List
        list_frame = ttk.Frame(self.window, padding=(12, 6))
        list_frame.grid(row=2, column=0, sticky="nsew")
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        columns = ("enabled", "time", "label", "repeat")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        self.tree.heading("enabled", text="Enabled")
        self.tree.heading("time", text="Time")
        self.tree.heading("label", text="Label")
        self.tree.heading("repeat", text="Repeat")
        self.tree.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscroll=sb.set)

        self._refresh_tree()
        self.tree.bind("<Configure>", lambda e: self._apply_tree_column_widths())

        # Footer
        footer = ttk.Frame(self.window, padding=(12, 8))
        footer.grid(row=3, column=0, sticky="ew")
        for c in range(5):
            footer.columnconfigure(c, weight=1 if c == 4 else 0)

        ttk.Button(footer, text="Toggle Enable", command=self._toggle_selected).grid(row=0, column=0, sticky="w")
        ttk.Button(footer, text="Edit Selected", command=self._edit_selected).grid(row=0, column=1, sticky="w")
        ttk.Button(footer, text="Delete Selected", style="Danger.TButton", command=self._delete_selected).grid(
            row=0, column=2, sticky="w"
        )

        # Dark mode toggle on the right
        self.dark_btn = ttk.Button(
            footer,
            text="Dark Mode: ON" if self.is_dark else "Dark Mode: OFF",
            command=self._toggle_theme,
        )
        self.dark_btn.grid(row=0, column=4, sticky="e")

        # Status
        self.status_label = ttk.Label(self.window, text="Ready", style="Subtle.TLabel")
        self.status_label.grid(row=4, column=0, sticky="e", padx=12, pady=(0, 8))

        # Apply palette to initial widgets
        self._apply_theme(self.is_dark)

    def _apply_tree_column_widths(self):
        total = max(self.tree.winfo_width() - 18, 200)
        widths = [int(total * w) for w in self.COL_WEIGHTS]
        cols = ("enabled", "time", "label", "repeat")
        anchors = {"enabled": "center", "time": "center", "label": "w", "repeat": "center"}
        for col, w in zip(cols, widths):
            self.tree.column(col, width=w, stretch=True, anchor=anchors[col])

    def _tick_clock(self):
        self.current_time_label.config(text=f"Current Time: {time.strftime('%H:%M:%S')}")
        self.window.after(1000, self._tick_clock)

    def _set_status(self, text: str):
        self.status_label.config(text=text)

    # ---------- Theme toggle ----------
    def _toggle_theme(self):
        self._apply_theme(not self.is_dark)
        self.dark_btn.config(text="Dark Mode: ON" if self.is_dark else "Dark Mode: OFF")

    # ---------- Actions ----------
    def _refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, a in enumerate(self.alarms):
            self.tree.insert(
                "",
                "end",
                iid=str(idx),
                values=(
                    "ON" if a.get("enabled", True) else "OFF",
                    a.get("time", "??:??"),
                    a.get("label", ""),
                    "daily" if a.get("repeat") == "daily" else "once",
                ),
            )

    def _add_alarm(self):
        t = self.time_entry.get().strip()
        label = self.label_entry.get().strip() or "Alarm"
        repeat = "daily" if self.repeat_var.get() else "none"
        if not is_valid_hhmm(t):
            messagebox.showerror("Invalid Time", "Enter time in HH:MM (24-hour), e.g., 07:30")
            return
        self.alarms.append({"time": t, "label": label, "repeat": repeat, "enabled": True})
        self._save_alarms()
        self._refresh_tree()
        self._set_status(f"Added alarm {t} ({label})")

    def _get_selected_index(self) -> int | None:
        sel = self.tree.selection()
        if not sel:
            return None
        try:
            return int(sel[0])
        except Exception:
            return None

    def _toggle_selected(self):
        idx = self._get_selected_index()
        if idx is None:
            messagebox.showinfo("Select Alarm", "Please select an alarm to toggle.")
            return
        self.alarms[idx]["enabled"] = not self.alarms[idx].get("enabled", True)
        self._save_alarms()
        self._refresh_tree()

    def _delete_selected(self):
        idx = self._get_selected_index()
        if idx is None:
            messagebox.showinfo("Select Alarm", "Please select an alarm to delete.")
            return
        a = self.alarms[idx]
        if messagebox.askyesno("Delete Alarm", f"Delete '{a.get('label','Alarm')}' at {a.get('time')}?"):
            self.alarms.pop(idx)
            self._save_alarms()
            self._refresh_tree()
            self._set_status("Alarm deleted")

    def _edit_selected(self):
        idx = self._get_selected_index()
        if idx is None:
            messagebox.showinfo("Select Alarm", "Please select an alarm to edit.")
            return
        a = self.alarms[idx]

        new_time = simpledialog.askstring("Edit Time", "Enter new time (HH:MM):", initialvalue=a.get("time"))
        if new_time is None:
            return
        if not is_valid_hhmm(new_time.strip()):
            messagebox.showerror("Invalid Time", "Enter time in HH:MM (24-hour), e.g., 07:30")
            return

        new_label = simpledialog.askstring("Edit Label", "Enter label:", initialvalue=a.get("label", "Alarm"))
        if new_label is None:
            return

        repeat_answer = messagebox.askyesno("Repeat", "Repeat daily?")
        new_repeat = "daily" if repeat_answer else "none"

        a["time"] = new_time.strip()
        a["label"] = (new_label or "Alarm").strip()
        a["repeat"] = new_repeat
        a["enabled"] = True
        self._save_alarms()
        self._refresh_tree()
        self._set_status("Alarm updated")

    # ---------- Alarm checking ----------
    def _check_loop(self):
        """Background worker: checks every second and schedules UI triggers."""
        while not self._stop_event.is_set():
            now_hm = time.strftime("%Y%m%d-%H:%M")  # include date to avoid re-ringing next day
            hm_only = now_hm.split("-")[1]
            today_key_prefix = now_hm.split("-")[0]

            # ring any enabled alarm that matches HH:MM
            for idx, a in enumerate(list(self.alarms)):
                if not a.get("enabled", True):
                    continue
                if a.get("time") == hm_only:
                    key = f"{today_key_prefix}-{idx}-{a.get('time')}"
                    if key in self._last_rung_keys:
                        continue  # already rang for this minute
                    self._last_rung_keys.add(key)
                    # schedule UI trigger
                    self.window.after(0, self._trigger_alarm_ui, idx)

            time.sleep(1)

    def _trigger_alarm_ui(self, idx: int):
        if idx < 0 or idx >= len(self.alarms):
            return
        a = self.alarms[idx]
        if not a.get("enabled", True):
            return

        # Play sound + popup
        play_alert(self.sound_file, duration_seconds=3)
        messagebox.showinfo("⏰ ALARM!", f"{a.get('label','Alarm')} — it's {a.get('time')}")

        # One-time alarms disable after ringing
        if a.get("repeat") == "none":
            a["enabled"] = False
        self._save_alarms()
        self._refresh_tree()

    # ---------- Shutdown ----------
    def _on_close(self):
        self._stop_event.set()
        try:
            if HAS_PYGAME and getattr(pygame, "mixer", None) and pygame.mixer.get_init():
                pygame.mixer.quit()
        except Exception:
            pass
        self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    # Optional: set a path to a custom sound file (e.g., "alarm.wav")
    SOUND_FILE = None
    app = AlarmClock(sound_file=SOUND_FILE)
    app.run()