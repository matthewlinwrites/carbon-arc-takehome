import { Link, useNavigate } from 'react-router-dom'
import { Button } from '../common/Button'
import type { Task } from '../../types/task'

interface TaskListItemProps {
  task: Task
  onToggleComplete: (taskId: string, completed: boolean) => void
  onDelete: (taskId: string) => void
}

export function TaskListItem({ task, onToggleComplete, onDelete }: TaskListItemProps) {
  const navigate = useNavigate()

  return (
    <div className={`task-list-item ${task.completed ? 'completed' : ''}`}>
      <input
        type="checkbox"
        checked={task.completed}
        onChange={() => onToggleComplete(task.id, !task.completed)}
        className="task-checkbox"
      />
      <Link to={`/tasks/${task.id}`} className="task-title">
        {task.title}
      </Link>
      <div className="task-actions">
        <Button variant="secondary" onClick={() => navigate(`/tasks/${task.id}`)}>
          Edit
        </Button>
        <Button variant="danger" onClick={() => onDelete(task.id)}>
          Delete
        </Button>
      </div>
    </div>
  )
}
