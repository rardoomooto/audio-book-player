import React from "react";
import { List, ListItem, ListItemText, IconButton, Divider, Card, CardContent, Stack, Typography, Button } from "@mui/material";
import DeleteIcon from "@mui/icons-material/Delete";
import { Permission } from "../hooks/usePermissions";

type Props = {
  permissions: Permission[];
  onDelete?: (id: string) => void;
  onEdit?: (id: string) => void;
};

const PermissionsList: React.FC<Props> = ({ permissions, onDelete }) => {
  return (
    <Card variant="outlined" sx={{ mt: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>Permissions</Typography>
        <List>
          {permissions.map((p) => (
            <React.Fragment key={p.id}>
              <ListItem secondaryAction={onDelete ? (
                <IconButton edge="end" aria-label="delete" onClick={() => onDelete?.(p.id)}>
                  <DeleteIcon />
                </IconButton>
              ) : null}>
                <ListItemText primary={p.name} secondary={p.description} />
              </ListItem>
              <Divider component="li" />
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default PermissionsList;
