// In-memory token storage for access/refresh tokens
// Access token is kept in memory (not persisted to localStorage)
let accessToken: string | null = null;
let refreshToken: string | null = null;
let accessTokenExpiresAt: number | null = null; // epoch ms

export function setAccessToken(token: string, expiresInSec?: number) {
  accessToken = token;
  if (typeof expiresInSec === 'number') {
    accessTokenExpiresAt = Date.now() + expiresInSec * 1000;
  } else {
    // Fallback to 15 minutes if not provided
    accessTokenExpiresAt = Date.now() + 15 * 60 * 1000;
  }
}

export function getAccessToken(): string | null {
  // Consider token expiry for a soft check; actual expiry should be enforced by server
  return accessToken;
}

export function getAccessTokenExpiry(): number | null {
  return accessTokenExpiresAt;
}

export function setRefreshToken(token: string) {
  refreshToken = token;
}

export function getRefreshToken(): string | null {
  return refreshToken;
}

export function clearTokens() {
  accessToken = null;
  refreshToken = null;
  accessTokenExpiresAt = null;
}
