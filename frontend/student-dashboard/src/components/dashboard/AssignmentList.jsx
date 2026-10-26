import { useMemo, useState } from 'react'
import { CalendarClock, ClipboardCheck, Search } from 'lucide-react'
import Panel from '../ui/Panel.jsx'
import Button from '../ui/Button.jsx'
import FilterTabs from '../ui/FilterTabs.jsx'
import StatusBadge from '../ui/StatusBadge.jsx'
import EmptyState from '../ui/EmptyState.jsx'
import { assignmentStatusLabels } from '../../data/assignments.js'
import { formatDate } from '../../lib/format.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

const order = { overdue: 0, pending: 1, submitted: 2 }

export default function AssignmentList({ limit, showSearch = false, initialFilter = 'all', onNavigate }) {
  const { assignments, courses, actions } = useDashboard()
  const [filter, setFilter] = useState(initialFilter)
  const [query, setQuery] = useState('')
  const courseById = Object.fromEntries(courses.map((c) => [c.id, c]))

  const counts = useMemo(() => {
    const c = { all: assignments.length, pending: 0, overdue: 0, submitted: 0 }
    assignments.forEach((a) => c[a.status]++)
    return c
  }, [assignments])

  const visible = assignments
    .filter((a) => filter === 'all' || a.status === filter)
    .filter((a) => {
      const q = query.trim().toLowerCase()
      return !q || `${a.title} ${courseById[a.courseId].title}`.toLowerCase().includes(q)
    })
    .sort((a, b) => order[a.status] - order[b.status] || a.dueDate.localeCompare(b.dueDate))

  const shown = limit ? visible.slice(0, limit) : visible

  return (
    <Panel
      title="Assignments"
      description={`${counts.pending} pending, ${counts.overdue} overdue`}
      action={
        limit && onNavigate ? (
          <Button size="sm" variant="ghost" onClick={() => onNavigate('assignments')}>
            All assignments
          </Button>
        ) : null
      }
    >
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <FilterTabs
          label="Filter assignments by status"
          value={filter}
          onChange={setFilter}
          options={[
            { value: 'all', label: 'All', count: counts.all },
            { value: 'pending', label: 'Pending', count: counts.pending },
            { value: 'overdue', label: 'Overdue', count: counts.overdue },
            { value: 'submitted', label: 'Submitted', count: counts.submitted },
          ]}
        />
        {showSearch && (
          <div className="relative sm:w-64">
            <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-ink-3" aria-hidden="true" />
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search assignments"
              aria-label="Search assignments"
              className="h-10 w-full rounded-lg border border-line bg-white pr-3 pl-9 text-sm focus:border-navy-500 focus:outline-none"
            />
          </div>
        )}
      </div>

      {shown.length ? (
        <ul className="mt-4 divide-y divide-line border-y border-line">
          {shown.map((a) => (
            <li key={a.id} className="flex flex-col gap-3 py-3.5 sm:flex-row sm:items-center sm:gap-4">
              <div className="min-w-0 flex-1">
                <p className="font-medium text-ink">{a.title}</p>
                <p className="mt-0.5 text-[13px] text-ink-3">{courseById[a.courseId].title}</p>
              </div>
              <div className="flex flex-wrap items-center gap-x-4 gap-y-2 sm:flex-nowrap">
                <span className={`inline-flex items-center gap-1.5 text-[13px] whitespace-nowrap tabular sm:w-[118px] ${a.status === 'overdue' ? 'font-semibold text-bad' : 'text-ink-2'}`}>
                  <CalendarClock className="size-4" aria-hidden="true" />
                  <span className="sr-only">Due </span>
                  {formatDate(a.dueDate)}
                </span>
                <span className="w-[104px]">
                  <StatusBadge status={a.status}>{assignmentStatusLabels[a.status]}</StatusBadge>
                </span>
                <Button size="sm" onClick={() => actions.openModal('assignment', a.id)} className="ml-auto sm:ml-0">
                  View details
                  <span className="sr-only">: {a.title}</span>
                </Button>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <div className="mt-4">
          <EmptyState icon={ClipboardCheck} title={query ? 'No assignments match your search' : `No ${assignmentStatusLabels[filter]?.toLowerCase() ?? ''} assignments`}>
            {query ? 'Try a different title or course name.' : 'Switch the filter to see the rest of your assignments.'}
          </EmptyState>
        </div>
      )}
      {limit && visible.length > limit && (
        <p className="mt-3 text-[13px] text-ink-3 tabular">
          Showing {limit} of {visible.length}
        </p>
      )}
    </Panel>
  )
}
