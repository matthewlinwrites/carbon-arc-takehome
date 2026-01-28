import { useState, type FormEvent } from 'react'
import { Button } from '../common/Button'
import { Input } from '../common/Input'
import { ErrorMessage } from '../common/ErrorMessage'
import { useAuth } from '../../hooks/useAuth'

interface LoginFormProps {
  onSuccess: () => void
}

export function LoginForm({ onSuccess }: LoginFormProps) {
  const { login } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)

    try {
      await login({ username, password })
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="login-form">
      <h2>Login</h2>
      {error && <ErrorMessage message={error} />}
      <Input
        label="Email"
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        required
        autoFocus
      />
      <Input
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <Button type="submit" disabled={loading}>
        {loading ? 'Logging in...' : 'Login'}
      </Button>
    </form>
  )
}
