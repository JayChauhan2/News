import React from 'react';

const agents = [
    {
        id: "watchtower",
        name: "The Watchtower",
        role: "Global News Monitor",
        status: "Scanning RSS Feeds",
        statusColor: "bg-green-100 text-green-800",
        bio: "An omnipresent observer that scans thousands of RSS feeds and API endpoints every 10 minutes. It identifies emerging patterns and clusters related stories to filter the noise from the signal."
    },
    {
        id: "editor",
        name: "The Editor-in-Chief",
        role: "Curator & Assignment Editor",
        status: "Assigning Tickets",
        statusColor: "bg-blue-100 text-blue-800",
        bio: "A discerning logic engine (Scikit-learn + LLM) that rates news clusters for relevance, novelty, and impact. It decides what makes the front page and assigns research tickets to the Journalist."
    },
    {
        id: "journalist",
        name: "Investigative Journalist",
        role: "Deep Researcher",
        status: "Gathering Intel",
        statusColor: "bg-purple-100 text-purple-800",
        bio: "Powered by Tavily and Vector Search. This agent takes an assignment ticket and scours the web for facts, figures, and verified sources to compile a comprehensive research dossier."
    },
    {
        id: "reporter",
        name: "The Senior Reporter",
        role: "Lead Writer & Publisher",
        status: "Drafting Stories",
        statusColor: "bg-yellow-100 text-yellow-800",
        bio: "The creative voice of the operation. Using Groq (Llama-3), it synthesizes the research dossier into a compelling narrative, adhering to strict WSJ-style guidelines, before sending it to the Copy Desk for specific formatting."
    },
];

const WritersPage = () => {
    return (
        <div className="max-w-4xl mx-auto py-8">
            <div className="border-b-4 border-black mb-12 pb-4 text-center">
                <h2 className="font-serif font-black text-5xl mb-4">The Newsroom</h2>
                <p className="font-sans text-gray-600 uppercase tracking-widest text-sm">Meet the Autonomous Agents powering the press</p>
            </div>

            <div className="grid grid-cols-1 gap-16">
                {agents.map((agent) => (
                    <div key={agent.id} className="flex flex-col md:flex-row gap-8 items-start group">
                        {/* Avatar / Icon Placeholder */}
                        <div className="w-32 h-32 rounded-full bg-gray-100 shrink-0 overflow-hidden border-2 border-gray-200 flex items-center justify-center">
                            <span className="font-serif text-4xl text-gray-400 font-bold">
                                {agent.name.charAt(4)}
                            </span>
                        </div>

                        <div className="flex-1">
                            <div className="flex justify-between items-start mb-2">
                                <div>
                                    <h3 className="font-serif font-bold text-2xl text-black mb-1">
                                        {agent.name}
                                    </h3>
                                    <div className="font-sans text-xs font-bold uppercase text-gray-500 tracking-wider">
                                        {agent.role}
                                    </div>
                                </div>
                                <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide border ${agent.statusColor.replace('text', 'border')}`}>
                                    ● {agent.status}
                                </span>
                            </div>

                            <p className="font-serif text-gray-800 leading-relaxed text-lg mb-4 border-l-2 border-gray-300 pl-4">
                                {agent.bio}
                            </p>

                            <div className="flex gap-4">
                                <button className="text-xs font-sans font-bold text-gray-400 uppercase disabled:opacity-50 cursor-not-allowed">
                                    View Agent Logs
                                </button>
                                <button className="text-xs font-sans font-bold text-gray-400 uppercase disabled:opacity-50 cursor-not-allowed">
                                    Inspect Configuration
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WritersPage;
