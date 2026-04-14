import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Home from './pages/Home'
import Library from './pages/Library'
import Player from './pages/Player'
import Stats from './pages/Stats'
import ContentDetail from './pages/ContentDetail'

const App: React.FC = () => {
  return (
    <BrowserRouter basename="/user">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="library" element={<Library />} />
        <Route path="content/:id" element={<ContentDetail />} />
        <Route path="player" element={<Player />} />
        <Route path="stats" element={<Stats />} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
