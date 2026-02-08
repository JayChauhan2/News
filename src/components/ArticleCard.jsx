import React from 'react';
import { Link } from 'react-router-dom';
import { Clock } from 'lucide-react';
import { getTimeAgo } from '../utils';

export default function ArticleCard({ article, className = "", variant = "standard" }) {
    const { id, title, summary, category, date, image, author } = article;

    // Variants: 'standard', 'compact', 'lead'

    if (variant === 'lead') {
        return (
            <div className={`group flex flex-col h-full ${className}`}>
                <Link to={`/article/${id}`} className="block overflow-hidden mb-4 relative aspect-[16/9] md:aspect-[3/1] max-h-[500px]">
                    <img
                        src={image || "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&q=80&w=1200"}
                        alt={title}
                        className="object-cover w-full h-full grayscale-[10%] group-hover:grayscale-0 transition-all duration-700"
                    />
                </Link>
                <div className="flex flex-col items-center text-center px-4 md:px-12">
                    <span className="text-[10px] font-bold tracking-[0.2em] uppercase text-accent mb-3 border-b border-accent pb-1">
                        {category || "Top Story"}
                    </span>
                    <Link to={`/article/${id}`}>
                        <h2 className="text-3xl md:text-5xl font-serif font-black leading-[1.1] mb-4 group-hover:text-secondary transition-colors text-balance">
                            {title}
                        </h2>
                    </Link>
                    <p className="text-secondary font-serif text-lg leading-relaxed mb-4 max-w-2xl line-clamp-3">
                        {summary}
                    </p>
                    <div className="text-xs font-sans text-secondary/60 uppercase tracking-widest">
                        By <span className="text-primary font-bold">{author || "Daily Agent"}</span> &bull; {getTimeAgo(date)}
                    </div>
                </div>
            </div>
        )
    }

    if (variant === 'compact') {
        return (
            <div className={`group flex flex-row items-start gap-4 border-b border-black/10 pb-4 mb-4 last:border-0 ${className}`}>
                <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                        <span className="text-[9px] font-bold tracking-widest uppercase text-accent">
                            {category}
                        </span>
                    </div>
                    <Link to={`/article/${id}`}>
                        <h3 className="text-lg font-serif font-bold leading-tight mb-2 group-hover:text-secondary transition-colors">
                            {title}
                        </h3>
                    </Link>
                    <p className="text-xs text-secondary line-clamp-2 mb-2 font-sans">
                        {summary}
                    </p>
                    <div className="text-[10px] text-secondary/60 font-sans">
                        {getTimeAgo(date)}
                    </div>
                </div>
                <Link to={`/article/${id}`} className="block w-24 h-24 flex-shrink-0 bg-gray-100 overflow-hidden">
                    <img
                        src={image}
                        alt={title}
                        className="object-cover w-full h-full grayscale group-hover:grayscale-0 transition-all duration-500"
                    />
                </Link>
            </div>
        )
    }

    // Standard card
    return (
        <div className={`group flex flex-col h-full ${className}`}>
            <Link to={`/article/${id}`} className="block overflow-hidden mb-3 relative aspect-[16/9]">
                <img
                    src={image || "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&q=80&w=800"}
                    alt={title}
                    className="object-cover w-full h-full grayscale-[20%] group-hover:grayscale-0 transition-all duration-500"
                />
            </Link>

            <div className="flex flex-col flex-grow">
                <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold tracking-widest uppercase text-accent">
                        {category || "News"}
                    </span>
                    {date && (
                        <span className="text-[10px] text-secondary/60 font-sans lowercase">
                            {getTimeAgo(date)}
                        </span>
                    )}
                </div>

                <Link to={`/article/${id}`} className="group-hover:opacity-80 transition-opacity">
                    <h3 className="text-xl font-serif font-bold leading-tight mb-2 text-primary">
                        {title}
                    </h3>
                </Link>

                <p className="text-secondary text-sm leading-relaxed mb-3 line-clamp-3 flex-grow font-sans">
                    {summary}
                </p>

                <div className="mt-auto pt-3 border-t border-black/5 flex items-center text-[10px] uppercase tracking-wider text-secondary">
                    <span>By <span className="text-primary font-bold">{author || "Daily Agent"}</span></span>
                </div>
            </div>
        </div>
    );
}
