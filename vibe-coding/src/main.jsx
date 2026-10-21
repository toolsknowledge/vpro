import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Master from './spa/Master.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Master />
  </StrictMode>,
)
