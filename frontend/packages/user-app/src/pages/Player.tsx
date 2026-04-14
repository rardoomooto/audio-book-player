import React, { useEffect, useState, useCallback } from "react";
import AudioPlayer from "../components/AudioPlayer";

type PlaybackState = {
  content_id?: string;
  title?: string;
  author?: string;
  cover?: string;
  duration?: number;
  currentTime?: number;
  state?: string; // 'playing' | 'paused' etc
};

type Limits = {
  dailyLimitSeconds: number;
};

export const PlayerPage: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [playback, setPlayback] = useState<PlaybackState | null>(null);
  const [streamUrl, setStreamUrl] = useState<string>("");
  const [limits, setLimits] = useState<Limits | null>(null);
  const [todayTime, setTodayTime] = useState<number>(0);

  // Load current playback and stream URL
  const loadCurrent = useCallback(async () => {
    try {
      setLoading(true);
      // Fetch current playback
      const currentRes = await fetch("/api/v1/playback/current");
      if (!currentRes.ok) throw new Error("Failed to fetch current playback");
      const current: PlaybackState = await currentRes.json();
      setPlayback(current);
      if (current?.content_id) {
        const urlRes = await fetch(`/api/v1/contents/${current.content_id}/stream`);
        if (urlRes.ok) {
          const data = await urlRes.json();
          setStreamUrl(data.url);
        }
      }
      // Limits
      const limRes = await fetch("/api/v1/playback/limits");
      if (limRes.ok) {
        const lim: Limits = await limRes.json();
        setLimits(lim);
      }
      // Today time
      const todayRes = await fetch("/api/v1/playback/today-time");
      if (todayRes.ok) {
        const j = await todayRes.json();
        setTodayTime(j.todayTimeSeconds ?? 0);
      }
    } catch (e) {
      // error handling
      console.error(e);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadCurrent();
  }, [loadCurrent]);

  // Sync with backend playback state periodically
  useEffect(() => {
    const t = setInterval(() => {
      // Attempt to refresh today time / limits and current playback
      fetch("/api/v1/playback/limits").then(r => r.json()).then((l) => setLimits(l)).catch(() => {});
      fetch("/api/v1/playback/today-time").then(r => r.json()).then((j) => setTodayTime(j.todayTimeSeconds ?? 0)).catch(() => {});
      // For demo, we skip refreshing current playback to avoid churning the UI.
    }, 15000);
    return () => clearInterval(t);
  }, []);
  // Actions wrappers to backend (real API calls)
  const handlePlay = async () => {
    if (limits && todayTime >= limits.dailyLimitSeconds) return;
    try {
      if (playback?.content_id) await fetch("/api/v1/playback/play", { method: "POST", headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ content_id: playback.content_id }) });
    } catch (e) {
      console.error(e);
    }
  };
  const handlePause = async () => {
    try {
      await fetch("/api/v1/playback/pause", { method: "POST" });
    } catch (e) {
      console.error(e);
    }
  };

  // Computed remaining time today
  const remainingToday = limits?.dailyLimitSeconds ? Math.max(0, limits.dailyLimitSeconds - todayTime) : 0;

  return (
    <div style={{ padding: 24 }}>
      <h1>User Player</h1>
      {loading && <div>Loading current track...</div>}
      {!loading && playback && (
        <div style={{ display: "flex", gap: 24 }}>
          <div style={{ minWidth: 280 }}>
            {playback.cover && <img src={playback.cover} alt="cover" style={{ width: 260, height: 260, objectFit: 'cover', borderRadius: 8 }} />}
            <h2 style={{ marginTop: 12 }}>{playback.title}</h2>
            <p style={{ color: "#666" }}>{playback.author}</p>
            <div style={{ marginTop: 8, padding: 8, border: '1px solid #eee', borderRadius: 6 }}>
              <strong>Today</strong>
              <div>Remaining: {remainingToday > 0 ? new Date(remainingToday * 1000).toISOString().substr(14, 5) : "0:00"}</div>
            </div>
          </div>
          <div style={{ flex: 1 }}>
            <AudioPlayer
              src={streamUrl}
              contentId={playback.content_id}
              title={playback.title}
              author={playback.author}
              cover={playback.cover}
              onPlay={handlePlay}
              onPause={handlePause}
            />
          </div>
        </div>
      )}
      {(!playback || !streamUrl) && !loading && <div>No track loaded.</div>}
    </div>
  );
};

export default function PlayerPageWrapper() {
  return <PlayerPage />;
}
