import React from 'react';

const writers = [
    { id: 1, name: "Sarah Jenkins", role: "Senior Market Analyst", bio: "Covering Wall Street and global financial markets for over a decade. Formerly with Bloomberg." },
    { id: 2, name: "David Chen", role: "Tech & AI Correspondent", bio: "Focusing on the intersection of artificial intelligence and consumer technology." },
    { id: 3, name: "Amanda Pierce", role: "Political Editor", bio: "Reporting on legislative developments and policy shifts from Washington D.C." },
    { id: 4, name: "Robert Fox", role: "Energy Sector Reporter", bio: "Deep dives into renewable energy trends and the global oil market." },
];

const WritersPage = () => {
    return (
        <div className="max-w-4xl mx-auto">
            <div className="border-b-4 border-black mb-8 pb-4">
                <h2 className="font-serif font-bold text-4xl">Our Writers</h2>
                <p className="font-sans text-gray-600 mt-2">Meet the team behind The News Journal.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                {writers.map((writer) => (
                    <div key={writer.id} className="flex gap-6 items-start group">
                        <div className="w-24 h-24 rounded-full bg-gray-200 shrink-0 overflow-hidden border border-gray-300">
                            <img src={`https://placehold.co/150x150/EEE/31343C?text=${writer.name.charAt(0)}`} className="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all" />
                        </div>
                        <div>
                            <h3 className="font-serif font-bold text-xl group-hover:underline decoration-2 decoration-blue-600 underline-offset-4">
                                {writer.name}
                            </h3>
                            <div className="font-sans text-xs font-bold uppercase text-gray-500 mb-2 tracking-wider">
                                {writer.role}
                            </div>
                            <p className="font-serif text-gray-700 leading-relaxed text-sm">
                                {writer.bio}
                            </p>
                            <button className="mt-3 text-xs font-sans font-bold text-blue-700 uppercase tracking-widest hover:text-black transition-colors">
                                View Latest Articles &rarr;
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default WritersPage;
