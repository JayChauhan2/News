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
            <footer className="border-t border-gray-300 mt-20 py-8 bg-white">
                <div className="container text-center">
                    <div className="font-sans text-[10px] text-gray-400 uppercase tracking-widest">
                        Copyright &copy; {new Date().getFullYear()} The Daily Agent. All Rights Reserved.
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
