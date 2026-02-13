import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchArticles, deleteArticle } from '../api/client';
import ArticleCard from '../components/ArticleCard';

export default function CategoryPage() {
    const { id } = useParams();
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            setLoading(true);
            const data = await fetchArticles();
            // Filter articles by category (case-insensitive)
            const filtered = data.filter(article =>
                article.category && article.category.toLowerCase() === id.toLowerCase()
            );
            setArticles(filtered);
            setLoading(false);
        }
        load();
    }, [id]);

    const handleDelete = async (articleId) => {
        const success = await deleteArticle(articleId);
        if (success) {
            setArticles(articles.filter(a => a.id !== articleId));
        }
    };

    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>
    );

    return (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-8 border-b border-slate-200 dark:border-slate-700 pb-4 capitalize">
                {id} News
            </h1>

            {articles.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {articles.map(article => (
                        <ArticleCard key={article.id} article={article} onDelete={handleDelete} />
                    ))}
                </div>
            ) : (
                <div className="text-center py-20 text-slate-500 dark:text-slate-400">
                    No articles found in this category.
                </div>
            )}
        </div>
    );
}
