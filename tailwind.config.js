/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["euanh_website/templates/**/*.jinja"],
  theme: {
    extend: {
      colors: {
        "header_green": "#9fb1b1",
        "header_green_hover": "#73a499",
      },
      fontFamily: {
        riffic: ["riffic", 'sans-serif'],
      },
      width: {
        '2/3': '66.666667%',
      }
    },
  },
  plugins: [require('@tailwindcss/typography')],
}
