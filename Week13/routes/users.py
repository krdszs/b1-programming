import json
from fastapi import APIRouter, HTTPException
from schema import User, UserCreate

router = APIRouter()

users_file = "users.txt"

def read_users():
    try:
        with open(users_file, "r") as f:
            return [json.loads(line) for line in f if line.strip()]
        
    except FileNotFoundError:
        return []

def write_users(users):
    with open(users_file, "w") as f:
        for user in users:
            f.write(json.dumps(user) + "\n")

def get_next_id(users):
    if not users:
        return 1
    return max(u["id"] for u in users) + 1

@router.get("/search")          # Search users
def search_users(parameter: str = ""):
    users = read_users()
    results = [u for u in users if parameter in u["name"]]

    if not results:
        return  "No user found"
    
    return results

@router.get("/")            # list qll users
def get_users():
    return read_users()

@router.get("/{user_id}")           # Search users by id
def get_user(user_id: int):
    users = read_users()
    user = next((u for u in users if u["id"] == user_id), None)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/", status_code=201)              # Create user
def create_user(user_data: UserCreate):
    users = read_users()

    new_user = {
        "id": get_next_id(users),
        "name": user_data.name,
        "email": user_data.email,
    }

    users.append(new_user)
    write_users(users)
    return new_user

@router.put("/{user_id}")               # Update user
def update_user(user_id: int, user_data: UserCreate):
    users = read_users()

    for i, user in enumerate(users):
        if user["id"] == user_id:
            users[i] = {"id": user_id, "name": user_data.name, "email": user_data.email}
            write_users(users)
            return users[i]
        
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}")            # Delete user
def delete_user(user_id: int):
    users = read_users()
    updated = [u for u in users if u["id"] != user_id]

    if len(updated) == len(users):
        raise HTTPException(status_code=404, detail="User not found")
    
    write_users(updated)
    return {"deleted": True}