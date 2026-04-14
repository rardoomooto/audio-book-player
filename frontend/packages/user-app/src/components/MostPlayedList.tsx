import React from "react";
import { useNavigate } from "react-router-dom";

type Content = { id: string; title: string; playCount: number; totalTimeMinutes: number };
interface Props { data?: Content[]; }

export const MostPlayedList: React.FC<Props> = ({ data = [] }) => {
  const nav = useNavigate();
  const top = data.slice(0, 10);
  return (
    <div className="most-played">
      <h3>Most Played Content</h3>
      <ul>
        {top.length === 0 && <li>No data</li>}
        {top.map((c) => (
          <li key={c.id} className="mp-item" onClick={() => nav(`/content/${c.id}`)}>
            <span className="mp-title">{c.title}</span>
            <span className="mp-meta">{c.playCount} plays • {formatTime(c.totalTimeMinutes)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

function formatTime(mins: number) {
  const h = Math.floor(mins / 60);
  const m = Math.floor(mins % 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}
