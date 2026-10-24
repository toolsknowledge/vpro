import LearningProgress from '../components/dashboard/LearningProgress.jsx'
import Panel from '../components/ui/Panel.jsx'
import Button from '../components/ui/Button.jsx'
import { courseStatus } from '../data/courses.js'
import { nextLesson } from '../lib/courses.js'
import { useDashboard } from '../state/DashboardContext.jsx'

export default function LearningView() {
  const { courses, actions } = useDashboard()
  const active = courses.filter((c) => courseStatus(c) !== 'completed')

  return (
    <div className="grid gap-6 *:min-w-0 xl:grid-cols-3">
      <div className="xl:col-span-2">
        <LearningProgress showCourses />
      </div>
      <Panel title="Up next" description="The next lesson in each course">
        <ul className="divide-y divide-line">
          {active.map((c) => {
            const lesson = nextLesson(c)
            return (
              <li key={c.id} className="py-3 first:pt-0">
                <p className="text-xs text-ink-3">{c.title}</p>
                <p className="mt-0.5 text-sm font-medium">{lesson.title}</p>
                <div className="mt-2 flex items-center justify-between gap-3">
                  <span className="text-xs text-ink-3 tabular">{lesson.duration} min</span>
                  <Button size="sm" onClick={() => actions.openModal('lesson', c.id)}>
                    {courseStatus(c) === 'not-started' ? 'Start' : 'Continue'}
                    <span className="sr-only"> {c.title}</span>
                  </Button>
                </div>
              </li>
            )
          })}
        </ul>
      </Panel>
    </div>
  )
}
