import React from 'react'
import { Box, TextField, FormControl, InputLabel, Select, MenuItem, Button, FormHelperText, Stack } from '@mui/material'
import { UserCreate, UserUpdate, User } from '../../shared/types/user'

type Props = {
  initial?: Partial<User>
  onSubmit: (payload: any) => void
  onCancel?: () => void
  isEdit?: boolean
  passwordField?: boolean
}

export const UserForm: React.FC<Props> = ({ initial = {}, onSubmit, onCancel, isEdit }) => {
  const [username, setUsername] = React.useState<string>(initial.username ?? '')
  const [email, setEmail] = React.useState<string>(initial.email ?? '')
  const [password, setPassword] = React.useState<string>('')
  const [role, setRole] = React.useState<string>(initial.role ?? 'user')
  const [touched, setTouched] = React.useState<boolean>(false)

  const validate = (): string | null => {
    if (!username) return 'Username is required'
    if (!email) return 'Email is required'
    // basic email check
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return 'Email is invalid'
    if (!isEdit && password?.length < 6) return 'Password must be at least 6 characters'
    return null
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setTouched(true)
    const err = validate()
    if (err) return
    const payload: any = { username, email, role }
    if (!isEdit && password) payload.password = password
    onSubmit(payload)
  }

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2, width: '100%', maxWidth: 600 }}>
      <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} required fullWidth />
      <TextField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} required fullWidth />
      {!isEdit && (
        <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} required fullWidth helperText="Minimum 6 characters" />
      )}
      <FormControl fullWidth>
        <InputLabel id="role-label">Role</InputLabel>
        <Select labelId="role-label" value={role} onChange={(e) => setRole(e.target.value)} label="Role">
          <MenuItem value="user">User</MenuItem>
          <MenuItem value="admin">Admin</MenuItem>
        </Select>
      </FormControl>
      {touched && validate() && (
        <FormHelperText error>{validate()}</FormHelperText>
      )}
      <Stack direction="row" spacing={2} sx={{ mt: 1 }}>
        <Button variant="contained" color="primary" type="submit">Save</Button>
        <Button variant="outlined" onClick={onCancel}>Cancel</Button>
      </Stack>
    </Box>
  )
}

export default UserForm
