import { CheckCircle2, Info, X } from 'lucide-react'
import { useDashboard } from '../../state/DashboardContext.jsx'

export default function Toasts() {
  const { toasts, actions } = useDashboard()
  return (
    <div aria-live="polite" className="pointer-events-none fixed inset-x-4 bottom-4 z-50 flex flex-col items-end gap-2 sm:inset-x-auto sm:right-6 sm:bottom-6">
      {toasts.map((t) => {
        const Icon = t.tone === 'success' ? CheckCircle2 : Info
        return (
          <div
            key={t.id}
            className="toast-in pointer-events-auto flex w-full max-w-sm items-start gap-3 rounded-xl bg-navy-950 px-4 py-3 text-sm text-white shadow-pop"
          >
            <Icon className={`mt-0.5 size-4 shrink-0 ${t.tone === 'success' ? 'text-[#7fd6a8]' : 'text-navy-300'}`} aria-hidden="true" />
            <p className="flex-1">{t.message}</p>
            <button type="button" onClick={() => actions.dismissToast(t.id)} className="-m-1 rounded p-1 text-navy-300 hover:text-white" aria-label="Dismiss">
              <X className="size-4" aria-hidden="true" />
            </button>
          </div>
        )
      })}
    </div>
  )
}
