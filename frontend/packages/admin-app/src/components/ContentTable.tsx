import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TablePagination, IconButton, Tooltip } from '@mui/material';
import { Content } from '../../../../shared/types/content';
import { Visibility, Edit, Delete, Search } from '@mui/icons-material';

type Props = {
  contents: Content[];
  total: number;
  onView: (id: string) => void;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
  onScan: (id: string) => void;
  page?: number;
  rowsPerPage?: number;
};

export const ContentTable: React.FC<Props> = ({ contents, total, onView, onEdit, onDelete, onScan, page = 0, rowsPerPage = 10 }) => {
  const [localPage, setLocalPage] = React.useState(page);
  const [rowsPer, setRowsPer] = React.useState(rowsPerPage);
  React.useEffect(() => setLocalPage(page), [page]);
  React.useEffect(() => setRowsPer(rowsPerPage), [rowsPerPage]);

  const handleChangePage = (_ev: any, newPage: number) => setLocalPage(newPage);
  const handleChangeRowsPerPage = (ev: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPer(parseInt(ev.target.value, 10));
    setLocalPage(0);
  };

  return (
    <Paper>
      <TableContainer>
        <Table size="small" aria-label="contents table">
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Author</TableCell>
              <TableCell>Duration</TableCell>
              <TableCell>Folder</TableCell>
              <TableCell>Format</TableCell>
              <TableCell>Date Added</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {contents.map((c) => (
              <TableRow key={c.id} hover>
                <TableCell>{c.title}</TableCell>
                <TableCell>{c.author}</TableCell>
                <TableCell>{c.duration ?? '—'}</TableCell>
                <TableCell>{c.folder?.name ?? c.folder ?? '—'}</TableCell>
                <TableCell>{c.format ?? '—'}</TableCell>
                <TableCell>{c.addedAt ?? c.createdAt ?? '—'}</TableCell>
                <TableCell align="right">
                  <Tooltip title="View">
                    <IconButton size="small" onClick={() => onView(c.id)}>
                      <Visibility fontSize="inherit" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Edit">
                    <IconButton size="small" onClick={() => onEdit(c.id)}>
                      <Edit fontSize="inherit" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Scan">
                    <IconButton size="small" onClick={() => onScan(c.id)}>
                      <Search fontSize="inherit" />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Delete">
                    <IconButton size="small" onClick={() => onDelete(c.id)} color="error">
                      <Delete fontSize="inherit" />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        count={total}
        page={localPage}
        onPageChange={handleChangePage}
        rowsPerPage={rowsPer}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Paper>
  );
};

export default ContentTable;
