import { apiClient } from './client'
import type { ApiResponse } from '../../types/api'

// Fetch stats for a given period (daily, weekly, monthly, yearly)
export async function fetchStats(
  period: 'daily' | 'weekly' | 'monthly' | 'yearly'
): Promise<any> {
  try {
    const resp = await apiClient.get(`/api/v1/stats/${period}`)
    return resp.data?.data ?? resp.data
  } catch (e) {
    // Propagate as-is for caller to handle
    throw e
  }
}

// Fetch dashboard statistics for admin dashboard (period can be daily|weekly|monthly|yearly)
export async function fetchDashboardStats(period: 'daily' | 'weekly' | 'monthly' | 'yearly' = 'daily'): Promise<any> {
  try {
    const resp = await apiClient.get(`/api/v1/stats/dashboard?period=${period}`)
    return resp.data?.data ?? resp.data
  } catch (e) {
    throw e
  }
}

// Fetch total play time for today (ms)
export async function fetchTodayTime(): Promise<number> {
  try {
    const resp = await apiClient.get('/api/v1/playback/today-time')
    const data = resp.data?.data ?? resp.data
    // Support multiple possible shapes from API
    const ms = (data && (data.todayMs ?? data.playTimeMs ?? data.timeMs ?? data.time)) as any
    if (typeof ms === 'number') return ms
    if (typeof ms === 'string') {
      const parsed = parseInt(ms, 10)
      return isNaN(parsed) ? 0 : parsed
    }
    // Fallback: try to extract from nested structure
    if (typeof data === 'object') {
      const v = (data as any).ms ?? (data as any).durationMs
      if (typeof v === 'number') return v
    }
    return 0
  } catch {
    return 0
  }
}

// Fetch user-specific statistics
export async function fetchUserStats(userId: string): Promise<any> {
  try {
    const resp = await apiClient.get(`/api/v1/stats/users/${userId}`)
    return resp.data?.data ?? resp.data
  } catch (e) {
    throw e
  }
}
