import React, { useEffect, useState } from 'react'
import { Box, Card, CardContent, Typography } from '@mui/material'
import { Layout } from '../../../shared/components/Layout'
import UserForm from '../components/UserForm'
import { useParams } from 'react-router-dom'
import { getUser, updateUser } from '../../shared/api-client/users'

const UserEditPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [initial, setInitial] = useState<any>({})
  useEffect(() => {
    if (!id) return
    ;(async () => {
      try {
        const u = await getUser(id)
        setInitial({ username: u.username, email: u.email, role: u.role as string })
      } catch (e) {
        console.error(e)
      }
    })()
  }, [id])

  const handleSubmit = async (payload: any) => {
    if (!id) return
    await updateUser(id, payload)
  }

  return (
    <Layout>
      <Typography variant="h5" gutterBottom>Edit User</Typography>
      <Card>
        <CardContent>
          <UserForm initial={initial} onSubmit={handleSubmit} onCancel={() => window.history.back()} isEdit />
        </CardContent>
      </Card>
    </Layout>
  )
}

export default UserEditPage
