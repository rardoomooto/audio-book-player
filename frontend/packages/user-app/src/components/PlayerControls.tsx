import React from "react";

type PlayerControlsProps = {
  isPlaying: boolean;
  onPlay: () => void;
  onPause: () => void;
  onSeekBackward: () => void;
  onSeekForward: () => void;
  onSpeedChange: (rate: number) => void;
  playbackRate: number;
  onPrev?: () => void;
  onNext?: () => void;
  onSeek?: (seconds: number) => void;
};

export const PlayerControls: React.FC<PlayerControlsProps> = ({
  isPlaying,
  onPlay,
  onPause,
  onSeekBackward,
  onSeekForward,
  onSpeedChange,
  playbackRate,
  onSeek,
}) => {
  const speedOptions = [0.5, 1, 1.25, 1.5, 2];
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12 }} aria-label="Playback controls">
      <button aria-label="Seek backward 30 seconds" onClick={onSeekBackward}>
        -30s
      </button>
      {isPlaying ? (
        <button aria-label="Pause" onClick={onPause}>Pause</button>
      ) : (
        <button aria-label="Play" onClick={onPlay}>Play</button>
      )}
      <button aria-label="Seek forward 30 seconds" onClick={onSeekForward}>+30s</button>

      <span style={{ width: 1, height: 20, background: "#ccc" }} aria-hidden />

      <label htmlFor="speed-select" style={{ fontSize: 12, color: "#555" }}>Speed</label>
      <select
        id="speed-select"
        value={playbackRate}
        onChange={(e) => onSpeedChange(Number(e.target.value))}
        aria-label="Playback speed"
        style={{ padding: 6 }}
      >
        {speedOptions.map((s) => (
          <option key={s} value={s}>
            {s}x
          </option>
        ))}
      </select>
    </div>
  );
};

export default PlayerControls;
