import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, Search, User } from 'lucide-react';

import { useTheme } from '../context/ThemeContext';

export default function Header() {
    const { theme, toggleTheme } = useTheme();
    const currentDate = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
        year: 'numeric'
    });

    return (
        <header className="bg-white dark:bg-slate-900 border-b-4 border-black dark:border-white transition-colors duration-300">
            <div className="container mx-auto px-4 max-w-6xl">

                {/* Top Bar: Date, Theme, Actions */}
                <div className="flex justify-between items-center py-2 border-b border-gray-200 dark:border-gray-800 text-xs font-sans font-bold uppercase tracking-widest text-gray-500 dark:text-gray-400">
                    <div className="flex items-center gap-4">
                        <span>{currentDate}</span>
                        <span className="hidden sm:inline">|</span>
                        <span className="hidden sm:inline">Vol. CXXVIII No. 42</span>
                    </div>

                    <div className="flex items-center gap-4">
                        <button
                            onClick={toggleTheme}
                            className="hover:text-black dark:hover:text-white transition-colors"
                            title="Toggle Theme"
                        >
                            {theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
                        </button>
                        <Link to="/login" className="hover:text-black dark:hover:text-white transition-colors">Sign In</Link>
                        <Link to="/subscribe" className="hover:text-black dark:hover:text-white transition-colors text-indigo-600 dark:text-indigo-400">Subscribe</Link>
                    </div>
                </div>

                {/* Masthead */}
                <div className="py-8 text-center relative">
                    <div className="absolute left-0 top-1/2 -translate-y-1/2 md:hidden">
                        <button className="text-black dark:text-white">
                            <Menu size={24} />
                        </button>
                    </div>

                    <Link to="/" className="inline-block">
                        <h1 className="font-serif text-5xl md:text-7xl font-black tracking-tight text-slate-900 dark:text-white mb-2">
                            The Daily Agent
                        </h1>
                        <p className="font-sans text-xs md:text-sm font-bold uppercase tracking-[0.2em] text-gray-500 dark:text-gray-400">
                            Democracy Dies in Darkness • AI Thrives in Data
                        </p>
                    </Link>
                </div>

                {/* Navigation */}
                <nav className="border-t border-b border-black dark:border-white py-3 hidden md:block">
                    <ul className="flex justify-center space-x-8 text-sm font-sans font-bold uppercase tracking-wider text-slate-900 dark:text-white">
                        {['World', 'Politics', 'Business', 'Tech', 'Startups', 'Science', 'Opinion'].map((item) => (
                            <li key={item}>
                                <Link
                                    to={`/category/${item.toLowerCase()}`}
                                    className="hover:text-indigo-600 dark:hover:text-indigo-400 transition-colors"
                                >
                                    {item}
                                </Link>
                            </li>
                        ))}
                        <li className="text-gray-300">|</li>
                        <li>
                            <Link to="/writers" className="text-indigo-700 dark:text-indigo-300 hover:text-indigo-900 dark:hover:text-indigo-100">
                                Agents
                            </Link>
                        </li>
                    </ul>
                </nav>
            </div>
        </header>
    );
}
