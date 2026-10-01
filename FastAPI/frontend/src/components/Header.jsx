import { useEffect, useRef, useState } from 'react'
import { Clock, LogOut, ChevronDown } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

function useCountdown(target) {
  const [now, setNow] = useState(() => Date.now())
  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(t)
  }, [])
  const left = Math.max(0, target - now)
  const m = Math.floor(left / 60000)
  const s = Math.floor((left % 60000) / 1000)
  return { label: `${m}:${String(s).padStart(2, '0')}`, low: left < 5 * 60000 }
}

export default function Header() {
  const { user, session, logout } = useAuth()
  const { label, low } = useCountdown(session.expiresAt)
  const [open, setOpen] = useState(false)
  const menuRef = useRef(null)

  useEffect(() => {
    const close = (e) => menuRef.current && !menuRef.current.contains(e.target) && setOpen(false)
    document.addEventListener('mousedown', close)
    return () => document.removeEventListener('mousedown', close)
  }, [])

  return (
    <header className="app-header">
      <div className="container header-inner">
        <a href="/" className="brand" aria-label="VPro Skills home">
          <img src="/logo.jpeg" alt="VPro Skills" className="brand-logo" />
          <span className="brand-divider" />
          <span className="brand-sub">Student Portal</span>
        </a>

        <div className="header-actions">
          <div className={`session-pill ${low ? 'is-low' : ''}`} title="Time until your session token expires">
            <Clock size={15} />
            <span className="session-label">Session</span>
            <strong>{label}</strong>
          </div>

          <div className="user-menu" ref={menuRef}>
            <button className="user-trigger" onClick={() => setOpen((o) => !o)} aria-expanded={open}>
              <span className="avatar">{user[0]?.toUpperCase()}</span>
              <span className="user-name">{user}</span>
              <ChevronDown size={16} className={`chev ${open ? 'up' : ''}`} />
            </button>
            {open && (
              <div className="dropdown">
                <div className="dropdown-head">
                  <span className="avatar lg">{user[0]?.toUpperCase()}</span>
                  <div>
                    <div className="dd-name">{user}</div>
                    <div className="dd-sub">Signed in with JWT</div>
                  </div>
                </div>
                <button className="dropdown-item danger" onClick={() => logout()}>
                  <LogOut size={16} /> Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
