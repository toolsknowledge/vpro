import Avatar from '../ui/Avatar.jsx'
import Panel from '../ui/Panel.jsx'
import { student } from '../../data/student.js'
import { formatDate } from '../../lib/format.js'

export default function StudentProfile() {
  const name = `${student.firstName} ${student.lastName}`
  const fields = [
    ['Student ID', student.studentId],
    ['Email', student.email],
    ['Phone', student.phone],
    ['Enrolled program', student.program],
    ['Batch', student.batch],
    ['Education', student.college],
    ['Mentor', student.mentor],
    ['Joined', formatDate(student.joinedOn)],
  ]

  return (
    <Panel id="profile" title="Profile" description="Sample student data for this prototype">
      <div className="flex items-center gap-4">
        <Avatar name={name} size="lg" />
        <div className="min-w-0">
          <p className="font-display text-xl font-bold">{name}</p>
          <p className="text-sm text-ink-3">{student.program}</p>
        </div>
      </div>
      <dl className="mt-6 grid gap-x-8 gap-y-4 sm:grid-cols-2">
        {fields.map(([label, value]) => (
          <div key={label} className="min-w-0 border-b border-line pb-3">
            <dt className="text-xs text-ink-3">{label}</dt>
            <dd className="mt-0.5 text-sm font-medium break-words">{value}</dd>
          </div>
        ))}
      </dl>
    </Panel>
  )
}
