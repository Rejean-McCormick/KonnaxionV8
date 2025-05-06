// lib/AntdRegistry.tsx
'use client';

import React, { PropsWithChildren, useMemo } from 'react';
import { useServerInsertedHTML }             from 'next/navigation';
import {
  createCache,
  extractStyle,
  StyleProvider,
}                                            from '@ant-design/cssinjs';

/**
 * AntdRegistry
 * — partage UN cache css‑in‑js global (globalThis.__ANTD_CSS_CACHE__)
 * — injecte les styles au SSR via useServerInsertedHTML
 * — réutilise exactement ce même cache côté client
 */
export default function AntdRegistry({ children }: PropsWithChildren) {
  /* -----------------------------------------------------------------
   * 1) cache unique — créé une fois puis stocké sur globalThis
   * ---------------------------------------------------------------- */
  const cache = useMemo(() => {
    if (!(globalThis as any).__ANTD_CSS_CACHE__) {
      (globalThis as any).__ANTD_CSS_CACHE__ = createCache({ key: 'antcss' });
    }
    return (globalThis as any).__ANTD_CSS_CACHE__;
  }, []);

  /* -----------------------------------------------------------------
   * 2) au SSR on extrait le CSS généré et on l’insère dans <head>
   * ---------------------------------------------------------------- */
  useServerInsertedHTML(() =>
    typeof window === 'undefined' ? (
      <style
        id="antd-css"
        dangerouslySetInnerHTML={{ __html: extractStyle(cache, true) }}
      />
    ) : null
  );

  /* -----------------------------------------------------------------
   * 3) côté client : StyleProvider avec le *même* cache
   * ---------------------------------------------------------------- */
  return (
    <StyleProvider cache={cache} hashPriority="high">
      {children}
    </StyleProvider>
  );
}
