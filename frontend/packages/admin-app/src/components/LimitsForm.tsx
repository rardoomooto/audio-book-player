import React, { useState } from "react";
import { Box, Button, Card, CardContent, Grid, TextField, Typography } from "@mui/material";
import { GlobalLimits } from "../hooks/useLimits";

type Props = {
  initial?: GlobalLimits;
  onSubmit: (payload: GlobalLimits) => void | Promise<void>;
  loading?: boolean;
};

const LimitsForm: React.FC<Props> = ({ initial, onSubmit, loading }) => {
  const [daily, setDaily] = useState<number>(initial?.dailyLimitMinutes ?? 0);
  const [weekly, setWeekly] = useState<number>(initial?.weeklyLimitMinutes ?? 0);
  const [monthly, setMonthly] = useState<number>(initial?.monthlyLimitMinutes ?? 0);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit({ dailyLimitMinutes: daily, weeklyLimitMinutes: weekly, monthlyLimitMinutes: monthly });
  };

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Update Global Limits</Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={4}>
              <TextField
                label="Daily (mins)"
                type="number"
                fullWidth
                value={daily}
                onChange={(e) => setDaily(Number(e.target.value))}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                label="Weekly (mins)"
                type="number"
                fullWidth
                value={weekly}
                onChange={(e) => setWeekly(Number(e.target.value))}
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <TextField
                label="Monthly (mins)"
                type="number"
                fullWidth
                value={monthly}
                onChange={(e) => setMonthly(Number(e.target.value))}
              />
            </Grid>
          </Grid>
          <Box display="flex" justifyContent="flex-end" mt={2}>
            <Button type="submit" variant="contained" color="primary" disabled={loading}>
              Save
            </Button>
          </Box>
        </form>
      </CardContent>
    </Card>
  );
};

export default LimitsForm;
