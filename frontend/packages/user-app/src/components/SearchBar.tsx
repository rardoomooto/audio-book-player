import React, { useEffect, useState } from 'react'
import { TextField, InputAdornment } from '@mui/material'
import SearchIcon from '@mui/icons-material/Search'

type SearchBarProps = {
  value?: string
  onQuery?: (q: string) => void
  onChange?: (q: string) => void
  placeholder?: string
  debounceMs?: number
}

// Debounced search bar that notifies parent after inactivity
export const SearchBar: React.FC<SearchBarProps> = ({ value = '', onQuery, onChange, placeholder = 'Search contents...', debounceMs = 300 }) => {
  const [local, setLocal] = useState<string>(value)

  useEffect(() => {
    setLocal(value)
  }, [value])

  useEffect(() => {
    const t = setTimeout(() => {
      const fn = onQuery ?? onChange
      fn?.(local)
    }, debounceMs)
    return () => clearTimeout(t)
  }, [local, debounceMs, onQuery, onChange])

  return (
    <TextField
      fullWidth
      variant="outlined"
      size="small"
      placeholder={placeholder}
      value={local}
      onChange={(e) => setLocal(e.target.value)}
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon fontSize="small" />
          </InputAdornment>
        ),
      }}
    />
  )
}
