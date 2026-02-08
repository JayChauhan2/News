import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { fetchArticle } from '../api/client';
import ReactMarkdown from 'react-markdown';
import { Clock, User } from 'lucide-react';

export default function ArticlePage() {
    const { id } = useParams();
    const [article, setArticle] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            const data = await fetchArticle(id);
            setArticle(data);
            setLoading(false);
        }
        load();
    }, [id]);

    if (loading) return (
        <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600"></div>
        </div>
    );

    if (!article) return (
        <div className="text-center py-20 text-slate-500">Article not found.</div>
    );

    return (
        <article className="max-w-4xl mx-auto py-12 px-4">
            {/* Article Header */}
            <header className="text-center mb-12">
                <span className="inline-block px-3 py-1 rounded-full bg-indigo-50 text-indigo-600 text-sm font-bold uppercase tracking-wide mb-6">
                    {article.category}
                </span>
                <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 mb-6 leading-tight">
                    {article.title || article.headline}
                </h1>

                <div className="flex items-center justify-center space-x-6 text-slate-500 text-sm font-medium">
                    <div className="flex items-center">
                        <User size={16} className="mr-2" />
                        <span>{article.author}</span>
                    </div>
                    <div className="flex items-center">
                        <Clock size={16} className="mr-2" />
                        <span>{new Date(article.date).toLocaleDateString()}</span>
                    </div>
                </div>
            </header>

            {/* Hero Image */}
            {(article.image || article.image_url) && (
                <figure className="mb-12 rounded-2xl overflow-hidden shadow-lg">
                    <img
                        src={article.image || article.image_url}
                        alt={article.title || article.headline}
                        className="w-full h-auto object-cover"
                    />
                    {article.image_caption && (
                        <figcaption className="text-center text-slate-500 text-sm mt-3">
                            {article.image_caption}
                        </figcaption>
                    )}
                </figure>
            )}

            {/* Article Content */}
            <div className="prose prose-lg prose-slate mx-auto max-w-2xl">
                <ReactMarkdown>{article.content}</ReactMarkdown>
            </div>
        </article>
    );
}
