/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./MiniTrello/**/*.html"
  ],
  theme: {
    extend: {
      fontFamily: {
        "roboto": ["Roboto", "sans-serif"],
        "roboto-mono": ["Roboto Mono", "monospace"]
      }
    },
  },
  plugins: [
    require("daisyui")
  ],
  daisyui: {
    themes: ["lemonade", "forest"],
  },
}
