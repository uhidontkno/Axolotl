from datetime import datetime, timedelta

class Cooldown:
    def __init__(self, duration: int):
        self.duration = duration
        self.cooldowns = {}

    def get_cooldown(self, user_id: int) -> float:
        if user_id not in self.cooldowns:
            return 0
        expiration_time = self.cooldowns[user_id]
        if expiration_time < datetime.utcnow():
            return 0
        return (expiration_time - datetime.utcnow()).total_seconds()

    def set_cooldown(self, user_id: int):
        expiration_time = datetime.utcnow() + timedelta(seconds=self.duration)
        self.cooldowns[user_id] = expiration_time