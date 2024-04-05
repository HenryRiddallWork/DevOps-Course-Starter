/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./todo_app/**/*.{html,js}"],
  theme: {
    extend: {
      keyframes: {
        jump: {
          "0%, 100%": {
            transform: "translateY(0)",
          },
          "33%": {
            transform: "translateY(20px)",
          },
          "33%": {
            transform: "translateY(-20px)",
          },
        },
      },
      animation: {
        jump: "jump 0.7s ease normal",
      },
    },
  },
  plugins: [],
};
