import React, { useEffect, useMemo, useState } from "react";
import { Card, CardContent, Typography, List, ListItem, ListItemText, Checkbox, ListItemSecondaryAction, IconButton, Box, Button } from "@mui/material";
import { Permission } from "../hooks/usePermissions";

type Props = {
  userId: string;
  allPermissions: Permission[];
  userPermissions: Permission[];
  onChange?: (ids: string[]) => void;
};

const UserPermissionsEditor: React.FC<Props> = ({ userId, allPermissions, userPermissions, onChange }) => {
  const [selected, setSelected] = useState<string[]>([]);

  useEffect(() => {
    const ids = userPermissions.map((p) => p.id);
    setSelected(ids);
  }, [userPermissions]);

  const toggle = (id: string) => {
    const idx = selected.indexOf(id);
    let next = [] as string[];
    if (idx === -1) next = [...selected, id]; else next = selected.filter((x) => x !== id);
    setSelected(next);
    onChange?.(next);
  };

  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6">Edit Permissions</Typography>
        <List>
          {allPermissions.map((p) => (
            <ListItem key={p.id} dense button onClick={() => toggle(p.id)}>
              <Checkbox checked={selected.includes(p.id)} />
              <ListItemText primary={p.name} secondary={p.description} />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default UserPermissionsEditor;
