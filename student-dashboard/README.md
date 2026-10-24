# VPRO Skills EDUTECH – Student Dashboard

Frontend-only prototype of the student dashboard: courses, learning progress, attendance,
assignments, upcoming classes, announcements, projects, certificates, support and settings.

All content is static sample data in `src/data/`. There is no backend, database, authentication
or API integration. Actions such as completing a lesson or submitting an assignment update
in-memory state and reset on reload.

## Run

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # production build into dist/
npm run lint     # oxlint
```

## Structure

```
src/
  App.jsx                 layout shell and view switching (hash based: #/courses, #/attendance …)
  state/DashboardContext  reducer for courses, assignments, notifications, modals, toasts, prefs
  data/                   static sample data
  components/
    layout/               Sidebar, Header, SearchBox, NotificationPanel, ProfileMenu
    dashboard/            WelcomeSection, StatCard, CourseCard, LearningProgress, AttendanceSummary,
                          AssignmentList, UpcomingClasses, Announcements, StudentProfile
    modals/               lesson, assignment and class detail dialogs
    ui/                   Button, Panel, ProgressBar, StatusBadge, FilterTabs, Modal, Toasts …
  views/                  one component per sidebar item
```

To connect a real backend later, replace the imports from `src/data/` in
`state/DashboardContext.jsx` with fetched data and keep the reducer actions.
