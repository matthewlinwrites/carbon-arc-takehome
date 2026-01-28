import { useState, useEffect, useCallback } from 'react'
import { getTask, getTaskActivity, updateTask, deleteTask } from '../api/tasks'
import type { Task, ActivityLog, TaskUpdate } from '../types/task'

export function useTask(taskId: string) {
  const [task, setTask] = useState<Task | null>(null)
  const [activity, setActivity] = useState<ActivityLog[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchTask = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      const [taskData, activityData] = await Promise.all([
        getTask(taskId),
        getTaskActivity(taskId),
      ])
      setTask(taskData)
      setActivity(activityData)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch task')
    } finally {
      setLoading(false)
    }
  }, [taskId])

  useEffect(() => {
    fetchTask()
  }, [fetchTask])

  const editTask = useCallback(async (data: TaskUpdate) => {
    const updated = await updateTask(taskId, data)
    setTask(updated)
    const activityData = await getTaskActivity(taskId)
    setActivity(activityData)
    return updated
  }, [taskId])

  const removeTask = useCallback(async () => {
    await deleteTask(taskId)
  }, [taskId])

  return {
    task,
    activity,
    loading,
    error,
    editTask,
    removeTask,
    refetch: fetchTask,
  }
}
