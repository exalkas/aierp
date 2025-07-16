/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    // Scan shared UI source files for Tailwind classes
    "../../packages/shared/ui/src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "maritime-blue": "#0066CC",
        "maritime-yellow": "#FFF700",
      },
    },
  },
  plugins: [],
};
