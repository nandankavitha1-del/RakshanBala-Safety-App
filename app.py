from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import sqlite3
import os
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ======================================================
# APP CONFIGURATION
# ======================================================

app.secret_key = "rakshanbala-change-this-secret-key"

# Session settings
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "rakshanbala.db")

latest_location = {}

# ======================================================
# DATABASE
# ======================================================

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

