import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import UsersPage from '../pages/Users'
import UserCreatePage from '../pages/UserCreate'
import UserEditPage from '../pages/UserEdit'
import UserDetailPage from '../pages/UserDetail'

const AdminRoutes: React.FC = () => {
  return (
    <Routes>
      <Route path="/admin/users" element={<UsersPage />} />
      <Route path="/admin/users/new" element={<UserCreatePage />} />
      <Route path="/admin/users/:id/edit" element={<UserEditPage />} />
      <Route path="/admin/users/:id" element={<UserDetailPage />} />
      <Route path="*" element={<Navigate to="/admin/users" />} />
    </Routes>
  )
}

export default AdminRoutes
