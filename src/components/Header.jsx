import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, Search } from 'lucide-react';

import { useTheme } from '../context/ThemeContext';

export default function Header() {
    const { theme, toggleTheme } = useTheme();
    const currentDate = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric'
    });

    return (
        <header className="border-b border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 sticky top-0 z-50 shadow-sm transition-colors duration-300">
            <div className="container mx-auto px-6 h-20 flex items-center justify-between">

                {/* Left: Logo */}
                <div className="flex items-center">
                    <Link to="/" className="flex items-center gap-2">
                        <div className="bg-black dark:bg-white text-white dark:text-black p-1 rounded-sm transition-colors">
                            <span className="font-extrabold text-xl tracking-tight">DA</span>
                        </div>
                        <h1 className="text-2xl font-extrabold tracking-tight text-slate-900 dark:text-white transition-colors">
                            The Daily Agent
                        </h1>
                    </Link>
                </div>

                {/* Center: Navigation (Desktop) */}
                <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-600 dark:text-slate-400">
                    {['World', 'Politics', 'Business', 'Tech', 'Startups', 'Science', 'Opinion'].map((item) => (
                        <Link
                            key={item}
                            to={`/category/${item.toLowerCase()}`}
                            className="hover:text-black dark:hover:text-white transition-colors"
                        >
                            {item}
                        </Link>
                    ))}
                    <span className="text-slate-300 dark:text-slate-700">|</span>
                    <Link to="/writers" className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-semibold transition-colors">
                        Agents
                    </Link>
                </nav>

                {/* Right: Actions */}
                <div className="flex items-center space-x-6">
                    <span className="hidden lg:block text-xs font-medium text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                        {currentDate}
                    </span>

                    {/* Theme Toggle */}
                    <button
                        onClick={toggleTheme}
                        className="text-slate-500 hover:text-black dark:text-slate-400 dark:hover:text-white transition-colors p-2 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800"
                        title={theme === 'dark' ? "Switch to Light Mode" : "Switch to Dark Mode"}
                    >
                        {theme === 'dark' ? (
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5" /><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" /></svg>
                        ) : (
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" /></svg>
                        )}
                    </button>

                    <button className="text-slate-500 hover:text-black dark:text-slate-400 dark:hover:text-white transition-colors">
                        <Search size={20} />
                    </button>
                    <button className="md:hidden text-slate-900 dark:text-white">
                        <Menu size={24} />
                    </button>
                    <Link to="/subscribe" className="hidden sm:block bg-black dark:bg-white text-white dark:text-black text-sm font-bold px-4 py-2 rounded-full hover:bg-slate-800 dark:hover:bg-slate-200 transition-colors">
                        Subscribe
                    </Link>
                </div>
            </div>
        </header>
    );
}
