import React from 'react'
import { login as apiLogin, getMe, refreshToken as refreshTokenApi, logout as apiLogout } from '../api-client/auth'
import { getAccessToken, getRefreshToken, setAccessToken, setRefreshToken, clearTokens } from '../api-client/tokenStore'
import { TokenResponse } from '../types/auth'

type User = any

type AuthContextValue = {
  user: User | null
  login: (credentials: { username: string; password: string }) => Promise<void>
  logout: () => Promise<void>
  refresh: () => Promise<void>
  isAuthenticated: boolean
}

export const AuthContext = React.createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = React.useState<User | null>(null)

  // Initialize from tokens if present
  React.useEffect(() => {
    const token = getAccessToken()
    if (token) {
      // Try to fetch user profile
      getMe()
        .then((data) => {
          setUser(data?.user || data)
        })
        .catch(() => {
          clearTokens()
          setUser(null)
        })
    }
  }, [])

  const login = async (credentials: { username: string; password: string }) => {
    const resp = await apiLogin(credentials)
    // Persist tokens in memory
    if (resp?.accessToken) {
      setAccessToken(resp.accessToken, resp.expiresIn)
    }
    if (resp?.refreshToken) {
      setRefreshToken(resp.refreshToken)
    }
    // Load user profile after login
    try {
      const me = await getMe()
      setUser(me?.user || me)
    } catch {
      setUser(null)
    }
  }

  const logout = async () => {
    try {
      await apiLogout()
    } catch {
      // ignore
    } finally {
      clearTokens()
      setUser(null)
    }
  }

  const refresh = async () => {
    const rt = getRefreshToken()
    if (!rt) {
      return
    }
    try {
      const resp: TokenResponse = await refreshTokenApi(rt)
      if (resp?.accessToken) {
        setAccessToken(resp.accessToken, resp.expiresIn)
      }
      if (resp?.refreshToken) {
        setRefreshToken(resp.refreshToken)
      }
      const me = await getMe()
      setUser(me?.user || me)
    } catch {
      // if refresh fails, logout
      await logout()
    }
  }

  const isAuthenticated = Boolean(user)

  const value = {
    user,
    login,
    logout,
    refresh,
    isAuthenticated,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = React.useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider')
  return ctx
}
