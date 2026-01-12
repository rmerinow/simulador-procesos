from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "estado": "ok",
        "mensaje": "Backend Flask funcionando correctamente"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
