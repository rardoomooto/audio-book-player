import React from 'react';
import type { ContentSummary } from '../../../../shared/types/stats';

type Props = {
  contents: ContentSummary[];
};

export const TopContentList: React.FC<Props> = ({ contents }) => {
  const top = [...contents].sort((a, b) => b.playCount - a.playCount).slice(0, 10);
  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, background: '#fff' }}>
      <div style={{ fontWeight: 600, marginBottom: 6 }}>Top 10 Content</div>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        {top.map((c) => (
          <li key={c.contentId} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0' }}>
            <span title={c.title}>{truncate(c.title, 28)}</span>
            <span>{c.playCount} plays • {formatTime(c.totalTime)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

function truncate(s: string, max: number) {
  return s.length > max ? s.slice(0, max - 1) + '…' : s;
}
function formatTime(s: number) {
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = Math.floor(s % 60);
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m ${sec}s`;
  return `${sec}s`;
}
