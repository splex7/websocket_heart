import { useState, useEffect } from 'react'
import io from 'socket.io-client'
import './App.css'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:5000'

function App() {
  const [socket, setSocket] = useState(null)
  const [clickCount, setClickCount] = useState(0)

  useEffect(() => {
    const newSocket = io(BACKEND_URL)
    setSocket(newSocket)

    newSocket.on('heart_click', (data) => {
      createFloatingHeart(data.x, data.y, true)
    })

    return () => newSocket.disconnect()
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
      <div id="heart-container"></div>
      <div className="click-count">
        Hearts sent: {clickCount}
      </div>
    </div>
  )
}

export default App