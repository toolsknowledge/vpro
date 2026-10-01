import { useState } from 'react'
import { BookOpen, Cake, Loader2, User } from 'lucide-react'

const EMPTY = { name: '', age: '', course: '' }

export default function StudentForm({ initial, onSubmit, onCancel, submitLabel }) {
  const [values, setValues] = useState(initial ? { ...initial, age: String(initial.age) } : EMPTY)
  const [errors, setErrors] = useState({})
  const [saving, setSaving] = useState(false)

  const set = (field) => (e) => {
    setValues((v) => ({ ...v, [field]: e.target.value }))
    setErrors((er) => ({ ...er, [field]: undefined }))
  }

  const validate = () => {
    const er = {}
    if (!values.name.trim()) er.name = 'Name is required'
    const age = Number(values.age)
    if (values.age === '') er.age = 'Age is required'
    else if (!Number.isInteger(age) || age < 1 || age > 120) er.age = 'Enter a whole number between 1 and 120'
    if (!values.course.trim()) er.course = 'Course is required'
    setErrors(er)
    return Object.keys(er).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setSaving(true)
    try {
      await onSubmit({ name: values.name.trim(), age: Number(values.age), course: values.course.trim() })
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="modal-body form-grid">
        <Field label="Full name" icon={User} error={errors.name} className="span-2">
          <input value={values.name} onChange={set('name')} placeholder="e.g. Ananya Sharma" autoFocus />
        </Field>
        <Field label="Age" icon={Cake} error={errors.age}>
          <input type="number" min="1" max="120" value={values.age} onChange={set('age')} placeholder="21" />
        </Field>
        <Field label="Course" icon={BookOpen} error={errors.course}>
          <input value={values.course} onChange={set('course')} placeholder="e.g. Python Full Stack" list="course-suggestions" />
          <datalist id="course-suggestions">
            {['Python Full Stack', 'Java Full Stack', 'Data Science', 'AI & ML', 'DevOps', 'React JS'].map((c) => (
              <option key={c} value={c} />
            ))}
          </datalist>
        </Field>
      </div>
      <div className="modal-foot">
        <button type="button" className="btn btn-ghost" onClick={onCancel} disabled={saving}>
          Cancel
        </button>
        <button type="submit" className="btn btn-primary" disabled={saving}>
          {saving && <Loader2 size={16} className="spin" />}
          {submitLabel}
        </button>
      </div>
    </form>
  )
}

export function Field({ label, icon: Icon, error, children, className = '', trailing }) {
  return (
    <label className={`field ${error ? 'has-error' : ''} ${className}`}>
      <span className="field-label">{label}</span>
      <span className="input-wrap">
        {Icon && <Icon size={18} className="input-icon" />}
        {children}
        {trailing}
      </span>
      {error && <span className="field-error">{error}</span>}
    </label>
  )
}
