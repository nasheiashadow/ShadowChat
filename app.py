# ==========================================================
# SHADOWCHAT PROFESSIONAL
# Version 1.2
# Developer : Nasheiashadow
# Flask Backend
# Part 1A
# ==========================================================

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash
)

from database import (
    load_users,
    load_messages,
    save_users,
    save_messages,
    create_user,
    change_status,
    change_password,
    set_online,
    set_last_seen,
    get_users,
    user_exists,
    get_profile
)

from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import secrets
import re

# ==========================================================
# FLASK APP
# ==========================================================

app = Flask(__name__)

app.secret_key = secrets.token_hex(32)

# ==========================================================
# LOAD DATABASE
# ==========================================================

users = load_users()

messages = load_messages()

# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

def strong_password(password):

    pattern = (
        r"^(?=.*[a-z])"
        r"(?=.*[A-Z])"
        r"(?=.*\d)"
        r"(?=.*[@#$%^&+=!*?])"
        r".{8,}$"
    )

    return re.match(pattern, password)

# ==========================================================
# USER HELPERS
# ==========================================================

def logged_in():

    return "username" in session


def current_user():

    if logged_in():

        return session["username"]

    return None


def ensure_message_store(username):

    global messages

    if username not in messages:

        messages[username] = {

            "inbox": [],

            "sent": []

        }

        save_messages(messages)

# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template("index.html")

# ==========================================================
# REGISTER
# ==========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    global users
    global messages

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if username == "" or password == "":

            return render_template(

                "register.html",

                error="Please complete all fields."

            )

        if user_exists(users, username):

            return render_template(

                "register.html",

                error="Username already exists."

            )

        if not strong_password(password):

            return render_template(

                "register.html",

                error=(
                    "Password must contain at least "
                    "8 characters, one uppercase "
                    "letter, one lowercase letter, "
                    "one number and one special "
                    "character."
                )

            )

        hashed_password = generate_password_hash(password)

        create_user(

            users,

            messages,

            username,

            hashed_password

        )

        users = load_users()

        messages = load_messages()

        flash(

            "Account created successfully."

        )

        return redirect(

            url_for("login")

        )

    return render_template(

        "register.html"

    )

# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    global users

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not user_exists(users, username):

            return render_template(

                "login.html",

                error="User not found."

            )

        stored_password = users[username]["password"]

        authenticated = False

        # --------------------------------------
        # Supports old plain-text users
        # and new hashed passwords
        # --------------------------------------

        if stored_password.startswith(
            "pbkdf2:"
        ) or stored_password.startswith(
            "scrypt:"
        ):

            authenticated = check_password_hash(

                stored_password,

                password

            )

        else:

            if stored_password == password:

                authenticated = True

                users[username]["password"] = (

                    generate_password_hash(password)

                )

                save_users(users)

        if not authenticated:

            return render_template(

                "login.html",

                error="Incorrect password."

            )

        session["username"] = username

        set_online(

            users,

            username,

            True

        )

        flash(

            f"Welcome back {username}!"

        )

        return redirect(

            url_for(

                "dashboard"

            )

        )

    return render_template(

        "login.html"

    )
# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():

    global users

    if not logged_in():

        return redirect(
            url_for("login")
        )

    username = current_user()

    available_users = []

    for user in users:

        if user != username:

            available_users.append(

                {
                    "username": user,
                    "online": users[user].get(
                        "online",
                        False
                    ),
                    "status": users[user].get(
                        "status",
                        ""
                    ),
                    "last_seen": users[user].get(
                        "last_seen",
                        "Never"
                    )
                }

            )


    return render_template(

        "dashboard.html",

        username=username,

        users=available_users,

        profile=users[username]

    )


# ==========================================================
# PROFILE PAGE
# ==========================================================

@app.route("/profile")
def profile():

    if not logged_in():

        return redirect(
            url_for("login")
        )


    username = current_user()


    profile_data = get_profile(

        users,

        username

    )


    return render_template(

        "profile.html",

        profile=profile_data

    )


# ==========================================================
# UPDATE STATUS
# ==========================================================

@app.route(
    "/update_status",
    methods=["POST"]
)
def update_status():

    if not logged_in():

        return redirect(
            url_for("login")
        )


    username = current_user()


    status = request.form.get(

        "status",

        ""

    ).strip()


    if status:

        change_status(

            users,

            username,

            status

        )


        flash(
            "Status updated."
        )


    return redirect(

        url_for("dashboard")

    )


# ==========================================================
# CHANGE PASSWORD
# ==========================================================

