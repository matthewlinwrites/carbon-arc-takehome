import { useState, useEffect, useCallback, useMemo } from 'react'
import { getTasks, createTask, deleteTask, updateTask } from '../api/tasks'
import type { Task, TaskCreate, TaskUpdate } from '../types/task'

const PAGE_SIZE = 10

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [currentPage, setCurrentPage] = useState(1)

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getTasks()
      setTasks(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchTasks()
  }, [fetchTasks])

  const totalPages = useMemo(() => Math.ceil(tasks.length / PAGE_SIZE), [tasks.length])

  const paginatedTasks = useMemo(() => {
    const start = (currentPage - 1) * PAGE_SIZE
    const end = start + PAGE_SIZE
    return tasks.slice(start, end)
  }, [tasks, currentPage])

  const addTask = useCallback(async (data: TaskCreate) => {
    const newTask = await createTask(data)
    setTasks((prev) => [...prev, newTask])
    return newTask
  }, [])

  const removeTask = useCallback(async (taskId: string) => {
    await deleteTask(taskId)
    setTasks((prev) => prev.filter((t) => t.id !== taskId))
  }, [])

  const editTask = useCallback(async (taskId: string, data: TaskUpdate) => {
    const updatedTask = await updateTask(taskId, data)
    setTasks((prev) => prev.map((t) => (t.id === taskId ? updatedTask : t)))
    return updatedTask
  }, [])

  const goToPage = useCallback((page: number) => {
    setCurrentPage(page)
  }, [])

  return {
    tasks: paginatedTasks,
    allTasks: tasks,
    loading,
    error,
    currentPage,
    totalPages,
    goToPage,
    addTask,
    removeTask,
    editTask,
    refetch: fetchTasks,
  }
}
