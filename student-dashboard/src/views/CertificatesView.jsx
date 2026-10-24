import { useState } from 'react'
import { Award, Lock } from 'lucide-react'
import Button from '../components/ui/Button.jsx'
import Modal from '../components/ui/Modal.jsx'
import ProgressBar from '../components/ui/ProgressBar.jsx'
import DemoNote from '../components/ui/DemoNote.jsx'
import logo from '../assets/logo.jpeg'
import { courseStatus, coursePercent } from '../data/courses.js'
import { student } from '../data/student.js'
import { useDashboard } from '../state/DashboardContext.jsx'

function CertificatePreview({ course }) {
  return (
    <div className="rounded-lg border-2 border-navy-900 p-1">
      <div className="rounded border border-brand px-6 py-8 text-center">
        <img src={logo} alt="VPRO Skills" width="96" height="66" className="mx-auto h-[66px] w-24 object-contain" />
        <p className="mt-4 text-sm text-ink-3">Certificate of completion</p>
        <p className="mt-3 font-display text-2xl font-bold">
          {student.firstName} {student.lastName}
        </p>
        <p className="mt-2 text-sm text-ink-2">has completed all {course.totalLessons} lessons of</p>
        <p className="mt-1 font-display text-lg font-semibold text-navy-800">{course.title}</p>
        <p className="mt-5 text-xs text-ink-3">
          Instructor: {course.instructor}. Student ID {student.studentId}
        </p>
      </div>
    </div>
  )
}

export default function CertificatesView({ onNavigate }) {
  const { courses } = useDashboard()
  const [viewing, setViewing] = useState(null)
  const earned = courses.filter((c) => courseStatus(c) === 'completed')
  const locked = courses.filter((c) => courseStatus(c) !== 'completed')

  return (
    <div className="space-y-8">
      <section aria-labelledby="earned-title">
        <h2 id="earned-title" className="text-[17px] font-semibold">
          Earned ({earned.length})
        </h2>
        <div className="mt-3 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {earned.map((c) => (
            <article key={c.id} className="flex items-center gap-4 rounded-card border border-line bg-white p-4">
              <span className="inline-flex size-11 shrink-0 items-center justify-center rounded-lg bg-navy-900 text-brand">
                <Award className="size-5" aria-hidden="true" />
              </span>
              <div className="min-w-0 flex-1">
                <h3 className="text-[15px] leading-snug font-semibold">{c.title}</h3>
                <p className="text-[13px] text-ink-3">{c.instructor}</p>
              </div>
              <Button size="sm" onClick={() => setViewing(c)}>
                View<span className="sr-only"> {c.title} certificate</span>
              </Button>
            </article>
          ))}
        </div>
      </section>

      <section aria-labelledby="locked-title">
        <h2 id="locked-title" className="text-[17px] font-semibold">
          In progress ({locked.length})
        </h2>
        <p className="mt-0.5 text-[13px] text-ink-3">Finish every lesson and keep attendance at 75% or more to unlock these.</p>
        <div className="mt-3 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {locked.map((c) => (
            <article key={c.id} className="rounded-card border border-line bg-white p-4">
              <div className="flex items-center gap-3">
                <Lock className="size-4 shrink-0 text-ink-3" aria-hidden="true" />
                <h3 className="min-w-0 text-[15px] leading-snug font-semibold">{c.title}</h3>
              </div>
              <div className="mt-3 mb-1.5 flex justify-between text-[13px]">
                <span className="text-ink-2 tabular">{c.totalLessons - c.completedLessons} lessons to go</span>
                <span className="font-semibold tabular">{coursePercent(c)}%</span>
              </div>
              <ProgressBar value={coursePercent(c)} label={`${c.title} progress`} size="sm" />
            </article>
          ))}
        </div>
        <Button className="mt-4" onClick={() => onNavigate('courses')}>
          Go to my courses
        </Button>
      </section>

      {viewing && (
        <Modal title="Certificate" subtitle={viewing.title} size="lg" onClose={() => setViewing(null)} footer={<Button onClick={() => setViewing(null)}>Close</Button>}>
          <CertificatePreview course={viewing} />
          <DemoNote className="mt-4">This is a preview. Verified, downloadable certificates are issued by the institute and are not part of this prototype.</DemoNote>
        </Modal>
      )}
    </div>
  )
}
