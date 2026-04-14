import React from 'react';
import { List, ListItem, ListItemText, Card, CardContent, Typography } from '@mui/material';
import { useFolders } from '../hooks/useFolders';

export const FolderList: React.FC = () => {
  const { folders, loading } = useFolders();
  if (loading) return <Typography>Loading folders...</Typography>;
  return (
    <List>
      {folders.map((f) => (
        <ListItem key={f.id} divider>
          <ListItemText primary={f.name} secondary={`${f.count ?? 0} items`} />
        </ListItem>
      ))}
    </List>
  );
};

export default FolderList;
