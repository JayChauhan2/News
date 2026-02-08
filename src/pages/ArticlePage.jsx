import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { useArticles } from '../api/client';
import { ArrowLeft, Clock, Share2 } from 'lucide-react';
import { getTimeAgo } from '../utils';

export default function ArticlePage() {
    const { id } = useParams();
    const { articles, loading, error } = useArticles();

    // Find article from the fetched list
    const article = articles.find(a => a.id === id);

    if (loading) {
        return (
            <div className="flex h-[50vh] items-center justify-center">
                <div className="text-xl font-serif animate-pulse">Loading Article...</div>
            </div>
        );
    }

    if (!article) {
        return (
            <div className="py-20 text-center">
                <h2 className="text-3xl font-serif mb-4">Article Not Found</h2>
                <Link to="/" className="text-accent underline">Return Home</Link>
            </div>
        );
    }

    const { title, content, category, date, image, author } = article;

    return (
        <div className="max-w-4xl mx-auto animate-fade-in">
            {/* Category & Breadcrumb */}
            <div className="flex items-center space-x-2 text-xs font-bold tracking-widest uppercase mb-6">
                <Link to="/" className="text-secondary hover:text-primary transition-colors">Home</Link>
                <span className="text-secondary">/</span>
                <Link to={`/category/${(category || "general").toLowerCase()}`} className="text-accent">{category}</Link>
            </div>

            {/* Headings */}
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-serif font-bold leading-tight mb-6">
                {title}
            </h1>

            <div className="flex items-center justify-between border-t border-b border-black/10 py-4 mb-8">
                <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 rounded-full bg-secondary/20 flex items-center justify-center text-secondary font-bold">
                        {author ? author.charAt(0) : "A"}
                    </div>
                    <div>
                        <p className="font-bold text-sm text-primary">By {author || "Daily Agent"}</p>
                        <div className="flex items-center text-xs text-secondary space-x-2">
                            <Clock size={12} />
                            <span>{getTimeAgo(date)}</span>
                        </div>
                    </div>
                </div>
                <div className="flex space-x-2">
                    <button className="p-2 hover:bg-black/5 rounded-full transition-colors">
                        <Share2 size={18} className="text-secondary" />
                    </button>
                </div>
            </div>

            {/* Main Image */}
            {image && (
                <div className="mb-10 h-[40vh] max-h-[400px] relative overflow-hidden bg-gray-100">
                    <img src={image} alt={title} className="w-full h-full object-cover" />
                </div>
            )}

            {/* Content */}
            <div className="max-w-2xl mx-auto prose prose-lg prose-headings:font-serif prose-headings:font-bold prose-p:font-sans prose-p:leading-relaxed prose-a:text-accent hover:prose-a:text-primary">
                {/* If content is HTML, render it. If it's plain text, wrap in p tags */}
                {content && (content.includes('<') ? (
                    <div dangerouslySetInnerHTML={{ __html: content }} />
                ) : (
                    content.split('\n\n').map((paragraph, index) => (
                        <p key={index}>{paragraph}</p>
                    ))
                ))}
            </div>

            {/* Footer Navigation */}
            <div className="mt-16 pt-8 border-t border-black/10 flex justify-between">
                <Link to="/" className="flex items-center font-bold text-primary hover:text-accent transition-colors">
                    <ArrowLeft size={16} className="mr-2" />
                    Back to Top Stories
                </Link>
            </div>
        </div>
    );
}
