import React, { useState } from "react";
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField, Box } from "@mui/material";

type Props = {
  open: boolean;
  onClose: () => void;
  onCreate: (payload: { name: string; description?: string }) => void;
};

const PermissionForm: React.FC<Props> = ({ open, onClose, onCreate }) => {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  const handleSubmit = () => {
    onCreate({ name: name.trim(), description: description.trim() });
    setName("");
    setDescription("");
    onClose();
  };

  return (
    <Dialog open={open} onClose={onClose}>
      <DialogTitle>Create Permission</DialogTitle>
      <DialogContent>
        <Box display="flex" flexDirection="column" gap={2} width={400}>
          <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} />
          <TextField label="Description" value={description} onChange={(e) => setDescription(e.target.value)} />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>Cancel</Button>
        <Button onClick={handleSubmit} color="primary" variant="contained">Create</Button>
      </DialogActions>
    </Dialog>
  );
};

export default PermissionForm;
