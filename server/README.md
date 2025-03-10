# Trae Cheer Server

## SSL Certificate Setup

1. Generate self-signed SSL certificates for development:
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

2. When prompted, fill in the certificate information. For development, you can use defaults or any values.

## Running the Server

1. Install required packages:
```bash
pip install flask flask-socketio flask-cors eventlet
```

2. Start the server:
```bash
python app.py
```

The server will run on https://localhost:5000

## Security Note
For production deployment, replace the self-signed certificates with proper SSL certificates from a trusted Certificate Authority.