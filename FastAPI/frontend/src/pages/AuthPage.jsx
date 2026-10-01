import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { AlertCircle, ArrowRight, CheckCircle2, Eye, EyeOff, Loader2, Lock, ShieldCheck, User, Users, Sparkles } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'
import { Field } from '../components/StudentForm'

const FEATURES = [
  { icon: ShieldCheck, title: 'JWT secured', text: 'Every request carries a signed bearer token.' },
  { icon: Users, title: 'Student records', text: 'Add, edit, search and manage students in one place.' },
  { icon: Sparkles, title: 'Works everywhere', text: 'Designed for desktop, tablet and mobile.' },
]

const YEAR = new Date().getFullYear()

export default function AuthPage({ mode }) {
  const isLogin = mode === 'login'
  const { login, register, expiredNotice, clearExpiredNotice } = useAuth()
  const toast = useToast()
  const navigate = useNavigate()
  const location = useLocation()

  const [username, setUsername] = useState(location.state?.username ?? '')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [showPwd, setShowPwd] = useState(false)
  const [errors, setErrors] = useState({})
  const [formError, setFormError] = useState('')
  const [loading, setLoading] = useState(false)

  const validate = () => {
    const er = {}
    if (!username.trim()) er.username = 'Username is required'
    if (!password) er.password = 'Password is required'
    else if (!isLogin && password.length < 6) er.password = 'Use at least 6 characters'
    if (!isLogin && confirm !== password) er.confirm = 'Passwords do not match'
    setErrors(er)
    return Object.keys(er).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setFormError('')
    clearExpiredNotice()
    if (!validate()) return
    setLoading(true)
    try {
      if (isLogin) {
        await login(username.trim(), password)
        toast(`Welcome back, ${username.trim()}!`)
        navigate('/', { replace: true })
      } else {
        const res = await register(username.trim(), password)
        toast(res?.message || 'Registration successful')
        navigate('/login', { replace: true, state: { username: username.trim() } })
      }
    } catch (err) {
      setFormError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const pwdToggle = (
    <button type="button" className="input-trailing" onClick={() => setShowPwd((s) => !s)} aria-label={showPwd ? 'Hide password' : 'Show password'}>
      {showPwd ? <EyeOff size={18} /> : <Eye size={18} />}
    </button>
  )

  return (
    <div className="auth-page">
      <aside className="auth-hero">
        <div className="hero-glow" />
        <img src="/logo.jpeg" alt="VPro Skills" className="hero-logo" />
        <div className="hero-copy">
          <h1>
            Manage your students <span>with confidence.</span>
          </h1>
          <p>A secure portal for VPro Skills, powered by FastAPI, MongoDB and JWT authentication.</p>
        </div>
        <ul className="hero-features">
          {FEATURES.map(({ icon: Icon, title, text }) => (
            <li key={title}>
              <span className="feature-icon">
                <Icon size={20} />
              </span>
              <div>
                <strong>{title}</strong>
                <p>{text}</p>
              </div>
            </li>
          ))}
        </ul>
        <p className="hero-foot">© {YEAR} VPro Skills</p>
      </aside>

      <main className="auth-main">
        <div className="auth-card">
          <img src="/logo.jpeg" alt="VPro Skills" className="auth-card-logo" />
          <div className="auth-head">
            <h2>{isLogin ? 'Sign in' : 'Create an account'}</h2>
            <p>{isLogin ? 'Enter your credentials to access the dashboard.' : 'Register to start managing student records.'}</p>
          </div>

          <div className="auth-tabs" role="tablist">
            <Link to="/login" className={isLogin ? 'active' : ''} role="tab" aria-selected={isLogin}>
              Sign in
            </Link>
            <Link to="/register" className={!isLogin ? 'active' : ''} role="tab" aria-selected={!isLogin}>
              Register
            </Link>
            <span className={`tab-indicator ${isLogin ? '' : 'right'}`} />
          </div>

          {expiredNotice && isLogin && (
            <div className="alert alert-info">
              <AlertCircle size={18} /> Your session has expired. Please sign in again.
            </div>
          )}
          {formError && (
            <div className="alert alert-error">
              <AlertCircle size={18} /> {formError}
            </div>
          )}

          <form onSubmit={handleSubmit} noValidate className="auth-form">
            <Field label="Username" icon={User} error={errors.username}>
              <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Enter your username" autoComplete="username" autoFocus />
            </Field>
            <Field label="Password" icon={Lock} error={errors.password} trailing={pwdToggle}>
              <input
                type={showPwd ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={isLogin ? 'Enter your password' : 'At least 6 characters'}
                autoComplete={isLogin ? 'current-password' : 'new-password'}
              />
            </Field>
            {!isLogin && (
              <Field label="Confirm password" icon={CheckCircle2} error={errors.confirm}>
                <input
                  type={showPwd ? 'text' : 'password'}
                  value={confirm}
                  onChange={(e) => setConfirm(e.target.value)}
                  placeholder="Re-enter your password"
                  autoComplete="new-password"
                />
              </Field>
            )}

            <button type="submit" className="btn btn-primary btn-block btn-lg" disabled={loading}>
              {loading ? <Loader2 size={18} className="spin" /> : null}
              {isLogin ? 'Sign in' : 'Create account'}
              {!loading && <ArrowRight size={18} />}
            </button>
          </form>

          <p className="auth-switch">
            {isLogin ? "Don't have an account? " : 'Already registered? '}
            <Link to={isLogin ? '/register' : '/login'}>{isLogin ? 'Create one' : 'Sign in'}</Link>
          </p>
        </div>
      </main>
    </div>
  )
}
