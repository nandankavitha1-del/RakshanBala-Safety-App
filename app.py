from flask import Flask, jsonify, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = "rakshanbala.db"

# Latest live location
latest_location = {}


# =========================
# DATABASE
# =========================
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Create database/table when app starts
init_db()


# =========================
# LOGIN PAGE
# =========================
@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        if not phone or not password:
            return "Phone number and password are required.", 400

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE phone = ?",
            (phone,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            return redirect(url_for("main_home"))

        return """
        <h3>❌ Invalid phone number or password</h3>
        <a href="/">Try Again</a>
        """

    return render_template("login.html")


# =========================
# REGISTER
# =========================
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not phone or not password:
            return "All fields are required.", 400

        if password != confirm_password:
            return """
            <h3>❌ Passwords do not match</h3>
            <a href="/register">Go Back</a>
            """

        password_hash = generate_password_hash(password)

        conn = get_db()

        try:
            conn.execute(
                """
                INSERT INTO users (name, phone, password)
                VALUES (?, ?, ?)
                """,
                (name, phone, password_hash)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()

            return """
            <h3>❌ Phone number already registered</h3>
            <a href="/">Go to Login</a>
            """

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# MAIN RAKSHANBALA PAGE
# =========================
@app.route("/home", methods=["GET"])
def main_home():
    return render_template("index.html")


# =========================
# UPDATE LOCATION
# =========================
@app.route("/update_location", methods=["POST"])
def update_location():

    global latest_location

    data = request.get_json(silent=True) or {}

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    latest_location = {
        "latitude": latitude,
        "longitude": longitude
    }

    return jsonify({
        "success": True
    })


# =========================
# LIVE LOCATION VIEWER
# =========================
@app.route("/viewer", methods=["GET"])
def viewer():
    return render_template("viewer.html")


@app.route("/get_live_location", methods=["GET"])
def get_live_location():

    if not latest_location:
        return jsonify({
            "success": False
        })

    return jsonify({
        "success": True,
        "latitude": latest_location.get("latitude"),
        "longitude": latest_location.get("longitude")
    })


# =========================
# SOS
# =========================
@app.route("/sos", methods=["POST"])
def sos():
    return jsonify({
        "success": True,
        "message": "SOS activated"
    })


# =========================
# EMERGENCY CONTACT
# =========================
@app.route("/emergency", methods=["POST"])
def emergency():

    data = request.get_json(silent=True) or {}

    name = data.get("name")
    phone = data.get("phone")

    if not name or not phone:
        return jsonify({
            "success": False,
            "message": "Name and phone are required"
        }), 400

    print("Emergency Contact Saved:", name, phone)

    return jsonify({
        "success": True,
        "message": "Emergency contact saved successfully"
    })


# =========================
# RUN LOCALLY
# =========================
if __name__ == "__main__":
    print("RakshanBala Flask Server")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
