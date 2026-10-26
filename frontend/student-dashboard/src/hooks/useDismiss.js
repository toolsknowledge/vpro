import { useEffect } from 'react'

// Closes a popover on outside click or Escape.
export function useDismiss(ref, open, onClose) {
  useEffect(() => {
    if (!open) return
    const onPointer = (e) => {
      if (ref.current && !ref.current.contains(e.target)) onClose()
    }
    const onKey = (e) => {
      if (e.key === 'Escape') onClose()
    }
    document.addEventListener('mousedown', onPointer)
    document.addEventListener('keydown', onKey)
    return () => {
      document.removeEventListener('mousedown', onPointer)
      document.removeEventListener('keydown', onKey)
    }
  }, [ref, open, onClose])
}
