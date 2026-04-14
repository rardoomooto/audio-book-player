export interface Permission {
  id: string;
  name: string;
  description?: string;
}

export interface UserPermissionAssignment {
  userId: string;
  permissionId: string;
  name?: string;
}

export interface GlobalLimits {
  dailyMinutes?: number; // daily limit in minutes
  weeklyMinutes?: number; // weekly limit in minutes
  monthlyMinutes?: number; // monthly limit in minutes
  // Optional usage fields if backend provides them
  usageTodayMinutes?: number;
  usageThisWeekMinutes?: number;
  usageThisMonthMinutes?: number;
}

export interface UserLimits {
  userId: string;
  dailyMinutes?: number;
  weeklyMinutes?: number;
  monthlyMinutes?: number;
  usageTodayMinutes?: number;
  usageThisWeekMinutes?: number;
  usageThisMonthMinutes?: number;
}
