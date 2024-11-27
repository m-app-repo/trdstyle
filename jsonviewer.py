import tkinter as tk
from tkinter import scrolledtext
import time
import os
import json

class JsonViewerApp:
    def __init__(self, master, filename):
        self.master = master
        self.filename = filename
        self.auto_scroll = True

        master.title("Real-Time JSON Viewer - v1.1")

        # Create a ScrolledText widget for displaying file content
        self.text = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.text.pack(fill=tk.BOTH, expand=True)

        # Frame for the toggle button
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(fill=tk.X)

        # Button to toggle auto-scrolling
        self.scroll_button = tk.Button(
            self.button_frame, text="Disable Auto-Scroll", command=self.toggle_scroll
        )
        self.scroll_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Track the last modification time of the file
        self.last_mtime = None

        # Start the content update loop
        self.update_content()

    def toggle_scroll(self):
        """Toggle the automatic scrolling feature."""
        self.auto_scroll = not self.auto_scroll
        if self.auto_scroll:
            self.scroll_button.config(text="Disable Auto-Scroll")
        else:
            self.scroll_button.config(text="Enable Auto-Scroll")

    def update_content(self):
        """Read the JSON file and update the Text widget."""
        try:
            # Check if the file has been modified
            mtime = os.path.getmtime(self.filename)
            if self.last_mtime != mtime:
                self.last_mtime = mtime
                with open(self.filename, 'r') as f:
                    data = f.read()
                    # Try to parse and pretty-print the JSON data
                    try:
                        json_data = json.loads(data)
                        formatted_json = json.dumps(json_data, indent=4)
                    except json.JSONDecodeError:
                        formatted_json = data  # Display raw data if JSON is invalid

                    # Update the Text widget
                    self.text.delete(1.0, tk.END)
                    self.text.insert(tk.END, formatted_json)

                    # Auto-scroll to the bottom if enabled
                    if self.auto_scroll:
                        self.text.see(tk.END)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist yet
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, "Waiting for file to be created...")
        except Exception as e:
            # Handle other exceptions
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, f"An error occurred:\n{e}")

        # Schedule the next update after 1 second
        self.master.after(1000, self.update_content)

if __name__ == "__main__":
    root = tk.Tk()
    # Replace 'path_to_your_json_file.json' with the path to your JSON file
    filename = "tradelog.json"
    app = JsonViewerApp(root, filename)
    root.mainloop()
 