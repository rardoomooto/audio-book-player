import React from 'react';
import type { ContentSummary } from '../../../../shared/types/stats';

type Props = {
  topContents: ContentSummary[];
};

export const ContentPopularityChart: React.FC<Props> = ({ topContents }) => {
  const width = 600;
  const height = 180;
  const padding = 20;
  const max = Math.max(1, ...topContents.map((c) => c.playCount));
  const barW = topContents.length ? (width - padding * 2) / topContents.length - 6 : 10;

  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, background: '#fff' }}>
      <div style={{ marginBottom: 8, fontWeight: 600 }}>Content Popularity</div>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} aria-label="content-popularity-chart">
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#ddd" />
        {topContents.map((c, i) => {
          const h = (c.playCount / max) * (height - padding * 2);
          const x = padding + i * (barW + 6);
          const y = height - padding - h;
          return (
            <g key={c.contentId}>
              <rect x={x} y={y} width={barW} height={h} fill="#7e57c2" rx={4} />
              <text x={x + barW / 2} y={height - 4} fontSize={10} textAnchor="middle" fill="#666">
                {truncateTitle(c.title, 12)}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

function truncateTitle(title: string, max: number) {
  if (title.length <= max) return title;
  return title.substring(0, max - 1) + '…';
}
