import React from 'react'
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button } from '@mui/material'

type Props = {
  open: boolean
  onClose: () => void
  onConfirm: () => void
  title?: string
  content?: string
}

export const UserDeleteDialog: React.FC<Props> = ({ open, onClose, onConfirm, title = 'Delete user', content = 'Are you sure you want to delete this user?' }) => {
  return (
    <Dialog open={open} onClose={onClose} aria-labelledby="delete-user-dialog-title">
      <DialogTitle id="delete-user-dialog-title">{title}</DialogTitle>
      <DialogContent>
        <DialogContentText>{content}</DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={onConfirm} color="error" variant="contained">Delete</Button>
      </DialogActions>
    </Dialog>
  )
}

export default UserDeleteDialog
