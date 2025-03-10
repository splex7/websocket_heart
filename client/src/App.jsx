import { useState, useEffect } from 'react'
import io from 'socket.io-client'
import './App.css'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://217.142.136.40:5000' || 'http://localhost:5000'

function App() {
  const [socket, setSocket] = useState(null)
  const [clickCount, setClickCount] = useState(0)
  const [connectionError, setConnectionError] = useState(false)

  useEffect(() => {
    const connectSocket = () => {
      const newSocket = io(BACKEND_URL, {
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
      })

      newSocket.on('connect', () => {
        setConnectionError(false)
        setSocket(newSocket)
      })

      newSocket.on('connect_error', (error) => {
        console.error('Socket connection error:', error)
        setConnectionError(true)
      })

      newSocket.on('heart_click', (data) => {
        createFloatingHeart(data.x, data.y, true)
      })

      return newSocket
    }

    const socket = connectSocket()

    return () => socket.disconnect()
  }, [])

  const createFloatingHeart = (x, y, isRemote = false) => {
    const heart = document.createElement('div')
    heart.innerHTML = '❤️'
    heart.className = 'floating-heart'
    heart.style.left = `${x}px`
    heart.style.top = `${y}px`
    document.getElementById('heart-container').appendChild(heart)

    if (!isRemote) {
      setClickCount(prev => prev + 1)
      socket?.emit('heart_click', { x, y })
    }

    setTimeout(() => heart.remove(), 2000)
  }

  const handleClick = (e) => {
    createFloatingHeart(e.clientX, e.clientY)
  }

  return (
    <div className="app" onClick={handleClick}>
      {connectionError && (
        <div className="error-message">
          Unable to connect to server. Please try again later.
        </div>
      )}
      <div id="heart-container"></div>
      <div className="click-count">
        Hearts sent: {clickCount}
      </div>
    </div>
  )
}

export default App