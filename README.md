# Trae Cheer - Interactive Heart Clicks

## Project Structure

The project is split into two main components:

- `client/`: React frontend application
- `server/`: Flask backend server with WebSocket support

## Deployment Guide

### Frontend Deployment (Netlify)

1. Push your code to a GitHub repository
2. Log in to Netlify and create a new site from Git
3. Select your repository
4. Configure build settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Base directory: `client`
5. Add environment variables:
   - Add `VITE_BACKEND_URL` pointing to your backend server URL (e.g., https://your-app-name.herokuapp.com)

### Backend Deployment (Heroku)

1. Install Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Add a Procfile in the server directory:
   ```
   web: gunicorn --worker-class eventlet -w 1 app:app
   ```

4. Add required dependencies to requirements.txt:
   ```
   Flask
   Flask-SocketIO
   eventlet
   gunicorn
   ```

5. Deploy the backend:
   ```bash
   git subtree push --prefix server heroku main
   ```

### Important Configuration Notes

1. CORS Configuration:
   - The backend already has CORS configured with `cors_allowed_origins="*"`
   - For production, update this to specific origins:
     ```python
     socketio = SocketIO(app, cors_allowed_origins=["https://your-frontend-domain.netlify.app"])
     ```

2. Environment Variables:
   - Frontend:
     - `VITE_BACKEND_URL`: URL of your Heroku backend
   - Backend:
     - Set `SECRET_KEY` for Flask using Heroku Config Vars
     - Configure any other sensitive data through Heroku Config Vars

3. SSL/HTTPS:
   - Netlify automatically provides SSL/HTTPS for frontend
   - Heroku automatically provides SSL/HTTPS for backend

4. Monitoring:
   - Use Heroku logs to monitor WebSocket connections:
     ```bash
     heroku logs --tail
     ```
   - Monitor server resources through Heroku dashboard
   - Set up logging for both frontend and backend

5. Scaling Considerations:
   - WebSocket connections require persistent connections
   - Use appropriate Heroku dyno types based on expected load
   - Consider upgrading to paid tiers for better performance

6. Troubleshooting:
   - If WebSocket connections fail, ensure:
     - CORS is properly configured
     - Frontend is using the correct backend URL
     - Heroku dyno is not sleeping (use hobby or paid tier)
   - For connection issues, check:
     - Network tab in browser dev tools
     - Heroku logs for backend errors
     - Netlify deploy logs for frontend issues