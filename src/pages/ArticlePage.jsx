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

    if (loading) {
        return (
            <div className="min-h-[50vh] flex items-center justify-center">
                <div className="font-sans text-xs uppercase tracking-widest text-gray-400 animate-pulse">
                    Loading Article...
                </div>
            </div>
        );
    }

    if (!article) {
        return (
            <div className="min-h-[50vh] flex flex-col items-center justify-center">
                <div className="font-headline text-2xl text-gray-400 italic mb-4">Article not found.</div>
                <Link to="/" className="text-xs font-sans font-bold uppercase tracking-widest hover:underline">
                    Return to Home
                </Link>
            </div>
        );
    }

    return (
        <article className="py-12 px-4">
            <div className="max-w-3xl mx-auto">
                {/* Header */}
                <header className="mb-10 text-center">
                    <nav className="flex justify-center items-center gap-2 text-[11px] font-sans font-bold uppercase tracking-widest text-[#0274b6] mb-6">
                        <Link to="/" className="hover:text-black transition-colors">Home</Link>
                        <span className="text-gray-300">/</span>
                        <Link to={`/category/${article.category || 'Tech'}`} className="hover:text-black transition-colors">
                            {article.category || 'Tech'}
                        </Link>
                    </nav>

                    <h1 className="font-headline text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6 text-black">
                        {article.headline}
                    </h1>

                    <div className="flex flex-col items-center justify-center border-y border-gray-100 py-4">
                        <div className="font-sans text-xs font-bold uppercase tracking-wider text-gray-900 mb-1">
                            By {article.author || "The Daily Agent Staff"}
                        </div>
                        <div className="font-sans text-[10px] uppercase tracking-wider text-gray-500">
                            {getTimeAgo(article.published_at)} • 2 Min Read
                        </div>
                    </div>
                </header>

                {/* Hero Image */}
                {article.image_url && (
                    <figure className="mb-12">
                        <div className="w-full max-h-[500px] overflow-hidden border border-gray-100 bg-gray-50">
                            <img
                                src={article.image_url}
                                alt={article.headline}
                                className="w-full h-full object-cover"
                            />
                        </div>
                        {article.image_prompt && (
                            <figcaption className="mt-2 text-right text-[10px] text-gray-400 font-sans uppercase tracking-wider">
                                AI Generated Image • Prompt: {article.image_prompt.substring(0, 50)}...
                            </figcaption>
                        )}
                    </figure>
                )}

                {/* Content */}
                <div className="prose prose-lg max-w-none 
                    prose-headings:font-headline prose-headings:font-bold prose-headings:text-black 
                    prose-p:font-body prose-p:text-gray-800 prose-p:text-[1.125rem] prose-p:leading-[1.8]
                    prose-a:text-[#0274b6] prose-a:no-underline hover:prose-a:underline
                    prose-blockquote:border-l-[3px] prose-blockquote:border-black prose-blockquote:pl-6 prose-blockquote:py-2 prose-blockquote:italic prose-blockquote:font-headline prose-blockquote:text-xl prose-blockquote:text-gray-900 prose-blockquote:bg-gray-50
                    first-letter:float-left first-letter:text-[5rem] first-letter:pr-4 first-letter:font-bold first-letter:font-headline first-letter:text-black first-letter:leading-[4rem] first-letter:mt-[-0.5rem]">
                    <ReactMarkdown
                        components={{
                            h1: ({ node, ...props }) => <h2 className="text-3xl mt-12 mb-6" {...props} />,
                            h2: ({ node, ...props }) => <h2 className="text-2xl mt-10 mb-4" {...props} />,
                            h3: ({ node, ...props }) => <h3 className="text-lg mt-8 mb-3 uppercase tracking-wider font-sans font-bold border-b border-gray-200 pb-1" {...props} />,
                            li: ({ node, ...props }) => <li className="pl-1 marker:text-gray-300" {...props} />,
                        }}
                    >
                        {article.content}
                    </ReactMarkdown>
                </div>

                {/* Footer Navigation */}
                <div className="mt-16 pt-8 border-t border-black flex justify-center">
                    <Link to="/" className="group flex items-center gap-2 text-xs font-sans font-bold uppercase tracking-widest text-gray-400 hover:text-black transition-colors">
                        <span>&larr;</span>
                        <span className="group-hover:translate-x-1 transition-transform">Return to Front Page</span>
                    </Link>
                </div>
            </div>
        </article>
    );
};

export default ArticlePage;
