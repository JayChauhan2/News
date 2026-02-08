import React, { useMemo } from 'react';
import { useParams } from 'react-router-dom';
import ArticleCard from '../components/ArticleCard';
import { useArticles } from '../api/client';

export default function HomePage() {
    const { category } = useParams();
    const { articles, loading, error } = useArticles();

    const filteredArticles = useMemo(() => {
        if (loading || error) return [];
        if (!category) return articles;
        return articles.filter(article =>
            (article.category || "").toLowerCase() === category.toLowerCase()
        );
    }, [category, articles, loading, error]);

    if (loading) {
        return (
            <div className="flex h-[50vh] items-center justify-center">
                <div className="text-xl font-serif animate-pulse tracking-widest uppercase">Loading The Daily Agent...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex h-[50vh] items-center justify-center">
                <div className="text-accent font-bold font-serif">Unable to fetch the latest wire. Please check connection.</div>
            </div>
        );
    }

    // Layout Logic
    const leadArticle = filteredArticles[0];
    const secondaryArticles = filteredArticles.slice(1, 4); // Next 3
    const sidebarArticles = filteredArticles.slice(4, 9); // Next 5 for sidebar
    const moreArticles = filteredArticles.slice(9);

    return (
        <div className="animate-fade-in pb-20">
            {category && (
                <div className="mb-12 border-b-2 border-black pb-4 text-center">
                    <h1 className="text-5xl font-serif font-black capitalize tracking-tighter">{category}</h1>
                </div>
            )}

            {/* A. Lead Story Section */}
            {leadArticle && (
                <section className="mb-16 border-b border-black/10 pb-12">
                    <ArticleCard article={leadArticle} variant="lead" />
                </section>
            )}

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                {/* B. Main Content Column (Left) */}
                <div className="lg:col-span-8 flex flex-col gap-12">
                    {/* B1. Secondary Row (3 columns) */}
                    {secondaryArticles.length > 0 && (
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 border-b border-black/10 pb-12">
                            {secondaryArticles.map(article => (
                                <ArticleCard key={article.id} article={article} variant="standard" />
                            ))}
                        </div>
                    )}

                    {/* B2. More Stories (List or Grid) */}
                    {moreArticles.length > 0 && (
                        <div>
                            <div className="flex items-center mb-6">
                                <span className="bg-black text-white text-xs font-bold px-2 py-1 uppercase tracking-widest">More News</span>
                                <div className="h-px bg-black flex-grow ml-4"></div>
                            </div>
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                {moreArticles.map(article => (
                                    <ArticleCard key={article.id} article={article} variant="compact" />
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {/* C. Sidebar Column (Right) - Sticky-ish */}
                <aside className="lg:col-span-4 pl-0 lg:pl-8 lg:border-l border-black/10">
                    <div className="sticky top-24">
                        <div className="mb-8">
                            <h3 className="font-serif font-bold text-xl mb-4 border-b-2 border-black pb-1">Trending</h3>
                            <div className="flex flex-col gap-6">
                                {sidebarArticles.map((article, index) => (
                                    <div key={article.id} className="group cursor-pointer">
                                        <div className="flex items-baseline space-x-3">
                                            <span className="text-3xl font-black text-black/10 font-serif -mb-4 z-0 group-hover:text-accent/20 transition-colors">
                                                {index + 1}
                                            </span>
                                            <div className="relative z-10 bg-paper pl-2">
                                                <span className="text-[9px] font-bold text-accent uppercase tracking-widest block mb-1">
                                                    {article.category}
                                                </span>
                                                <h4 className="font-serif font-bold text-lg leading-tight group-hover:text-secondary transition-colors">
                                                    {article.title}
                                                </h4>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="bg-news-gray/30 p-6 text-center border border-black/5">
                            <h4 className="font-serif font-bold text-lg mb-2">Daily Agent Newsletter</h4>
                            <p className="text-xs text-secondary mb-4">Get the most critical AI-curated news delivered to your inbox every morning.</p>
                            <input type="email" placeholder="Email address" className="w-full bg-white border border-black/10 px-3 py-2 text-sm mb-2" />
                            <button className="w-full bg-black text-white text-xs font-bold uppercase py-2 hover:bg-accent transition-colors">
                                Subscribe
                            </button>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
}
