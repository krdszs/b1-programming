from fastapi import APIRouter, HTTPException
from schema import User, UserCreate
from user_store import UserStore

router = APIRouter()

store = UserStore("users.db")

@router.get("/search")          # Search users
def search_users(parameter: str = ""):
    users = store.load()
    results = [u for u in users if parameter in u["name"]]

    if not results:
        return  "No user found"
    
    return results

@router.get("/")            # list qll users
def get_users():
    return store.load()

@router.get("/{user_id}")           # Search users by id
def get_user(user_id: int):
    user = store.find_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.post("/", status_code=201)              # Create user
def create_user(user_data: UserCreate):
    return store.create_user(name=user_data.name, email=user_data.email)

@router.put("/{user_id}")               # Update user
def update_user(user_id: int, user_data: UserCreate):
    success = store.update_user(user_id, {"name": user_data.name, "email": user_data.email})
    
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return store.find_by_id(user_id)

@router.delete("/{user_id}")            # Delete user
def delete_user(user_id: int):
    success = store.delete_user(user_id)

    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"deleted": True}