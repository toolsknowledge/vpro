import { useEffect, useRef } from 'react'
import { X } from 'lucide-react'

// Native <dialog> gives us focus trapping, Escape to close and an inert background for free.
export default function Modal({ title, subtitle, onClose, children, footer, size = 'md' }) {
  const ref = useRef(null)

  useEffect(() => {
    const dialog = ref.current
    const previouslyFocused = document.activeElement
    dialog.showModal()
    return () => {
      dialog.close()
      previouslyFocused?.focus?.()
    }
  }, [])

  const width = size === 'lg' ? 'max-w-2xl' : 'max-w-lg'

  return (
    <dialog
      ref={ref}
      aria-labelledby="modal-title"
      onCancel={(e) => {
        e.preventDefault()
        onClose()
      }}
      onClick={(e) => {
        if (e.target === ref.current) onClose()
      }}
      className={`m-auto max-h-[calc(100dvh-2rem)] w-[calc(100%-2rem)] ${width} overflow-hidden rounded-2xl bg-white p-0 text-ink shadow-pop`}
    >
      <div className="flex max-h-[calc(100dvh-2rem)] flex-col">
        <header className="flex items-start justify-between gap-4 border-b border-line px-6 py-4">
          <div className="min-w-0">
            <h2 id="modal-title" className="text-lg font-semibold">
              {title}
            </h2>
            {subtitle && <p className="mt-0.5 text-sm text-ink-3">{subtitle}</p>}
          </div>
          <button
            type="button"
            onClick={onClose}
            className="-mr-2 rounded-lg p-2 text-ink-3 hover:bg-navy-50 hover:text-ink"
            aria-label="Close"
          >
            <X className="size-5" aria-hidden="true" />
          </button>
        </header>
        <div className="overflow-y-auto px-6 py-5">{children}</div>
        {footer && <footer className="flex flex-wrap justify-end gap-2 border-t border-line bg-canvas/60 px-6 py-3">{footer}</footer>}
      </div>
    </dialog>
  )
}
