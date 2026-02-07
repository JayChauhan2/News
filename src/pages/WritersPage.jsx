import React from 'react';
import { Link } from 'react-router-dom';

const agents = [
    {
        id: "watchtower",
        name: "The Watchtower",
        role: "Global News Monitor",
        status: "Online",
        statusColor: "text-green-600",
        bio: "An omnipresent observer that scans thousands of RSS feeds and API endpoints. It identifies emerging patterns and clusters related stories to filter the noise from the signal."
    },
    {
        id: "editor",
        name: "The Editor-in-Chief",
        role: "Assignment Editor",
        status: "Reviewing",
        statusColor: "text-blue-600",
        bio: "A discerning logic engine that rates news clusters for relevance, novelty, and impact. It decides what makes the front page and assigns research tickets to the Journalist."
    },
    {
        id: "journalist",
        name: "The Journalist",
        role: "Deep Researcher",
        status: "Investigating",
        statusColor: "text-purple-600",
        bio: "Powered by vector search, this agent takes an assignment ticket and scours the web for facts, figures, and verified sources to compile a comprehensive research dossier."
    },
    {
        id: "reporter",
        name: "The Writer",
        role: "Lead Reporter",
        status: "Drafting",
        statusColor: "text-yellow-600",
        bio: "The creative voice of the operation. It synthesizes the research dossier into a compelling narrative, adhering to strict style guidelines, before sending it to the Copy Desk."
    },
];

const WritersPage = () => {
    return (
        <div className="py-12 px-4 bg-[#fcfbf7] min-h-screen">
            <div className="max-w-5xl mx-auto">
                <div className="text-center mb-16 border-b border-black pb-8">
                    <h2 className="font-headline text-5xl lg:text-6xl font-black mb-4">The Newsroom</h2>
                    <p className="font-sans text-xs font-bold uppercase tracking-[0.2em] text-gray-500">
                        The Autonomous Agents Powering The Press
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-16">
                    {agents.map((agent) => (
                        <div key={agent.id} className="group">
                            <div className="flex items-baseline justify-between border-b-2 border-black mb-4 pb-2">
                                <h3 className="font-headline text-2xl font-bold group-hover:text-[#0274b6] transition-colors">
                                    {agent.name}
                                </h3>
                                <div className={`font-sans text-[10px] uppercase font-bold tracking-widest ${agent.statusColor}`}>
                                    ● {agent.status}
                                </div>
                            </div>

                            <div className="mb-3">
                                <span className="font-sans text-[10px] font-bold uppercase tracking-widest text-gray-400 bg-gray-100 px-2 py-1 rounded">
                                    {agent.role}
                                </span>
                            </div>

                            <p className="font-body text-lg text-gray-800 leading-relaxed border-l border-gray-300 pl-4">
                                {agent.bio}
                            </p>
                        </div>
                    ))}
                </div>

                <div className="mt-20 text-center">
                    <Link to="/" className="inline-block border border-black px-8 py-3 text-xs font-sans font-bold uppercase tracking-widest hover:bg-black hover:text-white transition-colors">
                        Return to Front Page
                    </Link>
                </div>
            </div>
        </div>
    );
};

export default WritersPage;
