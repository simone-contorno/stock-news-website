import React from 'react'
import { Box, Typography, Link, Card, CardContent, Grid, Alert, Fade, CircularProgress } from '@mui/material'
import { Article as ArticleIcon } from '@mui/icons-material'

const NewsSection = ({ news = [], selectedDate, warning, isLoading }) => {
  const newsArray = Array.isArray(news) ? news : []
  const filteredNews = selectedDate
    ? newsArray.filter(article => {
        const articleDate = new Date(article.published_at)
        articleDate.setHours(0, 0, 0, 0)
        return articleDate.getTime() === selectedDate.getTime()
      })
    : newsArray

  return (
    <Box mt={4}>
      <Typography
        variant="h5"
        gutterBottom
        sx={{
          fontWeight: 600,
          color: 'text.primary',
          mb: 3,
          display: 'flex',
          alignItems: 'center',
          gap: 1
        }}
      >
        <ArticleIcon sx={{ color: 'primary.main' }} />
        {selectedDate
          ? `News for ${selectedDate.toLocaleDateString()}`
          : 'Latest News'}
      </Typography>

      {warning && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          {warning}
        </Alert>
      )}

      {isLoading ? (
        <Box display="flex" justifyContent="center" p={4}>
          <CircularProgress />
        </Box>
      ) : (!filteredNews || filteredNews.length === 0) ? (
        <Alert severity="info">
          {selectedDate
            ? `No news articles available for ${selectedDate.toLocaleDateString()}`
            : 'No news articles available'}
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {filteredNews.map((article, index) => (
            <Grid item xs={12} key={index}>
              <Fade in={true} timeout={300 + index * 100}>
                <Card
                  sx={{
                    transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: '0 4px 20px 0 rgba(0,0,0,0.1)'
                    }
                  }}
                >
                  <CardContent>
                    <Typography
                      variant="h6"
                      gutterBottom
                      sx={{
                        fontWeight: 500,
                        lineHeight: 1.4
                      }}
                    >
                      <Link
                        href={article.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        sx={{
                          color: 'primary.main',
                          textDecoration: 'none',
                          transition: 'color 0.2s ease-in-out',
                          '&:hover': {
                            color: 'primary.dark'
                          }
                        }}
                      >
                        {article.title}
                      </Link>
                    </Typography>
                    <Typography
                      variant="body2"
                      sx={{
                        color: 'text.secondary',
                        mb: 1.5,
                        display: 'flex',
                        alignItems: 'center',
                        gap: 1
                      }}
                    >
                      {article.source} • {new Date(article.published_at).toLocaleDateString()}
                    </Typography>
                    <Typography
                      variant="body1"
                      sx={{
                        color: 'text.primary',
                        lineHeight: 1.6
                      }}
                    >
                      {article.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Fade>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  )
}

export default NewsSection