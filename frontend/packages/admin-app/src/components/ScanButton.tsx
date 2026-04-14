import React from 'react';
import { Button } from '@mui/material';

type Props = {
  onClick: () => void;
  loading?: boolean;
  label?: string;
};

export const ScanButton: React.FC<Props> = ({ onClick, loading, label = 'Scan' }) => {
  return (
    <Button variant="contained" onClick={onClick} disabled={loading}>
      {loading ? 'Scanning...' : label}
    </Button>
  );
};

export default ScanButton;
