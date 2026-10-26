/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          950: '#0B0B0E',
          900: '#111117',
          850: '#161622',
          800: '#1C1C2B',
          700: '#28283D',
        },
        brand: {
          violet: '#9D4EDD',
          fuchsia: '#C77DFF',
          plum: '#5A189A',
          glow: '#E0AAFF',
        }
      },
      boxShadow: {
        'glow-violet': '0 0 25px -5px rgba(157, 78, 221, 0.35)',
        'glow-subtle': '0 0 15px -3px rgba(199, 125, 255, 0.2)',
      }
    },
  },
  plugins: [],
}
