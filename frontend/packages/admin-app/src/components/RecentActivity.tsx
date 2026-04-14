import React from 'react';

type Activity = {
  id: string;
  user: string;
  type: string;
  timestamp: string;
  details?: string;
};

type Props = {
  activities: Activity[];
};

export const RecentActivity: React.FC<Props> = ({ activities }) => {
  const recent = [...activities].slice(0, 10);
  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, background: '#fff' }}>
      <div style={{ fontWeight: 600, marginBottom: 6 }}>Recent Activity</div>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        {recent.map((a) => (
          <li key={a.id} style={{ padding: '6px 0', borderBottom: '1px solid #f0f0f0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>
                {a.user} • {a.type}
              </span>
              <span style={{ color: '#888', fontSize: 12 }}>{new Date(a.timestamp).toLocaleString()}</span>
            </div>
            {a.details && <div style={{ fontSize: 12, color: '#555' }}>{a.details}</div>}
          </li>
        ))}
      </ul>
    </div>
  );
};
