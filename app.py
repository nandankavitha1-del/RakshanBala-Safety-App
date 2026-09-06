from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
latest_location = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/update_location", methods=["POST"])
def update_location():
    global latest_location
    data = request.get_json() or {}
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    latest_location = {"latitude": latitude, "longitude": longitude}
    return jsonify({"success": True})

@app.route("/viewer")
def viewer():
    return render_template("viewer.html")

@app.route("/get_live_location")
def get_live_location():
    if not latest_location:
        return jsonify({"success": False})
    return jsonify({"success": True, "latitude": latest_location.get("latitude"), "longitude": latest_location.get("longitude")})

@app.route("/sos", methods=["POST"])
def sos():
    return jsonify({"success": True, "message": "SOS activated"})

@app.route("/emergency", methods=["POST"])
def emergency():
    data = request.get_json() or {}
    name = data.get("name")
    phone = data.get("phone")
    if not name or not phone:
        return jsonify({"success": False, "message": "Name and phone are required"}), 400
    print("Emergency Contact Saved:", name, phone)
    return jsonify({
        "success": True,
        "message": "Emergency contact saved successfully"
    })

if __name__ == "__main__":
    print("RakshanBala Flask Server")
    app.run(host="0.0.0.0", port=5000, debug=False)


