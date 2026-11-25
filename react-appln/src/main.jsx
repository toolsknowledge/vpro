import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Demo from './Demo.jsx'
import Comp2 from './Comp2.jsx'
import Master from './Master.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Master />
  </StrictMode>,
)
