import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  base: '/user/',
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        // remove /api prefix when proxying to backend
        // forward API calls as-is to the backend proxy
        rewrite: (p) => p
      }
    }
  },
  resolve: {
    alias: {
      '@shared': path.resolve(__dirname, '../../shared')
    }
  },
  build: {
    outDir: 'dist'
  }
})