@app.route(
    "/change_password",
    methods=["POST"]
)
def change_password_route():


    if not logged_in():

        return redirect(
            url_for("login")
        )


    username = current_user()


    new_password = request.form.get(

        "password",

        ""

    ).strip()


    if not strong_password(new_password):

        flash(

            "Password does not meet requirements."

        )

        return redirect(

            url_for("profile")

        )


    hashed_password = generate_password_hash(

        new_password

    )


    change_password(

        users,

        username,

        hashed_password

    )


    flash(

        "Password changed successfully."

    )


    return redirect(

        url_for("profile")

    )


# ==========================================================
# USER SEARCH
# ==========================================================

@app.route("/search")
def search_users():

    if not logged_in():

        return redirect(

            url_for("login")

        )


    keyword = request.args.get(

        "q",

        ""

    ).lower()


    results = []


    for username in users:


        if username == current_user():

            continue


        if keyword in username.lower():

            results.append(

                {
                    "username": username,

                    "online": users[username].get(
                        "online",
                        False
                    ),

                    "status": users[username].get(
                        "status",
                        ""
                    )

                }

            )


    return render_template(

        "search.html",

        results=results,

        keyword=keyword

    )


# ==========================================================
# USER LIST API
# ==========================================================

@app.route("/api/users")
def api_users():

    if not logged_in():

        return {

            "error":
            "Unauthorized"

        },401


    data=[]


    for username in users:


        data.append(

            {

                "username": username,

                "online":
                users[username].get(
                    "online",
                    False
                )

            }

        )


    return {

        "users": data

    }
    # ==========================================================
# CHAT SYSTEM
# ==========================================================

@app.route(
    "/chat/<receiver>",
    methods=["GET", "POST"]
)
def chat(receiver):

    global messages
    global users


    if not logged_in():

        return redirect(

            url_for("login")

        )


    sender = current_user()


    if receiver not in users:

        flash(

            "User does not exist."

        )

        return redirect(

            url_for("dashboard")

        )


    ensure_message_store(sender)

    ensure_message_store(receiver)



    # ======================================================
    # SEND MESSAGE
    # ======================================================

    if request.method == "POST":


        text = request.form.get(

            "message",

            ""

        ).strip()



        if text:


            now = datetime.now()


            message = {


                "id":
                len(
                    messages[sender]["sent"]
                ) + 1,


                "sender":

                sender,


                "receiver":

                receiver,


                "text":

                text,


                "date":

                now.strftime(
                    "%d-%m-%Y"
                ),


                "time":

                now.strftime(
                    "%H:%M:%S"
                ),


                "timestamp":

                now.strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),


                "status":

                "sent",


                "read":

                False

            }



            messages[receiver]["inbox"].append(

                message

            )


            messages[sender]["sent"].append(

                message

            )


            save_messages(messages)


            return redirect(

                url_for(

                    "chat",

                    receiver=receiver

                )

            )



    # ======================================================
    # LOAD CHAT HISTORY
    # ======================================================


    conversation = []



    for msg in messages[sender]["inbox"]:


        if msg.get("sender") == receiver:

            conversation.append(msg)



    for msg in messages[sender]["sent"]:


        if msg.get("receiver") == receiver:

            conversation.append(msg)



    conversation.sort(

        key=lambda x:

        (

            x.get(
                "date",
                ""
            ),

            x.get(
                "time",
                ""
            )

        )

    )



    return render_template(

        "chat.html",

        sender=sender,

        receiver=receiver,

        conversation=conversation

    )



# ==========================================================
# DELETE MESSAGE
# ==========================================================

@app.route(
    "/delete_message/<int:message_id>"
)
def delete_message(message_id):


    if not logged_in():

        return redirect(

            url_for("login")

        )


    username = current_user()



    messages[username]["sent"] = [

        msg for msg in messages[username]["sent"]

        if msg["id"] != message_id

    ]



    save_messages(messages)



    flash(

        "Message deleted."

    )


    return redirect(

        request.referrer

    )



# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
def logout():


    if logged_in():


        username = current_user()



        set_last_seen(

            users,

            username

        )


        session.pop(

            "username",

            None

        )


        flash(

            "Logged out successfully."

        )



    return redirect(

        url_for("home")

    )



# ==========================================================
# 404 ERROR
# ==========================================================

@app.errorhandler(404)
def page_not_found(error):


    return render_template(

        "404.html"

    ),404



# ==========================================================
# 500 ERROR
# ==========================================================

@app.errorhandler(500)
def internal_error(error):


    return (

        "<h1>500 - Internal Server Error</h1>",

        500

    )



# ==========================================================
# APPLICATION START
# ==========================================================

if __name__ == "__main__":


    print(
        """
==================================
 ShadowChat Professional v1.2
 Server Started
 Developer: Nasheiashadow
==================================
        """
    )


    app.run(

        host="0.0.0.0",

        port=5001,

        debug=True

    )