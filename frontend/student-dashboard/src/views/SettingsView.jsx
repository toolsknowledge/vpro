import StudentProfile from '../components/dashboard/StudentProfile.jsx'
import Panel from '../components/ui/Panel.jsx'
import DemoNote from '../components/ui/DemoNote.jsx'
import { useDashboard } from '../state/DashboardContext.jsx'

const prefItems = [
  { key: 'classReminders', label: 'Class reminders', hint: 'A reminder 30 minutes before each class' },
  { key: 'assignmentReminders', label: 'Assignment due dates', hint: 'A reminder two days before an assignment is due' },
  { key: 'announcementEmails', label: 'Institute announcements', hint: 'Exams, holidays and placement updates' },
  { key: 'weeklyReport', label: 'Weekly progress summary', hint: 'Your learning hours and attendance every Monday' },
]

function Toggle({ checked, onChange, id }) {
  return (
    <button
      id={id}
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => onChange(!checked)}
      className={`relative inline-flex h-6 w-11 shrink-0 items-center rounded-full border-2 transition-colors ${
        checked ? 'border-navy-900 bg-navy-900' : 'border-ink-3 bg-white'
      }`}
    >
      <span className={`inline-block size-4 rounded-full transition-transform ${checked ? 'translate-x-[22px] bg-white' : 'translate-x-0.5 bg-ink-3'}`} />
    </button>
  )
}

export default function SettingsView() {
  const { prefs, actions } = useDashboard()
  return (
    <div className="grid gap-6 *:min-w-0 xl:grid-cols-5">
      <div className="xl:col-span-3">
        <StudentProfile />
      </div>
      <Panel className="xl:col-span-2" title="Notifications" description="Choose what you want to hear about">
        <ul className="divide-y divide-line">
          {prefItems.map((p) => (
            <li key={p.key} className="flex items-center justify-between gap-4 py-3.5 first:pt-0">
              <label htmlFor={`pref-${p.key}`} className="min-w-0 cursor-pointer">
                <span className="block text-sm font-medium">{p.label}</span>
                <span className="block text-[13px] text-ink-3">{p.hint}</span>
              </label>
              <Toggle id={`pref-${p.key}`} checked={prefs[p.key]} onChange={(v) => actions.setPrefs({ [p.key]: v })} />
            </li>
          ))}
        </ul>
        <DemoNote className="mt-4">Preferences are saved in this browser only. No emails or reminders are sent from this prototype.</DemoNote>
      </Panel>
    </div>
  )
}
