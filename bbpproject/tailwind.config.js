/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./bbpproject/templates/**/*.html",
    "./bbpproject/**/*.js",
    "./core/templates/**/*.html",
    "./product/templates/**/*.html",
    "./users/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          50: '#fefdf4',
          100: '#fffae8',
          200: '#fff5cc',
          300: '#fff1b3',
          400: '#f4e5c3',
          500: '#e6d5a8',
          600: '#d4af37',
          700: '#b8941e',
          800: '#9c7a1f',
          900: '#7a5d18',
        },
      },
      fontFamily: {
        serif: ['Playfair Display', 'serif'],
        sans: ['Poppins', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
