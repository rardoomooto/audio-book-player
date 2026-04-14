import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Paper,
  Chip,
  Button,
  Divider,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement,
} from 'chart.js';
import { Bar, Pie, Line } from 'react-chartjs-2';
import { Layout } from '../../../../shared/components/Layout';
import DownloadIcon from '@mui/icons-material/Download';
import RefreshIcon from '@mui/icons-material/Refresh';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import PeopleIcon from '@mui/icons-material/People';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  LineElement,
  PointElement
);

interface ContentStatsData {
  content_id: string;
  content_title: string;
  total_plays: number;
  total_duration_seconds: number;
  unique_users: number;
  avg_session_duration: number;
  last_played: string;
  daily_stats: Array<{
    date: string;
    plays: number;
    duration_seconds: number;
    users: number;
  }>;
  top_users: Array<{
    user_id: string;
    username: string;
    plays: number;
    duration_seconds: number;
  }>;
  playback_by_hour: Array<{
    hour: number;
    plays: number;
  }>;
}

type Props = {
  contentId: string;
};

export const ContentStats: React.FC<Props> = ({ contentId }) => {
  const [data, setData] = useState<ContentStatsData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<any>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const resp = await fetch(`/api/v1/stats/contents/${encodeURIComponent(contentId)}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });
      if (!resp.ok) throw new Error('Failed to fetch data');
      const d = await resp.json();
      setData(d?.data ?? d);
    } catch (e) {
      setError(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [contentId]);

  const handleExport = async () => {
    const resp = await fetch(`/api/v1/stats/export/contents/${encodeURIComponent(contentId)}`, {
      method: 'GET',
      credentials: 'include',
    });
    const blob = await resp.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `content_${contentId}_stats.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    if (hours > 0) {
      return `${hours}h ${minutes}m`;
    }
    return `${minutes}m`;
  };

  // Chart data preparations
  const dailyChartData = {
    labels: data?.daily_stats?.map(s => s.date) || [],
    datasets: [
      {
        label: '播放次数',
        data: data?.daily_stats?.map(s => s.plays) || [],
        backgroundColor: 'rgba(25, 118, 210, 0.5)',
        borderColor: 'rgb(25, 118, 210)',
        borderWidth: 1,
      },
    ],
  };

  const hourlyChartData = {
    labels: data?.playback_by_hour?.map(h => `${h.hour}:00`) || [],
    datasets: [
      {
        label: '播放次数',
        data: data?.playback_by_hour?.map(h => h.plays) || [],
        fill: false,
        borderColor: 'rgb(46, 125, 50)',
        tension: 0.1,
      },
    ],
  };

  const userPieData = {
    labels: data?.top_users?.slice(0, 5).map(u => u.username) || [],
    datasets: [
      {
        data: data?.top_users?.slice(0, 5).map(u => u.plays) || [],
        backgroundColor: [
          'rgba(25, 118, 210, 0.8)',
          'rgba(46, 125, 50, 0.8)',
          'rgba(237, 108, 2, 0.8)',
          'rgba(156, 39, 176, 0.8)',
          'rgba(0, 188, 212, 0.8)',
        ],
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { position: 'top' as const },
    },
  };

  return (
    <Layout>
      <Box sx={{ padding: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4">
            内容统计: {data?.content_title || '加载中...'}
          </Typography>
          <Box>
            <Button
              startIcon={<RefreshIcon />}
              onClick={fetchData}
              disabled={loading}
              sx={{ mr: 1 }}
            >
              刷新
            </Button>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={handleExport}
              disabled={!data}
            >
              导出CSV
            </Button>
          </Box>
        </Box>

        {loading && <Typography>加载中...</Typography>}
        {error && <Typography color="error">加载失败</Typography>}

        {data && (
          <>
            {/* Summary Cards */}
            <Grid container spacing={3} sx={{ mb: 3 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <PlayArrowIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                    <Typography variant="h4">{data.total_plays}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      总播放次数
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <AccessTimeIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                    <Typography variant="h4">{formatDuration(data.total_duration_seconds)}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      总播放时长
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <PeopleIcon sx={{ fontSize: 40, color: 'warning.main', mb: 1 }} />
                    <Typography variant="h4">{data.unique_users}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      独立用户
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent sx={{ textAlign: 'center' }}>
                    <TrendingUpIcon sx={{ fontSize: 40, color: 'info.main', mb: 1 }} />
                    <Typography variant="h4">{formatDuration(data.avg_session_duration)}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      平均会话时长
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            {/* Charts */}
            <Grid container spacing={3} sx={{ mb: 3 }}>
              <Grid item xs={12} md={8}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      每日播放趋势
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <Bar data={dailyChartData} options={chartOptions} />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={4}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      用户播放分布
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <Pie data={userPieData} options={{ ...chartOptions, plugins: { legend: { position: 'bottom' } } }} />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            {/* Hourly Distribution */}
            <Grid container spacing={3} sx={{ mb: 3 }}>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      播放时间分布（按小时）
                    </Typography>
                    <Box sx={{ height: 250 }}>
                      <Line data={hourlyChartData} options={chartOptions} />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>

            {/* Top Users Table */}
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  活跃用户排行
                </Typography>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>排名</TableCell>
                        <TableCell>用户名</TableCell>
                        <TableCell align="right">播放次数</TableCell>
                        <TableCell align="right">播放时长</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {data.top_users?.map((user, index) => (
                        <TableRow key={user.user_id}>
                          <TableCell>
                            <Chip label={index + 1} size="small" color={index < 3 ? 'primary' : 'default'} />
                          </TableCell>
                          <TableCell>{user.username}</TableCell>
                          <TableCell align="right">{user.plays}</TableCell>
                          <TableCell align="right">{formatDuration(user.duration_seconds)}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </>
        )}
      </Box>
    </Layout>
  );
};

export default ContentStats;
