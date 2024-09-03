import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from tkinter import simpledialog

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("2025 Calendar")
        self.current_year = 2025
        self.current_month = 1
        self.events = {}  # Dictionary to store events

        # Add a header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=10)
        self.header_label = ttk.Label(header_frame, text=f"{calendar.month_name[self.current_month]} {self.current_year}", font=("Arial", 18))
        self.header_label.pack()

        # Create main frames
        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.pack(pady=20)

        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(pady=10)

        # Add buttons to navigate months with icons (assuming you have arrow icons)
        self.prev_button = ttk.Button(self.control_frame, text="<<", command=self.prev_month)
        self.prev_button.pack(side="left", padx=10)

        self.next_button = ttk.Button(self.control_frame, text=">>", command=self.next_month)
        self.next_button.pack(side="right", padx=10)

        # Display the current month
        self.display_calendar()

        # Add a status bar
        self.status_bar = ttk.Label(self.root, text="", relief=tk.SUNKEN, anchor="w")
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    def display_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.header_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")

        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Create header with days of the week
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for day in days:
            ttk.Label(self.calendar_frame, text=day, width=10, anchor='center').grid(row=0, column=days.index(day))

        # Display days in the calendar
        for r, week in enumerate(cal, start=1):
            for c, day in enumerate(week):
                if day != 0:
                    day_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
                    has_event = day_str in self.events
                    day_btn = ttk.Button(self.calendar_frame, text=str(day), width=10, command=lambda d=day: self.add_event(d))
                    if has_event:
                        day_btn.config(style="Event.TButton")
                    day_btn.grid(row=r, column=c, padx=5, pady=5)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
        else:
            self.current_month -= 1
        self.display_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
        else:
            self.current_month += 1
        self.display_calendar()

    def add_event(self, day):
        event_window = tk.Toplevel(self.root)
        event_window.title(f"Events on {day} {calendar.month_name[self.current_month]} {self.current_year}")

        # View existing events
        self.view_events(event_window, day)

        # Adding new event
        tk.Label(event_window, text="Add New Event").pack(pady=10)
        
        tk.Label(event_window, text="Event Time (HH:MM):").pack(pady=5)
        time_entry = tk.Entry(event_window)
        time_entry.pack(pady=5)

        tk.Label(event_window, text="Event Description:").pack(pady=5)
        desc_entry = tk.Entry(event_window, width=40)
        desc_entry.pack(pady=5)

        def save_event():
            time = time_entry.get()
            description = desc_entry.get()
            event_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
            if event_key not in self.events:
                self.events[event_key] = []
            self.events[event_key].append((time, description))
            event_window.destroy()
            self.display_calendar()

        ttk.Button(event_window, text="Save", command=save_event).pack(pady=10)

    def view_events(self, parent_window, day):
        event_key = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
        events = self.events.get(event_key, [])
        
        if events:
            tk.Label(parent_window, text="Scheduled Events:").pack(pady=10)
            for time, description in events:
                event_frame = ttk.Frame(parent_window)
                event_frame.pack(pady=5, fill=tk.X)
                ttk.Label(event_frame, text=f"{time} - {description}").pack(side=tk.LEFT, padx=5)
                ttk.Button(event_frame, text="Delete", command=lambda t=time: self.delete_event(event_key, t)).pack(side=tk.RIGHT, padx=5)
        else:
            tk.Label(parent_window, text="No events scheduled.").pack(pady=10)

    def delete_event(self, event_key, time):
        if event_key in self.events:
            self.events[event_key] = [event for event in self.events[event_key] if event[0] != time]
            if not self.events[event_key]:
                del self.events[event_key]
            messagebox.showinfo("Event Deleted", "The event has been deleted.")
            self.display_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.configure("Event.TButton", background="#ffd700")  # Gold color for event days
    app = CalendarApp(root)
    root.mainloop()