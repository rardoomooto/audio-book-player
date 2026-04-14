import React, { useMemo, useState } from 'react'
import { Box, FormControl, InputLabel, Select, MenuItem, TextField, Stack } from '@mui/material'
import type { ContentItem } from '../../shared/types/content'

type FilterPanelProps = {
  onChange: (filters: { folder?: string; format?: string; durationMin?: number; durationMax?: number }) => void
  folders?: string[]
  formats?: string[]
  value?: { folder?: string; format?: string; durationMin?: number; durationMax?: number }
  items?: ContentItem[]
}

// Lightweight filter panel deriving options from provided items when available
export const FilterPanel: React.FC<FilterPanelProps> = ({ onChange, folders: preFolders, formats: preFormats, value, items }) => {
  const [folder, setFolder] = useState<string>(value?.folder ?? '')
  const [format, setFormat] = useState<string>(value?.format ?? '')
  const [minD, setMinD] = useState<string>('')
  const [maxD, setMaxD] = useState<string>('')

  // Derive simple options from items if available; or use provided props
  const folders = preFolders ?? useMemo(() => {
    if (!items) return [] as string[]
    const s = new Set<string>()
    items.forEach((it) => {
      const f = (it as any).folder as string | undefined
      if (f) s.add(f)
    })
    return Array.from(s)
  }, [items])

  const formats = preFormats ?? useMemo(() => {
    if (!items) return [] as string[]
    const s = new Set<string>()
    items.forEach((it) => {
      const f = (it as any).format as string | undefined
      if (f) s.add(f)
    })
    return Array.from(s)
  }, [items])

  const apply = () => {
    onChange({ folder: folder || undefined, format: format || undefined, durationMin: minD ? Number(minD) : undefined, durationMax: maxD ? Number(maxD) : undefined })
  }

  React.useEffect(() => {
    // Debounced-ish, apply immediately when user changes but we'll push changes on any input change
    apply()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [folder, format, minD, maxD])

  return (
    <Box sx={{ p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 2 }}>
      <Stack spacing={2}>
        <FormControl fullWidth size="small">
          <InputLabel>Folder</InputLabel>
          <Select value={folder} label="Folder" onChange={(e) => setFolder(e.target.value)}>
            <MenuItem value="">All</MenuItem>
            {folders.map((f) => (
              <MenuItem key={f} value={f}>{f}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth size="small">
          <InputLabel>Format</InputLabel>
          <Select value={format} label="Format" onChange={(e) => setFormat(e.target.value)}>
            <MenuItem value="">All</MenuItem>
            {formats.map((f) => (
              <MenuItem key={f} value={f}>{f}</MenuItem>
            ))}
          </Select>
        </FormControl>
        <Stack direction="row" spacing={2}>
          <TextField label="Min duration (s)" type="number" size="small" value={minD} onChange={(e) => setMinD(e.target.value)} />
          <TextField label="Max duration (s)" type="number" size="small" value={maxD} onChange={(e) => setMaxD(e.target.value)} />
        </Stack>
      </Stack>
    </Box>
  )
}
