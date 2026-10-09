# PySide6 Study Planner

A colorful desktop study-planning app made with the PySide6 framework. The user enters a task, selects a category and study time, and the app adds it to a table and totals the planned minutes.

## Features

- Colorful, modern desktop interface
- Type any school subject and add tasks with planned time
- Set a daily study-minute goal and track it with a progress bar
- Mark selected tasks complete to update progress
- Remove individual tasks or clear the complete list
- Prevents blank tasks from being added

## Run it

1. Open Terminal and go to this project folder.
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install PySide6:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   python3 app.py
   ```

## What to demonstrate in the video

- Set a daily goal, then add two or three tasks with different categories and time amounts.
- Mark a task complete and point out that the progress bar updates.
- Remove a selected task and show that the total planned time updates.
- Try adding a blank task to show the input validation message.
