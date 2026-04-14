import { useEffect, useMemo, useState } from 'react';
import { fetchDashboardStats } from '../../shared/api-client/stats';
import type { DashboardStats } from '../../../../shared/types/stats';

export const useDashboardStats = (period: 'daily'|'weekly'|'monthly'|'yearly') => {
  const [data, setData] = useState<DashboardStats | undefined>(undefined);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<any>(null);

  const fetch = async () => {
    setLoading(true);
    setError(null);
    try {
      const d = await fetchDashboardStats(period);
      setData(d as DashboardStats);
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false);
    }
  };

  // initial fetch
  useEffect(() => {
    fetch();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [period]);

  // provide a manual refetch for error retry in component
  const refetch = fetch;

  return useMemo(() => ({ data, loading, error, refetch }), [data, loading, error]);
};
