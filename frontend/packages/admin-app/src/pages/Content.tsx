import React, { useEffect, useState } from 'react';
import { Box, Card, CardContent, Typography, TextField, Select, MenuItem, InputLabel, FormControl, IconButton, CircularProgress, Alert } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Layout } from '../../../../shared/components/Layout';
import { ContentTable } from '../components/ContentTable';
import { useContents } from '../hooks/useContents';
import { useFolders } from '../hooks/useFolders';

// Content list page
export const ContentPage: React.FC = () => {
  const navigate = useNavigate();
  const { contents, total, loading, error, fetchContents, setQuery } = useContents();
  const { folders, loading: foldersLoading } = useFolders();
  const [search, setSearch] = useState<string>("");
  const [folderId, setFolderId] = useState<string>("");
  const [sort, setSort] = useState<string>('addedAt');
  const [order, setOrder] = useState<'asc'|'desc'>('desc');

  useEffect(() => {
    fetchContents({ search, folderId, sort, order });
  }, [search, folderId, sort, order]);

  const onDelete = async (id: string) => {
    // simple confirmation
    if (!window.confirm('Are you sure you want to delete this content?')) return;
    try {
      // use content delete API
      const ok = await (await import('../../shared/api-client/content')).deleteContent?.(id);
      if (ok) fetchContents({ search, folderId, sort, order });
    } catch (e) {
      // ignore here; hook handles error state in UI
      console.error(e);
    }
  };

  return (
    <Layout>
      <Box sx={{ padding: 2 }}>
        <Typography variant="h4" gutterBottom>Contents</Typography>
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', marginBottom: 2, flexWrap: 'wrap' }}>
              <TextField
                label="Search"
                variant="outlined"
                size="small"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <FormControl sx={{ minWidth: 200 }} size="small">
                <InputLabel id="folder-filter-label">Folder</InputLabel>
                <Select
                  labelId="folder-filter-label"
                  label="Folder"
                  value={folderId}
                  onChange={(e) => setFolderId(e.target.value as string)}
                >
                  <MenuItem value="">All folders</MenuItem>
                  {folders?.map((f) => (
                    <MenuItem key={f.id} value={f.id}>{f.name}</MenuItem>
                  ))}
                </Select>
              </FormControl>
              <FormControl sx={{ minWidth: 150 }} size="small">
                <InputLabel id="sort-label">Sort</InputLabel>
                <Select
                  labelId="sort-label"
                  value={sort}
                  label="Sort"
                  onChange={(e) => setSort(e.target.value as string)}
                >
                  <MenuItem value="addedAt">Date Added</MenuItem>
                  <MenuItem value="title">Title</MenuItem>
                  <MenuItem value="author">Author</MenuItem>
                </Select>
              </FormControl>
              <FormControl sx={{ minWidth: 120 }} size="small">
                <InputLabel id="order-label">Order</InputLabel>
                <Select
                  labelId="order-label"
                  value={order}
                  label="Order"
                  onChange={(e) => setOrder(e.target.value as 'asc'|'desc')}
                >
                  <MenuItem value="asc">Ascending</MenuItem>
                  <MenuItem value="desc">Descending</MenuItem>
                </Select>
              </FormControl>
              <Box sx={{ flex: 1 }} />
              <button className="MuiButtonBase-root MuiButton-root MuiButton-contained" onClick={() => navigate('/admin/content/new')}>
                New Content
              </button>
            </Box>
            {loading ? (
              <Box display="flex" justifyContent="center" alignItems="center" p={3}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Alert severity="error">{String(error)}</Alert>
            ) : (
              <ContentTable
                contents={contents}
                total={total}
                onView={(id) => navigate(`/admin/content/${id}`)}
                onEdit={(id) => navigate(`/admin/content/${id}/edit`)}
                onDelete={onDelete}
                onScan={(id) => navigate(`/admin/content/${id}/scan`)}
              />
            )}
          </CardContent>
        </Card>
      </Layout>
    </Box>
  );
};

export default ContentPage;
