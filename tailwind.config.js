function color(name) {
  return `hsl(var(--color-${name}), <alpha-value>)`;
}

console.log(color("primary"));

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        sans: "'Inter', sans-serif",
      },
      colors: {
        primary: color("primary"),
        background: color("background"),
        background_dimmed: color("background_dimmed"),
        foreground: color("foreground"),
      },
    },
  },
  plugins: [require("@tailwindcss/typography"), require("@tailwindcss/forms")],
};
