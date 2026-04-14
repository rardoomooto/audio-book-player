import React from 'react'
import { Box, Typography } from '@mui/material'

type Props = {
  children: React.ReactNode
}

type State = {
  hasError: boolean
  error?: Error
}

export class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    // Could log to an external service here
    console.error('ErrorBoundary caught an error', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <Box sx={{ p: 4 }}>
          <Typography variant="h6" color="error">Something went wrong.</Typography>
          <Typography variant="body2" color="textSecondary">We encountered an unexpected error. Please try again later.</Typography>
        </Box>
      )
    }
    return this.props.children
  }
}

export default ErrorBoundary
