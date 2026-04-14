import { useEffect, useState } from "react";

export type Permission = {
  id: string;
  name: string;
  description?: string;
};

export const usePermissions = () => {
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAll = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/permissions/", {
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error("Failed to fetch permissions");
      const data = await res.json();
      setPermissions(Array.isArray(data) ? data : []);
    } catch (e: any) {
      setError(e?.message ?? String(e));
    } finally {
      setLoading(false);
    }
  };

  const create = async (payload: { name: string; description?: string }) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/v1/permissions/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("Failed to create permission");
      const data = await res.json();
      // refresh list
      await fetchAll();
      return data as Permission;
    } catch (e: any) {
      setError(e?.message ?? String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  const remove = async (permissionId: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/v1/permissions/${permissionId}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete permission");
      await fetchAll();
    } catch (e: any) {
      setError(e?.message ?? String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  // Load on mount
  useEffect(() => {
    fetchAll();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load user-specific permissions if needed
  const fetchUserPermissions = async (userId: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/v1/permissions/users/${userId}`, {
        headers: { "Content-Type": "application/json" },
      });
      if (!res.ok) throw new Error("Failed to fetch user permissions");
      const data = await res.json();
      return Array.isArray(data) ? data as Permission[] : [];
    } catch (e: any) {
      setError(e?.message ?? String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  const updateUserPermissions = async (userId: string, permissionIds: string[]) => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/v1/permissions/users/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ permissions: permissionIds }),
      });
      if (!res.ok) throw new Error("Failed to update user permissions");
      // refresh? caller may re-fetch
      return;
    } catch (e: any) {
      setError(e?.message ?? String(e));
      throw e;
    } finally {
      setLoading(false);
    }
  };

  return {
    permissions,
    loading,
    error,
    fetchAll,
    create,
    remove,
    fetchUserPermissions,
    updateUserPermissions,
  };
};
