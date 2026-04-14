import { useEffect, useMemo, useState } from 'react';
import { Content } from '../../../../shared/types/content';
import { getContents as apiGetContents, deleteContent as apiDeleteContent, scanContent as apiScanContent, getContent as apiGetContent } from '../../../../shared/api-client/content';

type FetchParams = {
  page?: number;
  pageSize?: number;
  search?: string;
  folderId?: string;
  sort?: string;
  order?: 'asc'|'desc';
};

export const useContents = () => {
  const [contents, setContents] = useState<Content[]>([]);
  const [total, setTotal] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState<number>(0);
  const [pageSize, setPageSize] = useState<number>(10);

  const fetchContents = async (params: FetchParams = {}) => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiGetContents({ page: params.page ?? page, pageSize: params.pageSize ?? pageSize, search: params.search ?? '', folderId: params.folderId ?? '', sort: params.sort ?? 'addedAt', order: params.order ?? 'desc' });
      setContents(res.data ?? []);
      setTotal(res.total ?? 0);
      setPage(params.page ?? page);
      setPageSize(params.pageSize ?? pageSize);
    } catch (e) {
      setError('Failed to load contents.');
    } finally {
      setLoading(false);
    }
  };

  // initial fetch
  useEffect(() => {
    fetchContents({});
    // eslint-disable-next-line
  }, []);

  // simple re-export for direct calls from UI
  return {
    contents,
    total,
    loading,
    error,
    fetchContents,
    setQuery: (q: string) => {},
  };
};
