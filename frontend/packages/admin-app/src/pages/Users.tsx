import React, { useEffect, useMemo, useState } from 'react'
import { Box, TextField, Select, MenuItem, InputLabel, FormControl, Paper, Typography, CircularProgress, Grid, Button } from '@mui/material'
import { Layout } from '../../../shared/components/Layout'
import { UserTable } from '../components/UserTable'
import { User } from '../../shared/types/user'
import { useUsers } from '../hooks/useUsers'
import { Outlet, Link } from 'react-router-dom'
import { UserDeleteDialog } from '../components/UserDeleteDialog'

type Props = {}

export const UsersPage: React.FC<Props> = () => {
  const { data, loading, error, fetchUsers, deleteExistingUser } = useUsers()
  const [deleteId, setDeleteId] = useState<string | null>(null)
  const [deleteOpen, setDeleteOpen] = useState(false)
  const [page, setPage] = useState(0)
  const [limit, setLimit] = useState(10)
  const [search, setSearch] = useState('')
  const [role, setRole] = useState<string>('')
  const [sortBy, setSortBy] = useState<string>('createdAt')
  const [sortDir, setSortDir] = useState<'asc'|'desc'>('desc')
  const total = data.total
  const users = data.users

  useEffect(() => {
    fetchUsers({ page: page + 1, limit, search, role, sortBy, sortDir })
  }, [page, limit, search, role, sortBy, sortDir])

  const onSort = (property: string) => {
    const dir = sortBy === property && sortDir === 'asc' ? 'desc' : 'asc'
    setSortBy(property)
    setSortDir(dir)
  }

  const handleDelete = (id: string) => {
    setDeleteId(id)
    setDeleteOpen(true)
  }

  const confirmDelete = async () => {
    if (!deleteId) return
    try {
      await deleteExistingUser(deleteId)
      setDeleteOpen(false)
      setDeleteId(null)
      fetchUsers({ page: page + 1, limit, search, role, sortBy, sortDir })
    } catch (e) {
      // handle error
      setDeleteOpen(false)
      setDeleteId(null)
    }
  }

  return (
    <Layout>
      <Typography variant="h4" gutterBottom>Users</Typography>
      <Box sx={{ display: 'flex', gap: 2, mb: 2, flexWrap: 'wrap' }}>
        <TextField placeholder="Search users" value={search} onChange={(e) => setSearch(e.target.value)} size="small" />
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel id="role-filter-label">Role</InputLabel>
          <Select labelId="role-filter-label" value={role} label="Role" onChange={(e) => setRole(e.target.value)}>
            <MenuItem value="">All</MenuItem>
            <MenuItem value="admin">Admin</MenuItem>
            <MenuItem value="user">User</MenuItem>
          </Select>
        </FormControl>
        <Button variant="contained" size="small" component={Link} to="new">New User</Button>
      </Box>

      <Paper elevation={1} sx={{ p: 2 }}>
        {loading ? (
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Box sx={{ p: 2, color: 'red' }}>{error}</Box>
        ) : (
          <UserTable
            users={users}
            onView={(id) => { /* navigate to detail if needed */ }}
            onEdit={(id) => { /* navigate to edit page if needed */ }}
            onDelete={(id) => handleDelete(id)}
          />
        )}
      </Paper>
      <UserDeleteDialog
        open={deleteOpen}
        onClose={() => setDeleteOpen(false)}
        onConfirm={confirmDelete}
        content={deleteId ? `Delete user ${deleteId}? This action cannot be undone.` : undefined}
      />
      <Box sx={{ mt: 2, display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="caption">Showing {Math.min((page + 1) * limit, total)} of {total} users</Typography>
        <Box>
          <Select size="small" value={limit} onChange={(e) => setLimit(parseInt(e.target.value as string, 10))}>
            <MenuItem value={5}>5</MenuItem>
            <MenuItem value={10}>10</MenuItem>
            <MenuItem value={25}>25</MenuItem>
          </Select>
        </Box>
      </Box>
    </Layout>
  )
}

export default UsersPage
