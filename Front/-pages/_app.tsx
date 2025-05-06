// pages/_app.tsx
import '@/styles/tailwind.css';

import type { AppProps, NextPage } from 'next/app';
import React from 'react';
import { ConfigProvider, theme as antdTheme } from 'antd';

import { ThemeProvider, useTheme } from '@/context/ThemeContext';
import MainLayout from '@/components/layout-components/MainLayout';

/* ——— helper types ———————————————————————————— */
type NextPageWithLayout = NextPage & {
  /** supply a custom layout or return just `page` to skip MainLayout */
  getLayout?: (page: React.ReactElement) => React.ReactNode;
};

type AppPropsWithLayout = AppProps & {
  Component: NextPageWithLayout;
};

/* ——— Ant Design provider (re-renders on theme change) ——— */
const AntdProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { theme } = useTheme(); // ← tokens chosen by the user

  return (
    <ConfigProvider
      theme={{
        algorithm: antdTheme.defaultAlgorithm,
        token    : theme,         // ← inject palette (incl. colorBgElevated)
      }}
    >
      {children}
    </ConfigProvider>
  );
};

/* ——— application root ———————————————————————————— */
function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  const defaultGetLayout = (page: React.ReactElement) => (
    <MainLayout>{page}</MainLayout>
  );
  const getLayout = Component.getLayout ?? defaultGetLayout;

  return (
    <ThemeProvider>
      <AntdProvider>{getLayout(<Component {...pageProps} />)}</AntdProvider>
    </ThemeProvider>
  );
}

export default MyApp;
