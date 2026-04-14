import { Permission, GlobalLimits, UserLimits } from "../types/permissions";

const API_BASE = "/api/v1";

// Permissions
export async function getPermissions(): Promise<Permission[]> {
  const res = await fetch(`${API_BASE}/permissions/`, { credentials: 'include' });
  if (!res.ok) throw new Error(`Failed to fetch permissions: ${res.status}`);
  return res.json();
}

export async function createPermission(payload: { name: string; description?: string }): Promise<Permission> {
  const res = await fetch(`${API_BASE}/permissions/`, {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Failed to create permission: ${res.status}`);
  return res.json();
}

export async function deletePermission(permissionId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/permissions/${permissionId}`, {
    method: "DELETE",
    credentials: 'include',
  });
  if (!res.ok) throw new Error(`Failed to delete permission: ${res.status}`);
}

export async function getUserPermissions(userId: string): Promise<Permission[]> {
  const res = await fetch(`${API_BASE}/permissions/users/${userId}`, {
    credentials: 'include',
  });
  if (!res.ok) throw new Error(`Failed to fetch user permissions: ${res.status}`);
  return res.json();
}

export async function updateUserPermissions(userId: string, payload: { permissionIds: string[] }): Promise<void> {
  const res = await fetch(`${API_BASE}/permissions/users/${userId}`, {
    method: "PUT",
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Failed to update user permissions: ${res.status}`);
}

// Limits
export async function getGlobalLimits(): Promise<GlobalLimits> {
  const res = await fetch(`${API_BASE}/limits/global`, { credentials: 'include' });
  if (!res.ok) throw new Error(`Failed to fetch global limits: ${res.status}`);
  return res.json();
}

export async function updateGlobalLimits(payload: GlobalLimits): Promise<GlobalLimits> {
  const res = await fetch(`${API_BASE}/limits/global`, {
    method: "PUT",
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Failed to update global limits: ${res.status}`);
  return res.json();
}

export async function getUserLimits(userId: string): Promise<UserLimits> {
  const res = await fetch(`${API_BASE}/limits/users/${userId}`, { credentials: 'include' });
  if (!res.ok) throw new Error(`Failed to fetch user limits: ${res.status}`);
  return res.json();
}

export async function updateUserLimits(userId: string, payload: UserLimits): Promise<UserLimits> {
  const res = await fetch(`${API_BASE}/limits/users/${userId}`, {
    method: "PUT",
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`Failed to update user limits: ${res.status}`);
  return res.json();
}

export async function resetUserLimits(userId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/limits/users/${userId}`, {
    method: "DELETE",
    credentials: 'include',
  });
  if (!res.ok) throw new Error(`Failed to reset user limits: ${res.status}`);
}
