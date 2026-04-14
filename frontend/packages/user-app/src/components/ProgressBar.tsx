import React from "react";

type ProgressBarProps = {
  currentTime: number;
  duration: number;
  onSeek: (seconds: number) => void;
};

const formatTime = (sec: number) => {
  if (!isFinite(sec) || sec < 0) return "0:00";
  const m = Math.floor(sec / 60);
  const s = Math.floor(sec % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
};

export const ProgressBar: React.FC<ProgressBarProps> = ({ currentTime, duration, onSeek }) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = Number(e.target.value);
    onSeek(val);
  };

  const value = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12 }} aria-label="Playback progress">
      <span style={{ width: 40, textAlign: "right" }}>{formatTime(currentTime)}</span>
      <input
        type="range"
        min={0}
        max={duration || 0}
        step={0.25}
        value={currentTime}
        onChange={handleChange}
        aria-valuemin={0}
        aria-valuemax={duration || 0}
        aria-valuenow={currentTime}
        style={{ flex: 1 }}
      />
      <span style={{ width: 60 }}>{formatTime(duration)}</span>
    </div>
  );
};

export default ProgressBar;
