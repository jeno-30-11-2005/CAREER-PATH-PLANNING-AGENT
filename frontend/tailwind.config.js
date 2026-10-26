/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        rubick: {
          blue: '#1b3bbb',
          'blue-dark': '#152e95',
          'blue-light': '#3b82f6',
          canvas: '#F1F5F9',
          card: '#FFFFFF',
          border: '#E2E8F0',
          dark: '#0F172A',
          navy: '#1E293B',
          muted: '#64748B',
        }
      },
      boxShadow: {
        'rubick': '0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05)',
        'rubick-md': '0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05)',
        'rubick-lg': '0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.04)',
      }
    },
  },
  plugins: [],
}
