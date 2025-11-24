'use client'

import { useEffect, useState } from 'react'
import { useSessionContext } from '@supabase/auth-helpers-react'
import { useRouter } from 'next/navigation'
import Protected from '@/components/Protected'

interface UserMe {
  id: string
  email: string
  role?: string
}

export default function DashboardPage() {
  const { session, isLoading } = useSessionContext()
  const router = useRouter()
  const [userData, setUserData] = useState<UserMe | null>(null)
  const [loadingUser, setLoadingUser] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!isLoading && !session) {
      router.push('/') // Redirect to login if not logged in
      return
    }

    if (session) {
      const fetchUser = async () => {
        setLoadingUser(true)
        setError(null)

        try {
          const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
            headers: {
              Authorization: `Bearer ${session.access_token}`,
              'Content-Type': 'application/json',
            },
          })

          if (!res.ok) {
            const text = await res.text()
            throw new Error(`Erro ao buscar usuário: ${res.status} - ${text}`)
          }

          const data = await res.json()
          setUserData(data)
        } catch (err: any) {
          setError(err.message)
        } finally {
          setLoadingUser(false)
        }
      }

      fetchUser()
    }
  }, [session, isLoading, router])

  return (
    <Protected>
      <div className="p-6">
        <h1 className="text-2xl font-bold mb-4">Dashboard</h1>

        {loadingUser && <p>Carregando dados do usuário...</p>}

        {error && <p className="text-red-500">{error}</p>}

        {userData && (
          <div>
            <p><strong>ID:</strong> {userData.id}</p>
            <p><strong>Email:</strong> {userData.email}</p>
            {userData.role && <p><strong>Role:</strong> {userData.role}</p>}
          </div>
        )}
      </div>
    </Protected>
  )
}
