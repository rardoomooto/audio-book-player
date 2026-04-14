import React from 'react';
import type { TimePeriod } from '../pages/Dashboard';

type Point = { date: string; activeUsers: number };

type Props = {
  data: Point[];
  period: TimePeriod;
};

export const UserActivityChart: React.FC<Props> = ({ data, period }) => {
  const width = 600;
  const height = 180;
  const padding = 20;
  const max = Math.max(1, ...data.map((d) => d.activeUsers));
  const barWidth = data.length ? (width - padding * 2) / data.length - 6 : 10;

  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, background: '#fff' }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>User Activity - {period}</div>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-label="user-activity-chart">
        {/* axes */}
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#ddd" />
        <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#ddd" />
        {data.map((d, i) => {
          const h = (d.activeUsers / max) * (height - padding * 2);
          const x = padding + i * (barWidth + 6);
          const y = height - padding - h;
          return (
            <rect key={i} x={x} y={y} width={barWidth} height={h} fill="#42a5f5" rx={4} />
          );
        })}
        {/* x labels */}
        {data.map((d, i) => {
          const x = padding + i * (barWidth + 6) + barWidth / 2;
          return (
            <text key={`lab-${i}`} x={x} y={height - 4} fontSize={10} textAnchor="middle" fill="#666">
              {d.date}
            </text>
          );
        })}
      </svg>
    </div>
  );
};
