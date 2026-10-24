import { useState } from 'react'
import { BookCheck, Clock, Flame, Target } from 'lucide-react'
import Panel from '../ui/Panel.jsx'
import FilterTabs from '../ui/FilterTabs.jsx'
import ProgressBar from '../ui/ProgressBar.jsx'
import WeeklyActivityChart from './WeeklyActivityChart.jsx'
import { learningTotals, todayIndex, weeklyActivity } from '../../data/learning.js'
import { courseStatus, coursePercent } from '../../data/courses.js'
import { formatMinutes } from '../../lib/format.js'
import { overallProgress } from '../../lib/courses.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

function Metric({ icon: Icon, label, value }) {
  return (
    <div className="flex items-center gap-3">
      <span className="inline-flex size-9 shrink-0 items-center justify-center rounded-lg bg-navy-50 text-navy-700">
        <Icon className="size-[18px]" aria-hidden="true" />
      </span>
      <div className="min-w-0">
        <p className="tabular font-display text-lg leading-tight font-bold">{value}</p>
        <p className="text-xs leading-snug text-ink-3">{label}</p>
      </div>
    </div>
  )
}

export default function LearningProgress({ showCourses = false, id, className }) {
  const { courses } = useDashboard()
  const [week, setWeek] = useState('thisWeek')
  const data = weeklyActivity[week]
  const total = data.minutes.reduce((a, b) => a + b, 0)
  const goal = learningTotals.weeklyGoalMinutes
  const overall = overallProgress(courses)

  return (
    <Panel
      id={id}
      className={className}
      title="Learning progress"
      description={`${data.range}: ${formatMinutes(total)} against a ${goal / 60} h weekly goal${total >= goal ? ', goal met' : ''}`}
      action={
        <FilterTabs
          label="Week"
          value={week}
          onChange={setWeek}
          options={[
            { value: 'thisWeek', label: 'This week' },
            { value: 'lastWeek', label: 'Last week' },
          ]}
        />
      }
    >
      <div className="grid grid-cols-2 gap-4 border-b border-line pb-5 @2xl:grid-cols-4">
        <Metric icon={Target} label="Overall completion" value={`${overall.percent}%`} />
        <Metric icon={BookCheck} label="Lessons this week" value={learningTotals.lessonsThisWeek} />
        <Metric icon={Clock} label="Hours this month" value={learningTotals.hoursThisMonth} />
        <Metric icon={Flame} label="Day streak" value={learningTotals.streakDays} />
      </div>

      <div className="pt-5">
        <WeeklyActivityChart minutes={data.minutes} highlightIndex={week === 'thisWeek' ? todayIndex : -1} />
        {week === 'thisWeek' && (
          <p className="mt-3 flex items-center gap-2 text-xs text-ink-3">
            <span className="size-2.5 rounded-sm bg-brand" aria-hidden="true" />
            Today so far
          </p>
        )}
      </div>

      {showCourses && (
        <div className="mt-6 border-t border-line pt-5">
          <h3 className="text-[15px] font-semibold">Completion by course</h3>
          <ul className="mt-3 space-y-4">
            {courses.map((c) => {
              const pct = coursePercent(c)
              return (
                <li key={c.id}>
                  <div className="mb-1.5 flex items-baseline justify-between gap-4 text-sm">
                    <span className="min-w-0 truncate font-medium">{c.title}</span>
                    <span className="shrink-0 text-ink-3 tabular">
                      {c.completedLessons}/{c.totalLessons} lessons, <span className="font-semibold text-ink">{pct}%</span>
                    </span>
                  </div>
                  <ProgressBar value={pct} tone={courseStatus(c) === 'completed' ? 'ok' : 'brand'} label={`${c.title} progress`} />
                </li>
              )
            })}
          </ul>
        </div>
      )}
    </Panel>
  )
}
