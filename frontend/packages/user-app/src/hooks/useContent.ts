import { useEffect, useState } from 'react'
import { fetchContents, searchContents } from '../../shared/api-client/content'
import type { ContentList } from '../../shared/types/content'

type Params = {
  page?: number
  perPage?: number
  sort?: string
  folder?: string
  format?: string
  durationMin?: number
  durationMax?: number
  query?: string
}

// Hook to fetch contents with optional search and filters
export function useContent(params?: Params) {
  const [contents, setContents] = useState<ContentList>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)
  const [total, setTotal] = useState<number | undefined>(undefined)

  useEffect(() => {
    let cancelled = false
    setLoading(true)

    const fetcher = (params?.query && params.query.length > 0)
      ? searchContents(params.query)
      : fetchContents({
          page: params?.page,
          perPage: params?.perPage,
          sort: params?.sort,
          folder: params?.folder,
          format: params?.format,
          durationMin: params?.durationMin,
          durationMax: params?.durationMax,
        } as any)

    fetcher
      .then((data: any) => {
        if (!cancelled) {
          const list = Array.isArray(data) ? data : (data as ContentList)
          setContents(list)
          // Attempt to derive total from API response if available
          const totalFromData = (data && typeof data === 'object') ? (data.total ?? (data as any).totalItems ?? undefined) : undefined
          if (typeof totalFromData === 'number') setTotal(totalFromData)
        }
      })
      .catch((e) => {
        if (!cancelled) setError(e as Error)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })

    return () => {
      cancelled = true
    }
  }, [params?.page, params?.perPage, params?.sort, params?.folder, params?.format, params?.durationMin, params?.durationMax, params?.query])

  return { items: contents, loading, error, total }
}
