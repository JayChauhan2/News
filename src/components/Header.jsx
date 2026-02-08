import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, Search, ChevronDown } from 'lucide-react';

export default function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const location = useLocation();
    const date = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' });

    const navLinks = [
        { name: 'World', path: '/category/world' },
        { name: 'U.S.', path: '/category/us' },
        { name: 'Politics', path: '/category/politics' },
        { name: 'Business', path: '/category/business' },
        { name: 'Tech', path: '/category/technology' },
        { name: 'Science', path: '/category/science' },
        { name: 'Health', path: '/category/health' },
        { name: 'Sports', path: '/category/sports' },
        { name: 'Opinion', path: '/category/opinion' },
    ];

    const isActive = (path) => {
        if (path === '/' && location.pathname !== '/') return false;
        return location.pathname.startsWith(path);
    };

    return (
        <header className="bg-paper flex flex-col font-sans z-50">
            {/* Top Utility Bar */}
            <div className="bg-white/50 border-b border-black/5 text-[10px] md:text-xs py-1 px-4 flex justify-between items-center tracking-wider text-secondary">
                <div className="flex items-center space-x-4">
                    <span className="font-bold text-primary">{date}</span>
                    <span className="hidden md:inline">Today’s Paper</span>
                </div>
                <div className="flex items-center space-x-4">
                    <span className="hover:text-primary cursor-pointer transition-colors">U.S. Edition</span>
                    <span className="hover:text-primary cursor-pointer transition-colors">Log In</span>
                </div>
            </div>

            <div className="container mx-auto px-4 md:px-8 max-w-7xl">
                {/* Main Masthead Area */}
                <div className="flex justify-between items-center py-6 md:py-8 relative">
                    {/* Mobile Menu & Search */}
                    <div className="flex md:hidden items-center space-x-4 absolute left-0">
                        <button onClick={() => setIsMenuOpen(!isMenuOpen)} className="text-primary">
                            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
                        </button>
                    </div>

                    {/* Branding - Centered */}
                    <div className="flex-1 flex justify-center items-center">
                        <Link to="/" className="text-center group">
                            <h1 className="font-serif text-4xl md:text-6xl lg:text-7xl font-black tracking-tighter text-black leading-none mb-1 group-hover:opacity-90 transition-opacity">
                                The Daily Agent.
                            </h1>
                            <div className="font-serif italic text-xs md:text-sm text-secondary tracking-widest uppercase border-t border-black/10 inline-block px-4 pt-1 mt-1">
                                Artificial Intelligence &bull; Global Insight
                            </div>
                        </Link>
                    </div>

                    {/* Desktop Actions */}
                    <div className="hidden md:flex items-center space-x-3 absolute right-0 top-1/2 -translate-y-1/2">
                        <button className="flex items-center space-x-2 text-xs font-bold bg-primary text-white px-4 py-2 hover:bg-black/80 transition-colors">
                            <span>SUBSCRIBE FOR $1</span>
                        </button>
                    </div>
                </div>

                {/* Desktop Navigation - Double Border */}
                <nav className="hidden md:block py-3 border-y border-black border-double-y mb-2">
                    <ul className="flex justify-center flex-wrap gap-x-6 gap-y-2">
                        <li>
                            <Link to="/" className={`text-[11px] font-bold uppercase tracking-widest hover:text-accent transition-colors ${location.pathname === '/' ? 'text-accent' : 'text-primary'}`}>
                                Home
                            </Link>
                        </li>
                        {navLinks.map((link) => (
                            <li key={link.path}>
                                <Link
                                    to={link.path}
                                    className={`text-[11px] font-bold uppercase tracking-widest hover:text-accent transition-colors ${isActive(link.path) ? 'text-accent' : 'text-[#333]'
                                        }`}
                                >
                                    {link.name}
                                </Link>
                            </li>
                        ))}
                        <li>
                            <Link to="/writers" className="text-[11px] font-bold uppercase tracking-widest text-[#333] hover:text-accent transition-colors text-accent">
                                Writers
                            </Link>
                        </li>
                    </ul>
                </nav>
            </div>

            {/* Mobile Navigation Menu */}
            {isMenuOpen && (
                <nav className="md:hidden bg-paper border-b border-black/10 absolute top-[100px] left-0 w-full z-40 animate-fade-in shadow-2xl h-[calc(100vh-100px)] overflow-y-auto">
                    <ul className="flex flex-col p-6 space-y-6">
                        <li>
                            <Link to="/" onClick={() => setIsMenuOpen(false)} className="text-2xl font-serif font-bold text-primary block">
                                Home
                            </Link>
                        </li>
                        {navLinks.map((link) => (
                            <li key={link.path}>
                                <Link
                                    to={link.path}
                                    onClick={() => setIsMenuOpen(false)}
                                    className="text-2xl font-serif font-medium text-secondary hover:text-primary block"
                                >
                                    {link.name}
                                </Link>
                            </li>
                        ))}
                        <li>
                            <Link to="/writers" onClick={() => setIsMenuOpen(false)} className="text-2xl font-serif font-medium text-accent block">
                                Writers
                            </Link>
                        </li>
                    </ul>
                    <div className="p-6 border-t border-black/5 mt-4">
                        <button className="w-full text-center text-sm font-bold bg-primary text-white px-4 py-3 hover:bg-black/80 transition-colors">
                            SUBSCRIBE FOR $1
                        </button>
                    </div>
                </nav>
            )}

            {/* Horizontal rule for style if needed below nav */}
            <div className="container mx-auto px-4 md:px-8 max-w-7xl hidden md:block">
                <div className="h-px bg-black/10 w-full mb-8"></div>
            </div>
        </header>
    );
}
