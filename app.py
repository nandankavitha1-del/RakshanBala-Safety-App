from flask import Flask, jsonify, render_template, request
import sqlite3
import os

app = Flask(**name**)

latest_location = {}

# Get the folder where app.py is located

BASE_DIR = os.path.dirname(os.path.abspath(**file**))
DATABASE = os.path.join(BASE_DIR, "rakshanbala.db")

# ======================================================

# CREATE DATABASE TABLE

# ======================================================

def init_database():
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

```
cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT NOT NULL
    )
""")

conn.commit()
conn.close()
```

# Create the table when the application starts

init_database()

# ======================================================

# HOME

# ======================================================

@app.route("/")
def home():
return render_template("index.html")

# ======================================================

# UPDATE LIVE LOCATION

# ======================================================

@app.route("/update_location", methods=["POST"])
def update_location():
global latest_location

```
data = request.get_json(silent=True) or {}

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
```

# ======================================================

# LIVE LOCATION VIEWER

# ======================================================

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

```
return jsonify({
    "success": True,
    "latitude": latest_location.get("latitude"),
    "longitude": latest_location.get("longitude")
})
```

# ======================================================

# SOS

# ======================================================

@app.route("/sos", methods=["POST"])
def sos():
return jsonify({
"success": True,
"message": "SOS activated"
})

# ======================================================

# SAVE EMERGENCY CONTACT

# ======================================================

@app.route("/emergency", methods=["POST"])
def emergency():
try:
data = request.get_json(silent=True) or {}

```
    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()

    if not name or not phone:
        return jsonify({
            "success": False,
            "message": "Name and phone are required"
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO emergency_contacts (name, phone) VALUES (?, ?)",
        (name, phone)
    )

    conn.commit()
    conn.close()

    print("Emergency Contact Saved:", name, phone)

    return jsonify({
        "success": True,
        "message": "Emergency contact saved successfully"
    })

except Exception as error:
    print("Emergency Contact Error:", error)

    return jsonify({
        "success": False,
        "message": "Unable to save emergency contact"
    }), 500
```

# ======================================================

# VIEW SAVED CONTACTS

# ======================================================

@app.route("/contacts")
def contacts():
try:
conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()

```
    cursor.execute(
        "SELECT id, name, phone FROM emergency_contacts ORDER BY id DESC"
    )

    contacts_list = cursor.fetchall()
    conn.close()

    return jsonify({
        "success": True,
        "contacts": [
            {
                "id": contact[0],
                "name": contact[1],
                "phone": contact[2]
            }
            for contact in contacts_list
        ]
    })

except Exception as error:
    return jsonify({
        "success": False,
        "message": str(error)
    }), 500
```

# ======================================================

# START SERVER

# ======================================================

if **name** == "**main**":
print("=" * 30)
print("RakshanBala Flask Server")
print("=" * 30)

```
app.run(host="0.0.0.0", port=5000, debug=False)
```
