import csv
import datetime

class ChatLogger:
    def __init__(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"chat_history_{timestamp}.csv"
        self._initialize_file()
    
    def _initialize_file(self):
        with open(self.filename, mode='w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Time', 'Question', 'Answer', 'Citations'])

    def log(self, question: str, answer: str, citations: str):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        with open(self.filename, mode='a', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow([current_time, question, answer, citations])