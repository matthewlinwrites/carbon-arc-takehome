export interface Task {
  id: string
  title: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface TaskStats {
  total: number
  completed: number
  pending: number
}

export interface ActivityLog {
  id: string
  task_id: string
  action: string
  timestamp: string
  old_value: string | null
  new_value: string | null
}

export interface TaskCreate {
  title: string
}

export interface TaskUpdate {
  title?: string
  completed?: boolean
}
