from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import socket

# Set your Mobile Hotspot IP (Change this to match your network)
HOTSPOT_IP = "172.20.10.3"
PORT = 5000

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

clients = {}

@socketio.on('connect')
def connect():
    print("✅ Client connected:", request.sid)

@socketio.on('offer')
def handle_offer(data):
    clients['client'] = request.sid
    print("📩 Received WebRTC Offer:", data)
    if not data:
        print("❌ Error: Received empty WebRTC Offer")
        return
    try:
        socketio.emit('offer', data, broadcast=True)
        print("📡 WebRTC Offer Broadcasted")
    except Exception as e:
        print(f"❌ WebRTC Offer Handling Error: {e}")

@socketio.on('answer')
def handle_answer(data):
    print("✅ Received WebRTC Answer:", data)
    try:
        socketio.emit('answer', data, broadcast=True)
    except Exception as e:
        print(f"❌ WebRTC Answer Handling Error: {e}")

@socketio.on('ice_candidate')
def handle_ice(data):
    print("📡 Received ICE Candidate:", data)
    try:
        socketio.emit('ice_candidate', data, broadcast=True)
    except Exception as e:
        print(f"❌ ICE Candidate Handling Error: {e}")

@app.route('/')
def index():
    print("📡 Serving index.html")
    return render_template('index.html')

if __name__ == "__main__":
    print(f"🚀 WebRTC Signaling Server Starting on {HOTSPOT_IP}:{PORT}...")
    try:
        socketio.run(app, host=HOTSPOT_IP, port=PORT, allow_unsafe_werkzeug=True)
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")
