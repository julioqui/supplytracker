'use client'

import { useState, useEffect } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { useSessionContext } from '@supabase/auth-helpers-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Warehouse } from 'lucide-react'
import { FcGoogle } from 'react-icons/fc'

export default function LoginPage() {
  const { session, supabaseClient, isLoading } = useSessionContext()
  const router = useRouter()
  const searchParams = useSearchParams()
  const errorMsg = searchParams.get('error')

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(errorMsg)

  const baseUrl = process.env.NEXT_PUBLIC_URL

  // Redirect if already logged in
  useEffect(() => {
    if (!isLoading && session) {
      router.push('/dashboard')
    }
  }, [session, isLoading, router])

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const { error: loginError } = await supabaseClient.auth.signInWithPassword({
        email,
        password,
      })

      if (loginError) throw loginError
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (isLoading || session) {
    return <p className="text-center mt-20">Carregando...</p>
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-purple-50 to-blue-50 p-4">
      <Card className="w-full max-w-md shadow-lg border-0">
        <CardHeader className="space-y-4 text-center">
          <div className="mx-auto w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center">
            <Warehouse className="w-8 h-8 text-purple-600" />
          </div>
          <CardTitle className="text-2xl font-bold text-gray-800">SupplyTracker</CardTitle>
        </CardHeader>

        <CardContent>
          <form onSubmit={handleLogin} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="seu@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">Senha</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            {error === 'Invalid login credentials' && <p className="text-red-500 text-sm text-center">Login ou senha inválidos</p>}

            <div className="space-y-3">
              <Button
                type="submit"
                className="w-full bg-purple-600 hover:bg-purple-700 transition"
                disabled={loading}
              >
                {loading ? 'Entrando...' : 'Entrar'}
              </Button>

              <div className="flex items-center">
                <div className="flex-grow h-px bg-gray-300"></div>
                <span className="px-3 text-sm text-gray-500">ou</span>
                <div className="flex-grow h-px bg-gray-300"></div>
              </div>

              <Button
                type="button"
                variant="outline"
                className="w-full flex items-center justify-center gap-2 border-gray-300"
                onClick={() =>
                  supabaseClient.auth.signInWithOAuth({
                    provider: 'google',
                    options: {
                      redirectTo: `${baseUrl}/auth/callback`,
                    },
                  })
                }
              >
                <FcGoogle className="w-5 h-5" />
                Fazer login com o Google
              </Button>
            </div>

            {error === 'access_denied' && <p className="text-red-500 text-sm text-center">Acesso negado. Entre em contato com o administrador.</p>}
          </form>
        </CardContent>
      </Card>
    </div>
  )
}
