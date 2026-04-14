import React from 'react'
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TableSortLabel, TextField, Box, Chip, IconButton } from '@mui/material'
import { User } from '../../shared/types/user'
import { Edit, Visibility, Delete } from '@mui/icons-material'

type Props = {
  users: User[]
  onView?: (id: string) => void
  onEdit?: (id: string) => void
  onDelete?: (id: string) => void
  sortBy?: string
  sortDir?: 'asc' | 'desc'
  onSort?: (property: string) => void
}

export const UserTable: React.FC<Props> = ({ users, onView, onEdit, onDelete, sortBy, sortDir, onSort }) => {
  const createSortHandler = (property: string) => () => {
    onSort?.(property)
  }

  return (
    <TableContainer component={Paper}>
      <Table aria-label="Users table">
        <TableHead>
          <TableRow>
            <TableCell sortDirection={sortBy === 'username' ? sortDir : false}>
              <TableSortLabel active={sortBy === 'username'} direction={sortDir ?? 'asc'} onClick={createSortHandler('username')}>
                Username
              </TableSortLabel>
            </TableCell>
            <TableCell> Email </TableCell>
            <TableCell sortDirection={sortBy === 'role' ? sortDir : false}>
              <TableSortLabel active={sortBy === 'role'} direction={sortDir ?? 'asc'} onClick={createSortHandler('role')}>
                Role
              </TableSortLabel>
            </TableCell>
            <TableCell sortDirection={sortBy === 'status' ? sortDir : false}>
              <TableSortLabel active={sortBy === 'status'} direction={sortDir ?? 'asc'} onClick={createSortHandler('status')}>
                Status
              </TableSortLabel>
            </TableCell>
            <TableCell sortDirection={sortBy === 'createdAt' ? sortDir : false}>
              <TableSortLabel active={sortBy === 'createdAt'} direction={sortDir ?? 'asc'} onClick={createSortHandler('createdAt')}>
                Created
              </TableSortLabel>
            </TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {users.map((u) => (
            <TableRow key={u.id} hover>
              <TableCell component="th" scope="row">{u.username}</TableCell>
              <TableCell>{u.email}</TableCell>
              <TableCell>
                <Chip label={u.role} size="small" color={u.role === 'admin' ? 'primary' : 'default'} />
              </TableCell>
              <TableCell>
                <Chip label={u.status} size="small" color={u.status === 'active' ? 'success' : u.status === 'inactive' ? 'warning' : 'default'} />
              </TableCell>
              <TableCell>{new Date(u.createdAt).toLocaleDateString()}</TableCell>
              <TableCell>
                <IconButton aria-label="view" onClick={() => onView?.(u.id)}><Visibility /></IconButton>
                <IconButton aria-label="edit" onClick={() => onEdit?.(u.id)}><Edit /></IconButton>
                <IconButton aria-label="delete" onClick={() => onDelete?.(u.id)}><Delete /></IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}

export default UserTable
