import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import time
import threading
import os
import json
import subprocess

# Try pygame for sound (optional). If it's not available, we'll fall back to macOS tools.
try:
    import pygame
    HAS_PYGAME = True
except Exception:
    HAS_PYGAME = False


ALARM_STORE = "alarms.json"  # simple persistence in current folder


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
            else:
                # If no file provided, just use fallback (afplay/say/bell)
                pass
        except Exception:
            pass

    mac_fallback_alert(duration_seconds)


def is_valid_hhmm(s: str) -> bool:
    try:
        time.strptime(s, "%H:%M")
        return True
    except ValueError:
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
    def __init__(self, sound_file: str | None = None):
        # Window
        self.window = tk.Tk()
        self.window.title("Capstone Alarm Clock")
        self.window.geometry("480x360")
        self.window.minsize(460, 340)

        # Data
        self.sound_file = sound_file
        self.alarms: list[dict] = self._load_alarms()
        self._stop_event = threading.Event()
        self._checker_thread = threading.Thread(target=self._check_loop, daemon=True)
        self._last_rung_keys = set()  # to avoid ringing multiple times within the same minute

        # UI
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
                # minimal validation
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
            # non-fatal
            pass

    # ---------- UI ----------
    def _build_ui(self):
        # Top: current time
        self.current_time_label = tk.Label(self.window, text="Current Time: ", font=("Arial", 12))
        self.current_time_label.pack(pady=8)
        self._tick_clock()

        # Frame: add alarm
        add_frame = tk.Frame(self.window)
        add_frame.pack(fill="x", padx=12, pady=6)

        tk.Label(add_frame, text="Time (HH:MM):").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.time_entry = tk.Entry(add_frame, width=8, justify="center")
        self.time_entry.insert(0, "07:30")
        self.time_entry.grid(row=0, column=1, sticky="w")

        tk.Label(add_frame, text="Label:").grid(row=0, column=2, sticky="w", padx=(12, 8))
        self.label_entry = tk.Entry(add_frame, width=18)
        self.label_entry.insert(0, "Alarm")
        self.label_entry.grid(row=0, column=3, sticky="w")

        self.repeat_var = tk.BooleanVar(value=False)
        tk.Checkbutton(add_frame, text="Repeat daily", variable=self.repeat_var).grid(row=0, column=4, padx=(12, 8))

        tk.Button(add_frame, text="Add Alarm", bg="lightgreen", command=self._add_alarm).grid(row=0, column=5, padx=(12, 0))

        # Middle: list of alarms
        list_frame = tk.Frame(self.window)
        list_frame.pack(fill="both", expand=True, padx=12, pady=6)

        columns = ("enabled", "time", "label", "repeat")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=8)
        for col, w in zip(columns, (80, 80, 220, 80)):
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=w, anchor="center" if col in ("enabled", "time", "repeat") else "w")
        self.tree.pack(side="left", fill="both", expand=True)

        sb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=sb.set)
        sb.pack(side="right", fill="y")

        self._refresh_tree()

        # Bottom: action buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(fill="x", padx=12, pady=8)

        tk.Button(btn_frame, text="Toggle Enable", command=self._toggle_selected).pack(side="left")
        tk.Button(btn_frame, text="Edit Selected", command=self._edit_selected).pack(side="left", padx=8)
        tk.Button(btn_frame, text="Delete Selected", command=self._delete_selected, fg="red", bg="#cc4444").pack(side="left")

        self.status_label = tk.Label(self.window, text="Ready", fg="gray")
        self.status_label.pack(pady=(4, 8))

    def _tick_clock(self):
        self.current_time_label.config(text=f"Current Time: {time.strftime('%H:%M:%S')}")
        self.window.after(1000, self._tick_clock)

    def _refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, a in enumerate(self.alarms):
            self.tree.insert("", "end", iid=str(idx), values=(
                "ON" if a.get("enabled", True) else "OFF",
                a.get("time", "??:??"),
                a.get("label", ""),
                "daily" if a.get("repeat") == "daily" else "once"
            ))

    def _set_status(self, text: str, color="gray"):
        self.status_label.config(text=text, fg=color)

    # ---------- Actions ----------
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
        self._set_status(f"Added alarm {t} ({label})", "green")

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
            self._set_status("Alarm deleted", "red")

    def _edit_selected(self):
        idx = self._get_selected_index()
        if idx is None:
            messagebox.showinfo("Select Alarm", "Please select an alarm to edit.")
            return
        a = self.alarms[idx]

        # Simple edit dialog using simpledialog for time/label; repeat via yes/no dialog.
        new_time = simpledialog.askstring("Edit Time", "Enter new time (HH:MM):", initialvalue=a.get("time"))
        if new_time is None:
            return  # cancelled
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
        a["enabled"] = True  # re-enable on edit by default
        self._save_alarms()
        self._refresh_tree()
        self._set_status("Alarm updated", "green")

    # ---------- Alarm checking ----------
    def _check_loop(self):
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

        # Play sound
        play_alert(self.sound_file, duration_seconds=3)

        # UI message
        messagebox.showinfo("⏰ ALARM!", f"{a.get('label','Alarm')} — it's {a.get('time')}")

        # Post-ring behavior
        if a.get("repeat") == "none":
            a["enabled"] = False  # one-time: disable
        # if daily: keep enabled for tomorrow

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