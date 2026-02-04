import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { getTimeAgo } from '../utils';

const ArticlePage = () => {
    const { id } = useParams();
    const [article, setArticle] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(`http://localhost:8000/articles?t=${Date.now()}`)
            .then(res => res.json())
            .then(data => {
                const found = data.find(a => a.id === id);
                setArticle(found);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });
    }, [id]);

    if (loading) return <div className="p-20 text-center font-sans">Loading Ticket #{id}...</div>;
    if (!article) return <div className="p-20 text-center font-sans">Article not found.</div>;

    return (
        <article className="max-w-3xl mx-auto py-12">
            {/* Header */}
            <header className="mb-12 text-center border-b pb-8 border-gray-200">
                <div className="flex justify-center items-center gap-2 text-[10px] font-sans font-bold uppercase tracking-widest text-[#0274b6] mb-6">
                    <Link to="/" className="hover:underline hover:text-black">Home</Link>
                    <span className="text-gray-300">/</span>
                    <Link to={`/category/${article.category || 'Tech'}`} className="hover:underline hover:text-black">{article.category || 'Tech'}</Link>
                </div>

                <h1 className="font-serif text-5xl font-bold leading-tight mb-6 text-black">
                    {article.headline}
                </h1>
                <div className="flex justify-center items-center gap-4 text-sm font-sans text-gray-600 uppercase tracking-wide">
                    <span className="font-bold text-black">By {article.author}</span>
                    <span>|</span>
                    <span>{getTimeAgo(article.published_at)}</span>
                </div>
            </header>

            {/* Hero Image */}
            {article.image_url && (
                <div className="mb-12">
                    <img
                        src={article.image_url}
                        alt={article.headline}
                        className="w-full h-auto object-cover rounded-lg shadow-lg"
                        style={{ maxHeight: '600px' }}
                    />
                    <p className="mt-2 text-center text-xs text-gray-500 font-sans uppercase tracking-widest">
                        Image Source: Associated Press / Web
                    </p>
                </div>
            )}

            {/* Content with Markdown */}
            <div className="prose prose-lg prose-headings:font-serif prose-headings:font-bold prose-headings:text-black prose-p:font-serif prose-p:text-gray-900 prose-blockquote:border-l-4 prose-blockquote:border-black prose-blockquote:bg-gray-50 prose-blockquote:py-2 prose-blockquote:pl-4 prose-blockquote:italic max-w-none">
                <ReactMarkdown
                    components={{
                        h1: ({ node, ...props }) => <h2 className="text-3xl mt-12 mb-6" {...props} />,
                        h2: ({ node, ...props }) => <h2 className="text-2xl mt-10 mb-4 border-b border-gray-200 pb-2" {...props} />,
                        h3: ({ node, ...props }) => <h3 className="text-xl mt-8 mb-4 uppercase tracking-wider font-sans text-gray-800" {...props} />,
                        p: ({ node, ...props }) => <p className="mb-6 leading-relaxed" {...props} />,
                        ul: ({ node, ...props }) => <ul className="list-disc pl-5 mb-6 space-y-2" {...props} />,
                        ol: ({ node, ...props }) => <ol className="list-decimal pl-5 mb-6 space-y-2" {...props} />,
                        li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                    }}
                >
                    {article.content}
                </ReactMarkdown>
            </div>

            {/* Footer tags */}
            <div className="mt-12 pt-8 border-t border-black">
                <div className="mb-4 font-sans text-xs font-bold uppercase text-gray-500">Topics</div>
                <div className="flex flex-wrap gap-2">
                    {article.seo_tags && article.seo_tags.map(tag => (
                        <span key={tag} className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-xs font-sans font-bold uppercase tracking-wide">
                            {tag}
                        </span>
                    ))}
                </div>
            </div>

            <div className="mt-8">
                <Link to="/" className="font-sans font-bold text-sm text-blue-700 uppercase tracking-widest hover:underline">
                    &larr; Back to Front Page
                </Link>
            </div>
        </article>
    );
};

export default ArticlePage;
