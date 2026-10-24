import { AlertCircle, CheckCircle2, Circle, Clock3, PlayCircle, XCircle } from 'lucide-react'

// Status always pairs an icon and a label with color, never color alone.
const styles = {
  pending: { cls: 'bg-wait-bg text-wait', icon: Clock3 },
  submitted: { cls: 'bg-ok-bg text-ok', icon: CheckCircle2 },
  overdue: { cls: 'bg-bad-bg text-bad', icon: AlertCircle },
  present: { cls: 'bg-ok-bg text-ok', icon: CheckCircle2 },
  absent: { cls: 'bg-bad-bg text-bad', icon: XCircle },
  completed: { cls: 'bg-ok-bg text-ok', icon: CheckCircle2 },
  approved: { cls: 'bg-ok-bg text-ok', icon: CheckCircle2 },
  'in-progress': { cls: 'bg-brand-100 text-brand-700', icon: PlayCircle },
  'not-started': { cls: 'bg-navy-50 text-ink-2', icon: Circle },
}

export default function StatusBadge({ status, children }) {
  const { cls, icon: Icon } = styles[status] ?? styles['not-started']
  return (
    <span className={`inline-flex items-center gap-1 rounded-md px-2 py-0.5 text-xs font-semibold whitespace-nowrap ${cls}`}>
      <Icon className="size-3.5" aria-hidden="true" />
      {children}
    </span>
  )
}
