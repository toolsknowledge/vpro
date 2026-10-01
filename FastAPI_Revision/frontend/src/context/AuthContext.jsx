import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { authApi, setUnauthorizedHandler, tokenStore } from '../api/client'

const AuthContext = createContext(null)

// Reads the payload of a JWT without verifying it (verification happens on the server).
function decodeToken(token) {
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')
    return JSON.parse(atob(payload))
  } catch {
    return null
  }
}

function sessionFromToken(token) {
  const payload = token && decodeToken(token)
  if (!payload?.sub || !payload?.exp) return null
  if (payload.exp * 1000 <= Date.now()) return null
  return { token, username: payload.sub, expiresAt: payload.exp * 1000 }
}

export function AuthProvider({ children }) {
  const [session, setSession] = useState(() => {
    const restored = sessionFromToken(tokenStore.get())
    if (!restored) tokenStore.clear()
    return restored
  })
  const [expiredNotice, setExpiredNotice] = useState(false)

  const logout = useCallback((reason) => {
    tokenStore.clear()
    setSession(null)
    setExpiredNotice(reason === 'expired')
  }, [])

  const login = useCallback(async (username, password) => {
    const data = await authApi.login(username, password)
    tokenStore.set(data.access_token)
    setSession(sessionFromToken(data.access_token))
    setExpiredNotice(false)
    return data
  }, [])

  const register = useCallback((username, password) => authApi.register(username, password), [])

  useEffect(() => {
    setUnauthorizedHandler(() => logout('expired'))
  }, [logout])

  // Log out automatically the moment the token expires.
  useEffect(() => {
    if (!session) return
    const ms = session.expiresAt - Date.now()
    const timer = setTimeout(() => logout('expired'), Math.max(ms, 0))
    return () => clearTimeout(timer)
  }, [session, logout])

  const value = useMemo(
    () => ({
      session,
      user: session?.username ?? null,
      isAuthenticated: !!session,
      expiredNotice,
      clearExpiredNotice: () => setExpiredNotice(false),
      login,
      register,
      logout,
    }),
    [session, expiredNotice, login, register, logout],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = () => useContext(AuthContext)
