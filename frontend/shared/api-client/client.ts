import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { getAccessToken, getRefreshToken, setAccessToken, setRefreshToken, clearTokens } from './tokenStore'
import { refreshToken as refreshTokenApi } from './auth'
// TokenResponse type imported from shared/types/auth in TS modules where needed

// Base Axios client for the shared API
export const apiClient: AxiosInstance = axios.create({
  baseURL: '/api',
})

export function setAuthToken(token: string) {
  apiClient.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// --- Token refresh handling (simple in-memory implementation) ---
let isRefreshing = false
let refreshSubscribers: Array<(token: string) => void> = []

function onRefreshed(token: string) {
  refreshSubscribers.forEach((cb) => cb(token))
  refreshSubscribers = []
}

function addRefreshSubscriber(cb: (token: string) => void) {
  refreshSubscribers.push(cb)
}

// Attach Authorization header for all requests if token exists
apiClient.interceptors.request.use((config: AxiosRequestConfig) => {
  const token = getAccessToken()
  if (token && config.headers) {
    (config.headers as any)['Authorization'] = `Bearer ${token}`
  } else if (token && !config.headers) {
    ;(config as any).headers = { Authorization: `Bearer ${token}` }
  }
  return config
}, (error) => Promise.reject(error))

// Response interceptor to auto-refresh on 401
apiClient.interceptors.response.use((response: AxiosResponse) => response, async (error) => {
  const originalRequest: any = error?.config
  if (error?.response?.status === 401 && !originalRequest?._retry) {
    originalRequest._retry = true
    const rt = getRefreshToken()
    if (!rt) {
      return Promise.reject(error)
    }
    try {
      if (!isRefreshing) {
        isRefreshing = true
        const resp = await refreshTokenApi(rt)
        if (resp?.accessToken) {
          setAccessToken(resp.accessToken, resp.expiresIn)
          if (resp.refreshToken) setRefreshToken(resp.refreshToken)
          onRefreshed(resp.accessToken)
          isRefreshing = false
          originalRequest.headers.Authorization = `Bearer ${resp.accessToken}`
          return apiClient(originalRequest)
        } else {
          isRefreshing = false
          clearTokens()
          return Promise.reject(error)
        }
      } else {
        // Waiting for in-flight refresh to complete
        return new Promise((resolve, reject) => {
          addRefreshSubscriber((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(apiClient(originalRequest))
          })
        })
      }
    } catch (e) {
      isRefreshing = false
      clearTokens()
      return Promise.reject(e)
    }
  }
  return Promise.reject(error)
})
