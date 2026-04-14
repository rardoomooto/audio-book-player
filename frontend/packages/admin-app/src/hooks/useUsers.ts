import { useEffect, useState, useCallback } from 'react'
import { User } from '../../shared/types/user'
import { listUsers, getUser, createUser, updateUser, deleteUser, changePassword, updateStatus } from '../../shared/api-client/users'

type SortDir = 'asc' | 'desc'

export function useUsers() {
  const [data, setData] = useState<{ users: User[]; total: number }>({ users: [], total: 0 })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchUsers = useCallback(async (params?: { page?: number; limit?: number; search?: string; role?: string; status?: string; sortBy?: string; sortDir?: SortDir }) => {
    setLoading(true)
    setError(null)
    try {
      const res = await listUsers(params as any)
      // Normalize to { users, total }
      const users = (res?.data ?? []) as User[]
      const total = (res?.total ?? users.length) as number
      setData({ users, total })
    } catch (err: any) {
      setError(err?.message ?? 'Failed to load users')
    } finally {
      setLoading(false)
    }
  }, [])

  const getUserById = useCallback(async (id: string) => {
    try {
      const user = await getUser(id)
      return user
    } catch (e) {
      throw e
    }
  }, [])

  const createNewUser = useCallback(async (payload: any) => {
    try {
      const user = await createUser(payload)
      return user
    } catch (e) {
      throw e
    }
  }, [])

  const updateExistingUser = useCallback(async (id: string, payload: any) => {
    try {
      const user = await updateUser(id, payload)
      return user
    } catch (e) {
      throw e
    }
  }, [])

  const deleteExistingUser = useCallback(async (id: string) => {
    await deleteUser(id)
  }, [])

  const changeUserPassword = useCallback(async (id: string, password: string) => {
    await changePassword(id, password)
  }, [])

  const setUserStatus = useCallback(async (id: string, status: string) => {
    await updateStatus(id, status)
  }, [])

  return {
    data,
    loading,
    error,
    fetchUsers,
    getUserById,
    createNewUser,
    updateExistingUser,
    deleteExistingUser,
    changeUserPassword,
    setUserStatus,
  }
}
