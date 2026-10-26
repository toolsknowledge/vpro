import LessonModal from './LessonModal.jsx'
import AssignmentModal from './AssignmentModal.jsx'
import ClassModal from './ClassModal.jsx'
import { useDashboard } from '../../state/DashboardContext.jsx'

export default function ModalHost() {
  const { modal, actions } = useDashboard()
  if (!modal) return null
  const key = `${modal.type}-${modal.id}`
  if (modal.type === 'lesson') return <LessonModal key={key} courseId={modal.id} onClose={actions.closeModal} />
  if (modal.type === 'assignment') return <AssignmentModal key={key} assignmentId={modal.id} onClose={actions.closeModal} />
  if (modal.type === 'class') return <ClassModal key={key} classId={modal.id} onClose={actions.closeModal} />
  return null
}
