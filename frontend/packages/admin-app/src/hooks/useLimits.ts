import { useEffect, useState } from "react";

export type GlobalLimits = {
  dailyLimitMinutes: number;
  weeklyLimitMinutes: number;
  monthlyLimitMinutes: number;
  // Optional usage fields to support progress display if API provides them
  dailyUsage?: number;
  weeklyUsage?: number;
  monthlyUsage?: number;
};

export type UserLimits = {
  dailyLimitMinutes?: number;
  weeklyLimitMinutes?: number;
  monthlyLimitMinutes?: number;
  dailyUsage?: number;
  weeklyUsage?: number;
  monthlyUsage?: number;
};

export const useLimits = () => {
  const [globalLimits, setGlobalLimits] = useState<GlobalLimits | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchGlobal = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/limits/global", {
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error("Failed to fetch global limits");
      const data: any = await res.json();
      const limits: GlobalLimits = {
        dailyLimitMinutes:
          data?.dailyLimitMinutes ?? data?.daily ?? 0,
        weeklyLimitMinutes:
          data?.weeklyLimitMinutes ?? data?.weekly ?? 0,
        monthlyLimitMinutes:
          data?.monthlyLimitMinutes ?? data?.monthly ?? 0,
        dailyUsage: data?.dailyUsage ?? data?.daily_usage ?? undefined,
        weeklyUsage: data?.weeklyUsage ?? data?.weekly_usage ?? undefined,
        monthlyUsage: data?.monthlyUsage ?? data?.monthly_usage ?? undefined,
      };
      setGlobalLimits(limits);
    } catch (e: any) {
      setError(e?.message ?? String(e));
    } finally {
      setLoading(false);
    }
  };

  const updateGlobal = async (payload: GlobalLimits) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/limits/global", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          dailyLimitMinutes: payload.dailyLimitMinutes,
          weeklyLimitMinutes: payload.weeklyLimitMinutes,
          monthlyLimitMinutes: payload.monthlyLimitMinutes,
        }),
      });
      if (!res.ok) throw new Error("Failed to update global limits");
      const data: any = await res.json();
      const limits: GlobalLimits = {
        dailyLimitMinutes:
          data?.dailyLimitMinutes ?? data?.daily ?? payload.dailyLimitMinutes ?? 0,
        weeklyLimitMinutes:
          data?.weeklyLimitMinutes ?? data?.weekly ?? payload.weeklyLimitMinutes ?? 0,
        monthlyLimitMinutes:
          data?.monthlyLimitMinutes ?? data?.monthly ?? payload.monthlyLimitMinutes ?? 0,
        dailyUsage: data?.dailyUsage ?? data?.daily_usage ?? undefined,
        weeklyUsage: data?.weeklyUsage ?? data?.weekly_usage ?? undefined,
        monthlyUsage: data?.monthlyUsage ?? data?.monthly_usage ?? undefined,
      };
      setGlobalLimits(limits);
      return limits;
    } catch (e: any) {
      setError(e?.message ?? String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchGlobal();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    globalLimits,
    loading,
    error,
    fetchGlobal,
    updateGlobal,
  };
};

export const useUserLimits = (userId: string) => {
  const [limits, setLimits] = useState<UserLimits | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchUser = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/v1/limits/users/${userId}`, {
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error("Failed to fetch user limits");
      const data: any = await res.json();
      const u: UserLimits = {
        dailyLimitMinutes: data?.dailyLimitMinutes ?? data?.daily ?? undefined,
        weeklyLimitMinutes: data?.weeklyLimitMinutes ?? data?.weekly ?? undefined,
        monthlyLimitMinutes: data?.monthlyLimitMinutes ?? data?.monthly ?? undefined,
        dailyUsage: data?.dailyUsage ?? data?.daily_usage ?? undefined,
        weeklyUsage: data?.weeklyUsage ?? data?.weekly_usage ?? undefined,
        monthlyUsage: data?.monthlyUsage ?? data?.monthly_usage ?? undefined,
      };
      setLimits(u);
    } catch (e: any) {
      setError(e?.message ?? String(e));
    } finally {
      setLoading(false);
    }
  };

  const updateUser = async (payload: UserLimits) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/v1/limits/users/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("Failed to update user limits");
      const data: any = await res.json();
      const updated: UserLimits = {
        dailyLimitMinutes: data?.dailyLimitMinutes ?? data?.daily ?? payload.dailyLimitMinutes,
        weeklyLimitMinutes: data?.weeklyLimitMinutes ?? data?.weekly ?? payload.weeklyLimitMinutes,
        monthlyLimitMinutes: data?.monthlyLimitMinutes ?? data?.monthly ?? payload.monthlyLimitMinutes,
        dailyUsage: data?.dailyUsage ?? data?.daily_usage ?? payload.dailyUsage ?? undefined,
        weeklyUsage: data?.weeklyUsage ?? data?.weekly_usage ?? payload.weeklyUsage ?? undefined,
        monthlyUsage: data?.monthlyUsage ?? data?.monthly_usage ?? payload.monthlyUsage ?? undefined,
      };
      setLimits(updated);
      return updated;
    } catch (e: any) {
      setError(e?.message ?? String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  const resetUser = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/v1/limits/users/${userId}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to reset user limits");
      const data: any = await res.json();
      const reset: UserLimits = {
        dailyLimitMinutes: data?.dailyLimitMinutes ?? undefined,
        weeklyLimitMinutes: data?.weeklyLimitMinutes ?? undefined,
        monthlyLimitMinutes: data?.monthlyLimitMinutes ?? undefined,
      };
      setLimits(reset);
      return reset;
    } catch (e: any) {
      setError(e?.message ?? String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  return {
    limits,
    loading,
    error,
    fetchUser,
    updateUser,
    resetUser,
  };
};
