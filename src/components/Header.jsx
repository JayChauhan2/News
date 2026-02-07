import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const CATEGORIES = [
    "World", "Business", "U.S.", "Politics", "Economy", "Tech",
    "Markets", "Opinion", "Arts", "Life", "Real Estate", "Sports"
];

const Header = () => {
    const location = useLocation();
    const today = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });

    return (
        <header className="bg-white">
            {/* Top Bar: Date & Edition */}
            <div className="border-b border-gray-100 py-2">
                <div className="container flex justify-between items-center text-[9px] uppercase font-bold tracking-widest font-sans text-gray-500">
                    <div>{today}</div>
                    <div>AI Edition</div>
                </div>
            </div>

            {/* Main Logo Area */}
            <div className="py-8 border-b border-black">
                <div className="container text-center">
                    <Link to="/" className="inline-block group">
                        <h1 className="font-headline text-5xl lg:text-7xl font-black tracking-tighter leading-none mb-2">
                            THE DAILY AGENT.
                        </h1>
                        <div className="text-[10px] font-sans font-bold uppercase tracking-[0.2em] text-gray-400 group-hover:text-[#0274b6] transition-colors">
                            The Newspaper of the Artificial Intelligence Age
                        </div>
                    </Link>
                </div>
            </div>

            {/* Navigation Bar */}
            <nav className="border-b-4 border-double border-gray-200 sticky top-0 bg-white/95 backdrop-blur-sm z-50">
                <div className="container overflow-x-auto no-scrollbar">
                    <ul className="flex justify-center items-center gap-6 py-3 min-w-max px-4">
                        <li>
                            <Link
                                to="/"
                                className={`text-[11px] font-sans font-bold uppercase tracking-wider hover:text-[#0274b6] transition-colors ${location.pathname === '/' ? 'text-black' : 'text-gray-500'}`}
                            >
                                Home
                            </Link>
                        </li>
                        {CATEGORIES.map(cat => (
                            <li key={cat}>
                                <Link
                                    to={`/category/${cat}`}
                                    className={`text-[11px] font-sans font-bold uppercase tracking-wider hover:text-[#0274b6] transition-colors ${decodeURIComponent(location.pathname) === `/category/${cat}` ? 'text-black' : 'text-gray-500'}`}
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
