'use client'

import { useState } from 'react'
import { useSessionContext } from '@supabase/auth-helpers-react'
import { useRouter } from 'next/navigation'
import Protected from '@/components/Protected'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { session, supabaseClient } = useSessionContext()
  const router = useRouter()

  const [currentPage, setCurrentPage] = useState('dashboard')
  const userName = session?.user.email || 'Usuário'

  const handleLogout = async () => {
    await supabaseClient.auth.signOut()
    router.push('/login')
  }

  return (
    <Protected>
      <div className="flex h-screen bg-gray-50">
        <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />

        <div className="flex-1 flex flex-col overflow-hidden">
          <Header userName={userName} onLogout={handleLogout} />

          <main className="flex-1 overflow-y-auto p-6">
            {children}
          </main>
        </div>
      </div>
    </Protected>
  )
}
