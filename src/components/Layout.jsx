import React from 'react';
import Header from './Header';
import Footer from './Footer';
import { Outlet } from 'react-router-dom';

export default function Layout() {
    return (
        <div className="min-h-screen flex flex-col bg-paper">
            <Header />
            <main className="flex-grow container mx-auto px-4 md:px-8 py-8 max-w-7xl">
                <Outlet />
            </main>
            <Footer />
        </div>
    );
}
