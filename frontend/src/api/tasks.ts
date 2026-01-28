import { apiClient } from './client'
import type { Task, TaskStats, ActivityLog, TaskCreate, TaskUpdate } from '../types/task'

export async function getTasks(): Promise<Task[]> {
  const response = await apiClient.get<Task[]>('/tasks')
  return response.data
}

export async function getTask(taskId: string): Promise<Task> {
  const response = await apiClient.get<Task>(`/tasks/${taskId}`)
  return response.data
}

export async function createTask(data: TaskCreate): Promise<Task> {
  const response = await apiClient.post<Task>('/tasks', data)
  return response.data
}

export async function updateTask(taskId: string, data: TaskUpdate): Promise<Task> {
  const response = await apiClient.patch<Task>(`/tasks/${taskId}`, data)
  return response.data
}

export async function completeTask(taskId: string): Promise<Task> {
  const response = await apiClient.put<Task>(`/tasks/${taskId}/complete`)
  return response.data
}

export async function deleteTask(taskId: string): Promise<void> {
  await apiClient.delete(`/tasks/${taskId}`)
}

export async function getTaskStats(): Promise<TaskStats> {
  const response = await apiClient.get<TaskStats>('/tasks/stats')
  return response.data
}

export async function getTaskActivity(taskId: string): Promise<ActivityLog[]> {
  const response = await apiClient.get<ActivityLog[]>(`/tasks/${taskId}/activity`)
  return response.data
}
