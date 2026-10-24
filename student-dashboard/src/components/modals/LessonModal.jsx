import { CheckCircle2, Clock, PlayCircle } from 'lucide-react'
import Modal from '../ui/Modal.jsx'
import Button from '../ui/Button.jsx'
import ProgressBar from '../ui/ProgressBar.jsx'
import DemoNote from '../ui/DemoNote.jsx'
import CourseThumb from '../ui/CourseThumb.jsx'
import { courseStatus, coursePercent } from '../../data/courses.js'
import { nextLesson } from '../../lib/courses.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

export default function LessonModal({ courseId, onClose }) {
  const { courses, actions } = useDashboard()
  const course = courses.find((c) => c.id === courseId)
  if (!course) return null
  const done = courseStatus(course) === 'completed'
  const lesson = nextLesson(course)
  const later = course.queue.slice(1, 4)
  const percent = coursePercent(course)

  const complete = () => {
    actions.completeLesson(course.id)
    const remaining = course.totalLessons - course.completedLessons - 1
    actions.toast(remaining ? `Lesson marked as complete. ${remaining} lessons left in this course.` : `Course complete. Your ${course.title} certificate is ready.`, 'success')
  }

  return (
    <Modal
      title={course.title}
      subtitle={`${course.instructor}, ${course.module}`}
      onClose={onClose}
      footer={
        <>
          <Button onClick={onClose}>Close</Button>
          {!done && (
            <Button variant="primary" icon={CheckCircle2} onClick={complete}>
              Mark lesson as complete
            </Button>
          )}
        </>
      }
    >
      {done ? (
        <p className="text-sm text-ink-2">You have completed every lesson in this course. Find your certificate under Certificates.</p>
      ) : (
        <>
          <div className="overflow-hidden rounded-xl border border-line">
            <div className="relative">
              <CourseThumb pattern={course.pattern} className="h-36" />
              <span className="absolute inset-0 flex items-center justify-center">
                <PlayCircle className="size-12 text-white/85" strokeWidth={1.5} aria-hidden="true" />
              </span>
            </div>
            <div className="p-4">
              <p className="text-xs text-ink-3">{course.completedLessons === 0 ? 'First lesson' : 'Up next'}</p>
              <p className="mt-0.5 font-display text-lg font-semibold">{lesson.title}</p>
              <p className="mt-1 inline-flex items-center gap-1.5 text-sm text-ink-3">
                <Clock className="size-4" aria-hidden="true" />
                {lesson.duration} min, lesson {course.completedLessons + 1} of {course.totalLessons}
              </p>
            </div>
          </div>

          <div className="mt-5">
            <div className="mb-1.5 flex justify-between text-[13px]">
              <span className="text-ink-2">Course progress</span>
              <span className="font-semibold tabular">{percent}%</span>
            </div>
            <ProgressBar value={percent} label="Course progress" />
          </div>

          {later.length > 0 && (
            <div className="mt-5">
              <h3 className="text-sm font-semibold">Coming after this</h3>
              <ol className="mt-2 space-y-1.5">
                {later.map((l) => (
                  <li key={l.title} className="flex justify-between gap-4 text-sm text-ink-2">
                    <span className="min-w-0 truncate">{l.title}</span>
                    <span className="shrink-0 text-ink-3 tabular">{l.duration} min</span>
                  </li>
                ))}
              </ol>
            </div>
          )}

          <DemoNote className="mt-5">Video playback is not part of this prototype. Marking a lesson as complete updates your progress until you reload the page.</DemoNote>
        </>
      )}
    </Modal>
  )
}
