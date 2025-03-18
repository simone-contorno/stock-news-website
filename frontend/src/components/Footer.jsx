import React from 'react'
import { Box, Container, Typography, Link, Divider } from '@mui/material'
import EmailIcon from '@mui/icons-material/Email'

const Footer = () => {
  const currentYear = new Date().getFullYear()

  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        mt: 'auto',
        backgroundColor: 'background.paper',
        borderTop: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'space-between', alignItems: { xs: 'flex-start', sm: 'center' }, gap: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <EmailIcon color="primary" fontSize="small" />
            <Link
              href="mailto:simone.contorno@outlook.it"
              sx={{
                color: 'primary.main',
                textDecoration: 'none',
                '&:hover': {
                  textDecoration: 'underline'
                }
              }}
            >
              simone.contorno@outlook.it
            </Link>
          </Box>
          <Typography variant="body2" color="text.secondary">
            © {currentYear} Stock News Website. Licensed under the{' '}
            <Link
              href="https://opensource.org/licenses/MIT"
              target="_blank"
              rel="noopener noreferrer"
              sx={{
                color: 'primary.main',
                textDecoration: 'none',
                '&:hover': {
                  textDecoration: 'underline'
                }
              }}
            >
              MIT License
            </Link>
          </Typography>
        </Box>
      </Container>
    </Box>
  )
}

export default Footer