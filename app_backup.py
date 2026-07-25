from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session
)

from database import (
    load_users,
    load_messages,
    save_users,
    save_messages
)

from datetime import datetime
import re

# ==========================================
# FLASK APP
# ==========================================

app = Flask(__name__)
app.secret_key = "shadowchat_secret_key_2026"

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
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template("index.html")

# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
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

@app.route("/login", methods=["GET", "POST"])
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
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:

        return redirect("/login")

    username = session["username"]

    return render_template(

        "dashboard.html",

        username=username,

        users=users

    )


# ==========================================
# CHAT
# ==========================================

@app.route("/chat/<receiver>", methods=["GET", "POST"])
def chat(receiver):

    global users
    global messages

    if "username" not in session:

        return redirect("/login")

    sender = session["username"]

    if receiver not in users:

        return redirect("/dashboard")

    # -------------------------
    # SEND MESSAGE
    # -------------------------

    if request.method == "POST":

        text = request.form["message"].strip()

        if text != "":

            now = datetime.now()

            message = {

                "id": len(messages[sender]["sent"]) + 1,

                "sender": sender,

                "receiver": receiver,

                "text": text,

                "date": now.strftime("%d-%m-%Y"),

                "time": now.strftime("%H:%M:%S")

            }

            messages[receiver]["inbox"].append(message)
            messages[sender]["sent"].append(message)

            save_messages(messages)

            return redirect(f"/chat/{receiver}")

    # -------------------------
    # LOAD CONVERSATION
    # -------------------------

    conversation = []

    # Inbox

    for msg in messages[sender]["inbox"]:

        if msg["sender"] == receiver:

            conversation.append(msg)

    # Sent

    for msg in messages[sender]["sent"]:

        if msg["receiver"] == receiver:

            conversation.append(msg)

    # Sort oldest → newest

    conversation.sort(

        key=lambda x: (

            x["date"],

            x["time"]

        )

    )

    return render_template(

        "chat.html",

        sender=sender,

        receiver=receiver,

        conversation=conversation

    )
    # ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

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


# ==========================================
# PROFILE
# ==========================================

@app.route("/profile")
def profile():

    if "username" not in session:

        return redirect("/login")

    username = session["username"]

    return {

        "username": username,
        "status": users[username]["status"],
        "joined": users[username]["joined"],
        "online": users[username]["online"],
        "last_seen": users[username]["last_seen"]

    }


# ==========================================
# UPDATE STATUS
# ==========================================

@app.route("/update_status", methods=["POST"])
def update_status():

    if "username" not in session:

        return redirect("/login")

    username = session["username"]

    status = request.form["status"].strip()

    if status != "":

        users[username]["status"] = status

        save_users(users)

    return redirect("/dashboard")


# ==========================================
# CHANGE PASSWORD
# ==========================================

@app.route("/change_password", methods=["POST"])
def change_password():

    if "username" not in session:

        return redirect("/login")

    username = session["username"]

    new_password = request.form["password"].strip()

    if strong_password(new_password):

        users[username]["password"] = new_password

        save_users(users)

    return redirect("/dashboard")


# ==========================================
# ERROR HANDLERS
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return (

        render_template(

            "404.html"

        ),

        404

    )


@app.errorhandler(500)
def server_error(error):

    return (

        "<h1>500 - Internal Server Error</h1>",

        500

    )


# ==========================================
# START SERVER
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5001,

        debug=True

    )