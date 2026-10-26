import { useState } from 'react'
import { Send } from 'lucide-react'
import Modal from '../ui/Modal.jsx'
import Button from '../ui/Button.jsx'
import StatusBadge from '../ui/StatusBadge.jsx'
import DemoNote from '../ui/DemoNote.jsx'
import { assignmentStatusLabels } from '../../data/assignments.js'
import { formatDate } from '../../lib/format.js'
import { useDashboard } from '../../state/DashboardContext.jsx'

export default function AssignmentModal({ assignmentId, onClose }) {
  const { assignments, courses, actions } = useDashboard()
  const [submitting, setSubmitting] = useState(false)
  const assignment = assignments.find((a) => a.id === assignmentId)
  if (!assignment) return null
  const course = courses.find((c) => c.id === assignment.courseId)
  const open = assignment.status !== 'submitted'

  const onSubmit = (e) => {
    e.preventDefault()
    actions.submitAssignment(assignment.id)
    actions.toast(`Assignment submitted: ${assignment.title}`, 'success')
    setSubmitting(false)
  }

  const facts = [
    ['Course', course.title],
    ['Due date', formatDate(assignment.dueDate)],
    ['Points', assignment.points],
    assignment.submittedOn && ['Submitted on', `${formatDate(assignment.submittedOn)}${assignment.late ? ' (late)' : ''}`],
    assignment.grade && ['Grade', assignment.grade],
  ].filter(Boolean)

  return (
    <Modal
      title={assignment.title}
      onClose={onClose}
      footer={
        submitting ? null : (
          <>
            <Button onClick={onClose}>Close</Button>
            {open && (
              <Button variant="primary" icon={Send} onClick={() => setSubmitting(true)}>
                Submit assignment
              </Button>
            )}
          </>
        )
      }
    >
      <StatusBadge status={assignment.status}>{assignmentStatusLabels[assignment.status]}</StatusBadge>
      <dl className="mt-4 grid grid-cols-2 gap-x-6 gap-y-3">
        {facts.map(([label, value]) => (
          <div key={label}>
            <dt className="text-xs text-ink-3">{label}</dt>
            <dd className="text-sm font-medium tabular">{value}</dd>
          </div>
        ))}
      </dl>
      <h3 className="mt-5 text-sm font-semibold">Brief</h3>
      <p className="mt-1 text-sm leading-relaxed text-ink-2">{assignment.description}</p>
      <h3 className="mt-4 text-sm font-semibold">What to submit</h3>
      <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-ink-2">
        {assignment.deliverables.map((d) => (
          <li key={d}>{d}</li>
        ))}
      </ul>

      {submitting && (
        <form onSubmit={onSubmit} className="mt-5 space-y-3 rounded-xl border border-line bg-canvas p-4">
          <div>
            <label htmlFor="submission-link" className="text-sm font-semibold">
              Repository or file link
            </label>
            <input
              id="submission-link"
              type="url"
              required
              autoFocus
              placeholder="https://github.com/your-name/project"
              className="mt-1 h-10 w-full rounded-lg border border-line bg-white px-3 text-sm focus:border-navy-500 focus:outline-none"
            />
          </div>
          <div>
            <label htmlFor="submission-note" className="text-sm font-semibold">
              Note to trainer <span className="font-normal text-ink-3">(optional)</span>
            </label>
            <textarea id="submission-note" rows={3} className="mt-1 w-full rounded-lg border border-line bg-white px-3 py-2 text-sm focus:border-navy-500 focus:outline-none" />
          </div>
          <DemoNote>Nothing is uploaded. The submission is recorded in this browser until you reload the page.</DemoNote>
          <div className="flex justify-end gap-2">
            <Button onClick={() => setSubmitting(false)}>Cancel</Button>
            <Button type="submit" variant="primary" icon={Send}>
              Submit assignment
            </Button>
          </div>
        </form>
      )}
    </Modal>
  )
}
