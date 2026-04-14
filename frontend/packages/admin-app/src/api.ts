// Lightweight shared API client for admin app (permissions + limits)
// This file uses the project's existing fetch-based API surface.
import { GlobalLimits, UserLimits, Permission } from './types/permissions';

type Json = any;

const handleResponse = async (res: Response) => {
  const contentType = res.headers.get('Content-Type') || '';
  let data: any = null;
  if (contentType.includes('application/json')) {
    data = await res.json();
  }
  if (!res.ok) {
    const err = data?.detail || data?.message || res.statusText;
    throw new Error(err);
  }
  return data;
};

// Permissions
export const fetchPermissions = async (): Promise<Permission[]> => {
  const res = await fetch('/api/v1/permissions/', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  return await handleResponse(res);
};

export const createPermission = async (name: string, description?: string): Promise<Permission> => {
  const body = { name, description };
  const res = await fetch('/api/v1/permissions/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  return await handleResponse(res);
};

export const deletePermission = async (permissionId: string): Promise<void> => {
  const res = await fetch(`/api/v1/permissions/${permissionId}`, {
    method: 'DELETE',
  });
  await handleResponse(res);
};

export const fetchUserPermissions = async (userId: string): Promise<string[]> => {
  const res = await fetch(`/api/v1/permissions/users/${userId}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  const data = await handleResponse(res);
  // expect { permissions: string[] } or array directly depending on backend
  return Array.isArray(data) ? data : data?.permissions ?? [];
};

export const updateUserPermissions = async (userId: string, permissions: string[]): Promise<string[]> => {
  const res = await fetch(`/api/v1/permissions/users/${userId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ permissions }),
  });
  const data = await handleResponse(res);
  return Array.isArray(data) ? data : data?.permissions ?? [];
};

// Global limits
export const fetchGlobalLimits = async (): Promise<GlobalLimits> => {
  const res = await fetch('/api/v1/limits/global', {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  return await handleResponse(res);
};

export const updateGlobalLimits = async (limits: GlobalLimits): Promise<GlobalLimits> => {
  const res = await fetch('/api/v1/limits/global', {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(limits),
  });
  return await handleResponse(res);
};

export const fetchUserLimits = async (userId: string): Promise<UserLimits> => {
  const res = await fetch(`/api/v1/limits/users/${userId}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });
  return await handleResponse(res);
};

export const updateUserLimits = async (userId: string, limits: UserLimits): Promise<UserLimits> => {
  const res = await fetch(`/api/v1/limits/users/${userId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(limits),
  });
  return await handleResponse(res);
};

export const resetUserLimitsToGlobal = async (userId: string): Promise<void> => {
  const res = await fetch(`/api/v1/limits/users/${userId}`, {
    method: 'DELETE',
  });
  await handleResponse(res);
};
