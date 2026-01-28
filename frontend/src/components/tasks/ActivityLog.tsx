import type { ActivityLog as ActivityLogType } from '../../types/task'

interface ActivityLogProps {
  activity: ActivityLogType[]
}

function formatTimestamp(timestamp: string): string {
  return new Date(timestamp).toLocaleString()
}

function formatAction(log: ActivityLogType): string {
  switch (log.action) {
    case 'created':
      return 'Task created'
    case 'completed':
    case 'status_changed':
      if (log.old_value && log.new_value) {
        return `Status changed from "${log.old_value}" to "${log.new_value}"`
      }
      return 'Status changed'
    case 'updated':
      if (log.old_value && log.new_value) {
        return `Title changed from "${log.old_value}" to "${log.new_value}"`
      }
      return 'Task updated'
    case 'deleted':
      return 'Task deleted'
    default:
      return log.action
  }
}

export function ActivityLog({ activity }: ActivityLogProps) {
  if (activity.length === 0) {
    return <div className="empty-state">No activity yet.</div>
  }

  return (
    <div className="activity-log">
      <h3>Activity Log</h3>
      <ul>
        {activity.map((log) => (
          <li key={log.id} className="activity-item">
            <span className="activity-timestamp">{formatTimestamp(log.timestamp)}</span>
            <span className="activity-action">{formatAction(log)}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
