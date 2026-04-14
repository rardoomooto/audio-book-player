import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, CircularProgress, Alert } from '@mui/material';
import { Layout } from '../../../../shared/components/Layout';
import { ContentForm } from '../components/ContentForm';
import { useParams, useNavigate } from 'react-router-dom';
import { getContent, updateContent } from '../../../../shared/api-client/content';
import { Folder } from '../../../../shared/types/content';
import { useFolders } from '../hooks/useFolders';

export const ContentEditPage: React.FC = () => {
  const { id } = useParams<string>();
  const navigate = useNavigate();
  const { folders } = useFolders();
  const [initial, setInitial] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    setLoading(true);
    getContent?.(id as string)
      .then((data) => {
        setInitial(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Failed to load content.');
        setLoading(false);
      });
  }, [id]);

  const onSubmit = async (payload: any) => {
    try {
      await updateContent?.(id as string, payload);
      navigate(`/admin/content/${id}`);
    } catch (e) {
      setError('Failed to update content.');
    }
  };

  return (
    <Layout>
      <Box sx={{ padding: 2 }}>
        <Typography variant="h4" gutterBottom>Edit Content</Typography>
        {loading ? (
          <CircularProgress />
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <Card>
            <CardContent>
              <ContentForm initial={initial} folders={folders as Folder[]} onSubmit={onSubmit} />
            </CardContent>
          </Card>
        )}
      </Box>
    </Layout>
  );
};

export default ContentEditPage;
