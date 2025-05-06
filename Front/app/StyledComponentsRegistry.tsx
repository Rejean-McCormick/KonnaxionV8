'use client'

/**
 *  Collecte des styles styled‑components côté serveur
 *  et injection dans <head>. À importer dans le layout serveur.
 */
import React, { ReactNode, useState } from 'react'
import { useServerInsertedHTML } from 'next/navigation'
import {
  ServerStyleSheet,
  StyleSheetManager,
} from 'styled-components'

export default function StyledComponentsRegistry({
  children,
}: {
  children: ReactNode
}) {
  const [sheet] = useState(() => new ServerStyleSheet())

  useServerInsertedHTML(() => {
    const styles = sheet.getStyleElement()
    sheet.instance.clearTag()          // prépare la prochaine requête
    return <>{styles}</>
  })

  return (
    <StyleSheetManager sheet={sheet.instance}>
      {children}
    </StyleSheetManager>
  )
}
