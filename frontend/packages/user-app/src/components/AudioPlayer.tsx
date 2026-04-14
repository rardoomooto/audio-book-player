import React, { useEffect } from "react";
import { useAudioPlayer } from "../hooks/useAudioPlayer";
import ProgressBar from "./ProgressBar";
import TimeDisplay from "./TimeDisplay";
import VolumeControl from "./VolumeControl";
import PlayerControls from "./PlayerControls";

type AudioPlayerProps = {
  src: string;
  contentId?: string;
  title?: string;
  author?: string;
  cover?: string;
  onPlay?: () => void;
  onPause?: () => void;
  onSeekBackend?: (seconds: number) => void;
  onRateBackend?: (rate: number) => void;
  onSeek?: (seconds: number) => void;
  durationOverride?: number;
  loadingHint?: string;
};

export const AudioPlayer: React.FC<AudioPlayerProps> = ({
  src,
  contentId,
  title,
  author,
  cover,
  onPlay,
  onPause,
  onSeekBackend,
  onRateBackend,
  onSeek,
  durationOverride,
  loadingHint,
}) => {
  const {
    audioRef,
    // internal state
    isLoading,
    error,
    isPlaying,
    duration,
    currentTime,
    volume,
    muted,
    playbackRate,
    play,
    pause,
    seek,
    setVolumeValue,
    toggleMute,
    setRate,
  } = useAudioPlayer(src);

  // Bind backend sync callbacks
  useEffect(() => {
    if (isPlaying) {
      onPlay?.();
    } else {
      onPause?.();
    }
  }, [isPlaying]);

  // Propagate user seek to backend if provided
  useEffect(() => {
    if (onSeek) {
      // No-op here; actual seek from ProgressBar triggers seek() which updates local time
    }
  }, [currentTime]);

  // Keyboard accessibility: space toggles play/pause
  const containerRef = React.useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        e.preventDefault();
        if (isPlaying) pause(); else play();
      }
    };
    el.addEventListener("keydown", onKey);
    return () => el.removeEventListener("keydown", onKey);
  }, [isPlaying]);

  // Render
  return (
    <div ref={containerRef} role="region" aria-label="Audio player" style={{ border: "1px solid #e5e5e5", padding: 16, borderRadius: 8, maxWidth: 800 }}>
      <audio ref={audioRef} preload="metadata" controls={false} style={{ display: "none" }} />
      <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
        {cover && (
          <img src={cover} alt="cover" style={{ width: 100, height: 100, objectFit: "cover", borderRadius: 8 }} />
        )}
        <div style={{ display: "flex", flexDirection: "column" }}>
          <strong style={{ fontSize: 16 }}>{title || "Unknown Title"}</strong>
          <span style={{ color: "#666" }}>{author || "Unknown Author"}</span>
        </div>
      </div>
      <div style={{ marginTop: 16 }}>
        <ProgressBar currentTime={currentTime} duration={duration} onSeek={seek} />
      </div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 12 }}>
        <TimeDisplay currentTime={currentTime} duration={duration} />
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div>
            <button aria-label={isPlaying ? "Pause" : "Play"} onClick={isPlaying ? pause : play}>
              {isPlaying ? "Pause" : "Play"}
            </button>
          </div>
          <VolumeControl
            volume={volume}
            muted={muted}
            onVolumeChange={(v) => setVolumeValue(v)}
            onToggleMute={toggleMute}
          />
          <div>
            <label htmlFor="rate" style={{ marginRight: 6 }}>Speed</label>
            <select id="rate" value={playbackRate} onChange={(e) => setRate(Number(e.target.value))} aria-label="Playback speed">
              {[0.5, 1, 1.25, 1.5, 2].map((r) => (
                <option key={r} value={r}>{r}x</option>
              ))}
            </select>
          </div>
        </div>
      </div>
      {error && (
        <div role="alert" style={{ color: "#b00020", marginTop: 8 }}>{error}</div>
      )}
      {isLoading && (
        <div aria-label="Loading" style={{ marginTop: 8 }}>Loading...</div>
      )}
    </div>
  );
};

export default AudioPlayer;
