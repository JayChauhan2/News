import React, { useState, useEffect } from 'react';
import ArticleGrid from '../components/ArticleGrid';
import { fetchArticles, deleteArticle } from '../api/client';

export default function HomePage() {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [visibleCount, setVisibleCount] = useState(11); // Initial count: 1 featured + 2 side + 8 grid

    useEffect(() => {
        async function load() {
            const data = await fetchArticles();
            setArticles(data);
            setLoading(false);
        }
        load();
    }, []);

    const handleDelete = async (id) => {
        const success = await deleteArticle(id);
        if (success) {
            setArticles(articles.filter(a => a.id !== id));
        }
    };

    const handleLoadMore = () => {
        setVisibleCount(prev => prev + 8);
    };

    if (loading) {
        return <div className="text-center py-20 font-serif text-lg">Loading the presses...</div>;
    }

    const visibleArticles = articles.slice(0, visibleCount);

    return (
        <div>
            <ArticleGrid articles={visibleArticles} onDelete={handleDelete} />

            {visibleCount < articles.length && (
                <div className="flex justify-center mb-12">
                    <button
                        onClick={handleLoadMore}
                        className="px-8 py-3 bg-white dark:bg-slate-800 border-2 border-black dark:border-white text-black dark:text-white font-serif font-bold uppercase tracking-widest hover:bg-black hover:text-white dark:hover:bg-white dark:hover:text-black transition-all duration-300"
                    >
                        See More News
                    </button>
                </div>
            )}
        </div>
    );
}
