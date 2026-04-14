import React from 'react'
import { Box, Typography, Card, CardContent } from '@mui/material'
import { Layout } from '../../../shared/components/Layout'
import UserForm from '../components/UserForm'
import { useNavigate } from 'react-router-dom'
import { createUser } from '../../../shared/api-client/users'

const UserCreatePage: React.FC = () => {
  const navigate = useNavigate()
  const handleSubmit = async (payload: any) => {
    try {
      // Use API client to create user
      await createUser(payload)
      navigate('/admin/users')
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <Layout>
      <Typography variant="h5" gutterBottom>Create User</Typography>
      <Card>
        <CardContent>
          <UserForm onSubmit={handleSubmit} onCancel={() => navigate(-1)} />
        </CardContent>
      </Card>
    </Layout>
  )
}

export default UserCreatePage
