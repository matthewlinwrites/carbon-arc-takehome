import { TaskListItem } from './TaskListItem'
import type { Task } from '../../types/task'

interface TaskListProps {
  tasks: Task[]
  onToggleComplete: (taskId: string, completed: boolean) => void
  onDelete: (taskId: string) => void
}

export function TaskList({ tasks, onToggleComplete, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return <div className="empty-state">No tasks yet. Add one above!</div>
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskListItem
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
