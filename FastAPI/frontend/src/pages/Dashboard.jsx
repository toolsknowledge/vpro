import { useCallback, useEffect, useMemo, useState } from 'react'
import {
  ArrowUpDown, BookOpen, Cake, GraduationCap, Inbox, Loader2, Pencil, Plus, RefreshCw, Search, Trash2, UserPlus, Users, X, AlertCircle,
} from 'lucide-react'
import Header from '../components/Header'
import Modal from '../components/Modal'
import StudentForm from '../components/StudentForm'
import { studentsApi } from '../api/client'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../context/ToastContext'

const PALETTE = ['#f47a0e', '#3a3a3a', '#0ea5e9', '#10b981', '#8b5cf6', '#ef4444', '#eab308', '#ec4899']
const colorFor = (str) => PALETTE[[...str].reduce((a, c) => a + c.charCodeAt(0), 0) % PALETTE.length]
const initials = (name) => name.split(/\s+/).filter(Boolean).slice(0, 2).map((p) => p[0].toUpperCase()).join('')

const SORTS = {
  name: (a, b) => a.name.localeCompare(b.name),
  age: (a, b) => a.age - b.age,
  course: (a, b) => a.course.localeCompare(b.course),
}

export default function Dashboard() {
  const { user } = useAuth()
  const toast = useToast()

  const [students, setStudents] = useState([])
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [loadError, setLoadError] = useState('')
  const [query, setQuery] = useState('')
  const [course, setCourse] = useState('all')
  const [sort, setSort] = useState({ key: 'name', dir: 1 })
  const [modal, setModal] = useState(null) // { type: 'create' | 'edit' | 'delete', student? }
  const [deleting, setDeleting] = useState(false)

  const load = useCallback(async (silent = false) => {
    if (silent) setRefreshing(true)
    else setLoading(true)
    setLoadError('')
    try {
      setStudents(await studentsApi.list())
    } catch (err) {
      setLoadError(err.message)
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }, [])

  useEffect(() => {
    studentsApi
      .list()
      .then(setStudents)
      .catch((err) => setLoadError(err.message))
      .finally(() => setLoading(false))
  }, [])

  const courses = useMemo(() => [...new Set(students.map((s) => s.course))].sort(), [students])

  const stats = useMemo(() => {
    const total = students.length
    const avgAge = total ? (students.reduce((a, s) => a + s.age, 0) / total).toFixed(1) : '—'
    const counts = students.reduce((m, s) => ({ ...m, [s.course]: (m[s.course] || 0) + 1 }), {})
    const top = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]
    return { total, avgAge, courseCount: Object.keys(counts).length, top: top?.[0] ?? '—', counts }
  }, [students])

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase()
    return students
      .filter((s) => course === 'all' || s.course === course)
      .filter((s) => !q || s.name.toLowerCase().includes(q) || s.course.toLowerCase().includes(q) || String(s.age) === q)
      .sort((a, b) => SORTS[sort.key](a, b) * sort.dir)
  }, [students, query, course, sort])

  const toggleSort = (key) => setSort((s) => ({ key, dir: s.key === key ? -s.dir : 1 }))

  const closeModal = useCallback(() => setModal(null), [])

  const handleCreate = async (data) => {
    try {
      const res = await studentsApi.create(data)
      setStudents((list) => [...list, { ...data, id: res.id }])
      toast(res.message || 'Student added')
      setModal(null)
    } catch (err) {
      toast(err.message, 'error')
    }
  }

  const handleUpdate = async (data) => {
    const { id } = modal.student
    try {
      const res = await studentsApi.update(id, data)
      setStudents((list) => list.map((s) => (s.id === id ? { ...s, ...data } : s)))
      toast(res.message || 'Student updated')
      setModal(null)
    } catch (err) {
      toast(err.message, 'error')
    }
  }

  const handleDelete = async () => {
    const { id } = modal.student
    setDeleting(true)
    try {
      const res = await studentsApi.remove(id)
      setStudents((list) => list.filter((s) => s.id !== id))
      toast(res.message || 'Student deleted')
      setModal(null)
    } catch (err) {
      toast(err.message, 'error')
    } finally {
      setDeleting(false)
    }
  }

  const hasFilters = query || course !== 'all'

  return (
    <div className="app-shell">
      <Header />

      <main className="container dashboard">
        <section className="page-head">
          <div>
            <p className="eyebrow">Dashboard</p>
            <h1>
              Hello, <span className="accent">{user}</span> 👋
            </h1>
            <p className="muted">Here's an overview of every student enrolled at VPro Skills.</p>
          </div>
          <button className="btn btn-primary btn-lg" onClick={() => setModal({ type: 'create' })}>
            <Plus size={18} /> Add student
          </button>
        </section>

        <section className="stats">
          <StatCard icon={Users} label="Total students" value={loading ? '…' : stats.total} tone="orange" />
          <StatCard icon={BookOpen} label="Courses offered" value={loading ? '…' : stats.courseCount} tone="dark" />
          <StatCard icon={Cake} label="Average age" value={loading ? '…' : stats.avgAge} tone="blue" />
          <StatCard icon={GraduationCap} label="Most popular" value={loading ? '…' : stats.top} tone="green" small />
        </section>

        {courses.length > 0 && (
          <section className="course-chips" aria-label="Filter by course">
            <button className={`chip ${course === 'all' ? 'active' : ''}`} onClick={() => setCourse('all')}>
              All <span>{students.length}</span>
            </button>
            {courses.map((c) => (
              <button key={c} className={`chip ${course === c ? 'active' : ''}`} onClick={() => setCourse(c)}>
                {c} <span>{stats.counts[c]}</span>
              </button>
            ))}
          </section>
        )}

        <section className="panel">
          <div className="panel-toolbar">
            <div className="panel-title">
              <h2>Students</h2>
              <span className="count-badge">{visible.length}</span>
            </div>
            <div className="toolbar-actions">
              <div className="search">
                <Search size={18} />
                <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Search name, course or age…" />
                {query && (
                  <button className="icon-btn" onClick={() => setQuery('')} aria-label="Clear search">
                    <X size={16} />
                  </button>
                )}
              </div>
              <select className="select" value={course} onChange={(e) => setCourse(e.target.value)} aria-label="Course filter">
                <option value="all">All courses</option>
                {courses.map((c) => (
                  <option key={c}>{c}</option>
                ))}
              </select>
              <button className="btn btn-ghost btn-icon" onClick={() => load(true)} disabled={refreshing} title="Refresh" aria-label="Refresh">
                <RefreshCw size={18} className={refreshing ? 'spin' : ''} />
              </button>
            </div>
          </div>

          {loading ? (
            <div className="skeleton-list">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="skeleton-row">
                  <span className="sk sk-avatar" />
                  <span className="sk sk-line" />
                  <span className="sk sk-short" />
                </div>
              ))}
            </div>
          ) : loadError ? (
            <EmptyState icon={AlertCircle} title="Couldn't load students" text={loadError} tone="error">
              <button className="btn btn-primary" onClick={() => load()}>
                <RefreshCw size={16} /> Try again
              </button>
            </EmptyState>
          ) : visible.length === 0 ? (
            hasFilters ? (
              <EmptyState icon={Search} title="No matches" text="No students match your search or filter.">
                <button className="btn btn-ghost" onClick={() => { setQuery(''); setCourse('all') }}>
                  Clear filters
                </button>
              </EmptyState>
            ) : (
              <EmptyState icon={Inbox} title="No students yet" text="Add your first student to get started.">
                <button className="btn btn-primary" onClick={() => setModal({ type: 'create' })}>
                  <UserPlus size={16} /> Add student
                </button>
              </EmptyState>
            )
          ) : (
            <>
              <div className="table-wrap">
                <table className="table">
                  <thead>
                    <tr>
                      <th><SortBtn sort={sort} onSort={toggleSort} k="name">Student</SortBtn></th>
                      <th><SortBtn sort={sort} onSort={toggleSort} k="age">Age</SortBtn></th>
                      <th><SortBtn sort={sort} onSort={toggleSort} k="course">Course</SortBtn></th>
                      <th>Record ID</th>
                      <th className="ta-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {visible.map((s) => (
                      <tr key={s.id}>
                        <td>
                          <div className="s-cell">
                            <Avatar name={s.name} />
                            <span className="s-name">{s.name}</span>
                          </div>
                        </td>
                        <td>{s.age} yrs</td>
                        <td><span className="course-tag">{s.course}</span></td>
                        <td><code className="id-code" title={s.id}>{s.id.slice(-8)}</code></td>
                        <td className="ta-right"><RowActions s={s} onEdit={() => setModal({ type: 'edit', student: s })} onDelete={() => setModal({ type: 'delete', student: s })} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <ul className="card-list">
                {visible.map((s) => (
                  <li key={s.id} className="s-card">
                    <Avatar name={s.name} />
                    <div className="s-card-body">
                      <strong>{s.name}</strong>
                      <div className="s-card-meta">
                        <span className="course-tag">{s.course}</span>
                        <span className="muted">{s.age} yrs</span>
                      </div>
                    </div>
                    <RowActions s={s} onEdit={() => setModal({ type: 'edit', student: s })} onDelete={() => setModal({ type: 'delete', student: s })} />
                  </li>
                ))}
              </ul>
            </>
          )}
        </section>
      </main>

      <button className="fab" onClick={() => setModal({ type: 'create' })} aria-label="Add student">
        <Plus size={24} />
      </button>

      {modal?.type === 'create' && (
        <Modal title="Add student" subtitle="Create a new student record" icon={UserPlus} onClose={closeModal}>
          <StudentForm onSubmit={handleCreate} onCancel={closeModal} submitLabel="Add student" />
        </Modal>
      )}
      {modal?.type === 'edit' && (
        <Modal title="Edit student" subtitle={`Updating ${modal.student.name}`} icon={Pencil} onClose={closeModal}>
          <StudentForm initial={modal.student} onSubmit={handleUpdate} onCancel={closeModal} submitLabel="Save changes" />
        </Modal>
      )}
      {modal?.type === 'delete' && (
        <Modal title="Delete student?" icon={Trash2} onClose={closeModal} size="sm">
          <div className="modal-body">
            <p className="confirm-text">
              <strong>{modal.student.name}</strong> will be permanently removed. This action cannot be undone.
            </p>
          </div>
          <div className="modal-foot">
            <button className="btn btn-ghost" onClick={closeModal} disabled={deleting}>Cancel</button>
            <button className="btn btn-danger" onClick={handleDelete} disabled={deleting}>
              {deleting ? <Loader2 size={16} className="spin" /> : <Trash2 size={16} />} Delete
            </button>
          </div>
        </Modal>
      )}
    </div>
  )
}

