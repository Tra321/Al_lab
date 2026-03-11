import tkinter as tk
import time
from time import strftime as _strftime

def get_current_time():
    return _strftime("%H:%M:%S")

def get_current_date():
    return _strftime("%Y-%m-%d %A")

class DesktopClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Clock")
        self.root.geometry("400x250")
        self.root.config(bg="#222222")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        
        self.time_label = tk.Label(
            root,
            font=("Arial", 48, "bold"),
            bg="#222222",
            fg="#00ff00"
        )
        self.time_label.pack(expand=True)
        
        self.date_label = tk.Label(
            root,
            font=("Arial", 16),
            bg="#222222",
            fg="#00ff00"
        )
        self.date_label.pack(pady=10)
        
        self.update_time()
    
    def update_time(self):
        current_time = get_current_time()
        current_date = get_current_date()
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    clock = DesktopClock(root)
    root.mainloop()