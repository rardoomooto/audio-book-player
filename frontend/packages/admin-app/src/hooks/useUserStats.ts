import { useState } from 'react';
import { fetchUserStats } from '../../shared/api-client/stats';

export const useUserStats = (userId: string) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<any>(null);

  const fetch = async () => {
    setLoading(true);
    setError(null);
    try {
      const d = await fetchUserStats(userId);
      setData(d);
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false);
    }
  };

  return { data, loading, error, fetch };
};
