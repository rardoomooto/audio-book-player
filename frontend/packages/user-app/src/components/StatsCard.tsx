import React from "react";
import "../styles/stats.css";

export interface StatsCardProps {
  title: string;
  value?: string;
  subtitle?: string;
  children?: React.ReactNode;
}

export const StatsCard: React.FC<StatsCardProps> = ({ title, value, subtitle, children }) => {
  return (
    <div className="stats-card">
      <div className="stats-card__header">
        <span className="stats-card__title">{title}</span>
        {value && <span className="stats-card__value">{value}</span>}
      </div>
      {subtitle && <div className="stats-card__subtitle">{subtitle}</div>}
      {children}
    </div>
  );
};
