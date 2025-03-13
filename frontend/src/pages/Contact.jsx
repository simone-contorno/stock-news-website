import React from 'react'
import { Container, Typography, Paper, Box, Link } from '@mui/material'
import EmailIcon from '@mui/icons-material/Email'

const Contact = () => {
  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper
        elevation={0}
        sx={{
          p: 4,
          borderRadius: 2,
          backgroundColor: 'background.paper',
          transition: 'box-shadow 0.3s ease-in-out',
          '&:hover': {
            boxShadow: '0 4px 20px 0 rgba(0,0,0,0.1)'
          }
        }}
      >
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 600 }}>
          Contact
        </Typography>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mt: 3 }}>
          <EmailIcon color="primary" />
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
      </Paper>
    </Container>
  )
}

export default Contact