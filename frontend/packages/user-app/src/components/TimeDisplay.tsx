import React from "react";

type TimeDisplayProps = {
  currentTime: number;
  duration: number;
};

const fmt = (sec: number) => {
  if (!isFinite(sec) || sec < 0) return "0:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
};

export const TimeDisplay: React.FC<TimeDisplayProps> = ({ currentTime, duration }) => {
  return (
    <div aria-label="Time display" style={{ display: "flex", gap: 8, alignItems: "center" }}>
      <span>{fmt(currentTime)}</span>
      <span style={{ opacity: 0.5 }}>/</span>
      <span style={{ opacity: 0.9 }}>{fmt(duration)}</span>
    </div>
  );
};

export default TimeDisplay;
