import { createContext, useContext, useState, useCallback, useEffect, type ReactNode } from 'react'
import { login as loginApi } from '../api/auth'
import type { LoginRequest } from '../types/auth'

interface AuthContextType {
  token: string | null
  isAuthenticated: boolean
  login: (credentials: LoginRequest) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('token')
  })

  const isAuthenticated = token !== null

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token])

  const login = useCallback(async (credentials: LoginRequest) => {
    const response = await loginApi(credentials)
    setToken(response.token)
  }, [])

  const logout = useCallback(() => {
    setToken(null)
  }, [])

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
