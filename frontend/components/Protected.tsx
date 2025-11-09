'use client'

import { useSessionContext } from '@supabase/auth-helpers-react'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export default function Protected({ children }: { children: React.ReactNode }) {
  const { session, isLoading } = useSessionContext()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !session) {
      router.replace('/login')
    }
  }, [session, isLoading, router])

  if (isLoading) return <p className="text-center mt-20">Carregando...</p>
  if (!session) return null

  return <>{children}</>
}
