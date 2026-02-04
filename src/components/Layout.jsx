import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header';

const Layout = () => {
    return (
        <div className="min-h-screen bg-white">
            <Header />
            <main className="container py-8">
                <Outlet />
            </main>

            {/* Simple Footer */}
            <footer className="border-t border-gray-200 mt-20 py-8 bg-gray-50">
                <div className="container text-center">
                    <div className="font-serif text-2xl font-bold mb-4">THE DAILY AGENT.</div>
                    <div className="text-xs font-sans text-gray-500 uppercase tracking-widest mb-4">
                        Copyright &copy; {new Date().getFullYear()} The Daily Agent. All Rights Reserved.
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
