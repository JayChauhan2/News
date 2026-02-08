import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchArticle } from '../api/client';
import ReactMarkdown from 'react-markdown';
import { Clock } from 'lucide-react';
import { formatDate } from '../utils/dateUtils';

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

    // Extract Source Link from content
    const sourceMatch = article.content.match(/\[Source\]\((.*?)\)/);
    const sourceUrl = sourceMatch ? sourceMatch[1] : article.source_link;
    const cleanContent = article.content.replace(/\[Source\]\((.*?)\)/g, '').trim();

    return (
        <article className="max-w-4xl mx-auto py-12 px-4">
            {/* Article Header */}
            <header className="text-center mb-12">
                <Link to={`/category/${article.category}`} className="inline-block px-3 py-1 rounded-full bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 text-sm font-bold uppercase tracking-wide mb-6 hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition-colors">
                    {article.category}
                </Link>
                <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 dark:text-white mb-6 leading-tight">
                    {article.title || article.headline}
                </h1>

                <div className="flex items-center justify-center space-x-6 text-slate-500 dark:text-slate-400 text-sm font-medium">
                    <div className="flex items-center">
                        <Clock size={16} className="mr-2" />
                        <span>{formatDate(article.date || article.published_at)}</span>
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
                        <figcaption className="text-center text-slate-500 dark:text-slate-400 text-sm mt-3">
                            {article.image_caption}
                        </figcaption>
                    )}
                </figure>
            )}

            {/* Article Content */}
            <div className="prose prose-lg prose-slate dark:prose-invert mx-auto max-w-2xl mb-16">
                <ReactMarkdown>{cleanContent}</ReactMarkdown>
            </div>

            {/* Source Link Footer */}
            {sourceUrl && (
                <div className="max-w-2xl mx-auto border-t border-slate-200 dark:border-slate-700 pt-8 mt-12">
                    <div className="bg-slate-50 dark:bg-slate-800 rounded-xl p-6 flex flex-col sm:flex-row items-center justify-between gap-4 transition-colors">
                        <div>
                            <h3 className="font-bold text-slate-900 dark:text-white mb-1">Original Source</h3>
                            <p className="text-sm text-slate-500 dark:text-slate-400">Read the full story at the publisher's website.</p>
                        </div>
                        <a
                            href={sourceUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="whitespace-nowrap inline-flex items-center px-5 py-2.5 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-bold text-sm hover:bg-slate-700 dark:hover:bg-slate-200 transition-colors"
                        >
                            Read Full Story
                            <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
                        </a>
                    </div>
                </div>
            )}
        </article>
    );
}
