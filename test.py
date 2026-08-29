from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "RakshanBala Test Server Working!"

@app.route("/health")
def health():
    return {
        "success": True,
        "status": "running"
    }

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False
    )