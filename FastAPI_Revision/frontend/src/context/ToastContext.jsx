import { createContext, useCallback, useContext, useState } from 'react'
import { AlertCircle, CheckCircle2, Info, X } from 'lucide-react'

const ToastContext = createContext(null)
const ICONS = { success: CheckCircle2, error: AlertCircle, info: Info }

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])

  const dismiss = useCallback((id) => setToasts((t) => t.filter((x) => x.id !== id)), [])

  const toast = useCallback(
    (message, type = 'success') => {
      const id = crypto.randomUUID()
      setToasts((t) => [...t, { id, message, type }])
      setTimeout(() => dismiss(id), 4000)
    },
    [dismiss],
  )

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="toast-stack" role="status" aria-live="polite">
        {toasts.map(({ id, message, type }) => {
          const Icon = ICONS[type]
          return (
            <div key={id} className={`toast toast-${type}`}>
              <Icon size={20} />
              <span>{message}</span>
              <button className="icon-btn" onClick={() => dismiss(id)} aria-label="Dismiss">
                <X size={16} />
              </button>
            </div>
          )
        })}
      </div>
    </ToastContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export const useToast = () => useContext(ToastContext)
