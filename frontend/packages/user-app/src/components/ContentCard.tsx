import React, { useEffect, useState } from 'react'
import { Card, CardActionArea, CardContent, CardMedia, Typography, Box, LinearProgress, Stack, Avatar } from '@mui/material'
import { useNavigate } from 'react-router-dom'
import type { ContentItem } from '../../shared/types/content'
import { formatDuration } from '../utils/formatDuration'

type ContentCardProps = {
  item: ContentItem
  onPlay?: (id: string) => void
  onOpenDetail?: (id: string) => void
}

// Simple progress persisted in localStorage per content id (non-persistent across sessions is fine for UI cue)
function useProgress(id: string) {
  const [progress, setProgress] = useState<number>(0)
  useEffect(() => {
    const key = `aap-progress-${id}`
    const v = localStorage.getItem(key)
    const n = v ? Number(v) : 0
    setProgress(isNaN(n) ? 0 : Math.max(0, Math.min(100, n)))
  }, [id])
  return progress
}

export const ContentCard: React.FC<ContentCardProps> = ({ item, onPlay, onOpenDetail }) => {
  const navigate = useNavigate()
  const progress = useProgress(item.id)

  const handleOpen = () => {
    if (onOpenDetail) onOpenDetail(item.id)
    else navigate(`/user/content/${item.id}`)
  }
  const handlePlay = () => {
    if (onPlay) onPlay(item.id)
    else navigate(`/player/${item.id}`)
  }

  const initials = (item.author && typeof item.author === 'string') ? item.author.charAt(0).toUpperCase() : 'A'

  return (
    <Card variant="outlined" sx={{ display: 'flex', flexDirection: 'column' }}>
      <CardActionArea onClick={handleOpen} sx={{ padding: 0 }}>
        {item.coverUrl ? (
          <CardMedia component="img" height="140" image={item.coverUrl} alt={item.title} />
        ) : (
          <Box sx={{ height: 140, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'rgba(0,0,0,0.04)' }}>
            <Avatar sx={{ bgcolor: 'primary.main' }}>{initials}</Avatar>
            <Box component="span" sx={{ ml: 1, fontWeight: 600 }}>No Cover</Box>
          </Box>
        )}
        <CardContent sx={{ paddingTop: 1 }}>
          <Typography variant="subtitle1" noWrap title={item.title}>{item.title}</Typography>
          <Typography variant="body2" color="text.secondary" noWrap title={item.author ?? ''}>
            {item.author ?? 'Unknown author'}
          </Typography>
          {typeof item.duration === 'number' && (
            <Typography variant="caption" color="text.secondary">
              {formatDuration(item.duration)}
            </Typography>
          )}
        </CardContent>
      </CardActionArea>
      {/* Progress indicator */}
      <Box sx={{ px: 2, pb: 1 }}>
        <LinearProgress variant="determinate" value={progress} sx={{ height: 6, borderRadius: 3 }} />
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'flex-end', px: 2, pb: 2 }}>
        <Typography variant="caption" color="text.secondary">{progress > 0 ? `Progress: ${progress}%` : ''}</Typography>
      </Box>
      <Stack direction="row" spacing={1} sx={{ px: 2, pb: 2 }}>
        <Box sx={{ flexGrow: 1 }} />
        <button onClick={handlePlay} style={{ padding: '6px 12px', borderRadius: 6, border: 'none', background: '#1976d2', color: 'white', cursor: 'pointer' }}>Play</button>
      </Stack>
    </Card>
  )
}
