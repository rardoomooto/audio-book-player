import React, { useMemo, useState } from 'react'
import { Box, Typography, Container, Button } from '@mui/material'
import { LoadingSpinner } from '../../../../shared/components/LoadingSpinner'
import Layout from '../../../../shared/components/Layout'
import { ContentGrid } from '../components/ContentGrid'
import { useContent } from '../hooks/useContent'
import { SearchBar } from '../components/SearchBar'
import { FilterPanel } from '../components/FilterPanel'
import { useNavigate } from 'react-router-dom'

const Library: React.FC = () => {
  const [query, setQuery] = useState<string>('')
  const [page, setPage] = useState<number>(1)
  const [perPage, setPerPage] = useState<number>(20)
  const [filters, setFilters] = useState<{ folder?: string; format?: string; duration?: [number, number] }>({})
  const { items, loading, error, total } = useContent({ page, perPage, query, folder: filters.folder, format: filters.format, durationMin: filters?.duration?.[0], durationMax: filters?.duration?.[1] })
  const navigate = useNavigate()

  // derive folders/formats from items for the filter panel
  const folders = useMemo(() => {
    const set = new Set<string>()
    items.forEach((it) => {
      const f = (it as any).folder
      if (f) set.add(String(f))
    })
    return Array.from(set)
  }, [items])
  const formats = useMemo(() => {
    const set = new Set<string>()
    items.forEach((it) => {
      const f = (it as any).format
      if (f) set.add(String(f))
    })
    return Array.from(set)
  }, [items])

  const onSearch = (q: string) => {
    setQuery(q)
    setPage(1)
  }

  const onFilterChange = (f: { folder?: string; format?: string; duration?: [number, number] }) => {
    setFilters((prev) => ({ ...prev, ...f }))
    setPage(1)
  }

  return (
    <Layout>
      <Container maxWidth={false}>
        <Typography variant="h4" gutterBottom>Content Library</Typography>
        <Box display="flex" gap={2} alignItems="center" mb={2}>
          <SearchBar value={query} onChange={onSearch} placeholder="Search contents..." />
          <Button variant="contained" onClick={() => setQuery('')}>Clear</Button>
        </Box>
        <FilterPanel folders={folders} formats={formats} value={filters as any} onChange={onFilterChange} />
        {loading && <LoadingSpinner />}
        {error && <Typography color="error">Error: {error}</Typography>}
        <Box mt={2}>
          <ContentGrid items={items as any} />
        </Box>
        <Box display="flex" justifyContent="center" mt={2}>
          <Button variant="outlined" disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>Previous</Button>
          <Typography sx={{ mx: 2, alignSelf: 'center' }}>Page {page}</Typography>
          <Button variant="outlined" onClick={() => setPage((p) => p + 1)} disabled={total !== undefined && (page * perPage >= total)}>Next</Button>
        </Box>
      </Container>
    </Layout>
  )
}

export default Library
