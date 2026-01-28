import { useParams, useNavigate, Link } from 'react-router-dom'
import { useTask } from '../hooks/useTask'
import { TaskDetail } from '../components/tasks/TaskDetail'
import { LoadingSpinner } from '../components/common/LoadingSpinner'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { Button } from '../components/common/Button'

export function TaskDetailPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { task, activity, loading, error, editTask, removeTask } = useTask(id!)

  const handleUpdateTitle = async (title: string) => {
    await editTask({ title })
  }

  const handleToggleComplete = async (completed: boolean) => {
    await editTask({ completed })
  }

  const handleDelete = async () => {
    await removeTask()
    navigate('/')
  }

  if (loading) {
    return (
      <div className="page">
        <LoadingSpinner />
      </div>
    )
  }

  if (error || !task) {
    return (
      <div className="page">
        <ErrorMessage message={error || 'Task not found'} />
        <Link to="/">
          <Button variant="secondary">Back to Tasks</Button>
        </Link>
      </div>
    )
  }

  return (
    <div className="page task-detail-page">
      <Link to="/" className="back-link">
        &larr; Back to Tasks
      </Link>
      <TaskDetail
        task={task}
        activity={activity}
        onUpdateTitle={handleUpdateTitle}
        onToggleComplete={handleToggleComplete}
        onDelete={handleDelete}
      />
    </div>
  )
}
