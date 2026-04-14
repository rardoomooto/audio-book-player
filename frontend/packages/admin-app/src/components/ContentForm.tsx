import React from 'react';
import { Box, TextField, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { Folder } from '../../../../shared/types/content';

type Props = {
  initial?: any;
  folders: Folder[];
  onSubmit: (payload: any) => void;
};

export const ContentForm: React.FC<Props> = ({ initial, folders, onSubmit }) => {
  const [title, setTitle] = React.useState<string>(initial?.title ?? '');
  const [author, setAuthor] = React.useState<string>(initial?.author ?? '');
  const [description, setDescription] = React.useState<string>(initial?.description ?? '');
  const [folderId, setFolderId] = React.useState<string>(initial?.folder?.id ?? initial?.folderId ?? '');

  const onSave = (e: React.FormEvent) => {
    e.preventDefault();
    const payload: any = { title, author, description, folderId };
    onSubmit(payload);
  };

  const isValid = title.trim().length > 0 && author.trim().length > 0;

  return (
    <form onSubmit={onSave}>
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
        <TextField label="Title" value={title} onChange={(e) => setTitle(e.target.value)} required />
        <TextField label="Author" value={author} onChange={(e) => setAuthor(e.target.value)} required />
        <TextField label="Description" value={description} onChange={(e) => setDescription(e.target.value)} multiline rows={4} />
        <FormControl>
          <InputLabel>Folder</InputLabel>
          <Select value={folderId} onChange={(e) => setFolderId(e.target.value as string)}>
            {folders.map((f) => (
              <MenuItem key={f.id} value={f.id}>{f.name}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>
      <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
        <Button type="submit" variant="contained" disabled={!isValid}>Save</Button>
        <Button variant="outlined" onClick={() => window.history.back()}>Cancel</Button>
      </Box>
    </form>
  );
};

export default ContentForm;
