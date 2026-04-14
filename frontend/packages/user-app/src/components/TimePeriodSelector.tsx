import React from "react";
type Period = "daily" | "weekly" | "monthly" | "yearly";
interface Props { value: Period; onChange: (p: Period) => void; }
export const TimePeriodSelector: React.FC<Props> = ({ value, onChange }) => {
  const tabs: { key: Period; label: string }[] = [
    { key: "daily", label: "Daily" },
    { key: "weekly", label: "Weekly" },
    { key: "monthly", label: "Monthly" },
    { key: "yearly", label: "Yearly" },
  ];
  return (
    <div className="time-period-selector" role="tablist" aria-label="Time period selector">
      {tabs.map((t) => (
        <button
          key={t.key}
          className={`tab ${value === t.key ? "active" : ""}`}
          onClick={() => onChange(t.key)}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
};
