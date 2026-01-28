import { useState, type FormEvent } from 'react'
import { Button } from '../common/Button'
import { Input } from '../common/Input'

interface TaskFormProps {
  onSubmit: (title: string) => Promise<void>
}

export function TaskForm({ onSubmit }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return

    setLoading(true)
    try {
      await onSubmit(title.trim())
      setTitle('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <Input
        placeholder="Add a new task..."
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <Button type="submit" disabled={loading || !title.trim()}>
        {loading ? 'Adding...' : 'Add Task'}
      </Button>
    </form>
  )
}
