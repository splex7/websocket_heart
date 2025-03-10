document.addEventListener('DOMContentLoaded', () => {
    const socket = io('http://localhost:5000', {
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5
    });

    socket.on('connect_error', (error) => {
        logMessage(`Connection error: ${error.message}`);
        console.error('Connection error:', error);
    });

    socket.on('connect', () => {
        logMessage(`Connected as ${socket.id}`);
        console.log(`Connected as ${socket.id}`);
    });

    document.body.addEventListener('click', () => {
        const randomX = Math.random() * window.innerWidth;
        socket.emit('heart_click', { x: randomX });
        createFloatingHeart(randomX);
    });

    socket.on('heart_click', (data) => {
        createFloatingHeart(data.x);
    });

    socket.on('disconnect', () => {
        logMessage('Disconnected from server.');
    });
});

function createFloatingHeart(x) {
    const heart = document.createElement('div');
    heart.className = 'floating-heart';
    heart.textContent = '❤️';
    heart.style.left = `${x}px`;
    heart.style.bottom = '0';
    document.getElementById('heart-container').appendChild(heart);

    heart.addEventListener('animationend', () => {
        heart.remove();
    });
}

function logMessage(msg) {
    const li = document.createElement('li');
    li.textContent = msg;
    document.getElementById('log').appendChild(li);
}
