from database import load_data, save_data

def login(user_type):
    """Handle user login authentication"""
    filename = f"{user_type}s.json"
    users = load_data(filename)
    user_id_key = f"{user_type}_id"

    user_id = input(f"Enter your {user_type} ID: ")
    password = input("Enter your password: ")

    for user in users:
        if user[user_id_key] == user_id and user['password'] == password:
            print("Login successful.")
            return user
    print("Invalid user ID or password.")
    return None

def change_password(user_type, user_id):
    """Allow users to change their password"""
    filename = f"{user_type}s.json"
    users = load_data(filename)
    user_id_key = f"{user_type}_id"

    for user in users:
        if user[user_id_key] == user_id:
            new_password = input("Enter new password: ")
            user['password'] = new_password
            save_data(filename, users)
            print("Password changed successfully.")
            return
    print("User not found.")