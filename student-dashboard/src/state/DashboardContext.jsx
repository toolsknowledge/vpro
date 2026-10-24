import { createContext, useCallback, useContext, useMemo, useReducer } from 'react'
import { courses } from '../data/courses.js'
import { assignments } from '../data/assignments.js'
import { notifications } from '../data/notifications.js'

const DashboardContext = createContext(null)

const PREFS_KEY = 'vpro-dashboard-prefs'

const defaultPrefs = {
  classReminders: true,
  assignmentReminders: true,
  weeklyReport: false,
  announcementEmails: true,
}

function loadPrefs() {
  try {
    const saved = JSON.parse(localStorage.getItem(PREFS_KEY))
    return { ...defaultPrefs, ...saved }
  } catch {
    return defaultPrefs
  }
}

function savePrefs(prefs) {
  try {
    localStorage.setItem(PREFS_KEY, JSON.stringify(prefs))
  } catch {
    // Storage can be unavailable (private mode); preferences then last for the session only.
  }
}

const initialState = {
  courses,
  assignments,
  notifications,
  modal: null, // { type: 'lesson' | 'assignment' | 'class', id }
  toasts: [],
}

function reducer(state, action) {
  switch (action.type) {
    case 'completeLesson':
      return {
        ...state,
        courses: state.courses.map((c) => {
          if (c.id !== action.courseId || c.completedLessons >= c.totalLessons) return c
          return {
            ...c,
            completedLessons: c.completedLessons + 1,
            moduleCompleted: Math.min(c.moduleCompleted + 1, c.moduleLessons),
            queue: c.queue.slice(1),
          }
        }),
      }
    case 'submitAssignment':
      return {
        ...state,
        assignments: state.assignments.map((a) =>
          a.id === action.id ? { ...a, status: 'submitted', submittedOn: action.date, late: a.status === 'overdue' } : a,
        ),
      }
    case 'readNotification':
      return {
        ...state,
        notifications: state.notifications.map((n) => (n.id === action.id ? { ...n, read: true } : n)),
      }
    case 'readAllNotifications':
      return { ...state, notifications: state.notifications.map((n) => ({ ...n, read: true })) }
    case 'openModal':
      return { ...state, modal: { type: action.modalType, id: action.id } }
    case 'closeModal':
      return { ...state, modal: null }
    case 'pushToast':
      return { ...state, toasts: [...state.toasts, action.toast] }
    case 'dismissToast':
      return { ...state, toasts: state.toasts.filter((t) => t.id !== action.id) }
    default:
      return state
  }
}

let toastId = 0

export function DashboardProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState)
  const [prefs, setPrefsState] = useReducer((prev, next) => {
    const merged = { ...prev, ...next }
    savePrefs(merged)
    return merged
  }, undefined, loadPrefs)

  const toast = useCallback((message, tone = 'info') => {
    const id = ++toastId
    dispatch({ type: 'pushToast', toast: { id, message, tone } })
    setTimeout(() => dispatch({ type: 'dismissToast', id }), 4200)
  }, [])

  const actions = useMemo(
    () => ({
      completeLesson: (courseId) => dispatch({ type: 'completeLesson', courseId }),
      submitAssignment: (id) => dispatch({ type: 'submitAssignment', id, date: new Date().toISOString().slice(0, 10) }),
      readNotification: (id) => dispatch({ type: 'readNotification', id }),
      readAllNotifications: () => dispatch({ type: 'readAllNotifications' }),
      openModal: (modalType, id) => dispatch({ type: 'openModal', modalType, id }),
      closeModal: () => dispatch({ type: 'closeModal' }),
      dismissToast: (id) => dispatch({ type: 'dismissToast', id }),
      setPrefs: setPrefsState,
      toast,
    }),
    [toast],
  )

  const value = useMemo(() => ({ ...state, prefs, actions }), [state, prefs, actions])

  return <DashboardContext.Provider value={value}>{children}</DashboardContext.Provider>
}

// eslint-disable-next-line react/only-export-components
export function useDashboard() {
  const ctx = useContext(DashboardContext)
  if (!ctx) throw new Error('useDashboard must be used inside DashboardProvider')
  return ctx
}
