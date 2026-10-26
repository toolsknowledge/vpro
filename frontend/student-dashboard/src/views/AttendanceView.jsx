import { useState } from 'react'
import Panel from '../components/ui/Panel.jsx'
import FilterTabs from '../components/ui/FilterTabs.jsx'
import StatusBadge from '../components/ui/StatusBadge.jsx'
import { AttendanceMeter, SessionStrip } from '../components/dashboard/AttendanceSummary.jsx'
import { attendanceRecords, attendanceTotals } from '../data/attendance.js'
import { formatShortDate } from '../lib/format.js'
import { attendancePercent } from '../lib/attendance.js'
import { useDashboard } from '../state/DashboardContext.jsx'

export default function AttendanceView() {
  const { courses } = useDashboard()
  const courseById = Object.fromEntries(courses.map((c) => [c.id, c]))
  const [filter, setFilter] = useState('all')
  const percent = attendancePercent()
  const absent = attendanceRecords.filter((r) => r.status === 'absent').length
  const rows = attendanceRecords.filter((r) => filter === 'all' || r.status === filter)

  return (
    <div className="grid gap-6 *:min-w-0 xl:grid-cols-3">
      <div className="space-y-6">
        <Panel title="Overall attendance" description={`Minimum required: ${attendanceTotals.minimumRequired}%`}>
          <p className="tabular font-display text-5xl font-bold">{percent}%</p>
          <p className="mt-1 text-sm text-ink-2 tabular">
            {attendanceTotals.attended} of {attendanceTotals.total} classes attended, {attendanceTotals.total - attendanceTotals.attended} missed
          </p>
          <AttendanceMeter percent={percent} className="mt-4" />
          <h3 className="mt-6 mb-2 text-sm font-semibold text-ink-2">Last {attendanceRecords.length} sessions</h3>
          <SessionStrip records={attendanceRecords} />
        </Panel>
        <Panel title="By course">
          <ul className="space-y-4">
            {attendanceTotals.byCourse.map((row) => {
              const pct = Math.round((row.attended / row.total) * 100)
              return (
                <li key={row.courseId}>
                  <div className="mb-1.5 flex justify-between gap-3 text-sm">
                    <span className="min-w-0 truncate font-medium">{courseById[row.courseId].title}</span>
                    <span className="shrink-0 text-ink-3 tabular">
                      {row.attended}/{row.total}, <span className="font-semibold text-ink">{pct}%</span>
                    </span>
                  </div>
                  <AttendanceMeter percent={pct} />
                </li>
              )
            })}
          </ul>
        </Panel>
      </div>

      <Panel
        className="xl:col-span-2"
        title="Session records"
        description="Most recent first"
        action={
          <FilterTabs
            label="Filter sessions"
            value={filter}
            onChange={setFilter}
            options={[
              { value: 'all', label: 'All', count: attendanceRecords.length },
              { value: 'present', label: 'Present', count: attendanceRecords.length - absent },
              { value: 'absent', label: 'Absent', count: absent },
            ]}
          />
        }
      >
        <div className="-mx-5 overflow-x-auto">
          <table className="w-full min-w-[560px] text-left text-sm">
            <thead>
              <tr className="border-y border-line bg-canvas text-xs text-ink-3">
                <th scope="col" className="px-5 py-2 font-medium">Date</th>
                <th scope="col" className="px-3 py-2 font-medium">Course</th>
                <th scope="col" className="px-3 py-2 font-medium">Topic</th>
                <th scope="col" className="px-5 py-2 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {rows.map((r) => (
                <tr key={r.id}>
                  <td className="px-5 py-3 whitespace-nowrap text-ink-2 tabular">{formatShortDate(r.date)}</td>
                  <td className="px-3 py-3 text-ink-2">{courseById[r.courseId].title}</td>
                  <td className="px-3 py-3 font-medium">{r.topic}</td>
                  <td className="px-5 py-3">
                    <StatusBadge status={r.status}>{r.status === 'present' ? 'Present' : 'Absent'}</StatusBadge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Panel>
    </div>
  )
}
