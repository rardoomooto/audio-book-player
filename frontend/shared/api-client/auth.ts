import axios, { AxiosResponse } from 'axios';
import { getRefreshToken } from './tokenStore';
import { LoginRequest, TokenResponse } from '../../types/auth';

// Base URL for API - read from Vite env, fallback to relative path
const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || '/api';

/**
 * Login using username/password. Returns tokens to be stored by the caller.
 */
export async function login(credentials: LoginRequest): Promise<TokenResponse> {
  const resp: AxiosResponse<TokenResponse> = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
  return resp.data;
}

/** Refresh access token using a refresh token. */
export async function refreshToken(refreshToken: string): Promise<TokenResponse> {
  const resp: AxiosResponse<TokenResponse> = await axios.post(`${API_BASE_URL}/auth/refresh`, {
    refreshToken,
  });
  return resp.data;
}

/** Fetch current user info (requires valid access token). */
export async function getMe(): Promise<any> {
  const resp: AxiosResponse<any> = await axios.get(`${API_BASE_URL}/auth/me`);
  return resp.data;
}

/** Logout current session. */
export async function logout(): Promise<void> {
  try {
    await axios.post(`${API_BASE_URL}/auth/logout`, {
      // The server may expect refresh token; we can omit in in-memory demos
    });
  } catch {
    // Ignore logout errors in client; tokens will be cleared locally
  }
}
