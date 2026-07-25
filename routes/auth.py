from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

import re

from database import (
    load_users,
    load_messages,
    save_users,
    save_messages
)

# ==========================================
# BLUEPRINT
# ==========================================

auth = Blueprint("auth", __name__)

# ==========================================
# LOAD DATABASE
# ==========================================

users = load_users()
messages = load_messages()

# ==========================================
# PASSWORD VALIDATION
# ==========================================

def strong_password(password):

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!*?]).{8,}$"

    return re.match(pattern, password)

# ==========================================
# REGISTER
# ==========================================

@auth.route("/register", methods=["GET", "POST"])
def register():

    global users
    global messages

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if username == "" or password == "":

            return render_template(
                "register.html",
                error="Please complete all fields."
            )

        if username in users:

            return render_template(
                "register.html",
                error="Username already exists."
            )

        if not strong_password(password):

            return render_template(
                "register.html",
                error="""
Password must contain:

• Minimum 8 characters

• One uppercase letter

• One lowercase letter

• One number

• One special character (@ # $ % ! &)
"""
            )

        users[username] = {

            "password": password,

            "status": "Hey there! I am using ShadowChat.",

            "online": False,

            "last_seen": "Never",

            "joined": "2026"

        }

        messages[username] = {

            "inbox": [],

            "sent": []

        }

        save_users(users)
        save_messages(messages)

        return redirect("/login")

    return render_template("register.html")

# ==========================================
# LOGIN
# ==========================================

@auth.route("/login", methods=["GET", "POST"])
def login():

    global users

    if request.method == "POST":

        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if username not in users:

            return render_template(
                "login.html",
                error="User not found."
            )

        if users[username]["password"] != password:

            return render_template(
                "login.html",
                error="Incorrect password."
            )

        users[username]["online"] = True

        save_users(users)

        session["username"] = username

        return redirect("/dashboard")

    return render_template("login.html")

# ==========================================
# LOGOUT
# ==========================================

@auth.route("/logout")
def logout():

    from datetime import datetime

    global users

    if "username" in session:

        username = session["username"]

        if username in users:

            users[username]["online"] = False

            users[username]["last_seen"] = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            save_users(users)

        session.pop("username")

    return redirect("/")