import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Header from "./Header.jsx"
import Comp2 from './Comp2.jsx'
import Parent from './Parent.jsx'
import StateEx from './StateEx.jsx'
import Electronics from "./Electronics.jsx"
import Get from './Get.jsx'
import Post from './Post.jsx'
import Put from './Put.jsx'
import Delete from './Delete.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Delete />
  </StrictMode>,
)
