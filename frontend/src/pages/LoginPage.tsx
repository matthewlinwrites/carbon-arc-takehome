import { useNavigate } from 'react-router-dom'
import { LoginForm } from '../components/auth/LoginForm'
import { useAuth } from '../hooks/useAuth'
import { useEffect } from 'react'

export function LoginPage() {
  const navigate = useNavigate()
  const { isAuthenticated } = useAuth()

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/')
    }
  }, [isAuthenticated, navigate])

  const handleLoginSuccess = () => {
    navigate('/')
  }

  return (
    <div className="page login-page">
      <div className="login-container">
        <h1>Task Management</h1>
        <LoginForm onSuccess={handleLoginSuccess} />
      </div>
    </div>
  )
}
