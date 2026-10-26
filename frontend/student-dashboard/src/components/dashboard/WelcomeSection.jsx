import { CalendarDays, Flame, GraduationCap } from 'lucide-react'
import Button from '../ui/Button.jsx'
import { student } from '../../data/student.js'
import { learningTotals } from '../../data/learning.js'
import { useDashboard } from '../../state/DashboardContext.jsx'
import { greeting } from '../../lib/format.js'
import { nextLesson } from '../../lib/courses.js'

// The lessons of the current module drawn as a track: done, current, still ahead.
function ModuleTrack({ total, done }) {
  return (
    <ol className="flex gap-1.5" aria-label={`Lesson ${done + 1} of ${total} in this module`}>
      {Array.from({ length: total }, (_, i) => {
        const state = i < done ? 'done' : i === done ? 'current' : 'ahead'
        return (
          <li
            key={i}
            className={`h-2 flex-1 rounded-full ${
              state === 'done' ? 'bg-brand' : state === 'current' ? 'lesson-current bg-brand/35 ring-1 ring-brand' : 'bg-white/15'
            }`}
          >
            <span className="sr-only">
              Lesson {i + 1}: {state === 'done' ? 'completed' : state === 'current' ? 'up next' : 'not started'}
            </span>
          </li>
        )
      })}
    </ol>
  )
}

export default function WelcomeSection() {
  const { courses, actions } = useDashboard()
  const course = courses.find((c) => c.title === student.program) ?? courses[0]
  const lesson = nextLesson(course)
  const left = course.moduleLessons - course.moduleCompleted

  return (
    <section aria-labelledby="welcome-title" className="on-dark overflow-hidden rounded-2xl bg-navy-900 text-white">
      <div className="grid gap-6 p-5 sm:p-7 lg:grid-cols-[1fr_minmax(0,400px)] lg:items-center lg:gap-10">
        <div className="min-w-0">
          <h2 id="welcome-title" className="text-2xl font-bold text-white sm:text-[28px]">
            {greeting()}, {student.firstName}
          </h2>
          <p className="mt-2 max-w-[52ch] text-[15px] leading-relaxed text-navy-100">
            {left > 0
              ? `${left} lessons stand between you and finishing ${course.module.split(': ')[1] ?? 'this module'}. One lesson today keeps your streak alive.`
              : 'You have finished this module. Start the next one while the ideas are fresh.'}
          </p>
          <dl className="mt-5 flex flex-wrap gap-x-6 gap-y-2 text-sm">
            <div className="flex items-center gap-2">
              <dt className="sr-only">Programme</dt>
              <GraduationCap className="size-4 text-navy-300" aria-hidden="true" />
              <dd className="font-semibold text-white">{student.program}</dd>
            </div>
            <div className="flex items-center gap-2">
              <dt className="sr-only">Batch</dt>
              <CalendarDays className="size-4 text-navy-300" aria-hidden="true" />
              <dd className="text-navy-100">{student.batch}</dd>
            </div>
            <div className="flex items-center gap-2">
              <dt className="sr-only">Learning streak</dt>
              <Flame className="size-4 text-brand" aria-hidden="true" />
              <dd className="text-navy-100">
                <span className="font-semibold text-white">{learningTotals.streakDays} day</span> streak
              </dd>
            </div>
          </dl>
        </div>

        <div className="rounded-xl bg-navy-950/60 p-5 ring-1 ring-white/10">
          <p className="text-[13px] text-navy-300">Pick up where you left off</p>
          <p className="mt-1 truncate font-display text-lg font-semibold text-white">{lesson.title}</p>
          <p className="mt-0.5 truncate text-sm text-navy-100">
            {course.module}, {lesson.duration} min
          </p>
          {course.moduleLessons > 0 && (
            <div className="mt-4">
              <ModuleTrack total={course.moduleLessons} done={course.moduleCompleted} />
              <p className="mt-2 text-xs text-navy-100 tabular">
                Lesson {Math.min(course.moduleCompleted + 1, course.moduleLessons)} of {course.moduleLessons} in this module
              </p>
            </div>
          )}
          <Button variant="accent" className="mt-5" onClick={() => actions.openModal('lesson', course.id)}>
            Resume lesson
          </Button>
        </div>
      </div>
    </section>
  )
}
