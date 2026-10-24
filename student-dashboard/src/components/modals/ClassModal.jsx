import { CalendarPlus, Clock, MapPin, UserRound } from 'lucide-react'
import Modal from '../ui/Modal.jsx'
import Button from '../ui/Button.jsx'
import DemoNote from '../ui/DemoNote.jsx'
import { upcomingClasses } from '../../data/classes.js'
import { formatShortDate, formatTime } from '../../lib/format.js'
import { downloadClassIcs } from '../../lib/calendar.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

export default function ClassModal({ classId, onClose }) {
  const { courses, actions } = useDashboard()
  const cls = upcomingClasses.find((c) => c.id === classId)
  if (!cls) return null
  const course = courses.find((c) => c.id === cls.courseId)

  const addToCalendar = () => {
    downloadClassIcs(cls, course.title)
    actions.toast('Calendar file downloaded. Open it to add the class to your calendar.', 'success')
  }

  const facts = [
    [Clock, `${formatShortDate(cls.start.slice(0, 10))}, ${formatTime(cls.start)} – ${formatTime(cls.end)}`],
    [UserRound, cls.trainer],
    [MapPin, cls.mode],
  ]

  return (
    <Modal
      title={cls.title}
      subtitle={course.title}
      onClose={onClose}
      footer={
        <>
          <Button onClick={onClose}>Close</Button>
          <Button variant="primary" icon={CalendarPlus} onClick={addToCalendar}>
            Add to calendar
          </Button>
        </>
      }
    >
      <ul className="space-y-2">
        {facts.map(([Icon, text]) => (
          <li key={text} className="flex items-center gap-2.5 text-sm text-ink-2">
            <Icon className="size-4 text-navy-500" aria-hidden="true" />
            <span className="tabular">{text}</span>
          </li>
        ))}
      </ul>
      <h3 className="mt-5 text-sm font-semibold">Agenda</h3>
      <ol className="mt-1 list-decimal space-y-1 pl-5 text-sm text-ink-2">
        {cls.agenda.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ol>
      <h3 className="mt-4 text-sm font-semibold">Before class</h3>
      <p className="mt-1 text-sm text-ink-2">{cls.prepare}</p>
      <DemoNote className="mt-5">
        {cls.mode === 'Live online'
          ? 'Your trainer shares the joining link before class. This prototype does not create meeting links.'
          : 'Classroom sessions are held at the institute. Arrive 10 minutes early to set up.'}
      </DemoNote>
    </Modal>
  )
}
