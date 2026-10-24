import { Check, X } from 'lucide-react'
import Panel from '../ui/Panel.jsx'
import Button from '../ui/Button.jsx'
import StatusBadge from '../ui/StatusBadge.jsx'
import { attendanceRecords, attendanceTotals } from '../../data/attendance.js'
import { formatShortDate } from '../../lib/format.js'
import { attendancePercent } from '../../lib/attendance.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

// Percentage bar with a tick at the minimum attendance requirement.
export function AttendanceMeter({ percent, className = '' }) {
  const min = attendanceTotals.minimumRequired
  return (
    <div className={`relative ${className}`}>
      <div
        role="progressbar"
        aria-valuenow={percent}
        aria-valuemin={0}
        aria-valuemax={100}
        aria-label={`Attendance ${percent}%, minimum required ${min}%`}
        className="h-2 overflow-hidden rounded-full bg-navy-100"
      >
        <div className={`h-full rounded-full ${percent >= min ? 'bg-ok' : 'bg-bad'}`} style={{ width: `${percent}%` }} />
      </div>
      <span className="absolute -top-1 h-4 w-0.5 rounded bg-ink" style={{ left: `${min}%` }} aria-hidden="true" />
    </div>
  )
}

// The last sessions as a strip of squares, oldest on the left.
export function SessionStrip({ records }) {
  return (
    <ol className="flex flex-wrap gap-1.5" aria-label="Recent sessions, oldest first">
      {[...records].reverse().map((r) => (
        <li
          key={r.id}
          title={`${formatShortDate(r.date)}: ${r.status === 'present' ? 'Present' : 'Absent'}`}
          className={`inline-flex size-6 items-center justify-center rounded-md ${
            r.status === 'present' ? 'bg-ok text-white' : 'bg-bad-bg text-bad ring-1 ring-bad/60 ring-inset'
          }`}
        >
          {r.status === 'present' ? <Check className="size-3.5" strokeWidth={3} aria-hidden="true" /> : <X className="size-3.5" strokeWidth={3} aria-hidden="true" />}
          <span className="sr-only">
            {formatShortDate(r.date)}, {r.status}
          </span>
        </li>
      ))}
    </ol>
  )
}

export default function AttendanceSummary({ onNavigate, limit = 4 }) {
  const { courses } = useDashboard()
  const courseById = Object.fromEntries(courses.map((c) => [c.id, c]))
  const percent = attendancePercent()
  const { attended, total, minimumRequired } = attendanceTotals

  return (
    <Panel
      title="Attendance"
      description={`Minimum required: ${minimumRequired}%`}
      action={
        <Button size="sm" variant="ghost" onClick={() => onNavigate('attendance')}>
          Full record
        </Button>
      }
    >
      <div className="flex items-end justify-between gap-4">
        <p className="tabular font-display text-[40px] leading-none font-bold">{percent}%</p>
        <dl className="grid grid-cols-2 gap-x-5 text-right">
          <dt className="text-xs text-ink-3">Attended</dt>
          <dt className="text-xs text-ink-3">Total classes</dt>
          <dd className="tabular font-display text-lg font-bold">{attended}</dd>
          <dd className="tabular font-display text-lg font-bold">{total}</dd>
        </dl>
      </div>
      <AttendanceMeter percent={percent} className="mt-4" />

      <h3 className="mt-6 mb-2 text-sm font-semibold text-ink-2">Last {attendanceRecords.length} sessions</h3>
      <SessionStrip records={attendanceRecords} />

      <ul className="mt-5 divide-y divide-line border-t border-line">
        {attendanceRecords.slice(0, limit).map((r) => (
          <li key={r.id} className="flex items-center justify-between gap-3 py-2.5">
            <div className="min-w-0">
              <p className="truncate text-sm font-medium">{r.topic}</p>
              <p className="truncate text-xs text-ink-3">
                {formatShortDate(r.date)}, {courseById[r.courseId].title}
              </p>
            </div>
            <StatusBadge status={r.status}>{r.status === 'present' ? 'Present' : 'Absent'}</StatusBadge>
          </li>
        ))}
      </ul>
    </Panel>
  )
}
