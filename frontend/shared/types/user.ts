export type UserRole = 'admin' | 'user'
export type UserStatus = 'active' | 'inactive' | 'blocked'

export interface User {
  id: string
  username: string
  email: string
  role: UserRole
  status: UserStatus
  createdAt: string
}

export interface UserCreate {
  username: string
  email: string
  password: string
  role: UserRole
}

export interface UserUpdate {
  username?: string
  email?: string
  role?: UserRole
  status?: UserStatus
}

export interface UserDetail extends User {
  // Optional additional fields for detail view
  playbackHistory?: any[]
  timeLimits?: any
}
