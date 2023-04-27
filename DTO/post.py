import json
from datetime import datetime


class FacebookPost:
    CSV_HEADER = ["username", "post_text", "shared_text", "timestamp"]

    def __init__(self, username: str, post_text: str, shared_text: str, timestamp: datetime):
        self.username = username
        self.post_text = post_text
        self.shared_text = shared_text
        self.timestamp = timestamp.strftime('%d/%m/%Y')

    def to_dict(self):
        return {
            "username": self.username,
            "post_text": self.post_text,
            "shared_text": self.shared_text,
            "timestamp":  self.timestamp
        }

    def to_csv_line(self):
        return f"{self.username},\"{self.post_text}\",\"{self.shared_text}\",{self.timestamp}"

    def __repr__(self):
        return json.dumps(self.to_dict())


class TwitterPost:
    CSV_HEADER = ["username", "post_text", "shared_text", "timestamp"]

    def __init__(self, username: str, post_text: str, shared_text: str, timestamp: datetime, pid: int):
        self.id = pid
        self.username = username
        self.post_text = post_text
        self.shared_text = shared_text
        self.timestamp = timestamp.strftime('%d/%m/%Y')

    def to_dict(self):
        return {
            "username": self.username,
            "post_text": self.post_text,
            "shared_text": self.shared_text,
            "timestamp": self.timestamp
        }

    def to_csv_line(self):
        return f"{self.username},{self.post_text},{self.shared_text},{self.timestamp}"

    def __repr__(self):
        return json.dumps(self.to_dict())
