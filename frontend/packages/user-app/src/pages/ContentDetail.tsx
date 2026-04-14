import React, { useEffect, useState } from 'react'
import { Box, Container, Typography, Button, Card, CardContent } from '@mui/material'
import { fetchContentById } from '../../shared/api-client/content'
import { useParams, useNavigate } from 'react-router-dom'
import type { ContentItem } from '../../shared/types/content'
import Layout from '../../shared/components/Layout'

const ContentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [content, setContent] = useState<ContentItem | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    setLoading(true)
    fetchContentById(id as string)
      .then((c) => {
        setContent(c as any)
        setError(null)
      })
      .catch((e) => setError((e as Error).message))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return (
    <Box sx={{ py: 4 }}>
      <Typography>Loading...</Typography>
    </Box>
  )
  if (error) return (
    <Box sx={{ py: 4 }}>
      <Typography color="error">Error: {error}</Typography>
    </Box>
  )
  if (!content) return (
    <Box sx={{ py: 4 }}>
      <Typography>No content found.</Typography>
    </Box>
  )

  const c = content as ContentItem & any

  return (
    <Layout>
      <Box>
      <Container maxWidth={false}>
        <Typography variant="h4" gutterBottom>{c.title ?? 'Untitled'}</Typography>
        <Box display="flex" alignItems="center" gap={2} mb={2}>
          <Typography variant="subtitle1">{c.author ?? 'Unknown author'}</Typography>
          {typeof c.duration === 'number' && (
            <Typography variant="subtitle2" color="text.secondary">{`Duration: ${Math.floor(c.duration / 60)}m ${c.duration % 60}s`}</Typography>
          )}
        </Box>
        {c.coverUrl && (
          <Box mb={2}>
            <img src={c.coverUrl} alt={c.title} style={{ maxWidth: '100%', height: 'auto' }} />
          </Box>
        )}
        {c.description && (
          <Box mb={2}>
            <Typography variant="body1">{c.description}</Typography>
          </Box>
        )}
        <Card variant="outlined" sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="subtitle1">File Info</Typography>
            <Typography variant="body2" color="text.secondary">ID: {c.id}</Typography>
          </CardContent>
        </Card>
        <Box>
          <Button variant="contained" onClick={() => navigate(`/player/${c.id}`)}>Play</Button>
        </Box>
      </Container>
    </Layout>
    )
}

export default ContentDetail
