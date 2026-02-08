import React, { useState, useEffect } from 'react';
import { fetchAgentStatus } from '../api/client';
import { Activity, Radio, Cpu, RefreshCw } from 'lucide-react';

// Map of agent names to their specific emojis
const AGENT_EMOJIS = {
    'Watchtower': '🗼',
    'Chief Editor': '📰',
    'Trend Spotter': '📈',
    'Investigative Journalist': '🕵️',
    'Opinion Columnist': '✒️',
    'Fact Checker': '✅',
    'Market Analyst': '📊',
    'Tech Reporter': '💻',
    'Sports Correspondent': '🏆',
    'Entertainment Critic': '🎬',
    'Political Pundit': '🏛️',
    'Science Editor': '🔬'
};

const getAgentEmoji = (name, role) => {
    // Try exact name match
    if (AGENT_EMOJIS[name]) return AGENT_EMOJIS[name];

    // Try to match based on role keywords if name doesn't match
    const lowerRole = (role || '').toLowerCase();
    if (lowerRole.includes('editor')) return '📝';
    if (lowerRole.includes('journalist') || lowerRole.includes('writer')) return '✍️';
    if (lowerRole.includes('analyst')) return '📉';
    if (lowerRole.includes('monitor')) return '👀';

    // Default fallback
    return '🤖';
};

export default function WritersPage() {
    const [writers, setWriters] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            const data = await fetchAgentStatus();
            setWriters(data);
            setLoading(false);
        }
        load();

        // Poll every 2 seconds for real-time updates
        const interval = setInterval(load, 2000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="max-w-6xl mx-auto py-12 px-6">
            <div className="mb-12 text-center">
                <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white mb-4">Our Agents</h1>
                <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
                    Meet the AI agents working around the clock to bring you the latest news.
                </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {loading ? (
                    <div className="col-span-full flex justify-center py-12">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
                    </div>
                ) : writers.length > 0 ? (
                    writers.map((writer, index) => (
                        <div key={index} className="bg-white dark:bg-slate-800 rounded-2xl p-8 shadow-sm border border-slate-100 dark:border-slate-700 hover:shadow-md transition-all relative overflow-hidden group">
                            {/* Animated Background Pulse for Active Agents */}
                            {writer.status !== 'Idle' && (
                                <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-50 dark:bg-indigo-900/30 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110"></div>
                            )}

                            <div className="flex items-center space-x-4 mb-6 relative z-10">
                                <div className={`w-14 h-14 rounded-full flex items-center justify-center font-bold text-3xl border-2 ${writer.status === 'Idle' ? 'bg-slate-50 dark:bg-slate-700 border-slate-200 dark:border-slate-600 grayscale' : 'bg-indigo-50 dark:bg-indigo-900/50 border-indigo-100 dark:border-indigo-800'}`}>
                                    {getAgentEmoji(writer.name, writer.role)}
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-slate-900 dark:text-white leading-tight">{writer.name || 'Unknown Agent'}</h3>
                                    <div className="flex items-center text-sm text-slate-500 dark:text-slate-400 font-medium mt-1">
                                        <Cpu size={12} className="mr-1.5" />
                                        {writer.role || 'System Process'}
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-4 relative z-10">
                                <div className="min-h-[80px]">
                                    <h4 className="flex items-center text-xs font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mb-2">
                                        <Radio size={12} className={`mr-1.5 ${writer.status !== 'Idle' ? 'text-green-500 animate-pulse' : 'text-slate-300 dark:text-slate-600'}`} />
                                        Current Activity
                                    </h4>
                                    <p className="text-slate-700 dark:text-slate-300 font-medium leading-relaxed">
                                        {writer.current_assignment || 'Waiting for tasks...'}
                                    </p>
                                </div>

                                <div className="pt-4 border-t border-slate-50 dark:border-slate-700 flex items-center justify-between">
                                    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-bold uppercase tracking-wide ${writer.status === 'Idle'
                                        ? 'bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400'
                                        : writer.status === 'Active'
                                            ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                                            : 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-400'
                                        }`}>
                                        {writer.status === 'Active' && <span className="w-1.5 h-1.5 rounded-full bg-green-500 mr-1.5 animate-pulse"></span>}
                                        {writer.status}
                                    </span>
                                    <div className="text-xs text-slate-400 dark:text-slate-500 font-mono flex items-center">
                                        <RefreshCw size={10} className="mr-1" />
                                        {writer.last_updated ? new Date(writer.last_updated).toLocaleTimeString() : 'Just now'}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="col-span-full text-center py-12 bg-slate-50 rounded-2xl">
                        <p className="text-slate-500">No agents currently active.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
