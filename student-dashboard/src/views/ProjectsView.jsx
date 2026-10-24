import { useState } from 'react'
import { CheckCircle2, ChevronDown, Circle } from 'lucide-react'
import ProgressBar from '../components/ui/ProgressBar.jsx'
import StatusBadge from '../components/ui/StatusBadge.jsx'
import { projectStatusLabels, projects } from '../data/projects.js'
import { formatDate } from '../lib/format.js'
import { useDashboard } from '../state/DashboardContext.jsx'

function ProjectCard({ project, courseTitle }) {
  const [open, setOpen] = useState(false)
  const done = project.milestones.filter((m) => m.done).length
  const pct = Math.round((done / project.milestones.length) * 100)
  const listId = `milestones-${project.id}`

  return (
    <article className="flex flex-col rounded-card border border-line bg-white p-5">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h2 className="text-[16px] font-semibold">{project.title}</h2>
          <p className="text-[13px] text-ink-3">{courseTitle}</p>
        </div>
        <StatusBadge status={project.status}>{projectStatusLabels[project.status]}</StatusBadge>
      </div>
      <p className="mt-3 text-sm text-ink-2">{project.summary}</p>
      <ul className="mt-3 flex flex-wrap gap-1.5" aria-label="Tech stack">
        {project.stack.map((s) => (
          <li key={s} className="rounded-md bg-navy-50 px-2 py-0.5 text-xs font-medium text-navy-800">
            {s}
          </li>
        ))}
      </ul>
      <div className="mt-4">
        <div className="mb-1.5 flex justify-between text-[13px]">
          <span className="text-ink-2 tabular">
            {done} of {project.milestones.length} milestones
          </span>
          <span className="text-ink-3 tabular">Due {formatDate(project.due)}</span>
        </div>
        <ProgressBar value={pct} tone={pct === 100 ? 'ok' : 'brand'} label={`${project.title} milestones`} />
      </div>
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        aria-expanded={open}
        aria-controls={listId}
        className="mt-4 inline-flex items-center gap-1.5 self-start rounded text-sm font-semibold text-navy-700 hover:text-navy-900"
      >
        {open ? 'Hide milestones' : 'Show milestones'}
        <ChevronDown className={`size-4 transition-transform ${open ? 'rotate-180' : ''}`} aria-hidden="true" />
      </button>
      {open && (
        <ol id={listId} className="mt-3 space-y-2 border-t border-line pt-3">
          {project.milestones.map((m) => (
            <li key={m.title} className="flex items-center gap-2 text-sm">
              {m.done ? <CheckCircle2 className="size-4 text-ok" aria-hidden="true" /> : <Circle className="size-4 text-navy-300" aria-hidden="true" />}
              <span className={m.done ? 'text-ink-2' : 'text-ink'}>{m.title}</span>
              <span className="sr-only">{m.done ? ', done' : ', to do'}</span>
            </li>
          ))}
        </ol>
      )}
    </article>
  )
}

export default function ProjectsView() {
  const { courses } = useDashboard()
  const courseById = Object.fromEntries(courses.map((c) => [c.id, c]))
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {projects.map((p) => (
        <ProjectCard key={p.id} project={p} courseTitle={courseById[p.courseId].title} />
      ))}
    </div>
  )
}
