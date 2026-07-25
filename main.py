# ==========================================
# SHADOWCHAT v1.2
# By Nasheiashadow
# ==========================================

from database import load_users, load_messages

from auth import (
    register,
    login,
    logout,
    update_password,
    update_status,
    view_profile
)

from chat import (
    send_message,
    inbox,
    sent_messages,
    view_users
)

# ==========================================
# LOAD DATABASE
# ==========================================

users = load_users()
messages = load_messages()

current_user = None


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    print("\n===================================")
    print("        WELCOME TO SHADOWCHAT")
    print("===================================")

    if current_user:
        print(f"Logged in as : {current_user}")

    print("\nMAIN MENU")
    print("1. Register")
    print("2. Login")
    print("3. Send Message")
    print("4. Inbox")
    print("5. Sent Messages")
    print("6. View Users")
    print("7. My Profile")
    print("8. Change Password")
    print("9. Change Status")
    print("10. Logout")
    print("11. Exit")

    choice = input("\nChoose an option: ").strip()

    if choice == "1":

        register(users, messages)

    elif choice == "2":

        if current_user is not None:
            print("A user is already logged in.")
        else:
            user = login(users)

            if user is not None:
                current_user = user

    elif choice == "3":

        send_message(current_user, users, messages)

    elif choice == "4":

        inbox(current_user, messages)

    elif choice == "5":

        sent_messages(current_user, messages)

    elif choice == "6":

        view_users(users)

    elif choice == "7":

        view_profile(users, current_user)

    elif choice == "8":

        update_password(users, current_user)

    elif choice == "9":

        update_status(users, current_user)

    elif choice == "10":

        current_user = logout(users, current_user)

    elif choice == "11":

        if current_user is not None:
            current_user = logout(users, current_user)

        print("\nThank you for using ShadowChat!")
        break

    else:

        print("Invalid option. Please try again.")