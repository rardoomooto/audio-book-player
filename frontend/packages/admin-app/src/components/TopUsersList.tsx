import React from 'react';
import type { UserSummary } from '../../../../shared/types/stats';

type Props = {
  users: UserSummary[];
};

export const TopUsersList: React.FC<Props> = ({ users }) => {
  const top = [...users].sort((a, b) => b.playtime - a.playtime).slice(0, 10);
  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, background: '#fff' }}>
      <div style={{ fontWeight: 600, marginBottom: 6 }}>Top 10 Active Users</div>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        {top.map((u) => (
          <li key={u.userId} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0' }}>
            <span>{u.name}</span>
            <span>{formatTime(u.playtime)} • {u.sessions} sessions</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

function formatTime(seconds: number) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m ${s}s`;
  return `${s}s`;
}
