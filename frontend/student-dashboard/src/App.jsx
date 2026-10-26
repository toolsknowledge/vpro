import { useCallback, useState } from 'react'
import Sidebar from './components/layout/Sidebar.jsx'
import Header from './components/layout/Header.jsx'
import ModalHost from './components/modals/ModalHost.jsx'
import Toasts from './components/ui/Toasts.jsx'
import DashboardView from './views/DashboardView.jsx'
import CoursesView from './views/CoursesView.jsx'
import LearningView from './views/LearningView.jsx'
import AttendanceView from './views/AttendanceView.jsx'
import AssignmentsView from './views/AssignmentsView.jsx'
import ProjectsView from './views/ProjectsView.jsx'
import CertificatesView from './views/CertificatesView.jsx'
import AnnouncementsView from './views/AnnouncementsView.jsx'
import SupportView from './views/SupportView.jsx'
import SettingsView from './views/SettingsView.jsx'
import { useHashView } from './hooks/useHashView.js'
import { allNavItems } from './data/navigation.js'

const views = {
  dashboard: { component: DashboardView, subtitle: 'Your courses, classes and deadlines at a glance' },
  courses: { component: CoursesView, subtitle: 'Every course you are enrolled in' },
  learning: { component: LearningView, subtitle: 'Time spent, lessons completed and what is next' },
  attendance: { component: AttendanceView, subtitle: 'Classes attended across your programme' },
  assignments: { component: AssignmentsView, subtitle: 'Track due dates and submit your work' },
  projects: { component: ProjectsView, subtitle: 'Capstone and course projects with milestones' },
  certificates: { component: CertificatesView, subtitle: 'Earned certificates and what is left to unlock' },
  announcements: { component: AnnouncementsView, subtitle: 'News from the institute' },
  support: { component: SupportView, subtitle: 'Answers to common questions and a way to reach your mentor' },
  settings: { component: SettingsView, subtitle: 'Your profile and notification preferences' },
}

const COLLAPSE_KEY = 'vpro-sidebar-collapsed'

function readCollapsed() {
  try {
    return localStorage.getItem(COLLAPSE_KEY) === '1'
  } catch {
    return false
  }
}

export default function App() {
  const [view, navigate] = useHashView()
  const [collapsed, setCollapsed] = useState(readCollapsed)
  const [mobileOpen, setMobileOpen] = useState(false)

  const toggleCollapsed = () => {
    setCollapsed((c) => {
      try {
        localStorage.setItem(COLLAPSE_KEY, c ? '0' : '1')
      } catch {
        // Ignore: the sidebar state just won't survive a reload.
      }
      return !c
    })
  }
  const closeMobile = useCallback(() => setMobileOpen(false), [])

  const { component: View, subtitle } = views[view]
  const title = allNavItems.find((item) => item.id === view).label

  return (
    <div className="flex min-h-dvh">
      <a
        href="#main"
        onClick={(e) => {
          // Move focus without touching the hash, which drives view routing.
          e.preventDefault()
          document.getElementById('main').focus()
        }}
        className="sr-only z-50 rounded-lg bg-navy-900 px-4 py-2 text-white focus:not-sr-only focus:fixed focus:top-3 focus:left-3">
        Skip to content
      </a>
      <Sidebar
        view={view}
        onNavigate={navigate}
        collapsed={collapsed}
        onToggleCollapsed={toggleCollapsed}
        mobileOpen={mobileOpen}
        onCloseMobile={closeMobile}
      />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header title={title} subtitle={subtitle} onOpenMobileNav={() => setMobileOpen(true)} onNavigate={navigate} />
        <main id="main" tabIndex={-1} className="mx-auto w-full max-w-[1440px] flex-1 px-4 py-6 focus:outline-none sm:px-6 lg:px-8 lg:py-8">
          <View onNavigate={navigate} />
        </main>
        <footer className="px-4 pb-6 text-center text-xs text-ink-3 sm:px-6 lg:px-8">
          Prototype with sample data. VPRO Skills EDUTECH student dashboard.
        </footer>
      </div>
      <ModalHost />
      <Toasts />
    </div>
  )
}
