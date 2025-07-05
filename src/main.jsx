import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './components/home.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
