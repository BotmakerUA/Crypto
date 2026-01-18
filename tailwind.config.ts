import type { Config } from 'tailwindcss'

const config: Config = {
  darkMode: 'class',
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#FFA07A', // Light Salmon (нежно-оранжевый)
          DEFAULT: '#FF7F50', // Coral
          dark: '#FF6347', // Tomato
        },
        background: {
          light: '#FFFFFF',
          dark: '#1F2937', // темно-серый
        },
        text: {
          light: '#1F2937',
          dark: '#F9FAFB',
        },
      },
    },
  },
  plugins: [],
}
export default config
