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
- **Dark Mode Support** (optional) 
- **Pop-up Alerts:** User-friendly reminders 
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
- Turn ON/OFF dark mode 


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
Reflection

Before learning Python, my background was primarily in web development and graphic design.
I was comfortable working with HTML, CSS, and JavaScript, creating structured websites with an emphasis on user experience, layout design, and clean visual presentation. My training in computer science also helped me develop logical thinking and an understanding of how different systems communicate, but I hadn’t yet worked much with backend logic, data handling, or automation.

When I began learning Python, I immediately noticed how its clean syntax and structured logic connected naturally with what I already knew from web programming.
Concepts like functions, loops, and modular organization felt familiar, but Python allowed me to apply them in new contexts, outside the browser — like file systems, automation, and desktop apps.

Building this Alarm Clock project was a perfect bridge between those worlds.

My design background helped me:
	•	Think carefully about user flow and layout when creating the Tkinter GUI.
	•	Choose colors, spacing, and fonts that made the interface clean and readable.
	•	Focus on responsiveness and balance, just like in web design.

My web development mindset also influenced how I structured the code:
	•	I treated each alarm like a small “data component,” similar to how I would manage UI elements in React or Next.js.
	•	I applied front-end thinking to create reusable elements — buttons, labels, and inputs with consistent styles.
	•	I prioritized interactivity and visual feedback (pop-up messages, status labels, color indicators).

At the same time, Python introduced me to entirely new programming ideas:
	•	Threading: running the alarm-checker in the background without freezing the interface.
	•	JSON persistence: saving and loading alarms like mini database records.

These skills expanded my sense of what I can build — not just websites, but full desktop applications that combine logic, design, and interactivity.

This project represents more than just an alarm clock — it’s where my web development, design sense, and new Python skills merged into one creative and technical product.
It gave me confidence that I can use Python not just for scripting or data analysis, but also for building functional tools with user-friendly interfaces — something I plan to keep improving in my next projects.
