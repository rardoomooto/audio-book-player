import React, { useEffect } from 'react';
import { ProtectedRoute } from '../../../../shared/components/ProtectedRoute';
import { useUserStats } from '../hooks/useUserStats';

type Props = {
  userId: string;
};

export const UserStats: React.FC<Props> = ({ userId }) => {
  const { data, loading, error, fetch } = useUserStats(userId);
  useEffect(() => {
    fetch();
  }, [userId]);
  return (
    <ProtectedRoute>
      <div style={{ padding: 20 }}>
        <h2>User Statistics</h2>
        {loading && <p>Loading...</p>}
        {error && <p>Error loading data</p>}
        {!loading && data && (
          <pre>{JSON.stringify(data, null, 2)}</pre>
        )}
      </div>
    </ProtectedRoute>
  );
};
