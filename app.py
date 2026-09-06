from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Store the latest location
latest_location = {}


# =========================
# LOGIN PAGE
# =========================
@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # For now, accept the submitted login form
        # and open the main RakshanBala page.
        return render_template("index.html")

    return render_template("login.html")


# =========================
# REGISTER PAGE
# =========================
@app.route("/register", methods=["GET"])
def register():
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
