import { PaletteMode } from '@mui/material'

type Palette = {
  mode: PaletteMode
  primary: { main: string }
  secondary: { main: string }
  background: { default: string; paper: string }
  text: { primary: string; secondary?: string }
}

export function getThemePalette(mode: PaletteMode) {
  const isLight = mode === 'light'
  return {
    palette: {
      mode,
      primary: { main: isLight ? '#3f51b5' : '#90caf9' },
      secondary: { main: isLight ? '#f44336' : '#ff8a80' },
      background: {
        default: isLight ? '#f6f7fb' : '#121212',
        paper: isLight ? '#ffffff' : '#1e1e1e',
      },
      text: {
        primary: isLight ? '#1b1b1b' : '#eaeaea',
      },
    } as any,
    typography: {
      // Distinctive typography choices for headers and body could be further enhanced by fonts loaded in app
      fontFamily: isLight
        ? '"Playfair Display", serif, Georgia'
        : '"Playfair Display", serif, Georgia',
    },
  } as any
}
