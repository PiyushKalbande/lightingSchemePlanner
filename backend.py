from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allows frontend to communicate with backend

@app.route('/get-room-config', methods=['POST'])
def get_room_config():
    data = request.json  # Get input from frontend
    return jsonify(data)  # Send back the same data

if __name__ == '__main__':
    app.run(debug=True)