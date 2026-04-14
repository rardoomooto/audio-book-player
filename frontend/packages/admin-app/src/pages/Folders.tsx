import React from 'react';
import { Box, Card, CardContent, Typography, Grid } from '@mui/material';
import { Layout } from '../../../../shared/components/Layout';
import { FolderList } from '../components/FolderList';
import { FolderForm } from '../components/FolderForm';

// Folder management page
export const FoldersPage: React.FC = () => {
  return (
    <Layout>
      <Box sx={{ padding: 2 }}>
        <Typography variant="h4" gutterBottom>Folders</Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <FolderList />
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>New / Edit Folder</Typography>
                <FolderForm />
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Layout>
  );
};

export default FoldersPage;
