import { Award, PlayCircle } from 'lucide-react'
import Button from '../ui/Button.jsx'
import CourseThumb from '../ui/CourseThumb.jsx'
import ProgressBar from '../ui/ProgressBar.jsx'
import StatusBadge from '../ui/StatusBadge.jsx'
import { courseStatus, coursePercent, courseStatusLabels } from '../../data/courses.js'
import { nextLesson } from '../../lib/courses.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

export default function CourseCard({ course, onNavigate }) {
  const { actions } = useDashboard()
  const status = courseStatus(course)
  const percent = coursePercent(course)

  return (
    <article className="flex flex-col rounded-card border border-line bg-white p-4">
      <div className="flex items-start justify-between gap-3">
        <CourseThumb pattern={course.pattern} compact className="size-10" />
        <StatusBadge status={status}>{courseStatusLabels[status]}</StatusBadge>
      </div>
      <h3 className="mt-3 text-[15px] leading-snug font-semibold">{course.title}</h3>
      <p className="mt-0.5 text-[13px] text-ink-3">{course.instructor}</p>

      <div className="mt-4">
        <div className="mb-1.5 flex items-baseline justify-between text-[13px]">
          <span className="text-ink-2 tabular">
            {course.completedLessons} of {course.totalLessons} lessons
          </span>
          <span className="font-semibold text-ink tabular">{percent}%</span>
        </div>
        <ProgressBar value={percent} tone={status === 'completed' ? 'ok' : 'brand'} label={`${course.title} progress`} />
      </div>

      <p className="mt-3 text-[13px] text-ink-2">
        {status === 'completed' ? (
          'All lessons complete. Your certificate is ready.'
        ) : (
          <>
            <span className="text-ink-3">{status === 'not-started' ? 'First lesson: ' : 'Next: '}</span>
            <span className="font-medium text-ink">{nextLesson(course).title}</span>
          </>
        )}
      </p>

      <div className="mt-auto pt-4">
        {status === 'completed' ? (
          <Button className="w-full" icon={Award} onClick={() => onNavigate('certificates')}>
            View certificate
          </Button>
        ) : (
          <Button variant="soft" className="w-full" icon={PlayCircle} onClick={() => actions.openModal('lesson', course.id)}>
            {status === 'not-started' ? 'Start course' : 'Continue learning'}
          </Button>
        )}
      </div>
    </article>
  )
}
