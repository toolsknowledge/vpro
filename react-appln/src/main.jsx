import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Header from "./Header.jsx"
import Comp2 from './Comp2.jsx'
import Parent from './Parent.jsx'
import StateEx from './StateEx.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <StateEx />
  </StrictMode>,
)
