import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ArticleCard from '../components/ArticleCard';
import { getTimeAgo } from '../utils';

const HomePage = () => {
    const { category } = useParams();
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchArticles = () => {
            setLoading(true); // Show loading state when switching categories
            fetch(`http://localhost:8000/articles?t=${Date.now()}`)
                .then(res => res.json())
                .then(data => {
                    // Filter if category is present
                    let filtered = data;
                    if (category) {
                        filtered = data.filter(a => a.category === category);
                    }
                    setArticles(filtered);
                    setLoading(false);
                })
                .catch(err => {
                    console.error("Failed to fetch articles", err);
                    setLoading(false);
                });
        };

        fetchArticles();
        const interval = setInterval(fetchArticles, 10000);
        return () => clearInterval(interval);
    }, [category]); // Re-run when category changes

    // Loading State
    if (loading && articles.length === 0) {
        return <div className="py-20 text-center font-sans uppercase tracking-widest text-gray-400">Updating Edition...</div>;
    }

    if (articles.length === 0) {
        return (
            <div className="py-20 text-center">
                <h2 className="font-serif text-2xl text-gray-400 italic">No news in {category || "this section"} yet.</h2>
                <p className="font-sans text-xs text-gray-300 mt-2 uppercase">The presses are running...</p>
            </div>
        );
    }

    const leadStory = articles[0];
    const sideStories = articles.slice(1, 5);
    const feedStories = articles.slice(5);

    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 divide-y lg:divide-y-0 lg:divide-x divide-gray-200">

            {/* LEFT COLUMN: Lead Story & Main Feed (8 Cols) */}
            <div className="lg:col-span-8 space-y-8">

                {/* LEAD STORY */}
                <section className="mb-8 group cursor-pointer">
                    <Link to={`/article/${leadStory.id}`}>
                        <div className="flex flex-col gap-4">
                            {leadStory.image_url ? (
                                <div className="w-full aspect-video overflow-hidden">
                                    <img
                                        src={leadStory.image_url}
                                        alt={leadStory.headline}
                                        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                                    />
                                </div>
                            ) : (
                                <div className="w-full h-64 bg-gray-100 flex items-center justify-center text-gray-300 font-serif italic">
                                    No Image Available
                                </div>
                            )}

                            <div className="mt-2">
                                <div className="flex items-center gap-2 mb-2 font-sans text-[10px] font-bold uppercase tracking-widest text-[#0274b6]">
                                    {leadStory.category || "Top Story"}
                                    <span className="text-gray-300">|</span>
                                    <span className="text-gray-400 font-normal">{getTimeAgo(leadStory.published_at)}</span>
                                </div>
                                <h2 className="font-serif text-4xl lg:text-5xl font-bold leading-tight mb-3 group-hover:text-[#0274b6] transition-colors">
                                    {leadStory.headline}
                                </h2>
                                <p className="font-serif text-lg text-gray-600 line-clamp-3 leading-relaxed">
                                    {leadStory.meta_description || leadStory.content.substring(0, 150) + "..."}
                                </p>
                            </div>
                        </div>
                    </Link>
                </section>

                <div className="border-t border-black pt-1"></div>

                {/* FEED OF OTHER STORIES */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {feedStories.map(article => (
                        <div key={article.id} className="group">
                            <Link to={`/article/${article.id}`}>
                                <div className="flex items-center gap-2 mb-2 font-sans text-[10px] font-bold uppercase tracking-wide text-gray-400">
                                    <span className="text-[#0274b6]">{article.category}</span>
                                    <span>•</span>
                                    <span>{getTimeAgo(article.published_at)}</span>
                                </div>
                                <h3 className="font-serif text-xl font-bold leading-snug mb-2 group-hover:text-[#0274b6] transition-colors">
                                    {article.headline}
                                </h3>
                                <p className="font-serif text-sm text-gray-500 line-clamp-2 leading-relaxed">
                                    {article.meta_description}
                                </p>
                            </Link>
                        </div>
                    ))}
                </div>
            </div>

            {/* RIGHT COLUMN: Sidebar / Opinion / Popular (4 Cols) */}
            <aside className="lg:col-span-4 pl-0 lg:pl-8 pt-8 lg:pt-0">
                <div className="sticky top-24">
                    <h4 className="font-sans text-xs font-bold uppercase tracking-widest border-b border-black pb-2 mb-4">
                        Latest Headlines
                    </h4>

                    <div className="space-y-6 divide-y divide-gray-100">
                        {sideStories.map(article => (
                            <Link key={article.id} to={`/article/${article.id}`} className="block group pt-4 first:pt-0">
                                <div className="flex flex-row-reverse gap-4">
                                    {article.image_url && (
                                        <img src={article.image_url} className="w-20 h-20 object-cover bg-gray-100" alt="" />
                                    )}
                                    <div className="flex-1">
                                        <div className="text-[10px] font-bold uppercase text-[#0274b6] mb-1">
                                            {article.category}
                                        </div>
                                        <h4 className="font-serif text-lg leading-tight font-medium group-hover:text-[#0274b6] transition-colors">
                                            {article.headline}
                                        </h4>
                                        <div className="text-[10px] text-gray-400 mt-1">
                                            {getTimeAgo(article.published_at)}
                                        </div>
                                    </div>
                                </div>
                            </Link>
                        ))}
                    </div>
                </div>
            </aside>
        </div>
    );
};
export default HomePage;
