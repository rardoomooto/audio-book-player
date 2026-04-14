import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Alert,
  Chip,
  Stack,
  Divider,
  Paper,
} from '@mui/material';
import { Layout } from '../../../../shared/components/Layout';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import StopIcon from '@mui/icons-material/Stop';
import RefreshIcon from '@mui/icons-material/Refresh';
import FolderIcon from '@mui/icons-material/Folder';
import AudioFileIcon from '@mui/icons-material/AudioFile';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import HourglassEmptyIcon from '@mui/icons-material/HourglassEmpty';

interface ScanStatus {
  isScanning: boolean;
  progress: number;
  currentPath: string;
  filesFound: number;
  filesProcessed: number;
  errors: string[];
  startTime: string | null;
  endTime: string | null;
}

const ScanStatusPage: React.FC = () => {
  const [scanStatus, setScanStatus] = useState<ScanStatus>({
    isScanning: false,
    progress: 0,
    currentPath: '',
    filesFound: 0,
    filesProcessed: 0,
    errors: [],
    startTime: null,
    endTime: null,
  });

  const [lastScanResult, setLastScanResult] = useState<{
    totalFiles: number;
    newFiles: number;
    updatedFiles: number;
    timestamp: string;
  } | null>(null);

  const handleStartScan = async () => {
    setScanStatus({
      isScanning: true,
      progress: 0,
      currentPath: '正在初始化...',
      filesFound: 0,
      filesProcessed: 0,
      errors: [],
      startTime: new Date().toISOString(),
      endTime: null,
    });

    // Simulate scan progress (in real app, this would be WebSocket or polling)
    // This is a placeholder - the actual implementation would call the backend API
    try {
      // Call the scan endpoint
      const response = await fetch('/api/v1/contents/scan', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (response.ok) {
        const result = await response.json();
        setLastScanResult({
          totalFiles: result.total_files || 0,
          newFiles: result.new_files || 0,
          updatedFiles: result.updated_files || 0,
          timestamp: new Date().toISOString(),
        });
      }
    } catch (error) {
      setScanStatus(prev => ({
        ...prev,
        errors: [...prev.errors, `扫描失败: ${error}`],
      }));
    } finally {
      setScanStatus(prev => ({
        ...prev,
        isScanning: false,
        progress: 100,
        endTime: new Date().toISOString(),
      }));
    }
  };

  const handleStopScan = () => {
    setScanStatus(prev => ({
      ...prev,
      isScanning: false,
      endTime: new Date().toISOString(),
    }));
  };

  const getStatusChip = () => {
    if (scanStatus.isScanning) {
      return <Chip icon={<HourglassEmptyIcon />} label="扫描中" color="primary" />;
    }
    if (scanStatus.errors.length > 0) {
      return <Chip icon={<ErrorIcon />} label="有错误" color="error" />;
    }
    return <Chip icon={<CheckCircleIcon />} label="就绪" color="success" />;
  };

  return (
    <Layout>
      <Box sx={{ padding: 3 }}>
        <Typography variant="h4" gutterBottom>
          内容扫描状态
        </Typography>

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 2 }}>
              <Box>
                <Typography variant="h6">扫描控制</Typography>
                <Typography variant="body2" color="text.secondary">
                  扫描NAS上的有声读物文件并更新索引
                </Typography>
              </Box>
              {getStatusChip()}
            </Stack>

            <Divider sx={{ my: 2 }} />

            <Stack direction="row" spacing={2}>
              <Button
                variant="contained"
                startIcon={<PlayArrowIcon />}
                onClick={handleStartScan}
                disabled={scanStatus.isScanning}
              >
                开始扫描
              </Button>
              <Button
                variant="outlined"
                startIcon={<StopIcon />}
                onClick={handleStopScan}
                disabled={!scanStatus.isScanning}
              >
                停止扫描
              </Button>
              <Button
                variant="outlined"
                startIcon={<RefreshIcon />}
                onClick={() => {
                  // Refresh status - in real app would poll backend
                }}
              >
                刷新状态
              </Button>
            </Stack>
          </CardContent>
        </Card>

        {/* Progress Section */}
        {scanStatus.isScanning && (
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                扫描进度
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={scanStatus.progress} 
                sx={{ mb: 2 }}
              />
              <Typography variant="body2" color="text.secondary">
                {scanStatus.currentPath || '准备中...'}
              </Typography>
            </CardContent>
          </Card>
        )}

        {/* Statistics Cards */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <FolderIcon sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                <Typography variant="h4">{scanStatus.filesFound}</Typography>
                <Typography variant="body2" color="text.secondary">
                  发现文件
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <AudioFileIcon sx={{ fontSize: 40, color: 'success.main', mb: 1 }} />
                <Typography variant="h4">{scanStatus.filesProcessed}</Typography>
                <Typography variant="body2" color="text.secondary">
                  已处理
                </Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <ErrorIcon sx={{ fontSize: 40, color: 'error.main', mb: 1 }} />
                <Typography variant="h4">{scanStatus.errors.length}</Typography>
                <Typography variant="body2" color="text.secondary">
                  错误
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        {/* Last Scan Result */}
        {lastScanResult && (
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                上次扫描结果
              </Typography>
              <Paper variant="outlined" sx={{ p: 2, bgcolor: 'grey.50' }}>
                <Typography variant="body2">
                  时间: {new Date(lastScanResult.timestamp).toLocaleString()}
                </Typography>
                <Typography variant="body2">
                  总文件: {lastScanResult.totalFiles}
                </Typography>
                <Typography variant="body2">
                  新增: {lastScanResult.newFiles}
                </Typography>
                <Typography variant="body2">
                  更新: {lastScanResult.updatedFiles}
                </Typography>
              </Paper>
            </CardContent>
          </Card>
        )}

        {/* Errors */}
        {scanStatus.errors.length > 0 && (
          <Card>
            <CardContent>
              <Typography variant="h6" color="error" gutterBottom>
                错误列表
              </Typography>
              {scanStatus.errors.map((error, index) => (
                <Alert severity="error" key={index} sx={{ mb: 1 }}>
                  {error}
                </Alert>
              ))}
            </CardContent>
          </Card>
        )}
      </Box>
    </Layout>
  );
};

// Import Grid component
import { Grid } from '@mui/material';

export default ScanStatusPage;
