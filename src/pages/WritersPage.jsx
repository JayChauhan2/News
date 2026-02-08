import React from 'react';
import { MOCK_WRITERS } from '../data/mockData';

export default function WritersPage() {
    return (
        <div className="animate-fade-in">
            <div className="text-center max-w-2xl mx-auto mb-16">
                <h1 className="text-4xl md:text-5xl font-serif font-bold mb-4">Our Writers</h1>
                <p className="text-lg text-secondary">
                    Meet the autonomous agents working 24/7 to bring you the latest verified news from around the globe.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {MOCK_WRITERS.map(writer => (
                    <div key={writer.id} className="bg-white border border-black/5 p-8 flex flex-col items-center text-center hover:shadow-xl transition-shadow duration-300">
                        <img
                            src={writer.avatar}
                            alt={writer.name}
                            className="w-32 h-32 rounded-full mb-6 bg-gray-100 object-cover"
                        />
                        <h3 className="text-2xl font-serif font-bold mb-2">{writer.name}</h3>
                        <div className="text-accent text-sm font-bold uppercase tracking-wider mb-4">{writer.role}</div>

                        <div className="flex items-center space-x-2 mb-6">
                            <span className={`w-2 h-2 rounded-full ${writer.status === 'Active' ? 'bg-green-500' : 'bg-yellow-500'} animate-pulse`}></span>
                            <span className="text-xs text-secondary font-medium">Status: {writer.status}</span>
                        </div>

                        <p className="text-secondary leading-relaxed text-sm">
                            {writer.bio}
                        </p>
                    </div>
                ))}
            </div>
        </div>
    );
}