function SortBtn({ k, sort, onSort, children }) {
  return (
    <button className={`th-sort ${sort.key === k ? 'active' : ''}`} onClick={() => onSort(k)}>
      {children}
      <ArrowUpDown size={14} className={sort.key === k && sort.dir < 0 ? 'flip' : ''} />
    </button>
  )
}

function RowActions({ s, onEdit, onDelete }) {
  return (
    <div className="row-actions">
      <button className="icon-btn edit" onClick={onEdit} aria-label={`Edit ${s.name}`} title="Edit">
        <Pencil size={16} />
      </button>
      <button className="icon-btn delete" onClick={onDelete} aria-label={`Delete ${s.name}`} title="Delete">
        <Trash2 size={16} />
      </button>
    </div>
  )
}

function Avatar({ name }) {
  return (
    <span className="s-avatar" style={{ '--c': colorFor(name) }}>
      {initials(name)}
    </span>
  )
}

function StatCard({ icon: Icon, label, value, tone, small }) {
  return (
    <div className={`stat stat-${tone}`}>
      <span className="stat-icon"><Icon size={22} /></span>
      <div className="stat-body">
        <span className="stat-label">{label}</span>
        <span className={`stat-value ${small ? 'small' : ''}`} title={String(value)}>{value}</span>
      </div>
    </div>
  )
}

function EmptyState({ icon: Icon, title, text, children, tone }) {
  return (
    <div className={`empty ${tone === 'error' ? 'empty-error' : ''}`}>
      <span className="empty-icon"><Icon size={28} /></span>
      <h3>{title}</h3>
      <p>{text}</p>
      {children}
    </div>
  )
}
