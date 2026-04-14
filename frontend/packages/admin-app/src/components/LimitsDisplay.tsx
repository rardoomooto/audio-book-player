import React from "react";
import { Box, Typography, LinearProgress, Card, CardContent, Grid } from "@mui/material";

type Props = {
  dailyLimitMinutes: number;
  weeklyLimitMinutes: number;
  monthlyLimitMinutes: number;
  dailyUsage?: number;
  weeklyUsage?: number;
  monthlyUsage?: number;
};

const format = (m: number) => {
  // Display as hours:minutes or just minutes if small
  const hours = Math.floor(m / 60);
  const mins = m % 60;
  if (hours > 0) return `${hours}h ${mins}m`;
  return `${mins}m`;
};

export const TimeBar: React.FC<{ label: string; limit: number; usage?: number }>=({label, limit, usage})=>{
  const value = limit > 0 ? Math.min(100, ((usage ?? 0) / limit) * 100) : 0;
  const warn = value >= 90;
  return (
    <Box sx={{ my: 1 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={0.5}>
        <Typography variant="body2" color={warn ? "error" : "text.primary"}>{label}</Typography>
        <Typography variant="caption" color="text.secondary">{usage ?? 0} / {limit} mins</Typography>
      </Box>
      <LinearProgress variant="determinate" value={value} sx={{ height: 8, borderRadius: 5, backgroundColor: '#eee', '& .MuiLinearProgress-bar': { backgroundColor: warn ? '#e57373' : '#3f51b5' } }} />
    </Box>
  );
};

const LimitsDisplay: React.FC<Props> = ({ dailyLimitMinutes, weeklyLimitMinutes, monthlyLimitMinutes, dailyUsage, weeklyUsage, monthlyUsage }) => {
  return (
    <Card variant="outlined" sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Global Playback Limits</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={4}>
            <TimeBar label="Daily" limit={dailyLimitMinutes} usage={dailyUsage} />
          </Grid>
          <Grid item xs={12} md={4}>
            <TimeBar label="Weekly" limit={weeklyLimitMinutes} usage={weeklyUsage} />
          </Grid>
          <Grid item xs={12} md={4}>
            <TimeBar label="Monthly" limit={monthlyLimitMinutes} usage={monthlyUsage} />
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default LimitsDisplay;
