import { useState, useCallback, useEffect } from 'react'

export function useApi<T>(callApi: () => Promise<T>, deps: any[] = []) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [error, setError] = useState<any>(null)

  const fetch = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const result = await callApi()
      setData(result)
    } catch (e) {
      setError(e)
    } finally {
      setLoading(false)
    }
  }, deps) // eslint-disable-line

  useEffect(() => {
    fetch()
  }, [fetch])

  const refetch = useCallback(() => fetch(), [fetch])

  return { data, loading, error, refetch }
}
