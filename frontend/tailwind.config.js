/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html",
  ],
  theme: {
    extend: {
      colors: {
        // Primary colors
        'primary-blue': '#4DA8DA', // Electric Sky Blue
        'primary-white': '#FFFFFF', // Pure White
        
        // Secondary colors
        'secondary-navy': '#0A2342', // Deep Navy
        'secondary-grey': '#B4BCC2', // Soft Slate Grey
        'secondary-mint': '#E6F7F9', // Mint Tint
        
        // Accent colors
        'accent-green': '#7ED957', // Lime Green (success)
        'accent-red': '#FF6B6B', // Salmon Red (error)
      },
    },
  },
  plugins: [],
}
