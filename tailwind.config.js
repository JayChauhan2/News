export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                serif: ['Escrow', 'Georgia', 'Times New Roman', 'serif'],
                sans: ['Retina', 'Arial', 'Helvetica', 'sans-serif'],
            },
            colors: {
                wsj: {
                    blue: '#0274b6'
                }
            }
        },
        container: {
            center: true,
            padding: '1rem',
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
        // require('@tailwindcss/forms'), // Optional, add if needed
    ],
}
