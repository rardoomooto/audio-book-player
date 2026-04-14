import React from 'react';

type Slice = { label: string; value: number; color?: string };

type Props = {
  distribution?: Slice[];
};

export const UserDistributionChart: React.FC<Props> = ({ distribution = [] }) => {
  const total = distribution.reduce((a, s) => a + s.value, 0) || 1;
  let acc = 0;
  const cx = 150, cy = 90, r = 60;
  const arcs = distribution.map((s, idx) => {
    const frac = s.value / total;
    const start = acc;
    const end = acc + frac * 2 * Math.PI;
    acc = end;
    const large = end - start > Math.PI ? 1 : 0;
    // compute end points on circle
    const x1 = cx + r * Math.cos(start);
    const y1 = cy + r * Math.sin(start);
    const x2 = cx + r * Math.cos(end);
    const y2 = cy + r * Math.sin(end);
    const path = `M ${cx} ${cy} L ${x1} ${y1} A ${r} ${r} 0 ${large} 1 ${x2} ${y2} Z`;
    return { path, color: s.color ?? '#'+Math.floor(Math.random()*0xffffff).toString(16), label: s.label, value: s.value };
  });

  return (
    <div style={{ border: '1px solid #e0e0e0', borderRadius: 8, padding: 12, background: '#fff' }}>
      <div style={{ fontWeight: 600, marginBottom: 8 }}>User Distribution</div>
      <svg width={320} height={180} viewBox="0 0 320 180" aria-label="user-distribution-chart">
        <g transform="translate(0,0)">
          {arcs.map((a, i) => (
            <path key={i} d={a.path} fill={a.color} opacity={0.85} />
          ))}
        </g>
        <circle cx={cx} cy={cy} r={r - 20} fill="#fff" stroke="#eee" />
        {distribution.map((s, i) => (
          <g key={`legend-${i}`} transform={`translate(210, ${20 + i * 14})`}>
            <rect width={10} height={10} fill={s.color ?? '#ccc'} />
            <text x={14} y={10} fontSize={10} fill="#333">{s.label} ({s.value})</text>
          </g>
        ))}
      </svg>
    </div>
  );
};
