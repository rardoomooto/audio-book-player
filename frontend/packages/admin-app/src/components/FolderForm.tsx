import React, { useState } from 'react';
import { Box, TextField, Button } from '@mui/material';
import { createFolder } from '../../../../shared/api-client/folders';

export const FolderForm: React.FC = () => {
  const [name, setName] = useState<string>('');
  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim()) return;
    try {
      await createFolder?.({ name });
      window.location.reload();
    } catch {
      // show error in UI in a real app; keep simple here
    }
  };
  return (
    <form onSubmit={onSubmit}>
      <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
        <TextField label="Folder Name" value={name} onChange={(e) => setName(e.target.value)} />
        <Button type="submit" variant="contained">Create</Button>
      </Box>
    </form>
  );
};

export default FolderForm;
