import React from 'react'
import { CircularProgress, Box } from '@mui/material'

export function LoadingSpinner() {
  return (
    <Box display="flex" alignItems="center" justifyContent="center" minHeight="100px">
      <CircularProgress />
    </Box>
  )
}

export default LoadingSpinner
