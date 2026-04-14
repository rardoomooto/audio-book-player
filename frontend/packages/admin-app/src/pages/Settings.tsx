import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Alert,
  Stack,
  Chip,
  Grid,
} from '@mui/material';
import { Layout } from '../../../../shared/components/Layout';
import SaveIcon from '@mui/icons-material/Save';
import RefreshIcon from '@mui/icons-material/Refresh';
import StorageIcon from '@mui/icons-material/Storage';
import SecurityIcon from '@mui/icons-material/Security';
import TuneIcon from '@mui/icons-material/Tune';
import InfoIcon from '@mui/icons-material/Info';

interface SettingsState {
  // Storage settings
  storageType: 'local' | 'webdav';
  webdavUrl: string;
  webdavUsername: string;
  webdavPassword: string;
  localMountPath: string;
  
  // App settings
  appName: string;
  enableDebug: boolean;
  enableCors: boolen;
  
  // Security settings
  jwtExpiration: number;
  enableRateLimit: boolean;
}

const Settings: React.FC = () => {
  const [settings, setSettings] = useState<SettingsState>({
    storageType: 'local',
    webdavUrl: '',
    webdavUsername: '',
    webdavPassword: '',
    localMountPath: '/mnt/audiobooks',
    appName: 'AudioBook Player',
    enableDebug: false,
    enableCors: true,
    jwtExpiration: 15,
    enableRateLimit: true,
  });

  const [saved, setSaved] = useState(false);

  const handleChange = (field: keyof SettingsState, value: any) => {
    setSettings(prev => ({ ...prev, [field]: value }));
    setSaved(false);
  };

  const handleSave = () => {
    // In a real app, this would save to backend
    console.log('Saving settings:', settings);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <Layout>
      <Box sx={{ padding: 3 }}>
        <Typography variant="h4" gutterBottom>
          系统设置
        </Typography>

        {saved && (
          <Alert severity="success" sx={{ mb: 3 }}>
            设置已保存成功！
          </Alert>
        )}

        {/* Storage Settings */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
              <StorageIcon color="primary" />
              <Typography variant="h6">存储设置</Typography>
              <Chip 
                label={settings.storageType === 'local' ? '本地存储' : 'WebDAV'} 
                size="small" 
                color="primary" 
              />
            </Stack>
            
            <Divider sx={{ my: 2 }} />

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.storageType === 'webdav'}
                      onChange={(e) => handleChange('storageType', e.target.checked ? 'webdav' : 'local')}
                    />
                  }
                  label="使用 WebDAV 存储"
                />
              </Grid>
            </Grid>

            {settings.storageType === 'webdav' ? (
              <Grid container spacing={2} sx={{ mt: 2 }}>
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="WebDAV URL"
                    value={settings.webdavUrl}
                    onChange={(e) => handleChange('webdavUrl', e.target.value)}
                    placeholder="http://nas.local:5005"
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="用户名"
                    value={settings.webdavUsername}
                    onChange={(e) => handleChange('webdavUsername', e.target.value)}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    type="password"
                    label="密码"
                    value={settings.webdavPassword}
                    onChange={(e) => handleChange('webdavPassword', e.target.value)}
                  />
                </Grid>
              </Grid>
            ) : (
              <TextField
                fullWidth
                label="本地挂载路径"
                value={settings.localMountPath}
                onChange={(e) => handleChange('localMountPath', e.target.value)}
                sx={{ mt: 2 }}
                helperText="有声读物文件在本地文件系统中的路径"
              />
            )}
          </CardContent>
        </Card>

        {/* Application Settings */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
              <TuneIcon color="primary" />
              <Typography variant="h6">应用设置</Typography>
            </Stack>
            
            <Divider sx={{ my: 2 }} />

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="应用名称"
                  value={settings.appName}
                  onChange={(e) => handleChange('appName', e.target.value)}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  type="number"
                  label="JWT过期时间（分钟）"
                  value={settings.jwtExpiration}
                  onChange={(e) => handleChange('jwtExpiration', parseInt(e.target.value))}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enableDebug}
                      onChange={(e) => handleChange('enableDebug', e.target.checked)}
                    />
                  }
                  label="启用调试模式"
                />
              </Grid>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enableCors}
                      onChange={(e) => handleChange('enableCors', e.target.checked)}
                    />
                  }
                  label="启用CORS"
                />
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Security Settings */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
              <SecurityIcon color="primary" />
              <Typography variant="h6">安全设置</Typography>
            </Stack>
            
            <Divider sx={{ my: 2 }} />

            <Grid container spacing={2}>
              <Grid item xs={12}>
                <FormControlLabel
                  control={
                    <Switch
                      checked={settings.enableRateLimit}
                      onChange={(e) => handleChange('enableRateLimit', e.target.checked)}
                    />
                  }
                  label="启用API速率限制"
                />
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Info Card */}
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Stack direction="row" alignItems="center" spacing={1} sx={{ mb: 2 }}>
              <InfoIcon color="primary" />
              <Typography variant="h6">系统信息</Typography>
            </Stack>
            
            <Divider sx={{ my: 2 }} />

            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  版本
                </Typography>
                <Typography variant="body1">0.1.0</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  环境
                </Typography>
                <Typography variant="body1">Development</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  数据库
                </Typography>
                <Typography variant="body1">SQLite</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2" color="text.secondary">
                  框架
                </Typography>
                <Typography variant="body1">FastAPI + React</Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        {/* Action Buttons */}
        <Stack direction="row" spacing={2}>
          <Button
            variant="contained"
            startIcon={<SaveIcon />}
            onClick={handleSave}
          >
            保存设置
          </Button>
          <Button
            variant="outlined"
            startIcon={<RefreshIcon />}
            onClick={() => window.location.reload()}
          >
            重置
          </Button>
        </Stack>
      </Box>
    </Layout>
  );
};

export default Settings;
