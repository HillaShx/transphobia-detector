from datetime import datetime


class FacebookPost:
    def __init__(self, username: str, post_text: str, shared_text: str, timestamp: datetime):
        self.username = username
        self.post_text = post_text
        self.shared_text = shared_text
        self.timestamp = timestamp

    def __repr__(self):
        return {
            "username": self.username,
            "post_text": self.post_text,
            "shared_text": self.shared_text,
            "timestamp": self.timestamp
        }


class TwitterPost:
    def __init__(self, username: str, post_text: str, shared_text: str, timestamp: datetime, pid: int):
        self.id = pid
        self.username = username
        self.post_text = post_text
        self.shared_text = shared_text
        self.timestamp = timestamp

    def __repr__(self):
        return {
            "username": self.username,
            "post_text": self.post_text,
            "shared_text": self.shared_text,
            "timestamp": self.timestamp
        }
