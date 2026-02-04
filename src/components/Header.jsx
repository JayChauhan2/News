import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const CATEGORIES = [
    "World", "Business", "U.S.", "Politics", "Economy", "Tech",
    "Markets & Finance", "Opinion", "Free Expression", "Arts",
    "Lifestyle", "Real Estate", "Personal Finance", "Health", "Style", "Sports"
];

const Header = () => {
    const location = useLocation();
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });

    return (
        <header className="font-sans">
            {/* Top Bar: Date */}
            <div className="bg-white border-b border-gray-200 py-1">
                <div className="container flex justify-between items-center text-[10px] uppercase font-bold tracking-widest text-gray-500">
                    <div>{today}</div>
                    <div className="flex gap-4">
                        {/* Functional links can go here later */}
                    </div>
                </div>
            </div>

            {/* Main Logo Area */}
            <div className="py-6 text-center border-b border-black relative">
                <Link to="/" className="inline-block group">
                    <h1 className="font-serif text-4xl lg:text-6xl font-black tracking-tight leading-none group-hover:opacity-90 transition-opacity">
                        THE DAILY AGENT.
                    </h1>
                </Link>
                <div className="hidden lg:block absolute right-0 bottom-6 text-xs font-bold text-gray-400 uppercase tracking-widest pr-4">
                    AI Edition
                </div>
            </div>

            {/* Navigation Bar */}
            <nav className="border-b border-gray-200 shadow-sm sticky top-0 bg-white z-50">
                <div className="container overflow-hidden">
                    <ul className="flex items-center gap-6 overflow-x-auto no-scrollbar py-3 text-xs font-bold uppercase tracking-wider whitespace-nowrap mask-linear-fade">
                        <li className="flex-shrink-0">
                            <Link
                                to="/"
                                className={`hover:text-[#0274b6] transition-colors ${location.pathname === '/' ? 'text-black border-b-2 border-black pb-3' : 'text-gray-600'}`}
                            >
                                Home
                            </Link>
                        </li>
                        {CATEGORIES.map(cat => (
                            <li key={cat} className="flex-shrink-0">
                                <Link
                                    to={`/category/${cat}`}
                                    className={`hover:text-[#0274b6] transition-colors ${decodeURIComponent(location.pathname) === `/category/${cat}` ? 'text-black border-b-2 border-black pb-3' : 'text-gray-600'}`}
                                >
                                    {cat}
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            </nav>
        </header>
    );
};

export default Header;
