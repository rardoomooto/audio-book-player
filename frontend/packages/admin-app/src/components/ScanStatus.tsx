import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';

export const ScanStatus: React.FC<{ status: string; results?: string[] }> = ({ status, results }) => {
  return (
    <Card>
      <CardContent>
        <Typography variant="subtitle1">Status: {status}</Typography>
        {results && results.length > 0 && (
          <Box>
            {results.map((r, idx) => (
              <Typography key={idx} variant="body2">- {r}</Typography>
            ))}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ScanStatus;
