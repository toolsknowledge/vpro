import { ChevronRight, MonitorPlay, School, UserRound } from 'lucide-react'
import Panel from '../ui/Panel.jsx'
import { upcomingClasses } from '../../data/classes.js'
import { formatTime, parseDate } from '../../lib/format.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

const dayFmt = new Intl.DateTimeFormat('en-IN', { weekday: 'short' })
const monthFmt = new Intl.DateTimeFormat('en-IN', { month: 'short' })

export default function UpcomingClasses({ limit }) {
  const { courses, actions } = useDashboard()
  const courseById = Object.fromEntries(courses.map((c) => [c.id, c]))
  const items = limit ? upcomingClasses.slice(0, limit) : upcomingClasses

  return (
    <Panel title="Upcoming classes" description="Next 7 days. Select a class for details.">
      <ol className="space-y-2.5">
        {items.map((c) => {
          const start = parseDate(c.start)
          const ModeIcon = c.mode === 'Live online' ? MonitorPlay : School
          return (
            <li key={c.id}>
              {/* The whole row opens the class details. */}
              <button
                type="button"
                onClick={() => actions.openModal('class', c.id)}
                className="group flex w-full gap-3.5 rounded-lg border border-line p-3 text-left transition-colors hover:border-navy-300 hover:bg-navy-50/50"
              >
                <span className="flex w-12 shrink-0 flex-col items-center justify-center rounded-md bg-navy-50 py-1.5 text-center" aria-hidden="true">
                  <span className="text-xs text-ink-3">{dayFmt.format(start)}</span>
                  <span className="tabular font-display text-xl leading-tight font-bold text-navy-900">{start.getDate()}</span>
                  <span className="text-xs text-ink-3">{monthFmt.format(start)}</span>
                </span>
                <span className="min-w-0 flex-1">
                  <span className="sr-only">View details: </span>
                  <span className="block leading-snug font-medium text-ink">{c.title}</span>
                  <span className="block truncate text-[13px] text-ink-3">{courseById[c.courseId].title}</span>
                  <span className="mt-1.5 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-ink-2">
                    <span className="sr-only">{start.toDateString()}, </span>
                    <span className="tabular font-semibold text-ink">
                      {formatTime(c.start)} – {formatTime(c.end)}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <UserRound className="size-3.5" aria-hidden="true" />
                      {c.trainer}
                    </span>
                    <span className="inline-flex items-center gap-1">
                      <ModeIcon className="size-3.5" aria-hidden="true" />
                      {c.mode}
                    </span>
                  </span>
                </span>
                <ChevronRight className="size-4 shrink-0 self-center text-ink-3 transition-transform group-hover:translate-x-0.5 group-hover:text-navy-700" aria-hidden="true" />
              </button>
            </li>
          )
        })}
      </ol>
    </Panel>
  )
}
