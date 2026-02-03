import React from 'react';

const LandingPage = () => {
    return (
        <div className="min-h-screen bg-slate-950 text-white font-sans overflow-x-hidden selection:bg-purple-500 selection:text-white">
            {/* Navbar */}
            <nav className="fixed w-full z-50 top-0 start-0 border-b border-white/10 bg-slate-950/80 backdrop-blur-md">
                <div className="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
                    <a href="#" className="flex items-center space-x-3 rtl:space-x-reverse">
                        <span className="self-center text-2xl font-bold whitespace-nowrap bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
                            Nexus
                        </span>
                    </a>
                    <button type="button" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-900 font-medium rounded-lg text-sm px-4 py-2 text-center transition-all shadow-[0_0_15px_rgba(59,130,246,0.5)] cursor-pointer">
                        Get Started
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <section className="relative pt-32 pb-20 lg:pt-48 lg:pb-32 overflow-hidden">
                {/* Background Gradients */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full z-0 pointer-events-none">
                    <div className="absolute top-20 left-[20%] w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-40 animate-pulse"></div>
                    <div className="absolute top-20 right-[20%] w-72 h-72 bg-blue-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-40 animate-pulse delay-1000"></div>
                </div>

                <div className="relative z-10 mx-auto max-w-7xl px-6 text-center">
                    <h1 className="mb-8 text-5xl font-extrabold tracking-tight text-white md:text-7xl lg:text-8xl">
                        The Future of <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500 animate-gradient-x">
                            Digital Experience
                        </span>
                    </h1>
                    <p className="mb-8 text-lg font-normal text-gray-300 lg:text-xl sm:px-16 lg:px-48">
                        Experience a web application designed with precision, speed, and aesthetics in mind. Built with React, Vite, and Tailwind CSS v4.
                    </p>
                    <div className="flex flex-col space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
                        <a href="#" className="inline-flex justify-center items-center py-3 px-6 text-base font-medium text-center text-white rounded-lg bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-900 transition-all shadow-lg shadow-blue-500/30 hover:shadow-blue-500/50 hover:-translate-y-1">
                            Get Started
                            <svg className="w-3.5 h-3.5 ms-2 rtl:rotate-180" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 10">
                                <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M1 5h12m0 0L9 1m4 4L9 9" />
                            </svg>
                        </a>
                        <a href="#" className="inline-flex justify-center items-center py-3 px-6 text-base font-medium text-center text-white rounded-lg border border-white/20 hover:bg-white/10 focus:ring-4 focus:ring-gray-800 backdrop-blur-sm transition-all hover:-translate-y-1">
                            Learn More
                        </a>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 bg-slate-900/50">
                <div className="max-w-screen-xl mx-auto px-4">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                        {[
                            { title: "Lightning Fast", desc: "Powered by Vite for instant server start and HMR.", color: "from-yellow-400 to-orange-500" },
                            { title: "Modern Design", desc: "Glassmorphism and vibrant gradients for a premium feel.", color: "from-blue-400 to-cyan-500" },
                            { title: "Scalable", desc: "Built with component-driven architecture in mind.", color: "from-purple-400 to-pink-500" }
                        ].map((feature, i) => (
                            <div key={i} className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-sm hover:bg-white/10 transition-colors group">
                                <div className={`w-12 h-12 mb-4 rounded-lg bg-gradient-to-br ${feature.color} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform`}>
                                    <div className="w-6 h-6 bg-white/20 rounded-full"></div>
                                </div>
                                <h3 className="mb-2 text-xl font-bold text-white">{feature.title}</h3>
                                <p className="text-gray-400">{feature.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-slate-950 py-8 border-t border-white/10">
                <div className="max-w-screen-xl mx-auto px-4 text-center text-gray-500">
                    <p>© 2026 Nexus Inc. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
