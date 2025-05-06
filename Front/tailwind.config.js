/* eslint-disable @typescript-eslint/no-var-requires */
const defaultTheme = require('tailwindcss/defaultTheme');

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // <html class="dark"> activé par ThemeContext
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      /* ------------ design‑tokens via CSS custom‑properties ------------ */
      colors: {
        /* Opacité variable grâce à <alpha-value> */
        primary : 'rgb(var(--color-primary) / <alpha-value>)',
        main    : 'rgb(var(--bg-main)      / <alpha-value>)',
        light   : 'rgb(var(--bg-light)     / <alpha-value>)',
        darkbg  : 'rgb(var(--bg-dark)      / <alpha-value>)',
        text    : 'rgb(var(--text-main)    / <alpha-value>)',
        accent  : 'rgb(var(--accent)       / <alpha-value>)',
      },
      borderRadius: {
        lg: 'var(--radius-lg)',
      },
      spacing: {
        md: 'var(--spacing-md)',
      },
      fontFamily: {
        sans: ['Inter', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [],
  future: { hoverOnlyWhenSupported: true },
};
