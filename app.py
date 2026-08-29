from flask import Flask, jsonify, render_template, request
import sqlite3
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
    latest_location = {
        "latitude": latitude,
        "longitude": longitude
    }
    return jsonify({
        "success": True,
        "message": "Location updated successfully"
    })
@app.route("/viewer")
def viewer():
    return render_template("viewer.html")
@app.route("/get_live_location")
def get_live_location():
    if not latest_location:
        return jsonify({
            "success": False,
            "message": "Live location not available yet"
        })
    return jsonify({
        "success": True,
        "latitude": latest_location.get("latitude"),
        "longitude": latest_location.get("longitude")
    })
@app.route("/sos", methods=["POST"])
def sos():
    return jsonify({
        "success": True,
        "message": "SOS activated"
    })
@app.route("/emergency", methods=["POST"])
def emergency():
    data = request.get_json() or {}
    name = data.get("name")
    phone = data.get("phone")
    if not name or not phone:
        return jsonify({
            "success": False,
            "message": "Name and phone are required"
        }), 400
    conn = sqlite3.connect("rakshanbala.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO emergency_contacts (name, phone) VALUES (?, ?)",
        (name, phone)
    )
    conn.commit()
    conn.close()
    print("Emergency Contact Saved to Database:", name, phone)
    return jsonify({
        "success": True,
        "message": "Emergency contact saved successfully"
    })
@app.route("/contacts")
def contacts():
    conn = sqlite3.connect("rakshanbala.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, phone FROM emergency_contacts ORDER BY id DESC"
    )
    contacts_list = cursor.fetchall()
    conn.close()
    return render_template("contacts.html", contacts=contacts_list)
if __name__ == "__main__":
    print("=" * 30)
    print("RakshanBala Flask Server")
    print("=" * 30)
    app.run(host="0.0.0.0", port=5000, debug=False)
