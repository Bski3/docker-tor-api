from flask import Flask, jsonify

app = Flask(__name__)   


@app.route("/")
def home():
    return "Hello, Friend!"


@app.route("/health.json")  
def health():
    return jsonify({"status": "UP"}), 200   


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=80,debug=False)