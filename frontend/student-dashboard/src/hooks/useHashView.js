import { useCallback, useEffect, useState } from 'react'
import { allNavItems } from '../data/navigation.js'

const validIds = new Set(allNavItems.map((item) => item.id))

function readHash() {
  const id = window.location.hash.replace('#/', '')
  return validIds.has(id) ? id : 'dashboard'
}

// Keeps the active view in the URL hash so the back button and reloads work without a router.
export function useHashView() {
  const [view, setView] = useState(readHash)

  useEffect(() => {
    const onHashChange = () => setView(readHash())
    window.addEventListener('hashchange', onHashChange)
    return () => window.removeEventListener('hashchange', onHashChange)
  }, [])

  const navigate = useCallback((id) => {
    if (!validIds.has(id)) return
    if (readHash() !== id) window.location.hash = `/${id}`
    setView(id)
    window.scrollTo({ top: 0 })
  }, [])

  return [view, navigate]
}
