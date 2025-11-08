'use client'

import { useSessionContext } from '@supabase/auth-helpers-react'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Protected({ children }: { children: React.ReactNode }) {
  const { session, isLoading } = useSessionContext()
  const router = useRouter()
  const user = session?.user

  useEffect(() => {
    if (!isLoading && !user) router.push('/')
  }, [user, isLoading, router])

  if (isLoading) return <p>Carregando...</p>
  if (!user) return null

  return <>{children}</>
}
