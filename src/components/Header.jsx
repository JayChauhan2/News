import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    const currentDate = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
    });

    return (
        <header className="border-b-4 border-black mb-8">
            {/* Top Bar with Login/Subscribe placeholders found in WSJ */}
            <div className="flex justify-between items-center py-1 px-4 border-b border-gray-300 text-xs font-sans uppercase tracking-wider">
                <div className="flex gap-4">
                    <span>English Edition</span>
                    <span>Today's Paper</span>
                </div>
                <div className="flex gap-4">
                    <span className="cursor-pointer hover:underline">Sign In</span>
                    <span className="font-bold cursor-pointer hover:underline">Subscribe</span>
                </div>
            </div>

            {/* Main Branding */}
            <div className="py-6 text-center">
                <Link to="/" className="no-underline text-black">
                    <h1 className="text-5xl md:text-7xl font-serif font-black tracking-tight mb-2">
                        The News Journal
                    </h1>
                </Link>
                <div className="flex justify-center items-center gap-4 text-sm font-sans text-gray-600 border-t border-b border-gray-200 py-2 mt-4 mx-4 md:mx-auto max-w-6xl">
                    <span className="font-bold text-black uppercase">{currentDate}</span>
                    <span className="hidden md:inline">|</span>
                    <span className="hidden md:inline">Business & Finance News</span>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex justify-center py-3 border-b border-black md:mx-4">
                <ul className="flex gap-8 font-sans font-bold text-sm uppercase tracking-widest">
                    <li>
                        <Link to="/" className="hover:text-gray-600 transition-colors">Home</Link>
                    </li>
                    <li>
                        <Link to="/writers" className="hover:text-gray-600 transition-colors">Writers</Link>
                    </li>
                    <li>
                        <span className="text-gray-400 cursor-not-allowed">Opinion</span>
                    </li>
                    <li>
                        <span className="text-gray-400 cursor-not-allowed">Market</span>
                    </li>
                    <li>
                        <span className="text-gray-400 cursor-not-allowed">Tech</span>
                    </li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;
