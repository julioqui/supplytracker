import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'

export async function getAuthToken() {
  const supabase = createClientComponentClient()
  const { data: { session } } = await supabase.auth.getSession()
  return session?.access_token
}
