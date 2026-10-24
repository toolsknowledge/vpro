import { BookOpen, CalendarCheck, ClipboardList, Target } from 'lucide-react'
import WelcomeSection from '../components/dashboard/WelcomeSection.jsx'
import StatCard from '../components/dashboard/StatCard.jsx'
import CourseCard from '../components/dashboard/CourseCard.jsx'
import LearningProgress from '../components/dashboard/LearningProgress.jsx'
import AttendanceSummary, { AttendanceMeter } from '../components/dashboard/AttendanceSummary.jsx'
import AssignmentList from '../components/dashboard/AssignmentList.jsx'
import UpcomingClasses from '../components/dashboard/UpcomingClasses.jsx'
import Announcements from '../components/dashboard/Announcements.jsx'
import Panel from '../components/ui/Panel.jsx'
import Button from '../components/ui/Button.jsx'
import ProgressBar from '../components/ui/ProgressBar.jsx'
import StatusBadge from '../components/ui/StatusBadge.jsx'
import { announcements } from '../data/announcements.js'
import { attendanceTotals } from '../data/attendance.js'
import { courseStatus } from '../data/courses.js'
import { overallProgress } from '../lib/courses.js'
import { formatShortDate } from '../lib/format.js'
import { attendancePercent } from '../lib/attendance.js'
import { useDashboard } from '../state/DashboardContext.jsx'

const statusDot = { 'in-progress': 'bg-brand', 'not-started': 'bg-navy-300' }

export default function DashboardView({ onNavigate }) {
  const { courses, assignments } = useDashboard()
  const overall = overallProgress(courses)
  const byStatus = (s) => courses.filter((c) => courseStatus(c) === s).length
  const pending = assignments.filter((a) => a.status === 'pending')
  const overdue = assignments.filter((a) => a.status === 'overdue').length
  const nextDue = [...pending].sort((a, b) => a.dueDate.localeCompare(b.dueDate))[0]
  const activeCourses = courses.filter((c) => courseStatus(c) === 'in-progress').slice(0, 4)
  const attendance = attendancePercent()

  return (
    <div className="space-y-6">
      <WelcomeSection />

      <section aria-label="Summary" className="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-4">
        <StatCard
          icon={BookOpen}
          label="Enrolled courses"
          value={courses.length}
          detail={`${byStatus('completed')} completed`}
          onClick={() => onNavigate('courses')}
        >
          <span className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-ink-2">
            {[
              ['in-progress', 'In progress'],
              ['not-started', 'Not started'],
            ].map(([s, label]) => (
              <span key={s} className="inline-flex items-center gap-1.5">
                <span className={`size-2 rounded-full ${statusDot[s]}`} aria-hidden="true" />
                <span className="tabular font-semibold text-ink">{byStatus(s)}</span> {label.toLowerCase()}
              </span>
            ))}
          </span>
        </StatCard>
        <StatCard
          icon={Target}
          label="Overall progress"
          value={`${overall.percent}%`}
          detail={`${overall.done} of ${overall.total} lessons`}
          onClick={() => onNavigate('learning')}
        >
          <ProgressBar value={overall.percent} label="Overall progress" />
        </StatCard>
        <StatCard
          icon={CalendarCheck}
          label="Attendance"
          value={`${attendance}%`}
          detail={`${attendanceTotals.attended} of ${attendanceTotals.total} classes`}
          onClick={() => onNavigate('attendance')}
        >
          <AttendanceMeter percent={attendance} />
        </StatCard>
        <StatCard
          icon={ClipboardList}
          label="Pending assignments"
          value={pending.length}
          detail={nextDue ? `Next due ${formatShortDate(nextDue.dueDate)}` : 'Nothing due right now'}
          onClick={() => onNavigate('assignments')}
        >
          {overdue ? (
            <StatusBadge status="overdue">{overdue} overdue</StatusBadge>
          ) : (
            <StatusBadge status="submitted">None overdue</StatusBadge>
          )}
        </StatCard>
      </section>

      <div className="grid gap-6 *:min-w-0 xl:grid-cols-3">
        <Panel
          className="xl:col-span-2"
          title="My courses"
          description={`${activeCourses.length} courses in progress`}
          action={
            <Button size="sm" variant="ghost" onClick={() => onNavigate('courses')}>
              All courses
            </Button>
          }
        >
          <div className="grid gap-4 sm:grid-cols-2">
            {activeCourses.map((c) => (
              <CourseCard key={c.id} course={c} onNavigate={onNavigate} />
            ))}
          </div>
        </Panel>
        <UpcomingClasses limit={4} />
      </div>

      <div className="grid gap-6 *:min-w-0 xl:grid-cols-3">
        <LearningProgress id="learning-progress" className="xl:col-span-2" />
        <AttendanceSummary onNavigate={onNavigate} limit={3} />
      </div>

      <div className="grid gap-6 *:min-w-0 xl:grid-cols-3">
        <div className="xl:col-span-2">
          <AssignmentList limit={5} onNavigate={onNavigate} />
        </div>
        <Announcements items={announcements.slice(0, 3)} onNavigate={onNavigate} />
      </div>
    </div>
  )
}
