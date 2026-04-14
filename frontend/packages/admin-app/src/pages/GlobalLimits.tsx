import React, { useMemo } from "react";
import { Box, CardContent, Typography } from "@mui/material";
import Layout from "../../shared/components/Layout";
import LimitsDisplay from "../../components/LimitsDisplay";
import LimitsForm from "../../components/LimitsForm";
import { useLimits } from "../../hooks/useLimits";

const GlobalLimits: React.FC = () => {
  const { globalLimits, loading, error, updateGlobal } = useLimits();

  // Normalize initial for the form
  const initial = useMemo(() => {
    if (!globalLimits) return undefined;
    return {
      dailyLimitMinutes: globalLimits.dailyLimitMinutes,
      weeklyLimitMinutes: globalLimits.weeklyLimitMinutes,
      monthlyLimitMinutes: globalLimits.monthlyLimitMinutes,
    } as any;
  }, [globalLimits]);

  const handleSubmit = async (payload: { dailyLimitMinutes: number; weeklyLimitMinutes: number; monthlyLimitMinutes: number }) => {
    await updateGlobal(payload as any);
  };

  return (
    <Layout title="Global Time Limits">
      <Box sx={{ p: 2 }}>
        <Typography variant="h4" gutterBottom>Global Time Limits</Typography>
        {loading && <Typography>Loading…</Typography>}
        {!loading && globalLimits && (
          <LimitsDisplay
            dailyLimitMinutes={globalLimits.dailyLimitMinutes}
            weeklyLimitMinutes={globalLimits.weeklyLimitMinutes}
            monthlyLimitMinutes={globalLimits.monthlyLimitMinutes}
            dailyUsage={globalLimits.dailyUsage}
            weeklyUsage={globalLimits.weeklyUsage}
            monthlyUsage={globalLimits.monthlyUsage}
          />
        )}
        {error && <Typography color="error">{error}</Typography>}
        <LimitsForm initial={initial as any} onSubmit={handleSubmit} loading={loading} />
      </Box>
    </Layout>
  );
};

export default GlobalLimits;
