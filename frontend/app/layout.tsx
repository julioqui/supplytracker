import Providers from '../providers'
import './globals.css'

export const metadata = {
  title: 'Supply Tracker',
  description: 'Sistema de gestão de insumos',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
