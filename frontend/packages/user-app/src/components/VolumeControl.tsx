import React from "react";

type VolumeControlProps = {
  volume: number;
  muted: boolean;
  onVolumeChange: (v: number) => void;
  onToggleMute: () => void;
};

export const VolumeControl: React.FC<VolumeControlProps> = ({ volume, muted, onVolumeChange, onToggleMute }) => {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 8 }} aria-label="Volume controls">
      <button aria-label={muted ? "Unmute" : "Mute"} onClick={onToggleMute} style={{ padding: 8 }}>
        {muted ? "🔇" : "🔊"}
      </button>
      <input
        type="range"
        min={0}
        max={1}
        step={0.01}
        value={volume}
        onChange={(e) => onVolumeChange(Number(e.target.value))}
        aria-valuemin={0}
        aria-valuemax={1}
        aria-valuenow={volume}
        style={{ width: 120 }}
      />
    </div>
  );
};

export default VolumeControl;
