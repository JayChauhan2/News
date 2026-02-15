import React from 'react';
import Header from './Header';
import Footer from './Footer';

export default function Layout({ children }) {
    return (
        <div className="min-h-screen flex flex-col bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 font-serif transition-colors duration-300">
            <Header />
            <main className="flex-grow container mx-auto px-4 max-w-7xl">
                {children}
            </main>
            <Footer />
        </div>
    );
}
