import React from 'react';
import type { TimePeriod } from '../pages/Dashboard';

type Point = { date: string; totalPlaytime: number };

type Props = {
  data: Point[];
  period: TimePeriod;
};

export const PlaytimeTrendsChart: React.FC<Props> = ({ data, period }) => {
  const width = 600;
  const height = 180;
  const padding = 20;
  const max = Math.max(1, ...data.map((d) => d.totalPlaytime));

  const path = data.map((d, i) => {
    const x = padding + (i / Math.max(1, data.length - 1)) * (width - padding * 2);
    const y = height - padding - (d.totalPlaytime / max) * (height - padding * 2);
    return `${i === 0 ? 'M' : 'L'} ${x},${y}`;
  }).join(' ');

  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, background: '#fff' }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>Playtime Trends - {period}</div>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-label="playtime-trends-chart">
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#ddd" />
        <path d={path} fill="none" stroke="#4caf50" strokeWidth={2} />
        {data.map((d, i) => {
          const x = padding + (i / Math.max(1, data.length - 1)) * (width - padding * 2);
          const y = height - padding - (d.totalPlaytime / max) * (height - padding * 2);
          return (
            <text key={i} x={x} y={height - 4} fontSize={9} textAnchor="middle" fill="#666">
              {d.date}
            </text>
          );
        })}
      </svg>
    </div>
  );
};
