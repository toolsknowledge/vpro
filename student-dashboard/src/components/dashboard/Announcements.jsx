import { CalendarDays, Flag } from 'lucide-react'
import Panel from '../ui/Panel.jsx'
import Button from '../ui/Button.jsx'
import { formatDate } from '../../lib/format.js'

export function AnnouncementItem({ item }) {
  return (
    <article className="py-4 first:pt-0 last:pb-0">
      <div className="flex flex-wrap items-center gap-2">
        <span className="rounded-md bg-navy-50 px-2 py-0.5 text-xs font-semibold text-navy-800">{item.category}</span>
        {item.priority === 'high' && (
          <span className="inline-flex items-center gap-1 text-xs font-semibold text-brand-700">
            <Flag className="size-3.5 fill-brand text-brand-700" aria-hidden="true" />
            Important
          </span>
        )}
        <span className="ml-auto inline-flex items-center gap-1 text-xs text-ink-3">
          <CalendarDays className="size-3.5" aria-hidden="true" />
          <time dateTime={item.date}>{formatDate(item.date)}</time>
        </span>
      </div>
      <h3 className="mt-2 text-[15px] leading-snug font-semibold">{item.title}</h3>
      <p className="mt-1 max-w-[72ch] text-sm text-ink-2">{item.body}</p>
    </article>
  )
}

export default function Announcements({ items, onNavigate }) {
  return (
    <Panel
      title="Announcements"
      action={
        <Button size="sm" variant="ghost" onClick={() => onNavigate('announcements')}>
          View all
        </Button>
      }
    >
      <div className="divide-y divide-line">
        {items.map((a) => (
          <AnnouncementItem key={a.id} item={a} />
        ))}
      </div>
    </Panel>
  )
}
