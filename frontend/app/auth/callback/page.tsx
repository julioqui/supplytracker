'use client'

import { useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useSessionContext } from '@supabase/auth-helpers-react'

export default function AuthCallbackPage() {
  const { supabaseClient } = useSessionContext()
  const router = useRouter()
  const searchParams = useSearchParams()

  useEffect(() => {
    const exchangeSession = async () => {
      const code = searchParams.get('code')
      if (code) {
        // Exchanges the "authorization code" for a session
        const { data, error } = await supabaseClient.auth.exchangeCodeForSession(code)
        if (error) {
          console.error('Error exchanging code for session:', error)
          router.push('/login')
          return
        }
        // Redirects to dashboard after login
        router.push('/dashboard')
      } else {
        router.push('/login')
      }
    }

    exchangeSession()
  }, [supabaseClient, router, searchParams])

  return <p className="text-center mt-20">Processando login...</p>
}
