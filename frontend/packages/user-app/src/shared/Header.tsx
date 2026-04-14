import React from 'react'

export const Header: React.FC<{title: string}> = ({ title }) => (
  <header className="site-header">
    <h1>{title}</h1>
  </header>
)
