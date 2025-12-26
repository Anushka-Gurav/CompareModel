/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'],
  content: [
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        heading: ['Space Grotesk', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        background: '#09090b',
        surface: '#18181b',
        surfaceHighlight: '#27272a',
        border: '#27272a',
        primary: '#4ade80',
        'primary-foreground': '#022c22',
        secondary: '#a78bfa',
        'secondary-foreground': '#2e1065',
        accent: '#facc15',
        textMain: '#f4f4f5',
        textMuted: '#a1a1aa',
        success: '#22c55e',
        error: '#ef4444',
        warning: '#f59e0b',
      },
      borderRadius: {
        lg: '0.5rem',
        md: '0.375rem',
        sm: '0.25rem',
      },
      boxShadow: {
        glow: '0 0 15px rgba(74, 222, 128, 0.3)',
        'glow-purple': '0 0 15px rgba(167, 139, 250, 0.3)',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}