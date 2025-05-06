'use client'

import type { ReactNode } from 'react'
import MainLayout     from '@/components/layout-components/MainLayout'
import { ThemeProvider } from '@/context/ThemeContext'

/**
 *  Fournit :
 *    – ThemeProvider (couleurs + ConfigProvider AntD)
 *    – MainLayout qui entoure la page
 *
 *  ⚠️ Plus de StyleProvider ici : déjà fait par AntdRegistry dans le layout
 *  ⚠️ Plus de ConfigProvider ici : déjà inclus dans ThemeProvider
 */
export default function ClientProviders({ children }: { children: ReactNode }) {
  return (
    <ThemeProvider>
      <MainLayout>{children}</MainLayout>
    </ThemeProvider>
  )
}
