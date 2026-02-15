import React from 'react';
import ArticleCard from './ArticleCard';

export default function ArticleGrid({ articles, onDelete }) {
    if (!articles || articles.length === 0) {
        return (
            <div className="py-20 text-center container mx-auto">
                <h3 className="text-2xl font-serif font-bold text-slate-900 mb-2">No News Found</h3>
                <p className="text-slate-500 font-sans">The world is quiet today.</p>
            </div>
        );
    }

    const outputArticles = [...articles];
    const featured = outputArticles.shift(); // First article is featured
    // Get next 2 for the "Top Stories" side column
    const sideStories = outputArticles.splice(0, 2);
    // The rest go in the bottom grid
    const remainingStories = outputArticles;

    return (
        <div className="py-8 border-b-2 border-black dark:border-white mb-12">

            {/* Top Section: Featured + Side Stories */}
            <section className="mb-12">
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

                    {/* Main Featured Article (Span 8) */}
                    <div className="lg:col-span-8 lg:pr-8 lg:border-r border-gray-200 dark:border-gray-800">
                        <ArticleCard article={featured} featured={true} onDelete={onDelete} />
                    </div>

                    {/* Side Column (Span 4) */}
                    <div className="lg:col-span-4 flex flex-col gap-8">
                        {sideStories.map((article, idx) => (
                            <div key={article.id} className={idx !== sideStories.length - 1 ? "border-b border-gray-200 dark:border-gray-800 pb-8" : ""}>
                                <ArticleCard article={article} onDelete={onDelete} />
                            </div>
                        ))}
                        {/* If no side stories, maybe show an ad or placeholder? Leaving empty for now. */}
                    </div>
                </div>
            </section>

            {/* Divider */}
            <div className="w-full h-px bg-black dark:bg-white mb-8 opacity-20"></div>

            {/* Bottom Grid Section */}
            <section>
                <div className="flex items-center justify-between mb-6">
                    <h3 className="font-sans font-bold text-xs uppercase tracking-widest text-gray-500">More News</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                    {remainingStories.map((article, idx) => (
                        // Add a right border to all except the last in each row (simplified as right border on all but 4n)
                        <div key={article.id} className="pb-8 border-b border-gray-100 dark:border-gray-800 lg:border-b-0">
                            <ArticleCard article={article} onDelete={onDelete} />
                        </div>
                    ))}
                </div>
            </section>
        </div>
    );
}
