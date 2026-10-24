import { useState } from 'react'
import { ChevronDown, Clock, Mail, Send } from 'lucide-react'
import Panel from '../components/ui/Panel.jsx'
import Button from '../components/ui/Button.jsx'
import DemoNote from '../components/ui/DemoNote.jsx'
import { faqs, supportTopics } from '../data/support.js'
import { student } from '../data/student.js'
import { useDashboard } from '../state/DashboardContext.jsx'

const fieldClass = 'mt-1 w-full rounded-lg border border-line bg-white px-3 text-sm focus:border-navy-500 focus:outline-none'

export default function SupportView() {
  const { actions } = useDashboard()
  const [sent, setSent] = useState(false)

  const onSubmit = (e) => {
    e.preventDefault()
    setSent(true)
    e.target.reset()
    actions.toast('Request recorded for this demo. No message was sent.', 'success')
  }

  return (
    <div className="grid gap-6 *:min-w-0 xl:grid-cols-5">
      <Panel className="xl:col-span-3" title="Common questions">
        <div className="divide-y divide-line border-y border-line">
          {faqs.map((f) => (
            <details key={f.q} className="group">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-4 py-3.5 font-medium [&::-webkit-details-marker]:hidden">
                {f.q}
                <ChevronDown className="size-4 shrink-0 text-ink-3 transition-transform group-open:rotate-180" aria-hidden="true" />
              </summary>
              <p className="max-w-[68ch] pb-4 text-sm leading-relaxed text-ink-2">{f.a}</p>
            </details>
          ))}
        </div>
        <div className="mt-5 grid gap-3 text-sm text-ink-2 sm:grid-cols-2">
          <p className="flex items-center gap-2">
            <Mail className="size-4 text-navy-500" aria-hidden="true" />
            Your mentor: {student.mentor}
          </p>
          <p className="flex items-center gap-2">
            <Clock className="size-4 text-navy-500" aria-hidden="true" />
            Front desk: Mon–Sat, 9 AM–7 PM
          </p>
        </div>
      </Panel>

      <Panel className="xl:col-span-2" title="Ask for help" description="Your mentor usually replies within a working day">
        <form onSubmit={onSubmit} className="space-y-4" onChange={() => sent && setSent(false)}>
          <div>
            <label htmlFor="topic" className="text-sm font-semibold">
              Topic
            </label>
            <select id="topic" required defaultValue="" className={`${fieldClass} h-10`}>
              <option value="" disabled>
                Choose a topic
              </option>
              {supportTopics.map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </div>
          <div>
            <label htmlFor="message" className="text-sm font-semibold">
              What do you need help with?
            </label>
            <textarea id="message" required minLength={10} rows={5} className={`${fieldClass} py-2`} />
          </div>
          <DemoNote>This form is a demonstration. Requests are not sent to the institute.</DemoNote>
          <Button type="submit" variant="primary" icon={Send}>
            Send request
          </Button>
          {sent && (
            <p role="status" className="text-sm font-medium text-ok">
              Request recorded. In the full product, your mentor would be notified.
            </p>
          )}
        </form>
      </Panel>
    </div>
  )
}
