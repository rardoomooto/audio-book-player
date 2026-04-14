import React, { useState } from "react";
import Layout from "../../shared/components/Layout";
import { Box, Typography, CardContent, Card, Button } from "@mui/material";
import PermissionsList from "../../components/PermissionsList";
import PermissionForm from "../../components/PermissionForm";
import { usePermissions } from "../../hooks/usePermissions";

const PermissionsPage: React.FC = () => {
  const { permissions, loading, fetchAll, create, remove } = usePermissions();
  const [open, setOpen] = useState(false);

  // Initialize by ensuring permissions are loaded
  // fetchAll is called inside hook on mount

  const handleCreate = async (payload: { name: string; description?: string }) => {
    await create(payload);
  };

  return (
    <Layout title="Permissions">
      <Box sx={{ p: 2 }}>
        <Typography variant="h4" gutterBottom>Permissions</Typography>
        <Card variant="outlined" sx={{ mb: 2 }}>
          <CardContent>
            <PermissionsList permissions={permissions} onDelete={remove} />
          </CardContent>
        </Card>
        <Button variant="contained" onClick={() => setOpen(true)}>Create Permission</Button>
        <PermissionForm open={open} onClose={() => setOpen(false)} onCreate={handleCreate} />
      </Box>
    </Layout>
  );
};

export default PermissionsPage;
