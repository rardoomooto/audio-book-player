import React, { useMemo, useState, useEffect } from "react";
import { Box, Typography, CardContent, Card, Button } from "@mui/material";
import Layout from "../../shared/components/Layout";
import PermissionsList from "../../components/PermissionsList";
import PermissionForm from "../../components/PermissionForm";
import UserPermissionsEditor from "../../components/UserPermissionsEditor";
import { usePermissions, Permission } from "../../hooks/usePermissions";
import { useParams } from "react-router-dom";

const UserPermissions: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const { permissions, loading, fetchAll, create, remove, fetchUserPermissions, updateUserPermissions } = usePermissions();
  const [allPermissions, setAllPermissions] = useState<Permission[]>([]);
  const [userPerms, setUserPerms] = useState<Permission[]>([]);
  const [openForm, setOpenForm] = useState(false);

  useEffect(() => {
    // Load all permissions
    fetchAll().then(() => {
      // @ts-ignore
      setAllPermissions(permissions);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (userId) {
      fetchUserPermissions(userId).then((perms) => {
        setUserPerms(perms);
      });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userId]);

  const handleSave = async (ids: string[]) => {
    if (!userId) return;
    await updateUserPermissions(userId, ids);
    // refresh
    const updated = await fetchUserPermissions(userId);
    setUserPerms(updated);
  };

  const addPermission = async (payload: { name: string; description?: string }) => {
    await create(payload);
    // refresh list
    const res = await fetchAll();
    setAllPermissions(permissions);
  };

  return (
    <Layout title="User Permissions">
      <Box sx={{ p: 2 }}>
        <Typography variant="h4" gutterBottom>User Permissions</Typography>
        <Card variant="outlined" sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6">Assign Permissions</Typography>
            <PermissionsList permissions={allPermissions} onDelete={(id)=>remove(id)} />
          </CardContent>
        </Card>
        <Button variant="contained" onClick={() => setOpenForm(true)}>Create Permission</Button>
        <PermissionForm open={openForm} onClose={() => setOpenForm(false)} onCreate={addPermission} />
        <Card variant="outlined" sx={{ mt: 2 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>Current User Permissions</Typography>
            <UserPermissionsEditor
              userId={userId ?? ''}
              allPermissions={allPermissions}
              userPermissions={userPerms}
              onChange={handleSave}
            />
          </CardContent>
        </Card>
      </Box>
    </Layout>
  );
};

export default UserPermissions;
