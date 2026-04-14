import React from "react";
import { Box, Typography } from "@mui/material";
import Layout from "../../shared/components/Layout";
import LimitsDisplay from "../../components/LimitsDisplay";
import LimitsForm from "../../components/LimitsForm";
import { useUserLimits } from "../../hooks/useLimits";
import { useParams } from "react-router-dom";

const UserLimits: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const { limits, loading, error, updateUser, resetUser } = useUserLimits(userId!);

  const initial = {
    dailyLimitMinutes: limits?.dailyLimitMinutes ?? 0,
    weeklyLimitMinutes: limits?.weeklyLimitMinutes ?? 0,
    monthlyLimitMinutes: limits?.monthlyLimitMinutes ?? 0,
  } as any;

  const handleSubmit = async (payload: { dailyLimitMinutes: number; weeklyLimitMinutes: number; monthlyLimitMinutes: number }) => {
    await updateUser({ dailyLimitMinutes: payload.dailyLimitMinutes, weeklyLimitMinutes: payload.weeklyLimitMinutes, monthlyLimitMinutes: payload.monthlyLimitMinutes });
  };

  return (
    <Layout title={`User Limits`}>
      <Box sx={{ p: 2 }}>
        <Typography variant="h4" gutterBottom>User Limits</Typography>
        {loading && <Typography>Loading…</Typography>}
        {!loading && limits && (
          <LimitsDisplay
            dailyLimitMinutes={limits.dailyLimitMinutes ?? 0}
            weeklyLimitMinutes={limits.weeklyLimitMinutes ?? 0}
            monthlyLimitMinutes={limits.monthlyLimitMinutes ?? 0}
            dailyUsage={limits.dailyUsage}
            weeklyUsage={limits.weeklyUsage}
            monthlyUsage={limits.monthlyUsage}
          />
        )}
        {error && <Typography color="error">{error}</Typography>}
        <LimitsForm initial={initial} onSubmit={handleSubmit} loading={loading} />
        <Box mt={2}>
          <Typography variant="body2">Reset to global defaults: use the reset button below.</Typography>
          <button onClick={async () => await resetUser()} style={{ padding: "8px 12px", marginTop: 8 }}>Reset to Global Defaults</button>
        </Box>
      </Box>
    </Layout>
  );
};

export default UserLimits;
