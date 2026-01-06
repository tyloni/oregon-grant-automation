export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // New England Patriots Color Scheme
        primary: {
          50: '#E8EAF0',   // Light navy background
          100: '#C5CAD9',
          200: '#9FA7C2',
          300: '#7984AB',
          400: '#5C6B9A',
          500: '#002244',   // Patriots Navy (main)
          600: '#001D3A',
          700: '#00172E',   // Dark navy (hover)
          800: '#001122',
          900: '#000B16',
        },
        accent: {
          50: '#FCE8E8',
          100: '#F7C5C5',
          200: '#F29E9E',
          300: '#ED7777',
          400: '#E95A5A',   // Patriots Red (main)
          500: '#C60C30',
          600: '#B00B2A',   // Deep red
          700: '#9A0924',
          800: '#84081E',
          900: '#6E0619',
        }
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        'display': ['Poppins', 'Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
