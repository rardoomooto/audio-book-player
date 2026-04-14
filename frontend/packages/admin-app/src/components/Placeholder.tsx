import React from 'react'

const Placeholder: React.FC<{ label?: string }> = ({ label = 'Placeholder' }) => (
  <div style={{ padding: 12, border: '1px dashed #ccc', borderRadius: 6, color: '#666' }}>
    {label}
  </div>
)

export default Placeholder
