import React from 'react'
import { Box, Typography, Link as MuiLink } from '@mui/material'

export function Footer() {
  const year = new Date().getFullYear()
  return (
    <Box component="footer" sx={{ py: 3, px: 2, mt: 'auto', bgcolor: 'background.paper', borderTop: '1px solid', borderColor: 'divider' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="caption" color="text.secondary">
          © {year} AudioBook. All rights reserved.
        </Typography>
        <Box>
          <MuiLink href="#" color="inherit" sx={{ mx: 1, textDecoration: 'none' }}>Privacy</MuiLink>
          <MuiLink href="#" color="inherit" sx={{ mx: 1, textDecoration: 'none' }}>Terms</MuiLink>
        </Box>
      </Box>
    </Box>
  )
}

export default Footer
