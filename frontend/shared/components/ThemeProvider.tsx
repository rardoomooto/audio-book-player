import React from 'react'
import { createTheme, ThemeProvider as MuiThemeProvider, Theme } from '@mui/material/styles'
import { CssBaseline } from '@mui/material'
import { PaletteMode } from '@mui/material'
import { Theme as MuiTheme } from '@mui/material/styles'
import { getThemePalette } from '../utils/theme'

type ColorMode = PaletteMode

type ThemeProviderProps = {
  children: React.ReactNode
}

type ColorModeContextValue = {
  toggleColorMode: () => void
}

export const ColorModeContext = React.createContext<ColorModeContextValue>({
  toggleColorMode: () => {},
})

export function ThemeProvider({ children }: ThemeProviderProps) {
  const [mode, setMode] = React.useState<ColorMode>('light')
  const colorMode = React.useMemo<ColorModeContextValue>(
    () => ({ toggleColorMode: () => setMode((m) => (m === 'light' ? 'dark' : 'light')) }),
    []
  )

  const theme = React.useMemo<MuiTheme>(() => createTheme(getThemePalette(mode)), [mode])

  return (
    <ColorModeContext.Provider value={colorMode}>
      <MuiThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MuiThemeProvider>
    </ColorModeContext.Provider>
  )
}

export function useColorMode() {
  return React.useContext(ColorModeContext)
}

export default ThemeProvider
