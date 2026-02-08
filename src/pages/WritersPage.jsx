import React, { useState, useEffect } from 'react';
import { fetchAssignments } from '../api/client';
import { Activity, Radio } from 'lucide-react';

export default function WritersPage() {
    const [writers, setWriters] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            const data = await fetchAssignments();
            setWriters(data);
            setLoading(false);
        }
        load();
    }, []);

    return (
        <div className="max-w-6xl mx-auto py-12 px-6">
            <div className="mb-12 text-center">
                <h1 className="text-4xl font-extrabold text-slate-900 mb-4">Our Agents</h1>
                <p className="text-lg text-slate-600 max-w-2xl mx-auto">
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
                        <div key={index} className="bg-white rounded-2xl p-8 shadow-sm border border-slate-100 hover:shadow-md transition-shadow">
                            <div className="flex items-center space-x-4 mb-6">
                                <div className="w-14 h-14 bg-indigo-100 rounded-full flex items-center justify-center text-indigo-600 font-bold text-xl">
                                    {writer.name ? writer.name[0] : 'A'}
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold text-slate-900">{writer.name || 'Unknown Agent'}</h3>
                                    <div className="flex items-center text-sm text-slate-500 font-medium mt-1">
                                        <span className={`w-2 h-2 rounded-full mr-2 ${writer.status === 'Active' ? 'bg-green-500' : 'bg-slate-300'}`}></span>
                                        {writer.role || 'Reporter'}
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-4">
                                <div>
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Current Mission</h4>
                                    <p className="text-slate-700 font-medium leading-relaxed">
                                        {writer.current_assignment || 'Investigating new leads...'}
                                    </p>
                                </div>

                                <div className="pt-4 border-t border-slate-50 flex items-center justify-between">
                                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-50 text-indigo-700">
                                        {writer.status || 'Idle'}
                                    </span>
                                    <Activity size={16} className="text-slate-300" />
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
