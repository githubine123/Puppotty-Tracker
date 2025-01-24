import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class PupPottyTracker:
    def __init__(self):
        self.logs = []  # List to store potty events
        self.dog_names = ["Buddy", "Max", "Bella", "Lucy"]  # Predefined dog names
        self.root = tk.Tk()
        self.root.title("PupPotty Tracker")
        self.root.state("zoomed")  # Make the app fullscreen

        self.create_gui()
        self.root.mainloop()

    def create_gui(self):
        # Main Frame to Center Widgets
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill="both")

        # Dog Name Label and Dropdown
        tk.Label(main_frame, text="Dog Name:").grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.dog_name_var = tk.StringVar()
        self.dog_name_dropdown = ttk.Combobox(main_frame, textvariable=self.dog_name_var, values=self.dog_names, state="readonly")
        self.dog_name_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Hour and Minute Dropdowns
        tk.Label(main_frame, text="Hour:").grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.hour_var = tk.StringVar()
        self.hour_dropdown = ttk.Combobox(main_frame, textvariable=self.hour_var, values=[f"{i:02d}" for i in range(24)], state="readonly")
        self.hour_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        tk.Label(main_frame, text="Minute:").grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.minute_var = tk.StringVar()
        self.minute_dropdown = ttk.Combobox(main_frame, textvariable=self.minute_var, values=[f"{i:02d}" for i in range(60)], state="readonly")
        self.minute_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Notes Label and Entry
        tk.Label(main_frame, text="Notes:").grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.notes_entry = tk.Entry(main_frame)
        self.notes_entry.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # Event Type Buttons
        tk.Button(main_frame, text="Log Pee", command=lambda: self.log_event("pee")).grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        tk.Button(main_frame, text="Log Poop", command=lambda: self.log_event("poop")).grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

        # View Logs Button
        tk.Button(main_frame, text="View Logs", command=self.view_logs).grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Analyze Patterns Button
        tk.Button(main_frame, text="Analyze Patterns", command=self.analyze_patterns).grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configure grid to fill the screen
        for row in range(7):
            main_frame.rowconfigure(row, weight=1)
        for col in range(2):
            main_frame.columnconfigure(col, weight=1)

    def log_event(self, event_type):
        """Log a potty event for a dog."""
        dog_name = self.dog_name_var.get()
        notes = self.notes_entry.get().strip()
        hour = self.hour_var.get()
        minute = self.minute_var.get()

        if not dog_name:
            messagebox.showerror("Error", "Please select a dog name.")
            return
        if not hour or not minute:
            messagebox.showerror("Error", "Please select both hour and minute.")
            return

        try:
            # Combine current date with user-selected time
            current_date = datetime.datetime.now().date()
            event_time = datetime.datetime.strptime(f"{current_date} {hour}:{minute}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format.")
            return

        event = {
            "timestamp": event_time,
            "event_type": event_type,
            "dog_name": dog_name,
            "notes": notes
        }
        self.logs.append(event)
        self.save_logs_to_file()
        messagebox.showinfo("Success", f"Logged {event_type} for {dog_name}.")
        self.notes_entry.delete(0, tk.END)

    def save_logs_to_file(self):
        """Save logs to a text file."""
        with open("dog_potty_logs.txt", "w") as file:
            for log in self.logs:
                timestamp = log["timestamp"].strftime("%d/%m/%y %H:%M")
                file.write(f"[{timestamp}] {log['dog_name']} - {log['event_type'].capitalize()} ({log['notes']})\n")

    def view_logs(self):
        """View all potty logs."""
        dog_name = self.dog_name_var.get()

        filtered_logs = [log for log in self.logs if not dog_name or log["dog_name"] == dog_name]

        if not filtered_logs:
            messagebox.showinfo("No Logs", "No logs found.")
            return

        log_text = "Potty Logs:\n"
        for log in filtered_logs:
            timestamp = log["timestamp"].strftime("%d/%m/%y %H:%M")
            log_text += f"[{timestamp}] {log['dog_name']} - {log['event_type'].capitalize()} ({log['notes']})\n"

        log_window = tk.Toplevel(self.root)
        log_window.title("Potty Logs")
        log_textbox = tk.Text(log_window, wrap="word")
        log_textbox.insert("1.0", log_text)
        log_textbox.config(state="disabled")
        log_textbox.pack(expand=True, fill="both", padx=5, pady=5)

    def analyze_patterns(self):
        """Analyze potty patterns for a specific dog."""
        dog_name = self.dog_name_var.get()

        if not dog_name:
            messagebox.showerror("Error", "Dog name is required for pattern analysis.")
            return

        dog_logs = [log for log in self.logs if log["dog_name"] == dog_name]

        if not dog_logs:
            messagebox.showinfo("No Logs", f"No logs found for dog: {dog_name}.")
            return

        pee_times = [log["timestamp"] for log in dog_logs if log["event_type"] == "pee"]
        poop_times = [log["timestamp"] for log in dog_logs if log["event_type"] == "poop"]

        analysis_text = f"Pattern Analysis for {dog_name}:\n"
        analysis_text += f"Total Pee Events: {len(pee_times)}\n"
        analysis_text += f"Total Poop Events: {len(poop_times)}\n"

        if len(pee_times) > 1:
            pee_intervals = [(pee_times[i] - pee_times[i - 1]).total_seconds() for i in range(1, len(pee_times))]
            avg_pee_interval = sum(pee_intervals) / len(pee_intervals) / 3600  # in hours
            analysis_text += f"Average Pee Interval: {avg_pee_interval:.2f} hours\n"

        if len(poop_times) > 1:
            poop_intervals = [(poop_times[i] - poop_times[i - 1]).total_seconds() for i in range(1, len(poop_times))]
            avg_poop_interval = sum(poop_intervals) / len(poop_intervals) / 3600  # in hours
            analysis_text += f"Average Poop Interval: {avg_poop_interval:.2f} hours\n"

        analysis_window = tk.Toplevel(self.root)
        analysis_window.title("Pattern Analysis")
        analysis_textbox = tk.Text(analysis_window, wrap="word")
        analysis_textbox.insert("1.0", analysis_text)
        analysis_textbox.config(state="disabled")
        analysis_textbox.pack(expand=True, fill="both", padx=5, pady=5)

# Run the app
if __name__ == "__main__":
    PupPottyTracker()
