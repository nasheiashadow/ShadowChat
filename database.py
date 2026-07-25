# ==========================================
# SHADOWCHAT DATABASE
# Professional Version 1.3
# Developer : Nasheiashadow
# ==========================================

import json
import os
import shutil
from datetime import datetime

# ==========================================
# FILES
# ==========================================

USERS_FILE = "users.json"
MESSAGES_FILE = "messages.json"

BACKUP_FOLDER = "backups"

# ==========================================
# BACKUP DIRECTORY
# ==========================================

if not os.path.exists(BACKUP_FOLDER):
    os.makedirs(BACKUP_FOLDER)

# ==========================================
# BACKUP FILE
# ==========================================

def create_backup(filename):

    if os.path.exists(filename):

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_name = os.path.join(
            BACKUP_FOLDER,
            f"{timestamp}_{filename}"
        )

        shutil.copy(filename, backup_name)

# ==========================================
# SAFE SAVE
# ==========================================

def safe_save(filename, data):

    temp_file = filename + ".tmp"

    with open(temp_file, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )

    if os.path.exists(filename):
        create_backup(filename)

    os.replace(temp_file, filename)

# ==========================================
# USER DEFAULTS
# ==========================================

def default_user():

    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    return {

        "password": "",

        "status": "Hey there! I am using ShadowChat.",

        "joined": now,

        "created_at": now,

        "last_seen": "Never",

        "online": False,

        "friends": [],

        "blocked": [],

        "theme": "default",

        "profile_picture": ""

    }

# ==========================================
# MESSAGE DEFAULTS
# ==========================================

def default_message_store():

    return {

        "inbox": [],

        "sent": []

    }

# ==========================================
# DATABASE MIGRATION
# ==========================================

def migrate_users(users):

    changed = False

    defaults = default_user()

    for username in users:

        for key, value in defaults.items():

            if key not in users[username]:

                users[username][key] = value

                changed = True

    if changed:

        save_users(users)

    return users

# ==========================================
# LOAD USERS
# ==========================================

def load_users():

    if not os.path.exists(USERS_FILE):

        return {}

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            users = json.load(file)

    except Exception:

        return {}

    return migrate_users(users)

# ==========================================
# SAVE USERS
# ==========================================

def save_users(users):

    safe_save(
        USERS_FILE,
        users
    )

# ==========================================
# LOAD MESSAGES
# ==========================================

def load_messages():

    if not os.path.exists(MESSAGES_FILE):

        return {}

    try:

        with open(
            MESSAGES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            messages = json.load(file)

    except Exception:

        return {}

    return messages

# ==========================================
# SAVE MESSAGES
# ==========================================

def save_messages(messages):

    safe_save(
        MESSAGES_FILE,
        messages
    )

# ==========================================
# CREATE USER
# ==========================================

def create_user(
    users,
    messages,
    username,
    password
):

    info = default_user()

    info["password"] = password

    users[username] = info

    messages[username] = default_message_store()

    save_users(users)

    save_messages(messages)

# ==========================================
# CHANGE PASSWORD
# ==========================================

def change_password(
    users,
    username,
    new_password
):

    if username not in users:
        return

    users[username]["password"] = new_password

    save_users(users)

# ==========================================
# CHANGE STATUS
# ==========================================

def change_status(
    users,
    username,
    status
):

    if username not in users:
        return

    users[username]["status"] = status

    save_users(users)

# ==========================================
# ONLINE STATUS
# ==========================================

def set_online(
    users,
    username,
    state
):

    if username not in users:
        return

    users[username]["online"] = state

    save_users(users)

# ==========================================
# LAST SEEN
# ==========================================

def set_last_seen(
    users,
    username
):

    if username not in users:
        return

    users[username]["last_seen"] = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    users[username]["online"] = False

    save_users(users)

# ==========================================
# FRIENDS
# ==========================================

def add_friend(
    users,
    username,
    friend
):

    if username not in users:
        return

    if friend not in users:
        return

    if friend not in users[username]["friends"]:

        users[username]["friends"].append(friend)

        save_users(users)

# ==========================================
# BLOCK USER
# ==========================================

def block_user(
    users,
    username,
    blocked_user
):

    if username not in users:
        return

    if blocked_user not in users:
        return

    if blocked_user not in users[username]["blocked"]:

        users[username]["blocked"].append(
            blocked_user
        )

        save_users(users)

# ==========================================
# GET USERS
# ==========================================

def get_users(users):

    return sorted(users.keys())

# ==========================================
# USER EXISTS
# ==========================================

def user_exists(
    users,
    username
):

    return username in users

# ==========================================
# GET PROFILE
# ==========================================

def get_profile(
    users,
    username
):

    if username not in users:

        return None

    return users[username]