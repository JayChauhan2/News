/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                serif: ['"Playfair Display"', 'Georgia', 'serif'],
                sans: ['"Inter"', 'system-ui', 'sans-serif'],
            },
            colors: {
                primary: '#111111', // Deep Rich Black
                secondary: '#555555', // Neutral Dark Gray for subtext
                accent: '#8B0000', // Deep Dark Red (Premium news feel)
                paper: '#FDFBF7', // "Newsprint" Off-white
                'news-black': '#0a0a0a', // Almost black
                'news-gray': '#e5e5e5', // Light gray for borders/backgrounds
                'border-light': '#d1d5db', // Subtle borders
            },
            animation: {
                'fade-in': 'fadeIn 0.5s ease-out forwards',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
            spacing: {
                '18': '4.5rem',
            }
        },
    },
    plugins: [],
}
