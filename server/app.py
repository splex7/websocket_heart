import eventlet
import eventlet.wsgi
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
from flask_cors import CORS
import threading
import time
from datetime import datetime
import json
import os
import ssl

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

clients = {}
LOG_FILE = 'heart_clicks.json'

def load_clicks():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_click(client_id, timestamp):
    clicks = load_clicks()
    if client_id not in clicks:
        clicks[client_id] = []
    clicks[client_id].append(timestamp)
    with open(LOG_FILE, 'w') as f:
        json.dump(clicks, f)

@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    clients[client_id] = {'hearts': 0}
    print(f"Client {client_id} connected.")

@socketio.on('heart_click')
def handle_heart(data):
    client_id = request.sid
    if client_id in clients:
        clients[client_id]['hearts'] += 1
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_click(client_id, timestamp)
        print(f"Client {client_id} clicked heart at {timestamp}!")
        emit('heart_click', data, broadcast=True, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in clients:
        print(f"Client {client_id} disconnected.")
        del clients[client_id]

def monitor_clients():
    while True:
        time.sleep(15)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nMonitoring Report at {current_time}:")
        print("Connected Clients and Heart Counts:")
        for client_id, data in clients.items():
            print(f"ID: {client_id}, Hearts: {data['hearts']}")
        
        clicks = load_clicks()
        if clicks:
            print("\nStored Click History:")
            for client_id, timestamps in clicks.items():
                print(f"Client {client_id}: {len(timestamps)} clicks")
                for ts in timestamps[-5:]:
                    print(f"  - {ts}")

if __name__ == "__main__":
    threading.Thread(target=monitor_clients, daemon=True).start()
    # SSL configuration
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain("cert.pem", "key.pem")
    
    # Create eventlet socket and wrap with SSL
    eventlet_socket = eventlet.listen(("0.0.0.0", 5000))
    wrapped_socket = ssl_context.wrap_socket(eventlet_socket, server_side=True)
    print("🚀 Server running with HTTPS on port 5000")
    
    # Run eventlet WSGI server with SSL
    eventlet.wsgi.server(wrapped_socket, socketio.wsgi_app)
