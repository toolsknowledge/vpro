import { useId, useMemo, useRef, useState } from 'react'
import { BookOpen, ClipboardList, Search } from 'lucide-react'
import { useDashboard } from '../../state/DashboardContext.jsx'
import { courseStatus } from '../../data/courses.js'
import { useDismiss } from '../../hooks/useDismiss.js'

// Searches courses and assignments. Picking a result opens it directly.
export default function SearchBox({ onNavigate, className = '', autoFocus = false }) {
  const { courses, assignments, actions } = useDashboard()
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(false)
  const [activeIndex, setActiveIndex] = useState(0)
  const wrapRef = useRef(null)
  const listId = useId()

  useDismiss(wrapRef, open, () => setOpen(false))

  const results = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return []
    const courseById = Object.fromEntries(courses.map((c) => [c.id, c]))
    const courseHits = courses
      .filter((c) => `${c.title} ${c.instructor}`.toLowerCase().includes(q))
      .map((c) => ({ type: 'course', id: c.id, title: c.title, meta: c.instructor, item: c }))
    const assignmentHits = assignments
      .filter((a) => `${a.title} ${courseById[a.courseId].title}`.toLowerCase().includes(q))
      .map((a) => ({ type: 'assignment', id: a.id, title: a.title, meta: courseById[a.courseId].title, item: a }))
    return [...courseHits, ...assignmentHits].slice(0, 8)
  }, [query, courses, assignments])

  const choose = (result) => {
    if (result.type === 'course') {
      if (courseStatus(result.item) === 'completed') onNavigate('certificates')
      else actions.openModal('lesson', result.id)
    } else {
      actions.openModal('assignment', result.id)
    }
    setQuery('')
    setOpen(false)
  }

  const onKeyDown = (e) => {
    if (!results.length) return
    if (e.key === 'ArrowDown') {
      e.preventDefault()
      setOpen(true)
      setActiveIndex((i) => (i + 1) % results.length)
    } else if (e.key === 'ArrowUp') {
      e.preventDefault()
      setActiveIndex((i) => (i - 1 + results.length) % results.length)
    } else if (e.key === 'Enter') {
      e.preventDefault()
      choose(results[activeIndex])
    } else if (e.key === 'Escape') {
      setOpen(false)
    }
  }

  const showList = open && query.trim().length > 0

  return (
    <div ref={wrapRef} className={`relative ${className}`}>
      <Search className="pointer-events-none absolute top-1/2 left-3 size-4 -translate-y-1/2 text-ink-3" aria-hidden="true" />
      <input
        type="search"
        role="combobox"
        aria-label="Search courses and assignments"
        aria-expanded={showList}
        aria-controls={listId}
        aria-activedescendant={showList && results[activeIndex] ? `${listId}-${activeIndex}` : undefined}
        aria-autocomplete="list"
        autoFocus={autoFocus}
        value={query}
        onChange={(e) => {
          setQuery(e.target.value)
          setActiveIndex(0)
          setOpen(true)
        }}
        onFocus={() => setOpen(true)}
        onKeyDown={onKeyDown}
        placeholder="Search courses and assignments"
        className="h-10 w-full rounded-lg border border-line bg-canvas pr-3 pl-9 text-sm text-ink placeholder:text-ink-3 focus:border-navy-500 focus:bg-white focus:outline-none"
      />
      {showList && (
        <div className="absolute inset-x-0 top-12 z-30 overflow-hidden rounded-xl border border-line bg-white shadow-pop">
          {results.length ? (
            <ul id={listId} role="listbox" aria-label="Search results" className="max-h-80 overflow-y-auto py-1">
              {results.map((r, i) => {
                const Icon = r.type === 'course' ? BookOpen : ClipboardList
                return (
                  <li
                    key={`${r.type}-${r.id}`}
                    id={`${listId}-${i}`}
                    role="option"
                    aria-selected={i === activeIndex}
                    onMouseEnter={() => setActiveIndex(i)}
                    onMouseDown={(e) => e.preventDefault()}
                    onClick={() => choose(r)}
                    className={`flex cursor-pointer items-center gap-3 px-3 py-2 ${i === activeIndex ? 'bg-navy-50' : ''}`}
                  >
                    <Icon className="size-4 shrink-0 text-navy-500" aria-hidden="true" />
                    <span className="min-w-0">
                      <span className="block truncate text-sm font-medium text-ink">{r.title}</span>
                      <span className="block truncate text-xs text-ink-3">
                        {r.type === 'course' ? 'Course' : 'Assignment'}, {r.meta}
                      </span>
                    </span>
                  </li>
                )
              })}
            </ul>
          ) : (
            <p id={listId} className="px-4 py-3 text-sm text-ink-3">
              No courses or assignments match “{query.trim()}”.
            </p>
          )}
        </div>
      )}
    </div>
  )
}
