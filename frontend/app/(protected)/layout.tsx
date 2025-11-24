'use client'

import { useState, useEffect } from 'react'
import { useSessionContext } from '@supabase/auth-helpers-react'
import { useRouter, usePathname } from 'next/navigation'
import Protected from '@/components/Protected'
import Sidebar from '@/components/Sidebar'
import Header from '@/components/Header'

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  const { session, supabaseClient } = useSessionContext()
  const router = useRouter()
  const pathname = usePathname()
  
  const [currentPage, setCurrentPage] = useState('dashboard')
  const [isClient, setIsClient] = useState(false)
  const userName = session?.user.email || 'Usuário'

  useEffect(() => {
    setIsClient(true)
    
    // Set initial page based on pathname
    if (pathname.includes('/supplies')) {
      setCurrentPage('supplies')
    } else {
      setCurrentPage('dashboard')
    }
  }, [pathname])

  const handleLogout = async () => {
    try {
      await supabaseClient.auth.signOut()
      router.push('/login')
      router.refresh()
    } catch (error) {
      console.error('Error during sign out:', error)
    }
  }

  const handleNavigation = (page: string) => {
    setCurrentPage(page)
    if (page === 'dashboard') {
      router.push('/dashboard')
    } else {
      router.push(`/${page}`)
    }
  }

  // Only render the layout on the client side
  if (!isClient) {
    return null
  }

  return (
    <Protected>
      <div className="flex h-screen bg-gray-50">
        <Sidebar currentPage={currentPage} onNavigate={handleNavigation} />
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
