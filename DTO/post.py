import json
from datetime import datetime


class FacebookPost:
    CSV_HEADER = ["username", "post_text", "shared_text", "timestamp"]

    def __init__(self, pid: int, username: str, post_text: str, shared_text: str, timestamp: datetime):
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
            "timestamp":  self.timestamp
        }

    def to_csv_line(self):
        return f"{self.username},\"{self.post_text}\",\"{self.shared_text}\",{self.timestamp}"

    def __repr__(self):
        return json.dumps(self.to_dict())


class TwitterPost:
    CSV_HEADER = ["username", "text", "created_at", "lang", "possibly_sensitive"]

    def __init__(self, pid: int, username: str, text: str, created_at: datetime, lang: str, possibly_sensitive: bool):
        self.id = pid
        self.username = username
        self.text = text
        self.created_at = created_at.strftime('%d/%m/%Y')
        self.lang = lang
        self.possibly_sensitive = possibly_sensitive

    def to_dict(self):
        return {
            "username": self.username,
            "text": self.text,
            "created_at": self.created_at,
            "lang": self.lang,
            "possibly_sensitive": self.possibly_sensitive
        }

    def to_csv_line(self):
        return f"{self.username},\"{self.text}\",{self.created_at},{self.lang},{self.possibly_sensitive}"

    def __repr__(self):
        return json.dumps(self.to_dict())
