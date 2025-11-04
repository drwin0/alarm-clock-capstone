# Capstone Project — Alarm Clock

## 📘 Overview

This project began as a simple **Alarm Clock** concept proposed for my **NCLab Python Capstone**.  
The original goal was to build a basic time-based alarm program that could play a sound at a set time — something minimal, easy to code, and functional for beginners.

Over time, I enhanced the idea and turned it into a **full-featured, responsive desktop alarm clock application** that feels like a real, usable tool.

---

## 🎯 Original Goals

From my project proposal, my initial objectives were:

1. **Build a basic Alarm Clock program** that allows the user to:
   - Set a specific time for an alarm  
   - Trigger a simple alert or sound when that time arrives  

2. **Practice key Python concepts:**
   - Loops and conditionals  
   - Time-based functions (`time` module)  
   - User input and output  
   - Simple functions and modular design  

3. **Use beginner-friendly tools only:**
   - **IDE:** Visual Studio Code  
   - **OS:** macOS  
   - **No external frameworks** except possibly `winsound` or `pygame` for sound  

4. **Add a flowchart** showing how the program waits for the right time and plays a sound.

---

## 🚀 What I Actually Built

During development, the project evolved into a complete **Graphical User Interface (GUI)** application with multiple features that go far beyond the initial concept.

### Final Version Highlights

- **Graphical (GUI):** Built with Tkinter  
- **Cross-platform:** Fully functional on macOS  
- **Multi-alarm capable:** Add, edit, delete, and toggle multiple alarms  
- **Persistent:** Alarms are automatically saved in `alarms.json`  
- **Responsive:** Layout dynamically adjusts to window resizing  
- **Customizable:** Supports custom sound files via `pygame` or macOS system sounds  

---

## 🧩 Design Choices and Improvements

### Responsive Layout

Rather than stacking all widgets vertically, I redesigned the interface using **Tkinter’s grid system**.  
Each component (header, input form, alarm list, footer) expands fluidly when the window is resized.

### Persistent Storage

I added a simple `alarms.json` file that automatically saves and loads alarm data.  
This persistence ensures users don’t lose their alarms after closing the app.

### Cross-Platform Sound System

Originally, I planned to use `winsound`, but since I developed on macOS, I implemented a **dual sound system**:
- `pygame` for custom `.wav` and `.mp3` files  
- macOS fallback using system sounds via `afplay` or text-to-speech via `say`

### Smarter Alarm Logic

The alarm-checking loop runs in a **background thread**, keeping the GUI responsive while waiting for alarms.  
Each alarm is managed individually and can repeat daily if desired.

### User Interface Components

- Treeview table displaying all alarms  
- Edit, Delete, and Toggle buttons for control  
- Status label for instant feedback  
- Pop-up notifications when alarms ring  

---

## 🧠 Learning Focus

Through this project, I practiced:

- Event-driven programming  
- Thread management in GUI applications  
- File handling and JSON serialization  
- Responsive interface design  

---

## 🧰 Technical Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.11 |
| **GUI Library** | Tkinter + ttk |
| **Sound** | `pygame` + macOS fallback (`afplay` / `say`) |
| **Storage** | JSON |
| **Threading** | Python `threading` module |
| **IDE** | Visual Studio Code |
| **OS** | macOS |

---

## 🖥 How to Run

### 1. Install Dependencies
```bash
pip install pygame
```

### 2. Run the Program
```bash
python3 gui_alarm_clock.py
```

### 3. Add Alarms
- Enter a time (`HH:MM`)  
- Add a label (optional)  
- Check “Repeat daily” if needed  
- Click **Add Alarm**

### 4. Manage Alarms
- Select any alarm and click **Edit**, **Delete**, or **Toggle Enable**

### 5. Use a Custom Alarm Sound
Set the `SOUND_FILE` path to `"alarm.wav"` instead of `None`.

---

## 📂 Project Structure

```
alarm-clock/
│
├── gui_alarm_clock.py   # Main program file
├── alarms.json          # Auto-saved alarm data
├── README.md            # Project documentation
└── alarm.wav (optional) # Custom alarm sound
```

---

## 🌱 Possible Future Enhancements

- Add a **Snooze** button (5 or 10 minutes) when an alarm rings  
- Implement **dark mode**  
- Allow **custom sound selection** from the file system  
- Improve **UI responsiveness and animations**  

---

## 💭 Reflection

Before learning Python, my background was primarily in **web development** and **graphic design**.  
I was comfortable working with HTML, CSS, and JavaScript, creating structured websites with a focus on user experience, layout, and visual design.  

When I started learning Python, I immediately noticed how its clean syntax and logical flow connected with what I already knew from front-end development.  
Concepts like **functions**, **loops**, and **modular design** felt familiar, but Python expanded those ideas into new territories like **automation**, **file handling**, and **desktop applications**.

### How My Design Background Helped

- I focused on **user flow** and layout when creating the Tkinter GUI.  
- I emphasized **readability and balance**, similar to web UI design principles.  
- I ensured consistent colors, fonts, and spacing to create a professional look.

### Applying Front-End Thinking to Python

- Treated each alarm like a reusable “data component,” similar to React components.  
- Designed consistent, reusable UI elements (buttons, labels, inputs).  
- Prioritized interactivity and visual feedback through pop-ups and status indicators.

### What Python Taught Me

- **Threading:** Running background processes without freezing the UI.  
- **JSON Persistence:** Saving and loading alarms as structured data.  

This project represents a **bridge between design and development** — where my visual and logical skills came together to create something both functional and polished.  

It gave me confidence that Python can be a powerful tool not only for scripting or data analysis but also for **building complete, user-friendly desktop applications** — something I intend to continue exploring in future projects.
