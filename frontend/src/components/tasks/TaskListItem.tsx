import { Link } from 'react-router-dom'
import { Button } from '../common/Button'
import type { Task } from '../../types/task'

interface TaskListItemProps {
  task: Task
  onToggleComplete: (taskId: string, completed: boolean) => void
  onDelete: (taskId: string) => void
}

export function TaskListItem({ task, onToggleComplete, onDelete }: TaskListItemProps) {
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
      <Button variant="danger" onClick={() => onDelete(task.id)}>
        Delete
      </Button>
    </div>
  )
}
