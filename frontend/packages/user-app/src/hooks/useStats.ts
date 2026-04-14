import { useCallback, useEffect, useState } from "react";

type Period = "daily" | "weekly" | "monthly" | "yearly";

type StatsPeriodDatum = {
  date: string; // e.g., '2026-03-28' or 'Mon'
  minutes: number;
};

type TopContent = {
  id: string;
  title: string;
  playCount: number;
  totalTimeMinutes: number;
};

type DistributionItem = {
  id?: string;
  title: string;
  minutes: number;
  percent?: number;
};

interface StatsResponse {
  totalPlayTimeMinutes?: number;
  contentCount?: number;
  streakDays?: number;
  daily?: StatsPeriodDatum[];
  weekly?: StatsPeriodDatum[];
  monthly?: StatsPeriodDatum[];
  yearly?: StatsPeriodDatum[];
  topContent?: TopContent[];
  distribution?: DistributionItem[];
  recentActivity?: { id: string; title: string; playedAt: string; durationMinutes: number }[];
}

export function useStats(period: Period) {
  const [data, setData] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // simple in-memory cache timestamp per period
const [cacheTime, setCacheTime] = useState<number>(0);

  const fetchStats = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch(`/api/v1/stats/${period}`);
      if (!resp.ok) {
        throw new Error(`Failed to fetch stats: ${resp.status}`);
      }
      const json = await resp.json();
      setData(json);
      setCacheTime(Date.now());
    } catch (e) {
      setError((e as Error).message);
      setData(null);
    } finally {
      setLoading(false);
    }
  }, [period]);

  // Load on mount or period change, with simple 5-minute cache
  useEffect(() => {
    const now = Date.now();
    if (data && cacheTime && now - cacheTime < 1000 * 60 * 5) {
      // use cached
      return;
    }
    fetchStats();
  }, [period]);

  return { data, loading, error, refetch: fetchStats };
}
