from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "rakshanbala-change-this-secret-key"

DATABASE = "rakshanbala.db"

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


init_db()


# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET"])
def home():
    if "user_id" in session:
        return redirect(url_for("main_home"))

    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        conn = get_db()

        user = conn.execute(
            "SELECT * FROM users WHERE phone = ?",
            (phone,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_phone"] = user["phone"]

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

        if not name or not phone or not password or not confirm_password:
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
            <a href="/register">Go to Login</a>
            """

        conn.close()

        return redirect(url_for("login"))

    return render_template("register.html")


# =========================
# FORGOT PASSWORD PAGE
# =========================
@app.route("/forgot_password", methods=["GET"])
def forgot_password_page():
    return render_template("forgot_password.html")


# =========================
# RESET PASSWORD
# =========================
@app.route("/reset_password", methods=["POST"])
def reset_password():

    phone = request.form.get("phone", "").strip()
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    phone = phone.replace(" ", "")

    if not phone or not new_password or not confirm_password:
        return render_template(
            "forgot_password.html",
            error="Please fill all fields"
        )

    if new_password != confirm_password:
        return render_template(
            "forgot_password.html",
            error="Passwords do not match"
        )

    conn = get_db()

    user = conn.execute(
        "SELECT id FROM users WHERE phone = ?",
        (phone,)
    ).fetchone()

    if not user:
        conn.close()

        return render_template(
            "forgot_password.html",
            error="Phone number not registered"
        )

    password_hash = generate_password_hash(new_password)

    conn.execute(
        "UPDATE users SET password = ? WHERE phone = ?",
        (password_hash, phone)
    )

    conn.commit()
    conn.close()

    return """
    <h3>✅ Password reset successfully</h3>
    <a href="/">Go to Login</a>
    """


# =========================
# MAIN APP
# =========================
@app.route("/home", methods=["GET"])
def main_home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout", methods=["GET"])
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================
# UPDATE LOCATION
# =========================
@app.route("/update_location", methods=["POST"])
def update_location():

    global latest_location

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    data = request.get_json(silent=True) or {}

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return jsonify({
            "success": False,
            "message": "Latitude and longitude are required"
        }), 400

    latest_location = {
        "latitude": latitude,
        "longitude": longitude
    }

    return jsonify({
        "success": True
    })


# =========================
# LIVE VIEWER
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

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

    return jsonify({
        "success": True,
        "message": "SOS activated"
    })


# =========================
# EMERGENCY CONTACT
# =========================
@app.route("/emergency", methods=["POST"])
def emergency():

    if "user_id" not in session:
        return jsonify({
            "success": False,
            "message": "Login required"
        }), 401

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
# RUN
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
