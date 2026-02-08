import React from 'react';
import Header from './Header';
import Footer from './Footer';

export default function Layout({ children }) {
    return (
        <div className="min-h-screen flex flex-col bg-white text-slate-900 font-sans">
            <Header />
            <main className="flex-grow container mx-auto px-4 max-w-7xl">
                {children}
            </main>
            <Footer />
        </div>
    );
}
