import React from 'react'
import { Box, Button, Stack } from '@mui/material'

type Props = {
  onView?: () => void
  onEdit?: () => void
  onDelete?: () => void
}

export const UserActions: React.FC<Props> = ({ onView, onEdit, onDelete }) => {
  return (
    <Stack direction="row" spacing={1}>
      <Button size="small" variant="outlined" onClick={onView}>View</Button>
      <Button size="small" variant="outlined" onClick={onEdit}>Edit</Button>
      <Button size="small" color="error" variant="outlined" onClick={onDelete}>Delete</Button>
    </Stack>
  )
}

export default UserActions
