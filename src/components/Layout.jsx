import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';
import Footer from './Footer';

const Layout = () => {
    return (
        <div className="min-h-screen bg-white text-black font-serif selection:bg-blue-100">
            <Header />
            <main className="max-w-7xl mx-auto px-4 md:px-8">
                <Outlet />
            </main>
            <Footer />
        </div>
    );
};

export default Layout;
