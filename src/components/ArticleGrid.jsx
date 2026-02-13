import React from 'react';
import ArticleCard from './ArticleCard';

export default function ArticleGrid({ articles, onDelete }) {
    if (!articles || articles.length === 0) {
        return (
            <div className="py-20 text-center">
                <h3 className="text-2xl font-bold text-slate-900 mb-2">No News Found</h3>
                <p className="text-slate-500">The world is quiet today.</p>
            </div>
        );
    }

    const outputArticles = [...articles];
    const featured = outputArticles.shift(); // First article is featured

    return (
        <div className="py-12 px-6 container mx-auto">
            {/* Featured Section */}
            <section className="mb-16">
                <ArticleCard article={featured} featured={true} onDelete={onDelete} />
            </section>

            {/* Grid Section */}
            <section>
                <div className="flex items-center justify-between mb-8">
                    <h3 className="text-2xl font-bold text-slate-900">Latest Stories</h3>
                    <span className="h-px bg-slate-200 flex-grow ml-6"></span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-12">
                    {outputArticles.map(article => (
                        <ArticleCard key={article.id} article={article} onDelete={onDelete} />
                    ))}
                </div>
            </section>
        </div>
    );
}
