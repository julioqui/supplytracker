'use client'

import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'
import { useRouter, useSearchParams } from 'next/navigation'
import { useEffect } from 'react'

export default function RootPage() {
  const router = useRouter()
  const supabase = createClientComponentClient()
  const searchParams = useSearchParams()

  useEffect(() => {
    const checkSession = async () => {
      const { data: { session } } = await supabase.auth.getSession()
      const error = searchParams.get('error')
      if (error) {
        router.push(`/login?error=${encodeURIComponent(error)}`)
        return
      }
      router.push(session ? '/dashboard' : '/login')
    }

    checkSession()
  }, [router, supabase, searchParams])

  return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
    </div>
  )
}
