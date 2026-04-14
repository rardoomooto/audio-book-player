import React from 'react'
import { Grid, Box } from '@mui/material'
import type { ContentItem } from '../../shared/types/content'
import { ContentCard } from './ContentCard'

type ContentGridProps = {
  contents?: ContentItem[]
  items?: ContentItem[]
  onPlay?: (id: string) => void
  onOpenDetail?: (id: string) => void
}

export const ContentGrid: React.FC<ContentGridProps> = ({ contents, items, onPlay, onOpenDetail }) => {
  const list = contents ?? items ?? []
  return (
    <Grid container spacing={2}>
      {list.map((c) => (
        <Grid item key={c.id} xs={12} sm={6} md={4} lg={3}>
          <ContentCard item={c} onPlay={onPlay} onOpenDetail={onOpenDetail} />
        </Grid>
      ))}
    </Grid>
  )
}
