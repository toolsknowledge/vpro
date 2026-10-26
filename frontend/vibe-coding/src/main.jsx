import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import GetEx from './components/api/GetEx.jsx'
import PostEx from './components/api/PostEx.jsx'
import PutEx from './components/api/PutEx.jsx'
import DeleteEx from './components/api/DeleteEx.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <GetEx />
    <PostEx />
    <PutEx />
    <DeleteEx />
  </StrictMode>,
)
