import React from 'react';

type Props = {
  title: string;
  value: string | number;
  loading?: boolean;
  subtitle?: string;
};

export const DashboardCard: React.FC<Props> = ({ title, value, loading, subtitle }) => {
  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 16, background: '#fff' }}>
      <div style={{ fontSize: 14, color: '#666', marginBottom: 6 }}>{title}</div>
      <div style={{ fontSize: 22, fontWeight: 700 }}>{loading ? 'Loading...' : value}</div>
      {subtitle && <div style={{ fontSize: 12, color: '#888' }}>{subtitle}</div>}
    </div>
  );
};
