import { User, UserCreate, UserUpdate } from "../types/user";

const API_BASE = "/api/v1/users";

async function handleResponse<T>(response: Response): Promise<T> {
  const text = await response.text();
  try {
    const data = text ? JSON.parse(text) : {};
    if (!response.ok) {
      const err = data?.detail || data?.message || response.statusText;
      throw new Error(err);
    }
    return data as T;
  } catch (e) {
    // If not JSON, throw status text
    throw new Error(response.statusText || String(e));
  }
}

function getAuthHeader(): HeadersInit {
  // Try to get token from localStorage or a shared auth context if available
  // This repository expects an AuthContext; fallback to empty header if not found
  const token = typeof window !== 'undefined'
    ? (localStorage.getItem('auth_token') || '')
    : '';
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export async function listUsers(params?: {
  page?: number;
  limit?: number;
  search?: string;
  role?: string;
  status?: string;
  sortBy?: string;
  sortDir?: 'asc' | 'desc';
}): Promise<{ data: User[]; total: number }> {
  const query = new URLSearchParams();
  if (params?.page != null) query.set('page', String(params.page));
  if (params?.limit != null) query.set('limit', String(params.limit));
  if (params?.search) query.set('search', params.search);
  if (params?.role) query.set('role', params.role);
  if (params?.status) query.set('status', params.status);
  if (params?.sortBy) query.set('sortBy', params.sortBy);
  if (params?.sortDir) query.set('sortDir', params.sortDir);

  const res = await fetch(`${API_BASE}/?${query.toString()}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
    },
  });
  const data = await handleResponse<{ data: User[]; total: number }>(res);
  // Normalize shape if backend returns { users, total } etc.
  return data as any;
}

export async function getUser(userId: string): Promise<User> {
  const res = await fetch(`${API_BASE}/${userId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
    },
  });
  return handleResponse<User>(res);
}

export async function createUser(payload: UserCreate): Promise<User> {
  const res = await fetch(`${API_BASE}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
    },
    body: JSON.stringify(payload),
  });
  return handleResponse<User>(res);
}

export async function updateUser(userId: string, payload: UserUpdate): Promise<User> {
  const res = await fetch(`${API_BASE}/${userId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
    },
    body: JSON.stringify(payload),
  });
  return handleResponse<User>(res);
}

export async function deleteUser(userId: string): Promise<void> {
  const res = await fetch(`${API_BASE}/${userId}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
    },
  });
  await handleResponse<void>(res);
}

export async function changePassword(userId: string, password: string): Promise<void> {
  const res = await fetch(`${API_BASE}/${userId}/password`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
    },
    body: JSON.stringify({ password }),
  });
  await handleResponse<void>(res);
}

export async function updateStatus(userId: string, status: string): Promise<void> {
  const res = await fetch(`${API_BASE}/${userId}/status`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...getAuthHeader(),
    },
    body: JSON.stringify({ status }),
  });
  await handleResponse<void>(res);
}
