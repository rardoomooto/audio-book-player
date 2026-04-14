import React from 'react'
import { Box, Card, CardContent, Typography } from '@mui/material'
import { Layout } from '../../../shared/components/Layout'
import { useParams } from 'react-router-dom'
import { getUser } from '../../shared/api-client/users'

const UserDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const [user, setUser] = React.useState<any>(null)
  React.useEffect(() => {
    if (!id) return
    ;(async () => {
      try {
        const u = await getUser(id)
        setUser(u)
      } catch (e) {
        console.error(e)
      }
    })()
  }, [id])

  if (!user) return (
    <Layout><Box p={4}><Typography>Loading...</Typography></Box></Layout>
  )

  return (
    <Layout>
      <Typography variant="h5" gutterBottom>User Detail</Typography>
      <Card>
        <CardContent>
          <Typography variant="body1">Username: {user.username}</Typography>
          <Typography variant="body1">Email: {user.email}</Typography>
          <Typography variant="body1">Role: {user.role}</Typography>
          <Typography variant="body1">Status: {user.status}</Typography>
        </CardContent>
      </Card>
    </Layout>
  )
}

export default UserDetailPage
