import React, { useEffect, useMemo, useState } from "react";
import { Layout } from "../shared/Layout";
import { Header } from "../shared/Header";
import { Footer } from "../shared/Footer";
import { StatsCard } from "../components/StatsCard";
import { PlayTimeChart } from "../components/PlayTimeChart";
import { ContentDistributionChart } from "../components/ContentDistributionChart";
import { MostPlayedList } from "../components/MostPlayedList";
import { TimePeriodSelector } from "../components/TimePeriodSelector";
import { useStats } from "../hooks/useStats";

type Period = "daily" | "weekly" | "monthly" | "yearly";

export const StatsPage: React.FC = () => {
  const [period, setPeriod] = useState<Period>("daily");
  const { data, loading, error, refetch } = useStats(period);
  const [todayMinutes, setTodayMinutes] = useState<number | null>(null);

  // Fetch today time separately (always up-to-date)
  useEffect(() => {
    let canceled = false;
    async function fetchToday() {
      try {
        const r = await fetch("/api/v1/playback/today-time");
        if (!r.ok) return;
        const j = await r.json();
        if (!canceled) setTodayMinutes(j?.minutes ?? 0);
      } catch {
        // ignore
      }
    }
    fetchToday();
    return () => { canceled = true; };
  }, []);

  const periodData = data?.[period] ?? [];
  const dailyChartData = useMemo(() => {
    // normalize minutes per day to keep chart readable
    return (periodData as any[]).map((d) => ({ date: d.date ?? "", minutes: d.minutes ?? 0 }));
  }, [periodData]);

  const topContent = data?.topContent ?? [];
  const distribution = data?.distribution ?? [];
  const recentActivity = data?.recentActivity ?? [];

  return (
    <Layout>
      <Header title="Personal Statistics" />
      <main className="stats-page">
        <section className="stats-overview">
          <StatsCard title="Today" value={formatMinutes(todayMinutes ?? 0)}>
            <div className="stats-sub">Total play time today</div>
          </StatsCard>
          <StatsCard title="This Week" value={formatMinutes(averageFrom(period, data?.weekly))}>
            <div className="stats-sub">Total play time this week</div>
          </StatsCard>
          <StatsCard title="This Month" value={formatMinutes(averageFrom(period, data?.monthly))}>
            <div className="stats-sub">Total play time this month</div>
          </StatsCard>
          <StatsCard title="Unique Content" value={`${data?.contentCount ?? 0}`}>
            <div className="stats-sub">Unique content played</div>
          </StatsCard>
          <StatsCard title="Current Streak" value={String(data?.streakDays ?? 0)}>
            <div className="stats-sub">Consecutive days with playback</div>
          </StatsCard>
        </section>

        <section className="stats-charts">
          <div className="chart-wrap"><PlayTimeChart data={dailyChartData} periodLabel={period} height={320} /></div>
          <div className="chart-wrap"><ContentDistributionChart data={distribution} /></div>
        </section>

        <section className="stats-side-by-side">
          <MostPlayedList data={topContent} />
        </section>

        <TimePeriodSelector value={period} onChange={setPeriod} />
        {loading && <div className="loading">Loading statistics...</div>}
        {error && <div className="error">Error loading statistics: {error}</div>}

        <section className="stats-recent">
          <h3>Recent Activity</h3>
          <ul>
            {recentActivity.length === 0 && <li>No recent activity</li>}
            {recentActivity.map((a) => (
              <li key={a.id}>{a.title} — played at {new Date(a.playedAt).toLocaleString()} for {formatMinutes(a.durationMinutes)}</li>
            ))}
          </ul>
        </section>
      </main>
      <Footer />
    </Layout>
  );
};

function formatMinutes(mins: number) {
  const h = Math.floor(mins / 60);
  const m = Math.floor(mins % 60);
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

function averageFrom(_period: Period, data?: any[]){
  if (!data || data.length === 0) return 0;
  const total = data.reduce((acc, d) => acc + (d.minutes ?? 0), 0);
  const avg = total / data.length;
  return avg;
}

export default StatsPage;
