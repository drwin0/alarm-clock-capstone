🕒 Capstone Project — Alarm Clock

📘 Overview

This project began as a simple Alarm Clock concept proposed for my NCLab Python Capstone.
The original goal was to build a basic time-based alarm program that could play a sound at a set time, something minimal, easy to code, and functional for beginners.

I decided to enhance the idea and turn it into a full-featured, responsive desktop alarm clock app that feels like a real, usable tool.

🎯 Original Goals

From my project proposal, my initial objectives were:

1.	Build a basic Alarm Clock program that allows the user to:
	•	Set a specific time for an alarm
	•	Trigger a simple alert or sound when that time arrives
2.	Practice key Python concepts:
	•	Loops and conditionals
	•	Time-based functions (time module)
	•	User input and output
	•	Simple functions and modular design
3.	Use only beginner-friendly tools:
	•	IDE: Visual Studio Code
	•	OS: macOS
	•	No external frameworks except possibly winsound or pygame for sound
4.	Add a hand-drawn flowchart showing how the program waits for the right time and plays a sound.


## 🚀 What I Built

The final app evolved far beyond the original idea.

### Final Features
- 🖥 **GUI:** Built with Tkinter  
- 🎵 **Sound:** Cross-platform alert system  
- ⏰ **Multi-alarm:** Add, edit, delete, and toggle multiple alarms  
- 💾 **Persistent Storage:** Alarms saved to `alarms.json`  
- 💡 **Responsive Layout:** Window dynamically resizes  
- 🌙 **Dark Mode Support** (optional)  
- 🔔 **Pop-up Alerts:** User-friendly reminders  
- 🧵 **Background Thread:** Prevents interface freezing  


## 🧩 Design Choices and Improvements

### 🪟 Responsive Layout
The GUI uses Tkinter’s grid system for scalable design, ensuring that all elements resize proportionally.

### 💾 Persistent Storage
All alarms are automatically saved and loaded via a simple JSON file (`alarms.json`).

### 🎵 Cross-Platform Audio
Since `winsound` doesn’t work on macOS, I implemented:
- `pygame` for custom `.wav`/`.mp3` sounds  
- macOS system fallback (`afplay` or `say`)

### 🧠 Improved Alarm Logic
A background thread continuously checks current time without blocking the main window — allowing the UI to stay responsive.

### 🧱 Enhanced UI Components
- **Treeview** list for displaying alarms  
- **Buttons** to edit, delete, toggle  
- **Pop-up messages** for instant feedback  
- **Status label** showing program activity  

🧰 Technical Stack
    Component:	Technology
    Language:	Python 3.11
    GUI Library:	Tkinter + ttk
    Sound:	pygame + macOS fallback (afplay/say)
    Storage:	JSON
    Threading:	Python threading module
    IDE:	Visual Studio Code
    OS:	macOS



🖥 How to Run
1.	Install dependencies
        pip install pygame


2.	Run the program
        python3 gui_alarm_clock.py


3.	Add alarms
        •Enter a time (HH:MM)
        •Add a label (optional)
        •Check “Repeat daily” if needed
        •Click Add Alarm

4.	Manage alarms
        •Select any alarm and click Edit, Delete, or Toggle Enable
		
5.  Use custom alarm sound     
		•Set SOUND_FILE path to **"alarm.wav"** instead of **None**

📂 Project Structure


    alarm-clock/
    │
    ├── gui_alarm_clock.py   # Main program file
    ├── alarms.json          # Auto-saved alarm data
    ├── README.md            # Project documentation
    └── alarm.wav (optional) # Custom alarm sound



🌱 Possible Future Enhancements

•	Add Snooze (5 or 10 minutes) button when an alarm rings
•	Optional dark mode
•	Custom sound selection 
•	Work on the responsive side of the app

💭 Reflection

Before learning Python, my background was primarily in web development and graphic design.
I was comfortable working with HTML, CSS, and JavaScript, creating structured websites with an emphasis on user experience, layout design, and clean visual presentation ￼. My training in computer science also helped me develop logical thinking and an understanding of how different systems communicate, but I hadn’t yet worked much with backend logic, data handling, or automation.

When I began learning Python, I immediately noticed how its clean syntax and structured logic connected naturally with what I already knew from web programming.
Concepts like functions, loops, and modular organization felt familiar, but Python allowed me to apply them in new contexts, outside the browser, like file systems, automation, and desktop apps.

Building this Alarm Clock project was a perfect bridge between those worlds.

My design background helped me:
	•	Think carefully about user flow and layout when creating the Tkinter GUI.
	•	Choose colors, spacing, and fonts that made the interface clean and readable.
	•	Focus on responsiveness and balance, just like in web design.

My web development mindset also influenced how I structured the code:
	•	I treated each alarm like a small “data component,” similar to how I would manage UI elements in React or NextJS.
	•	I applied front-end thinking to create reusable elements — buttons, labels, and inputs with consistent styles.
	•	I prioritized interactivity and visual feedback (pop-up messages, status labels, color indicators).

At the same time, Python introduced me to entirely new programming ideas:
	•	Threading: running the alarm-checker in the background without freezing the interface.
	•	JSON persistence: saving and loading alarms like mini database records.

Those skills expanded my sense of what I can build, not just websites, but full desktop applications that combine logic, design, and interactivity.

This project represents more than just an alarm clock, it’s where my web development, design sense, and new Python skills merged into one creative and technical product.
It gave me confidence that I can use Python not just for scripting or data analysis, but also for building functional tools with user-friendly interfaces, something I plan to keep improving in my next projects.
