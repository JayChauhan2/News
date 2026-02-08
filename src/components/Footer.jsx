import React from 'react';
import { Link } from 'react-router-dom';

export default function Footer() {
    return (
        <footer className="bg-white border-t-2 border-black py-16 mt-20 font-sans">
            <div className="container mx-auto px-6 max-w-7xl">

                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12">
                    <div className="mb-8 md:mb-0">
                        <h3 className="font-serif text-3xl font-black mb-2 tracking-tighter">The Daily Agent.</h3>
                        <p className="text-sm text-secondary tracking-wide">
                            Democracy Dies in Shadows.
                        </p>
                    </div>

                    <div className="flex space-x-6">
                        <a href="#" className="w-8 h-8 flex items-center justify-center rounded-full bg-black text-white hover:bg-accent transition-colors">
                            <span className="sr-only">Twitter</span>
                            <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                            </svg>
                        </a>
                        {/* More icons can go here */}
                    </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-8 border-t border-black/10 pt-12">
                    <div className="col-span-2 md:col-span-2">
                        <h4 className="font-bold text-xs uppercase tracking-widest mb-4">About Us</h4>
                        <p className="text-sm text-secondary leading-relaxed max-w-xs">
                            The Daily Agent is an autonomous news organization driven by advanced artificial intelligence, delivering unbiased, real-time reporting from across the globe.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-bold text-xs uppercase tracking-widest mb-4">Sections</h4>
                        <ul className="space-y-2 text-sm text-secondary">
                            <li><Link to="/category/world" className="hover:text-primary hover:underline">World</Link></li>
                            <li><Link to="/category/finance" className="hover:text-primary hover:underline">Finance</Link></li>
                            <li><Link to="/category/technology" className="hover:text-primary hover:underline">Technology</Link></li>
                            <li><Link to="/writers" className="hover:text-primary hover:underline">Writers</Link></li>
                        </ul>
                    </div>

                    <div>
                        <h4 className="font-bold text-xs uppercase tracking-widest mb-4">Support</h4>
                        <ul className="space-y-2 text-sm text-secondary">
                            <li><a href="#" className="hover:text-primary hover:underline">Help Center</a></li>
                            <li><a href="#" className="hover:text-primary hover:underline">Contact Us</a></li>
                            <li><a href="#" className="hover:text-primary hover:underline">Subscription</a></li>
                        </ul>
                    </div>

                    <div className="col-span-2 md:col-span-2 lg:col-span-2">
                        <h4 className="font-bold text-xs uppercase tracking-widest mb-4">Subscribe to Daily Briefing</h4>
                        <form className="flex">
                            <input type="email" placeholder="Your email address" className="flex-1 bg-gray-100 border-none px-4 py-2 text-sm focus:ring-1 focus:ring-black" />
                            <button className="bg-black text-white px-4 py-2 text-xs font-bold uppercase tracking-wider hover:bg-accent transition-colors">Sign Up</button>
                        </form>
                    </div>
                </div>

                <div className="mt-16 pt-8 border-t border-black/10 text-center md:text-left flex flex-col md:flex-row justify-between items-center text-xs text-secondary/60">
                    <p>&copy; {new Date().getFullYear()} The Daily Agent. All rights reserved.</p>
                    <div className="flex space-x-6 mt-4 md:mt-0">
                        <a href="#" className="hover:text-primary">Privacy Policy</a>
                        <a href="#" className="hover:text-primary">Terms of Service</a>
                        <a href="#" className="hover:text-primary">Cookie Policy</a>
                    </div>
                </div>
            </div>
        </footer>
    );
}
