import type { TaskStats as TaskStatsType } from '../../types/task'

interface TaskStatsProps {
  stats: TaskStatsType
}

export function TaskStats({ stats }: TaskStatsProps) {
  return (
    <div className="task-stats">
      <div className="stat">
        <span className="stat-value">{stats.total}</span>
        <span className="stat-label">Total</span>
      </div>
      <div className="stat">
        <span className="stat-value">{stats.completed}</span>
        <span className="stat-label">Completed</span>
      </div>
      <div className="stat">
        <span className="stat-value">{stats.pending}</span>
        <span className="stat-label">Pending</span>
      </div>
    </div>
  )
}
