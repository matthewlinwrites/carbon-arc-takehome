import { useState } from 'react'
import { Button } from '../common/Button'
import { Input } from '../common/Input'
import { ActivityLog } from './ActivityLog'
import type { Task, ActivityLog as ActivityLogType } from '../../types/task'

interface TaskDetailProps {
  task: Task
  activity: ActivityLogType[]
  onUpdateTitle: (title: string) => Promise<void>
  onToggleComplete: (completed: boolean) => Promise<void>
  onDelete: () => Promise<void>
}

export function TaskDetail({
  task,
  activity,
  onUpdateTitle,
  onToggleComplete,
  onDelete,
}: TaskDetailProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [editTitle, setEditTitle] = useState(task.title)
  const [loading, setLoading] = useState(false)

  const handleSaveTitle = async () => {
    if (!editTitle.trim() || editTitle.trim() === task.title) {
      setIsEditing(false)
      setEditTitle(task.title)
      return
    }

    setLoading(true)
    try {
      await onUpdateTitle(editTitle.trim())
      setIsEditing(false)
    } finally {
      setLoading(false)
    }
  }

  const handleToggle = async () => {
    setLoading(true)
    try {
      await onToggleComplete(!task.completed)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      await onDelete()
    }
  }

  return (
    <div className="task-detail">
      <div className="task-detail-header">
        {isEditing ? (
          <div className="edit-title">
            <Input
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              autoFocus
            />
            <Button onClick={handleSaveTitle} disabled={loading}>
              Save
            </Button>
            <Button variant="secondary" onClick={() => {
              setIsEditing(false)
              setEditTitle(task.title)
            }}>
              Cancel
            </Button>
          </div>
        ) : (
          <div className="title-display">
            <h2 className={task.completed ? 'completed' : ''}>{task.title}</h2>
            <Button variant="secondary" onClick={() => setIsEditing(true)}>
              Edit
            </Button>
          </div>
        )}
      </div>

      <div className="task-detail-info">
        <p>
          <strong>Status:</strong>{' '}
          <span className={`status ${task.completed ? 'completed' : 'pending'}`}>
            {task.completed ? 'Completed' : 'Pending'}
          </span>
        </p>
        <p>
          <strong>Created:</strong> {new Date(task.created_at).toLocaleString()}
        </p>
        <p>
          <strong>Updated:</strong> {new Date(task.updated_at).toLocaleString()}
        </p>
      </div>

      <div className="task-detail-actions">
        <Button onClick={handleToggle} disabled={loading}>
          {task.completed ? 'Mark as Pending' : 'Mark as Complete'}
        </Button>
        <Button variant="danger" onClick={handleDelete}>
          Delete Task
        </Button>
      </div>

      <ActivityLog activity={activity} />
    </div>
  )
}
