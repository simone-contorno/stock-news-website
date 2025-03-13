import React, { useState } from 'react'
import { Link as RouterLink } from 'react-router-dom'
import { AppBar, Toolbar, Typography, Link, Box, Container, IconButton, Menu, MenuItem, useTheme, useMediaQuery } from '@mui/material'
import ShowChartIcon from '@mui/icons-material/ShowChart'
import MenuIcon from '@mui/icons-material/Menu'

const Navbar = () => {
  const [anchorEl, setAnchorEl] = useState(null)
  const theme = useTheme()
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'))

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  const navItems = [
    { text: 'Home', path: '/' },
    { text: 'Indices', path: '/indices' },
    { text: 'Contact', path: '/contact' }
  ]

  return (
    <AppBar
      position="sticky"
      elevation={0}
      sx={{
        backgroundColor: 'background.paper',
        borderBottom: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters sx={{ height: 64, justifyContent: 'space-between' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <ShowChartIcon
              sx={{
                mr: 1,
                color: 'primary.main',
                fontSize: 32,
                transition: 'transform 0.2s ease-in-out',
                '&:hover': { transform: 'scale(1.1)' },
              }}
            />
            <Typography
              variant="h6"
              component="div"
              sx={{
                fontWeight: 600,
                letterSpacing: '-0.5px',
              }}
            >
              <Link
                component={RouterLink}
                to="/"
                sx={{
                  textDecoration: 'none',
                  color: 'primary.main',
                  transition: 'color 0.2s ease-in-out',
                  '&:hover': { color: 'primary.dark' },
                }}
              >
                Stock News
              </Link>
            </Typography>
          </Box>

          {isMobile ? (
            <Box>
              <IconButton
                size="large"
                edge="end"
                color="primary"
                aria-label="menu"
                onClick={handleMenu}
              >
                <MenuIcon />
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                {navItems.map((item) => (
                  <MenuItem
                    key={item.text}
                    onClick={handleClose}
                    component={RouterLink}
                    to={item.path}
                  >
                    {item.text}
                  </MenuItem>
                ))}
              </Menu>
            </Box>
          ) : (
            <Box sx={{ display: 'flex', gap: 4 }}>
              {navItems.map((item) => (
                <Link
                  key={item.text}
                  component={RouterLink}
                  to={item.path}
                  sx={{
                    textDecoration: 'none',
                    color: 'text.primary',
                    fontWeight: 500,
                    transition: 'color 0.2s ease-in-out',
                    '&:hover': { color: 'primary.main' },
                  }}
                >
                  {item.text}
                </Link>
              ))}
            </Box>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  )
}

export default Navbar