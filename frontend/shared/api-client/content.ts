import { apiClient } from './client'
import type { ContentList, ContentItem } from '../../types/content'

// Fetch multiple contents with pagination, sorting and basic filters
export async function fetchContents(params?: {
  page?: number
  perPage?: number
  sort?: string
  folder?: string
  format?: string
  durationMin?: number
  durationMax?: number
}): Promise<ContentList> {
  const resp = await apiClient.get('/api/v1/contents', {
    params: {
      page: params?.page ?? 1,
      per_page: params?.perPage ?? 20,
      sort: params?.sort ?? 'title',
      folder: params?.folder,
      format: params?.format,
      duration_min: params?.durationMin,
      duration_max: params?.durationMax,
    },
  })
  // API might return { data: [...] } or { data: { items: [...] } }
  const data: any = resp.data?.data ?? resp.data
  // Normalize to ContentList if possible
  if (Array.isArray(data)) return data as ContentList
  if (Array.isArray(data?.items)) return data.items as ContentList
  return data as ContentList
}

// Fetch a single content by id
export async function fetchContentById(id: string): Promise<ContentItem> {
  const resp = await apiClient.get(`/api/v1/contents/${id}`)
  const data: any = resp.data?.data ?? resp.data
  return data as ContentItem
}

// Search contents by query
export async function searchContents(query: string): Promise<ContentList> {
  const resp = await apiClient.get('/api/v1/contents/search', {
    params: { q: query },
  })
  const data: any = resp.data?.data ?? resp.data
  return data as ContentList
}

// Fetch streaming URL for a content id
export async function fetchContentStreamUrl(id: string): Promise<string> {
  const resp = await apiClient.get(`/api/v1/contents/${id}/stream`)
  // Expecting { url: '...' } or { data: '...' }
  const data: any = resp.data?.data ?? resp.data
  return typeof data === 'string' ? data : data?.url
}
