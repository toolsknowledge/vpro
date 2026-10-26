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
import UseStateEx from "./UseStateEx.jsx"
import UseEffectEx from "./UseEffectEx.jsx"
import ContextEx from "./ContextEx.jsx"
import UseRefEx from "./UseRefEx.jsx"
import UseMemoEx from './UseMemoEx.jsx'
import CustomHook from './CustomHook.jsx'
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <CustomHook />
  </StrictMode>,
)
