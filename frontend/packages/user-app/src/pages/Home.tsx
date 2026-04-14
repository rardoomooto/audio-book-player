import React from 'react';
import { Box, Card, CardContent, CardActionArea, Typography, Grid, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import LibraryMusicIcon from '@mui/icons-material/LibraryMusic';
import PlayCircleIcon from '@mui/icons-material/PlayCircle';
import BarChartIcon from '@mui/icons-material/BarChart';

const Home: React.FC = () => {
  const navigate = useNavigate();

  const quickLinks = [
    {
      title: '浏览内容',
      description: '浏览和搜索有声读物',
      icon: <LibraryMusicIcon sx={{ fontSize: 48 }} />,
      path: '/library',
      color: '#1976d2',
    },
    {
      title: '继续播放',
      description: '从上次位置继续播放',
      icon: <PlayCircleIcon sx={{ fontSize: 48 }} />,
      path: '/player',
      color: '#2e7d32',
    },
    {
      title: '播放统计',
      description: '查看您的播放历史和统计',
      icon: <BarChartIcon sx={{ fontSize: 48 }} />,
      path: '/stats',
      color: '#ed6c02',
    },
  ];

  return (
    <Box sx={{ padding: 3 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
        欢迎使用有声读物播放器
      </Typography>

      <Paper sx={{ p: 3, mb: 4, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <Typography variant="h6">
          选择一个功能开始使用
        </Typography>
      </Paper>

      <Grid container spacing={3}>
        {quickLinks.map((link) => (
          <Grid item xs={12} sm={6} md={4} key={link.path}>
            <Card 
              sx={{ 
                height: '100%',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                },
              }}
            >
              <CardActionArea 
                onClick={() => navigate(link.path)}
                sx={{ height: '100%', minHeight: 200 }}
              >
                <CardContent sx={{ textAlign: 'center', py: 4 }}>
                  <Box sx={{ color: link.color, mb: 2 }}>
                    {link.icon}
                  </Box>
                  <Typography variant="h6" gutterBottom>
                    {link.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {link.description}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default Home;
