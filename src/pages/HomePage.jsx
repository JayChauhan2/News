import React from 'react';

const HomePage = () => {
    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 pt-4">
            {/* LEFT COLUMN (2/12) - Sidebar / Opinion */}
            <div className="lg:col-span-2 hidden lg:block border-r border-gray-200 pr-4">
                <h3 className="font-sans font-bold text-xs uppercase text-gray-500 mb-3 tracking-wider">Opinion</h3>
                <div className="space-y-6">
                    {[1, 2, 3].map((i) => (
                        <div key={i}>
                            <h4 className="font-serif font-bold text-lg leading-tight mb-1 hover:text-blue-700 cursor-pointer">
                                The Global Economy Needs a Reset Button
                            </h4>
                            <p className="font-sans text-xs text-gray-500">By John Smith</p>
                        </div>
                    ))}
                </div>
            </div>

            {/* CENTER COLUMN (6/12) - Main Featured Stories */}
            <div className="lg:col-span-6 lg:border-r lg:border-gray-200 lg:pr-6">
                {/* Hero Article */}
                <div className="mb-8 group cursor-pointer">
                    <h2 className="font-serif font-bold text-4xl md:text-5xl leading-tight mb-4 group-hover:text-gray-700 transition-colors">
                        Markets Rally as Tech Stocks Surge to New All-Time Highs
                    </h2>
                    <div className="aspect-video bg-gray-200 mb-4 overflow-hidden relative">
                        <img
                            src="https://placehold.co/800x450/EEE/31343C"
                            alt="Market chart"
                            className="object-cover w-full h-full"
                        />
                        <span className="absolute bottom-2 left-2 bg-black text-white px-2 py-1 text-xs font-sans uppercase tracking-wider">
                            Markets
                        </span>
                    </div>
                    <p className="font-serif text-lg text-gray-800 leading-relaxed mb-2">
                        Investors are betting big on the latest wave of artificial intelligence innovations, pushing the Nasdaq to record territories despite lingering inflation concerns. The rally marks a significant turnaround from last quarter's slump.
                    </p>
                    <div className="font-sans text-xs text-gray-500 flex gap-2">
                        <span className="font-bold text-gray-900">By Sarah Jenkins</span>
                        <span>•</span>
                        <span>4 min read</span>
                    </div>
                </div>

                {/* Secondary Stories Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 border-t border-black pt-6">
                    {[1, 2].map((i) => (
                        <div key={i} className="group cursor-pointer">
                            <div className="aspect-[3/2] bg-gray-200 mb-3">
                                <img src={`https://placehold.co/400x300/EEE/31343C?text=Story+${i}`} className="w-full h-full object-cover" />
                            </div>
                            <h3 className="font-serif font-bold text-xl leading-tight mb-2 group-hover:text-blue-700">
                                New Policy Shifts in Urban Development
                            </h3>
                            <p className="font-serif text-sm text-gray-600 line-clamp-3">
                                City planners are unveiling a simplified zone code that purposes to reduce red tape and encourage mixed-use developments in downtown areas.
                            </p>
                        </div>
                    ))}
                </div>
            </div>

            {/* RIGHT COLUMN (4/12) - Top Stories List */}
            <div className="lg:col-span-4">
                <h3 className="font-sans font-bold text-xs uppercase text-red-700 mb-3 tracking-wider border-b border-black pb-1">
                    Top News
                </h3>
                <div className="space-y-6">
                    {[1, 2, 3, 4, 5].map((i) => (
                        <div key={i} className="flex gap-4 group cursor-pointer border-b border-gray-100 pb-4 last:border-0">
                            <div className="flex-1">
                                <h4 className="font-serif font-bold text-lg leading-snug mb-2 group-hover:text-blue-700">
                                    Global Supply Chains Face New Bottlenecks at Major Ports
                                </h4>
                                <div className="font-sans text-xs text-gray-400">2 hrs ago</div>
                            </div>
                            <div className="w-24 h-24 bg-gray-200 shrink-0">
                                <img src={`https://placehold.co/100x100/EEE/31343C?text=News+${i}`} className="w-full h-full object-cover" />
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default HomePage;
