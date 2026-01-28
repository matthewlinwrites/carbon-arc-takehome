import { useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTasks } from '../hooks/useTasks'
import { useTaskStats } from '../hooks/useTaskStats'
import { useAuth } from '../hooks/useAuth'
import { TaskStats } from '../components/tasks/TaskStats'
import { TaskForm } from '../components/tasks/TaskForm'
import { TaskList } from '../components/tasks/TaskList'
import { Pagination } from '../components/common/Pagination'
import { LoadingSpinner } from '../components/common/LoadingSpinner'
import { ErrorMessage } from '../components/common/ErrorMessage'
import { Button } from '../components/common/Button'

export function TaskListPage() {
  const navigate = useNavigate()
  const { logout } = useAuth()
  const {
    tasks,
    loading,
    error,
    currentPage,
    totalPages,
    goToPage,
    addTask,
    removeTask,
    editTask,
    refetch,
  } = useTasks()
  const { stats, refetch: refetchStats } = useTaskStats()

  const handleAddTask = useCallback(async (title: string) => {
    await addTask({ title })
    refetchStats()
  }, [addTask, refetchStats])

  const handleToggleComplete = useCallback(async (taskId: string, completed: boolean) => {
    await editTask(taskId, { completed })
    refetchStats()
  }, [editTask, refetchStats])

  const handleDelete = useCallback(async (taskId: string) => {
    await removeTask(taskId)
    refetchStats()
  }, [removeTask, refetchStats])

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (loading) {
    return (
      <div className="page">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="page">
        <ErrorMessage message={error} />
        <Button onClick={refetch}>Retry</Button>
      </div>
    )
  }

  return (
    <div className="page task-list-page">
      <header className="page-header">
        <h1>Task Management</h1>
        <Button variant="secondary" onClick={handleLogout}>
          Logout
        </Button>
      </header>

      {stats && <TaskStats stats={stats} />}

      <TaskForm onSubmit={handleAddTask} />

      <TaskList
        tasks={tasks}
        onToggleComplete={handleToggleComplete}
        onDelete={handleDelete}
      />

      <Pagination
        currentPage={currentPage}
        totalPages={totalPages}
        onPageChange={goToPage}
      />
    </div>
  )
}
