import React from 'react'
import { AppBar, Toolbar, Typography, Button, IconButton, Avatar, Menu, MenuItem, Box, Tooltip } from '@mui/material'
import { Link } from 'react-router-dom'
import { useColorMode } from './ThemeProvider'
import { useAuth } from '../contexts/AuthContext'

export function Header() {
  const { toggleColorMode } = useColorMode()
  const { user, login, logout, isAuthenticated } = useAuth()
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null)
  const [loginOpen, setLoginOpen] = React.useState(false)

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }
  const handleClose = () => {
    setAnchorEl(null)
  }

  const onLoginSubmit = async (username: string, password: string) => {
    await login?.({ username, password } as any)
    setLoginOpen(false)
  }

  return (
    <AppBar position="sticky" color="default" sx={{ bgcolor: 'background.paper', borderBottom: '1px solid', borderColor: 'divider' }}>
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Typography variant="h6" component={Link} to="/" sx={{ textDecoration: 'none', color: 'inherit' }}>
            AudioBook
          </Typography>
          <Box sx={{ ml: 4, display: { xs: 'none', md: 'flex' } }}>
            <Button component={Link} to="/" color="inherit">Home</Button>
            <Button component={Link} to="/library" color="inherit">Library</Button>
            <Button component={Link} to="/content" color="inherit">Content</Button>
          </Box>
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Tooltip title="Toggle theme">
            <IconButton color="inherit" onClick={toggleColorMode} aria-label="toggle theme">
              <span style={{ width: 20, height: 20, display: 'inline-block', borderRadius: 4, background: '#000' }} />
            </IconButton>
          </Tooltip>
          {isAuthenticated ? (
            <div>
              <IconButton onClick={handleMenu} aria-controls="user-menu" aria-haspopup="true" color="inherit">
                <Avatar alt={user?.displayName || 'User'} src={user?.avatarUrl || ''} />
              </IconButton>
              <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleClose}>
                <MenuItem onClick={handleClose} component={Link} to="/profile">Profile</MenuItem>
                <MenuItem onClick={handleClose} component={Link} to="/settings">Settings</MenuItem>
                <MenuItem onClick={() => { handleClose(); logout?.(); }}>Logout</MenuItem>
              </Menu>
            </div>
          ) : (
            <Button color="inherit" onClick={() => setLoginOpen(true)}>Login</Button>
          )}
        </Box>
      </Toolbar>
      {/* Simple login dialog could be wired here if needed */}
    </AppBar>
  )
}

export default Header
