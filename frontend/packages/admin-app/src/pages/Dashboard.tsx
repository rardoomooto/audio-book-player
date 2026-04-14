import React, { useEffect, useState } from 'react';
import { ProtectedRoute } from '../../../../shared/components/ProtectedRoute';
import { DashboardCard } from '../components/DashboardCard';
import { UserActivityChart } from '../components/UserActivityChart';
import { ContentPopularityChart } from '../components/ContentPopularityChart';
import { PlaytimeTrendsChart } from '../components/PlaytimeTrendsChart';
import { TopUsersList } from '../components/TopUsersList';
import { TopContentList } from '../components/TopContentList';
import { RecentActivity } from '../components/RecentActivity';
import { UserDistributionChart } from '../components/UserDistributionChart';
import { useDashboardStats } from '../hooks/useDashboardStats';
import type { DashboardStats } from '../../../../shared/types/stats';

export type TimePeriod = 'daily' | 'weekly' | 'monthly' | 'yearly';

export const Dashboard: React.FC = () => {
  // Time period selector
  const [period, setPeriod] = useState<TimePeriod>('daily');
  const { data, loading, error, refetch } = useDashboardStats(period);

  // Local derived data with safe defaults to avoid rendering when loading
  const totalUsers = data?.totalUsers ?? 0;
  const totalContent = data?.totalContent ?? 0;
  const totalPlaytime = data?.totalPlaytime ?? 0; // seconds
  const activeUsers =
    period === 'daily'
      ? data?.activeUsersToday ?? 0
      : period === 'weekly'
      ? data?.activeUsersThisWeek ?? 0
      : period === 'monthly'
      ? data?.activeUsersThisMonth ?? 0
      : 0;

  const averageSessionDuration = data?.averageSessionDuration ?? 0;

  // chart data
  const userActivitySeries = data?.userActivitySeries ?? [];
  const topContents = data?.topContents ?? [];
  const playtimeTrend = data?.playtimeTrend ?? [];
  const distribution = data?.userDistribution ?? [];

  // Simple retry if error
  useEffect(() => {
    if (error) {
      // try a refresh once
      refetch();
    }
  }, [error]);

  return (
    <ProtectedRoute>
      <div style={{ padding: 20 }}>
        <h1>Admin Dashboard</h1>

        {/* Period selector */}
        <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 16 }}>
          {(['daily', 'weekly', 'monthly', 'yearly'] as TimePeriod[]).map((p) => (
            <button
              key={p}
              onClick={() => setPeriod(p)}
              style={{
                padding: '8px 12px',
                borderRadius: 6,
                border: period === p ? '2px solid #1976d2' : '1px solid #ccc',
                background: period === p ? '#e3f2fd' : '#fff',
                cursor: 'pointer',
              }}
            >
              {p.charAt(0).toUpperCase() + p.slice(1)}
            </button>
          ))}
        </div>

        {/* Overview cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16, marginBottom: 24 }}>
          <DashboardCard title="Total Users" value={totalUsers.toLocaleString()} loading={loading} />
          <DashboardCard title="Total Content" value={totalContent.toLocaleString()} loading={loading} />
          <DashboardCard
            title="Total Playtime"
            value={formatSeconds(totalPlaytime)}
            loading={loading}
            subtitle="hh:mm:ss"
          />
          <DashboardCard
            title={`Active Users (${capitalize(period)})`}
            value={activeUsers.toLocaleString()}
            loading={loading}
          />
        </div>

        {/* Charts & Lists */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: 16 }}>
          <div style={{ display: 'grid', gap: 16 }}>
            <UserActivityChart data={userActivitySeries} period={period} />
            <PlaytimeTrendsChart data={playtimeTrend} period={period} />
          </div>
          <div style={{ display: 'grid', gap: 16 }}>
            <ContentPopularityChart topContents={topContents} />
            <UserDistributionChart distribution={distribution} />
          </div>
        </div>

        {/* Top lists & recent activity */}
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: 16, marginTop: 16 }}>
          <TopUsersList users={(data?.topUsers ?? []) as any} />
          <TopContentList contents={(data?.topContents ?? []) as any} />
        </div>
        <div style={{ marginTop: 16 }}>
          <RecentActivity activities={data?.recentActivity ?? []} />
        </div>
      </div>
    </ProtectedRoute>
  );
};

function formatSeconds(totalSeconds: number): string {
  if (!Number.isFinite(totalSeconds)) return '0s';
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = Math.floor(totalSeconds % 60);
  return [h, m, s]
    .map((v) => v.toString().padStart(2, '0'))
    .join(':');
}

function capitalize(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export default Dashboard;
