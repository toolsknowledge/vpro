import { useState } from 'react'
import { BookOpen, Search } from 'lucide-react'
import CourseCard from '../components/dashboard/CourseCard.jsx'
import FilterTabs from '../components/ui/FilterTabs.jsx'
import EmptyState from '../components/ui/EmptyState.jsx'
import Button from '../components/ui/Button.jsx'
import { courseStatus } from '../data/courses.js'
import { useDashboard } from '../state/DashboardContext.jsx'

export default function CoursesView({ onNavigate }) {
  const { courses } = useDashboard()
  const [filter, setFilter] = useState('all')
  const [query, setQuery] = useState('')

  const count = (s) => courses.filter((c) => courseStatus(c) === s).length
  const q = query.trim().toLowerCase()
  const visible = courses
    .filter((c) => filter === 'all' || courseStatus(c) === filter)
    .filter((c) => !q || `${c.title} ${c.instructor}`.toLowerCase().includes(q))

  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <FilterTabs
          label="Filter courses by status"
          value={filter}
          onChange={setFilter}
          options={[
            { value: 'all', label: 'All', count: courses.length },
            { value: 'in-progress', label: 'In progress', count: count('in-progress') },
            { value: 'not-started', label: 'Not started', count: count('not-started') },
            { value: 'completed', label: 'Completed', count: count('completed') },
          ]}
        />
        <div className="relative md:w-72">
          <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-ink-3" aria-hidden="true" />
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search by course or instructor"
            aria-label="Search courses"
            className="h-10 w-full rounded-lg border border-line bg-white pr-3 pl-9 text-sm focus:border-navy-500 focus:outline-none"
          />
        </div>
      </div>

      {visible.length ? (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
          {visible.map((c) => (
            <CourseCard key={c.id} course={c} onNavigate={onNavigate} />
          ))}
        </div>
      ) : (
        <EmptyState
          icon={BookOpen}
          title="No courses match"
          action={
            <Button
              onClick={() => {
                setFilter('all')
                setQuery('')
              }}
            >
              Clear filters
            </Button>
          }
        >
          Try another name, or clear the filters to see all your courses.
        </EmptyState>
      )}
    </div>
  )
}
