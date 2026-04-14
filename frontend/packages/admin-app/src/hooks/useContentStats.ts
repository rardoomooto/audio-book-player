import { useState } from 'react';
// Simple fetch to per-content stats

export const useContentStats = (contentId: string) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<any>(null);

  const fetch = async () => {
    setLoading(true);
    setError(null);
    try {
      // Fallback: fetch per-content stats from API
      const resp = await fetch(`/api/v1/stats/contents/${encodeURIComponent(contentId)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });
      const d = await resp.json();
      setData(d?.data ?? d);
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, fetch };
};
