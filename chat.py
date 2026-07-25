# ==========================================
# SHADOWCHAT CHAT
# Version 1.2
# By Nasheiashadow
# ==========================================

from datetime import datetime
from database import save_messages, get_users


# ==========================================
# SEND MESSAGE
# ==========================================

def send_message(current_user, users, messages):

    if current_user is None:
        print("Please login first.")
        return

    print("\n========== SEND MESSAGE ==========")

    receiver = input("Send to: ").strip()

    if receiver not in users:
        print("User does not exist.")
        return

    text = input("Message: ").strip()

    if text == "":
        print("Message cannot be empty.")
        return

    now = datetime.now()

    message = {
        "id": len(messages[receiver]["inbox"]) + 1,
        "sender": current_user,
        "receiver": receiver,
        "text": text,
        "date": now.strftime("%d-%m-%Y"),
        "time": now.strftime("%H:%M:%S")
    }

    # Receiver inbox
    messages[receiver]["inbox"].append(message)

    # Sender sent messages
    messages[current_user]["sent"].append(message)

    save_messages(messages)

    print("\nMessage sent successfully!")


# ==========================================
# INBOX
# ==========================================

def inbox(current_user, messages):

    if current_user is None:
        print("Please login first.")
        return

    print("\n========== INBOX ==========")

    inbox_messages = messages[current_user]["inbox"]

    if len(inbox_messages) == 0:
        print("No messages.")
        return

    for msg in inbox_messages:

        print("----------------------------------------")
        print("ID      :", msg["id"])
        print("FROM    :", msg["sender"])
        print("DATE    :", msg["date"])
        print("TIME    :", msg["time"])
        print("----------------------------------------")
        print(msg["text"])
        print("----------------------------------------")


# ==========================================
# SENT MESSAGES
# ==========================================

def sent_messages(current_user, messages):

    if current_user is None:
        print("Please login first.")
        return

    print("\n========== SENT MESSAGES ==========")

    sent = messages[current_user]["sent"]

    if len(sent) == 0:
        print("No sent messages.")
        return

    for msg in sent:

        print("----------------------------------------")
        print("ID      :", msg["id"])
        print("TO      :", msg["receiver"])
        print("DATE    :", msg["date"])
        print("TIME    :", msg["time"])
        print("----------------------------------------")
        print(msg["text"])
        print("----------------------------------------")


# ==========================================
# VIEW USERS
# ==========================================

def view_users(users):

    print("\n========================================")
    print("         REGISTERED USERS")
    print("========================================")

    all_users = get_users(users)

    if len(all_users) == 0:
        print("No registered users.")
        return

    for number, username in enumerate(all_users, start=1):

        user = users[username]

        print(f"\n{number}. {username}")

        if user["online"]:
            print("🟢 Online")
        else:
            print("⚫ Offline")
            print("Last Seen :", user["last_seen"])

        print("Status    :", user["status"])
        print("----------------------------------------")