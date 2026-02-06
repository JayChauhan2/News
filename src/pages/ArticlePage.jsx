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

    if (loading) return <div className="p-20 text-center font-sans tracking-widest text-xs uppercase animate-pulse">Loading Edition...</div>;
    if (!article) return <div className="p-20 text-center font-serif italic text-xl">Article not found.</div>;

    return (
        <article className="py-8 lg:py-12 px-4 lg:px-0 mt-12" style={{ maxWidth: '650px', marginLeft: '100px' }}>
            {/* Header */}
            <header className="mb-8 text-center">
                <nav className="flex justify-center items-center gap-2 text-[10px] font-sans font-bold uppercase tracking-widest text-[#0274b6] mb-4">
                    <Link to="/" className="hover:text-black transition-colors">Home</Link>
                    <span className="text-gray-300">/</span>
                    <Link to={`/category/${article.category || 'Tech'}`} className="hover:text-black transition-colors">{article.category || 'Tech'}</Link>
                </nav>

                <h1 className="font-serif text-4xl lg:text-5xl font-bold leading-tight mb-4 text-black">
                    {article.headline}
                </h1>

                {/* Standard WSJ-style Byline */}
                <div className="flex flex-col items-center gap-1 text-xs font-sans uppercase tracking-wider text-gray-500 mb-8">
                    <div className="font-bold text-gray-900">
                        By {article.author}
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="text-gray-400">{getTimeAgo(article.published_at)}</span>
                    </div>
                </div>
            </header>

            {/* Hero Image - Sharp, no shadow, classic caption */}
            {article.image_url && (
                <div className="mb-10">
                    <figure>
                        <img
                            src={article.image_url}
                            alt={article.headline}
                            className="w-full h-auto object-cover border border-gray-100"
                            style={{ maxHeight: '600px' }}
                        />
                        <figcaption className="mt-2 text-right text-[10px] text-gray-500 font-sans uppercase tracking-widest">
                            Image Source: Associated Press / Web
                        </figcaption>
                    </figure>
                </div>
            )}

            {/* Content with Markdown - Refined Typography */}
            <div className="prose prose-lg max-w-none 
                prose-headings:font-serif prose-headings:font-bold prose-headings:text-black 
                prose-p:font-serif prose-p:text-gray-900 prose-p:leading-loose
                prose-a:text-[#0274b6] prose-a:no-underline hover:prose-a:underline
                prose-blockquote:border-l-2 prose-blockquote:border-black prose-blockquote:pl-4 prose-blockquote:italic prose-blockquote:font-serif prose-blockquote:text-gray-700
                first-letter:float-left first-letter:text-5xl first-letter:pr-3 first-letter:font-bold first-letter:font-serif first-letter:text-black">
                <ReactMarkdown
                    components={{
                        h1: ({ node, ...props }) => <h2 className="text-3xl mt-12 mb-6 font-bold" {...props} />,
                        h2: ({ node, ...props }) => <h2 className="text-2xl mt-10 mb-4 font-bold" {...props} />,
                        h3: ({ node, ...props }) => <h3 className="text-lg mt-8 mb-3 uppercase tracking-wider font-sans font-bold text-black border-b border-gray-200 pb-1" {...props} />,
                        p: ({ node, ...props }) => <p className="mb-6" {...props} />,
                        ul: ({ node, ...props }) => <ul className="list-disc pl-5 mb-6 space-y-2 marker:text-gray-400" {...props} />,
                        ol: ({ node, ...props }) => <ol className="list-decimal pl-5 mb-6 space-y-2 marker:text-gray-400" {...props} />,
                        li: ({ node, ...props }) => <li className="pl-1" {...props} />,
                    }}
                >
                    {article.content}
                </ReactMarkdown>
            </div>

            {/* Footer tags - Rectangular tags */}
            <div className="mt-12 pt-8 border-t border-black">
                <div className="mb-3 font-sans text-[10px] font-bold uppercase tracking-widest text-gray-400">Related Topics</div>
                <div className="flex flex-wrap gap-2">
                    {article.seo_tags && article.seo_tags.map(tag => (
                        <span key={tag} className="bg-gray-100 text-gray-600 hover:bg-gray-200 hover:text-black transition-colors px-2 py-1 text-[10px] font-sans font-bold uppercase tracking-wide cursor-pointer">
                            {tag}
                        </span>
                    ))}
                </div>
            </div>

            <div className="mt-12 mb-20 flex justify-center">
                <Link to="/" className="inline-block px-6 py-3 text-xs font-sans font-bold uppercase tracking-widest text-gray-400 hover:text-black transition-colors">
                    &larr; Return to Front Page
                </Link>
            </div>
        </article>
    );
};

export default ArticlePage;
