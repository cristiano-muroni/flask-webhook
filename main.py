from flask import Flask, jsonify, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/webhook', methods=['GET'])
def analyse():     
    hub_challenge = request.json.get('hub.challenge')                   
    return hub_challenge

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
