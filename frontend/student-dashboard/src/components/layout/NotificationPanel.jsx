import { useCallback, useRef, useState } from 'react'
import { Award, Bell, CalendarClock, ClipboardList, Megaphone, Star } from 'lucide-react'
import { useDashboard } from '../../state/DashboardContext.jsx'
import { useDismiss } from '../../hooks/useDismiss.js'
import { formatShortDate, formatTime } from '../../lib/format.js'

const kindIcons = { assignment: ClipboardList, class: CalendarClock, grade: Star, announcement: Megaphone, certificate: Award }

export default function NotificationPanel({ onNavigate }) {
  const { notifications, actions } = useDashboard()
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const close = useCallback(() => setOpen(false), [])
  useDismiss(ref, open, close)

  const unread = notifications.filter((n) => !n.read).length

  const openTarget = (n) => {
    actions.readNotification(n.id)
    setOpen(false)
    onNavigate(n.target.view)
    if (n.target.assignmentId) actions.openModal('assignment', n.target.assignmentId)
    if (n.target.classId) actions.openModal('class', n.target.classId)
  }

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-haspopup="true"
        aria-label={unread ? `Notifications, ${unread} unread` : 'Notifications'}
        className="relative inline-flex size-10 items-center justify-center rounded-lg text-ink-2 hover:bg-navy-50 hover:text-navy-900"
      >
        <Bell className="size-5" aria-hidden="true" />
        {unread > 0 && (
          <span className="tabular absolute top-1.5 right-1.5 inline-flex min-w-4 items-center justify-center rounded-full bg-brand px-1 text-[10px] leading-4 font-bold text-navy-950 ring-2 ring-white">
            {unread}
          </span>
        )}
      </button>

      {open && (
        <div className="fixed inset-x-3 top-[68px] z-40 overflow-hidden rounded-xl border border-line bg-white shadow-pop sm:absolute sm:inset-x-auto sm:top-12 sm:right-0 sm:w-96">
          <div className="flex items-center justify-between border-b border-line px-4 py-3">
            <h2 className="text-[15px] font-semibold">Notifications</h2>
            <button
              type="button"
              onClick={actions.readAllNotifications}
              disabled={!unread}
              className="rounded text-[13px] font-semibold text-navy-700 hover:text-navy-900 disabled:text-ink-3"
            >
              Mark all as read
            </button>
          </div>
          <ul className="max-h-[min(420px,calc(100dvh-140px))] divide-y divide-line overflow-y-auto">
            {notifications.map((n) => {
              const Icon = kindIcons[n.kind]
              return (
                <li key={n.id}>
                  <button type="button" onClick={() => openTarget(n)} className={`flex w-full gap-3 px-4 py-3 text-left hover:bg-navy-50 ${n.read ? '' : 'bg-brand-100/35'}`}>
                    <span className="mt-0.5 inline-flex size-8 shrink-0 items-center justify-center rounded-lg bg-navy-50 text-navy-700">
                      <Icon className="size-4" aria-hidden="true" />
                    </span>
                    <span className="min-w-0 flex-1">
                      <span className={`block text-sm ${n.read ? 'text-ink-2' : 'font-semibold text-ink'}`}>{n.text}</span>
                      <span className="mt-0.5 block text-xs text-ink-3">
                        {formatShortDate(n.time.slice(0, 10))}, {formatTime(n.time)}
                      </span>
                    </span>
                    {!n.read && (
                      <span className="mt-2 size-2 shrink-0 rounded-full bg-brand">
                        <span className="sr-only">Unread</span>
                      </span>
                    )}
                  </button>
                </li>
              )
            })}
          </ul>
        </div>
      )}
    </div>
  )
}
