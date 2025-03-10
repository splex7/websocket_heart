from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, disconnect
import threading
import time
from datetime import datetime
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

clients = {}
LOG_FILE = 'heart_clicks.json'
INACTIVE_TIMEOUT = 180  # 3 minutes in seconds

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
    clients[client_id] = {
        'hearts': 0,
        'last_active': time.time()
    }
    print(f"Client {client_id} connected.")
    # Broadcast active user count to all clients
    socketio.emit('active_users_update', len(clients))

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in clients:
        print(f"Client {client_id} disconnected.")
        del clients[client_id]
        # Broadcast updated active user count to all clients
        socketio.emit('active_users_update', len(clients))

@socketio.on('heart_click')
def handle_heart(data):
    client_id = request.sid
    if client_id in clients:
        clients[client_id]['hearts'] += 1
        clients[client_id]['last_active'] = time.time()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        save_click(client_id, timestamp)
        print(f"Client {client_id} clicked heart at {timestamp}!")
        emit('heart_click', data, broadcast=True, include_self=False)

def cleanup_inactive_clients():
    current_time = time.time()
    inactive_clients = []
    
    for client_id, data in clients.items():
        if current_time - data['last_active'] > INACTIVE_TIMEOUT:
            inactive_clients.append(client_id)
    
    if inactive_clients:
        # Remove from memory
        for client_id in inactive_clients:
            print(f"Removing inactive client {client_id}")
            del clients[client_id]
            disconnect(client_id)
        
        # Remove from JSON file
        clicks = load_clicks()
        for client_id in inactive_clients:
            if client_id in clicks:
                del clicks[client_id]
                print(f"Removed click history for inactive client {client_id}")
        
        # Save updated click history
        with open(LOG_FILE, 'w') as f:
            json.dump(clicks, f)

def monitor_clients():
    while True:
        cleanup_inactive_clients()
        time.sleep(180)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"\nMonitoring Report at {current_time}:")
        print("Connected Clients and Heart Counts:")
        for client_id, data in clients.items():
            inactive_time = time.time() - data['last_active']
            print(f"ID: {client_id}, Hearts: {data['hearts']}, Inactive for: {int(inactive_time)}s")
        
        clicks = load_clicks()
        if clicks:
            print("\nStored Click History:")
            for client_id, timestamps in clicks.items():
                print(f"Client {client_id}: {len(timestamps)} clicks")
                for ts in timestamps[-5:]:
                    print(f"  - {ts}")

if __name__ == "__main__":
    threading.Thread(target=monitor_clients, daemon=True).start()
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
