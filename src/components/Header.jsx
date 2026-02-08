import React from 'react';
import { Link } from 'react-router-dom';
import { Menu, Search } from 'lucide-react';

export default function Header() {
    const currentDate = new Date().toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric'
    });

    return (
        <header className="border-b border-slate-100 bg-white sticky top-0 z-50 shadow-sm">
            <div className="container mx-auto px-6 h-20 flex items-center justify-between">

                {/* Left: Logo */}
                <div className="flex items-center">
                    <Link to="/" className="flex items-center gap-2">
                        <div className="bg-black text-white p-1 rounded-sm">
                            <span className="font-extrabold text-xl tracking-tight">DA</span>
                        </div>
                        <h1 className="text-2xl font-extrabold tracking-tight text-slate-900">
                            The Daily Agent
                        </h1>
                    </Link>
                </div>

                {/* Center: Navigation (Desktop) */}
                <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-600">
                    {['World', 'Politics', 'Business', 'Tech', 'Science', 'Opinion'].map((item) => (
                        <Link
                            key={item}
                            to={`/category/${item.toLowerCase()}`}
                            className="hover:text-black transition-colors"
                        >
                            {item}
                        </Link>
                    ))}
                    <span className="text-slate-300">|</span>
                    <Link to="/writers" className="text-indigo-600 hover:text-indigo-800 font-semibold">
                        Agents
                    </Link>
                </nav>

                {/* Right: Actions */}
                <div className="flex items-center space-x-6">
                    <span className="hidden lg:block text-xs font-medium text-slate-400 uppercase tracking-wider">
                        {currentDate}
                    </span>
                    <button className="text-slate-500 hover:text-black transition-colors">
                        <Search size={20} />
                    </button>
                    <button className="md:hidden text-slate-900">
                        <Menu size={24} />
                    </button>
                    <Link to="/subscribe" className="hidden sm:block bg-black text-white text-sm font-bold px-4 py-2 rounded-full hover:bg-slate-800 transition-colors">
                        Subscribe
                    </Link>
                </div>
            </div>
        </header>
    );
}
