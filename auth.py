# ==========================================
# SHADOWCHAT AUTHENTICATION
# Version 1.2
# By Nasheiashadow
# ==========================================

from datetime import datetime

from database import (
    create_user,
    change_password,
    change_status,
    set_online,
    set_last_seen
)


# ==========================================
# REGISTER
# ==========================================

def register(users, messages):

    print("\n========== REGISTER ==========")

    username = input("Choose Username: ").strip()

    if username == "":
        print("Username cannot be empty.")
        return

    if username in users:
        print("Username already exists.")
        return

    password = input("Choose Password: ").strip()

    if password == "":
        print("Password cannot be empty.")
        return

    create_user(users, messages, username, password)

    print("\nRegistration Successful!")


# ==========================================
# LOGIN
# ==========================================

def login(users):

    print("\n========== LOGIN ==========")

    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username not in users:
        print("User not found.")
        return None

    if users[username]["password"] != password:
        print("Incorrect password.")
        return None

    set_online(users, username, True)

    print(f"\nWelcome back, {username}!")

    return username


# ==========================================
# LOGOUT
# ==========================================

def logout(users, current_user):

    if current_user is None:
        print("No user is currently logged in.")
        return None

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    set_online(users, current_user, False)
    set_last_seen(users, current_user, now)

    print(f"\nGoodbye {current_user}!")

    return None


# ==========================================
# CHANGE PASSWORD
# ==========================================

def update_password(users, current_user):

    if current_user is None:
        print("Please login first.")
        return

    print("\n====== CHANGE PASSWORD ======")

    old_password = input("Current Password: ").strip()

    if users[current_user]["password"] != old_password:
        print("Wrong password.")
        return

    new_password = input("New Password: ").strip()
    confirm = input("Confirm Password: ").strip()

    if new_password != confirm:
        print("Passwords do not match.")
        return

    change_password(users, current_user, new_password)

    print("\nPassword changed successfully!")


# ==========================================
# CHANGE STATUS
# ==========================================

def update_status(users, current_user):

    if current_user is None:
        print("Please login first.")
        return

    print("\n====== CHANGE STATUS ======")

    status = input("New Status: ").strip()

    if status == "":
        print("Status cannot be empty.")
        return

    change_status(users, current_user, status)

    print("Status updated successfully!")


# ==========================================
# PROFILE
# ==========================================

def view_profile(users, current_user):

    if current_user is None:
        print("Please login first.")
        return

    user = users[current_user]

    print("\n==============================")
    print("        MY PROFILE")
    print("==============================")
    print("Username  :", current_user)
    print("Joined    :", user["joined"])
    print("Status    :", user["status"])
    print("Online    :", "Yes" if user["online"] else "No")
    print("Last Seen :", user["last_seen"])
    print("==============================")