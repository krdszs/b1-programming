import json

class UserStore:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        try:
            with open(self.file_path, "r") as f:
                return [json.loads(line) for line in f if line.strip()]
            
        except FileNotFoundError:
            return []

    def save(self, users):
        with open(self.file_path, "w") as f:
            for user in users:
                f.write(json.dumps(user) + "\n")

    def find_by_id(self, user_id):
        users = self.load()
        for user in users:
            if user["id"] == user_id:
                return user
        return None

    def update_user(self, user_id, updated_data):
        users = self.load()

        for i, user in enumerate(users):
            if user["id"] == user_id:
                users[i] = {
                    "id": user_id,
                    "name": updated_data["name"],
                    "email": updated_data["email"]
                    }
                self.save(users)
                return True
            
        return False

    def delete_user(self, user_id: int) -> bool:
        users = self.load()
        updated = [u for u in users if u["id"] != user_id]

        if len(updated) == len(users):
            return False
        
        self.save(updated)
        return True
    