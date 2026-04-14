import { useEffect, useCallback, useRef, useState } from "react";

type AudioState = {
  isLoading: boolean;
  error: string | null;
  isPlaying: boolean;
  duration: number;
  currentTime: number;
  volume: number;
  muted: boolean;
  playbackRate: number;
};

// Lightweight hook wrapping HTMLAudioElement with simple controls.
export function useAudioPlayer(initialSrc: string) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const [src, setSrc] = useState<string>(initialSrc);
  const [state, setState] = useState<AudioState>({
    isLoading: false,
    error: null,
    isPlaying: false,
    duration: 0,
    currentTime: 0,
    volume: 1,
    muted: false,
    playbackRate: 1,
  });

  // Initialize event bindings
  useEffect(() => {
    const el = audioRef.current;
    if (!el) return;

    const onTimeUpdate = () => setState((s) => ({ ...s, currentTime: el.currentTime }));
    const onLoadedMetadata = () => {
      setState((s) => ({ ...s, duration: el.duration || 0 }));
      setState((s) => ({ ...s, isLoading: false }));
    };
    const onPlay = () => setState((s) => ({ ...s, isPlaying: true }));
    const onPause = () => setState((s) => ({ ...s, isPlaying: false }));
    const onEnded = () => setState((s) => ({ ...s, isPlaying: false }));
    const onWaiting = () => setState((s) => ({ ...s, isLoading: true }));
    const onPlaying = () => setState((s) => ({ ...s, isLoading: false }));

    el.addEventListener("timeupdate", onTimeUpdate);
    el.addEventListener("loadedmetadata", onLoadedMetadata);
    el.addEventListener("play", onPlay);
    el.addEventListener("pause", onPause);
    el.addEventListener("ended", onEnded);
    el.addEventListener("waiting", onWaiting);
    el.addEventListener("playing", onPlaying);

    // cleanup
    return () => {
      el.removeEventListener("timeupdate", onTimeUpdate);
      el.removeEventListener("loadedmetadata", onLoadedMetadata);
      el.removeEventListener("play", onPlay);
      el.removeEventListener("pause", onPause);
      el.removeEventListener("ended", onEnded);
      el.removeEventListener("waiting", onWaiting);
      el.removeEventListener("playing", onPlaying);
    };
  }, [/* run once when ref available */]);

  // Update src on change
  useEffect(() => {
    const el = audioRef.current;
    if (!el) return;
    if (!src) return;
    el.src = src;
    el.load();
    setState((s) => ({ ...s, isLoading: true }));
  }, [src]);

  // Apply volume/mute
  useEffect(() => {
    const el = audioRef.current;
    if (!el) return;
    el.volume = state.volume;
    el.muted = state.muted;
  }, [state.volume, state.muted]);

  // Apply playback rate
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.playbackRate = state.playbackRate;
    }
  }, [state.playbackRate]);

  const play = useCallback(() => {
    const el = audioRef.current;
    if (!el) return;
    const p = el.play();
    if (p && typeof p.then === "function") {
      p.catch(() => {
        setState((s) => ({ ...s, error: s.error ?? "Playback failed" }));
      });
    }
  }, []);

  const pause = useCallback(() => {
    const el = audioRef.current;
    if (el) el.pause();
  }, []);

  const stop = useCallback(() => {
    const el = audioRef.current;
    if (!el) return;
    el.pause();
    el.currentTime = 0;
    setState((s) => ({ ...s, currentTime: 0 }));
  }, []);

  const seek = useCallback((seconds: number) => {
    const el = audioRef.current;
    if (!el) return;
    const max = isFinite(state.duration) && state.duration > 0 ? state.duration : el.duration || Number.POSITIVE_INFINITY;
    const t = Math.max(0, Math.min(seconds, max));
    el.currentTime = t;
    setState((s) => ({ ...s, currentTime: t }));
  }, [state.duration]);

  const setVolumeValue = useCallback((v: number) => {
    setState((s) => ({ ...s, volume: Math.max(0, Math.min(1, v)) }));
  }, []);

  const toggleMute = useCallback(() => {
    setState((s) => ({ ...s, muted: !s.muted }));
  }, []);

  const setRate = useCallback((rate: number) => {
    setState((s) => ({ ...s, playbackRate: rate }));
  }, []);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      const el = audioRef.current;
      if (el) {
        el.pause();
        // clear sources to aid GC
        el.src = "";
      }
    };
  }, []);

  return {
    audioRef,
    src,
    setSrc,
    isLoading: state.isLoading,
    error: state.error,
    isPlaying: state.isPlaying,
    duration: state.duration,
    currentTime: state.currentTime,
    volume: state.volume,
    muted: state.muted,
    playbackRate: state.playbackRate,
    play,
    pause,
    stop,
    seek,
    setVolumeValue,
    toggleMute,
    setRate,
  };
}

export default useAudioPlayer;
