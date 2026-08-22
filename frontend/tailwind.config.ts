import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{ts,tsx}', './components/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink:   { DEFAULT: '#0B1622', soft: '#12212F', line: '#1E3145' },
        paper: { DEFAULT: '#F7F8F7', card: '#FFFFFF', line: '#DFE3E1' },
        sea:   { DEFAULT: '#12566B', deep: '#0E3E4E', pale: '#E4EEF1' },
        rust:  { DEFAULT: '#9A4A21', pale: '#F6EAE3' },
        moss:  { DEFAULT: '#3F6B4A', pale: '#E7EFE8' },
      },
      fontFamily: {
        sans: ['ui-sans-serif', 'system-ui', '-apple-system', 'Segoe UI', 'Helvetica Neue', 'Arial', 'sans-serif'],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      },
      maxWidth: { prose: '68ch' },
    },
  },
  plugins: [],
};
export default config;
