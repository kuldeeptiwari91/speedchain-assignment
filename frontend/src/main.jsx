import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import AIReceptionist from './components/AIReceptionist'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AIReceptionist />
  </StrictMode>,
)
