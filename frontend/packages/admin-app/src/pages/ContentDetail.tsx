import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, CircularProgress, Alert } from '@mui/material';
import { Layout } from '../../../../shared/components/Layout';
import { getContent } from '../../../../shared/api-client/content';

// Content detail page
export const ContentDetailPage: React.FC<{ id: string }> = ({ id }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    getContent?.(id)
      .then((d) => {
        setData(d);
        setLoading(false);
      })
      .catch((e) => {
        setError('Failed to load content.');
        setLoading(false);
      });
  }, [id]);

  return (
    <Layout>
      <Box sx={{ padding: 2 }}>
        <Typography variant="h4" gutterBottom>Content Details</Typography>
        <Card>
          <CardContent>
            {loading && <CircularProgress />}
            {error && <Alert severity="error">{error}</Alert>}
            {data && (
              <Box sx={{ display: 'grid', gap: 2 }}>
                <Typography><strong>Title:</strong> {data.title}</Typography>
                <Typography><strong>Author:</strong> {data.author}</Typography>
                <Typography><strong>Description:</strong> {data.description ?? '—'}</Typography>
                <Typography><strong>Duration:</strong> {data.duration ?? '—'} seconds</Typography>
                <Typography><strong>Folder:</strong> {data.folder?.name ?? data.folder ?? '—'}</Typography>
                <Typography><strong>Format:</strong> {data.format ?? '—'}</Typography>
                <Typography><strong>Added:</strong> {data.addedAt ?? data.createdAt ?? '—'}</Typography>
                <Typography><strong>File:</strong> {data.fileInfo?.path ?? data.path ?? '—'}</Typography>
              </Box>
            )}
          </CardContent>
        </Card>
      </Layout>
    </Box>
  );
};

export default ContentDetailPage;
