import json
from datetime import datetime

class Logger:
    def __init__(self):
        self.log_data = []

    def log_activity(self, action, request=None, response=None, log_book=None):
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "request": request,
            "response": response
        }
        self.log_data.append(log_entry)

        # Update log book in the UI if provided
        if log_book:
            log_book.append(f"{log_entry['timestamp']} - {action}")

        # Append the log entry to the file (tradelog.json)
        try:
            with open("tradelog.json", "a") as logfile:
                logfile.write(json.dumps(log_entry, indent=4, default=str) + "\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")

