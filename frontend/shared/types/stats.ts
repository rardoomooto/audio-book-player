export type TimePeriod = 'daily' | 'weekly' | 'monthly' | 'yearly';

export interface UserSummary {
  userId: string;
  name: string;
  playtime: number; // seconds
  sessions: number;
}

export interface ContentSummary {
  contentId: string;
  title: string;
  playCount: number;
  totalTime: number; // seconds
}

export interface DashboardStats {
  totalUsers: number;
  totalContent: number;
  totalPlaytime: number; // seconds
  activeUsersToday?: number;
  activeUsersThisWeek?: number;
  activeUsersThisMonth?: number;
  averageSessionDuration?: number; // seconds
  topUsers: UserSummary[];
  topContents: ContentSummary[];
  recentActivity: Array<{ id: string; user: string; type: string; timestamp: string; details?: string }>;
  userDistribution?: Array<{ label: string; value: number; color?: string }>;
  userActivitySeries?: Array<{ date: string; activeUsers: number }>;
  playtimeTrend?: Array<{ date: string; totalPlaytime: number }>;
}
