import { useEffect, useState } from 'react';
import { Folder } from '../../../../shared/types/content';
import { getFolders as apiGetFolders, createFolder as apiCreateFolder, updateFolder as apiUpdateFolder, deleteFolder as apiDeleteFolder } from '../../../../shared/api-client/folders';

export const useFolders = () => {
  const [folders, setFolders] = useState<Folder[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const fetchFolders = async () => {
    setLoading(true);
    try {
      const res = await apiGetFolders?.();
      setFolders(res?.data ?? []);
    } catch {
      // ignore for brevity; in real app show error
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFolders();
  }, []);

  // simple create/update/delete wrappers (no optimistic UI here)
  const createFolderFn = async (payload: any) => apiCreateFolder?.(payload).then(() => fetchFolders());
  const updateFolderFn = async (id: string, payload: any) => apiUpdateFolder?.(id, payload).then(() => fetchFolders());
  const deleteFolderFn = async (id: string) => apiDeleteFolder?.(id).then(() => fetchFolders());

  return { folders, loading, fetchFolders, createFolder: createFolderFn, updateFolder: updateFolderFn, deleteFolder: deleteFolderFn };
};

export default useFolders;
