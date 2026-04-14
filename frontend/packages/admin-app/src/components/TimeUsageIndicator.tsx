import React from "react";
import { Box, Typography, LinearProgress } from "@mui/material";

type Props = {
  label: string;
  used: number;
  limit: number;
};

const TimeUsageIndicator: React.FC<Props> = ({ label, used, limit }) => {
  const percent = limit > 0 ? Math.min(100, (used / limit) * 100) : 0;
  const warn = percent > 90;
  return (
    <Box my={1}>
      <Box display="flex" justifyContent="space-between" mb={0.5}>
        <Typography variant="body2">{label}</Typography>
        <Typography variant="caption" color={warn ? "error" : "text.secondary"}>{used} / {limit} mins</Typography>
      </Box>
      <LinearProgress variant="determinate" value={percent} sx={{ height: 6, borderRadius: 3, backgroundColor: '#eee', '& .MuiLinearProgress-bar': { backgroundColor: warn ? '#e57373' : '#3f51b5' } }} />
    </Box>
  );
};

export default TimeUsageIndicator;
