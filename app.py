import json
import os
from flask import Flask, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# =========================
# JSON FILE (DATABASE)
# =========================
DB_FILE = "users.json"

# create file if not exists
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump([], f)
@app.route('/img/<path:filename>')
def serve_img(filename):
    from flask import send_from_directory
    return send_from_directory('static/img', filename)
# read users
def read_users():
    with open(DB_FILE, "r") as f:
        return json.load(f)

# write users
def write_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)


# =========================
# ROUTES (HTML PAGES)
# =========================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/upload")
def upload():
    return render_template("upload.html")
@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route("/opportunities")
def opportunities():
    return render_template("opportunities.html")

@app.route("/roadmap")
def roadmap():
    return render_template("roadmap.html")

@app.route("/roadmap-ai")
def roadmap_ai():
    return render_template("roadmapai.html")

@app.route("/roadmap-ds")
def roadmap_ds():
    return render_template("roadmapdatascience.html")

@app.route("/roadmap-cyber")
def roadmap_cyber():
    return render_template("roadmacyber.html")

@app.route("/webroad")
def webroad():
    return render_template("webroad.html")

# =========================
# REGISTER API
# =========================
@app.route("/register-user", methods=["POST"])
def register():
    data = request.json

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    users = read_users()

    # check if user exists
    for user in users:
        if user["email"] == email:
            return jsonify({"message": "User already exists"})

    # hash password
    hashed_password = generate_password_hash(password)

    users.append({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    write_users(users)

    return jsonify({"message": "Registered successfully"})


# =========================
# LOGIN API
# =========================
@app.route("/login-user", methods=["POST"])
def login():
    data = request.json

    email = data.get("email")
    password = data.get("password")

    users = read_users()

    for user in users:
        if user["email"] == email:
            if check_password_hash(user["password"], password):
                return jsonify({"message": "Login successful"})
            else:
                return jsonify({"message": "Wrong password"})

    return jsonify({"message": "User not found"})


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)