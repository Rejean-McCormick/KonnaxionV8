/* -----------------------------------------------------------------------
   app/layout.tsx – root layout (SERVER COMPONENT)
   --------------------------------------------------------------------- */

import type { ReactNode } from 'react'
import '@/styles/tailwind.css'

import StyledComponentsRegistry from './StyledComponentsRegistry'
import AntdRegistry             from '@/lib/AntdRegistry'   // ← de retour
import ClientProviders          from './ClientProviders'

/* —— SEO / métadonnées optionnelles ————————— */
export const metadata = {
  title      : 'Mon application',
  description: 'Démo App Router + styled‑components + Ant Design',
}


console.log('[layout] server render');

/* —— Root Layout ————————— */
export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="fr">
      <body>
        <StyledComponentsRegistry>
          {/* 1 seul StyleProvider + cache partagé, injecté par AntdRegistry */}
          <AntdRegistry>
            <ClientProviders>{children}</ClientProviders>
          </AntdRegistry>
        </StyledComponentsRegistry>
      </body>
    </html>
  )
}
