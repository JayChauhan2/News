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
            <footer className="border-t-4 border-double border-gray-300 mt-20 py-12 bg-white">
                <div className="container text-center">
                    <div className="font-serif text-3xl font-bold mb-6 tracking-tight">THE DAILY AGENT.</div>
                    <div className="flex justify-center gap-6 text-[10px] font-sans font-bold uppercase tracking-widest text-gray-400 mb-6">
                        <a href="#" className="hover:text-black">Subscribe</a>
                        <a href="#" className="hover:text-black">About Us</a>
                        <a href="#" className="hover:text-black">Contact</a>
                        <a href="#" className="hover:text-black">Privacy Policy</a>
                    </div>
                    <div className="text-[10px] font-sans text-gray-400 uppercase tracking-widest">
                        Copyright &copy; {new Date().getFullYear()} The Daily Agent. All Rights Reserved.
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default Layout;
