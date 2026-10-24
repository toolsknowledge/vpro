import { useCallback, useRef, useState } from 'react'
import { ChevronDown, LifeBuoy, Settings, UserRound } from 'lucide-react'
import Avatar from '../ui/Avatar.jsx'
import { student } from '../../data/student.js'
import { useDismiss } from '../../hooks/useDismiss.js'

export default function ProfileMenu({ onNavigate }) {
  const [open, setOpen] = useState(false)
  const ref = useRef(null)
  const close = useCallback(() => setOpen(false), [])
  useDismiss(ref, open, close)
  const name = `${student.firstName} ${student.lastName}`

  const go = (view) => {
    setOpen(false)
    onNavigate(view)
  }

  const items = [
    { label: 'View profile', icon: UserRound, view: 'settings' },
    { label: 'Settings', icon: Settings, view: 'settings' },
    { label: 'Help & Support', icon: LifeBuoy, view: 'support' },
  ]

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-haspopup="true"
        className="flex items-center gap-2.5 rounded-lg py-1 pr-1.5 pl-1 hover:bg-navy-50 sm:pr-2"
      >
        <Avatar name={name} size="sm" />
        <span className="hidden text-left md:block">
          <span className="block text-sm leading-tight font-semibold text-ink">{name}</span>
          <span className="block text-xs leading-tight text-ink-3">{student.studentId}</span>
        </span>
        <ChevronDown className="hidden size-4 text-ink-3 sm:block" aria-hidden="true" />
        <span className="sr-only md:hidden">Open profile menu for {name}</span>
      </button>

      {open && (
        <div className="absolute top-12 right-0 z-40 w-72 overflow-hidden rounded-xl border border-line bg-white shadow-pop">
          <div className="flex items-center gap-3 border-b border-line px-4 py-4">
            <Avatar name={name} />
            <div className="min-w-0">
              <p className="truncate font-semibold">{name}</p>
              <p className="truncate text-xs text-ink-3">{student.email}</p>
              <p className="mt-1 truncate text-xs font-medium text-navy-700">{student.program}</p>
            </div>
          </div>
          <ul className="py-1">
            {items.map(({ label, icon: Icon, view }) => (
              <li key={label}>
                <button type="button" onClick={() => go(view)} className="flex w-full items-center gap-3 px-4 py-2.5 text-sm text-ink-2 hover:bg-navy-50 hover:text-navy-900">
                  <Icon className="size-4 text-ink-3" aria-hidden="true" />
                  {label}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
