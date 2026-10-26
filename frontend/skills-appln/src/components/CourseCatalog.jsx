import { useMemo, useState } from 'react'
import Container from './Container'
import SectionHeading from './SectionHeading'
import CourseCard from './CourseCard'
import { courses, tracks } from '../data/site'

const filters = [{ key: 'all', label: 'All courses' }, ...Object.entries(tracks).map(([key, t]) => ({ key, label: t.label }))]

export default function CourseCatalog() {
  const [active, setActive] = useState('all')
  const visible = useMemo(() => (active === 'all' ? courses : courses.filter((c) => c.track === active)), [active])

  return (
    <section id="courses" className="border-t border-line bg-white/60 py-20 lg:py-28">
      <Container>
        <SectionHeading
          title="Courses that start from where you are"
          intro="Every course runs live with a mentor, includes recordings and ends with a project you deploy yourself."
        />

        <div role="tablist" aria-label="Filter courses by track" className="-mx-4 mt-10 flex gap-2 overflow-x-auto px-4 pb-1 [scrollbar-width:none] sm:mx-0 sm:px-0">
          {filters.map((f) => {
            const selected = active === f.key
            const count = f.key === 'all' ? courses.length : courses.filter((c) => c.track === f.key).length
            return (
              <button
                key={f.key}
                type="button"
                role="tab"
                aria-selected={selected}
                onClick={() => setActive(f.key)}
                className={`flex shrink-0 items-center gap-2 rounded-full px-4 py-2 text-sm font-semibold transition-colors ${
                  selected ? 'bg-ink text-white' : 'bg-white text-slate ring-1 ring-line hover:text-ink hover:ring-ink/25'
                }`}
              >
                {f.label}
                <span className={`text-xs ${selected ? 'text-white/60' : 'text-slate/70'}`}>{count}</span>
              </button>
            )
          })}
        </div>

        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {visible.map((course) => (
            <CourseCard key={course.id} course={course} />
          ))}
        </div>
      </Container>
    </section>
  )
}
