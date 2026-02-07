import React from 'react';
import { Link } from 'react-router-dom';

const getTimeAgo = (dateFormatted) => {
    if (!dateFormatted) return '';
    try {
        const date = new Date(dateFormatted);
        const now = new Date();
        const diffInSeconds = Math.floor((now - date) / 1000);

        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`;
        return `${Math.floor(diffInSeconds / 86400)}d ago`;
    } catch (e) {
        return '';
    }
};

const StoryCard = ({ article, variant = "standard", showImage = true }) => {
    if (!article) return null;

    const { id, headline, meta_description, published_at, category, image_url, image_prompt } = article;
    const timeAgo = getTimeAgo(published_at);
    const cat = Array.isArray(category) ? category[0] : category;

    // HERO VARIANT (Large Image, Large Headline)
    if (variant === "hero") {
        return (
            <div className="mb-8 group cursor-pointer">
                <Link to={`/article/${id}`}>
                    <div className="flex flex-col gap-3">
                        {image_url && showImage && (
                            <div className="w-full aspect-[2/1] max-h-[400px] overflow-hidden border border-gray-100 mb-2">
                                <img
                                    src={image_url}
                                    alt={headline}
                                    className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105"
                                />
                            </div>
                        )}
                        <div className="flex items-center gap-2">
                            <span className="kicker">{cat}</span>
                            <span className="timestamp px-2 border-l border-gray-300">{timeAgo}</span>
                        </div>
                        <h2 className="font-headline text-3xl lg:text-5xl leading-tight group-hover:text-[#0274b6] transition-colors">
                            {headline}
                        </h2>
                        <p className="font-body text-lg text-gray-600 leading-relaxed line-clamp-3">
                            {meta_description}
                        </p>
                    </div>
                </Link>
            </div>
        );
    }

    // COMPACT VARIANT (Headline Only, Small)
    if (variant === "compact") {
        return (
            <div className="mb-4 group border-b border-gray-100 pb-2 last:border-0 last:pb-0">
                <Link to={`/article/${id}`}>
                    <div className="flex items-start justify-between gap-2">
                        <div>
                            <span className="kicker text-[10px] mb-1">{cat}</span>
                            <h4 className="font-headline text-md leading-snug group-hover:text-[#0274b6] transition-colors">
                                {headline}
                            </h4>
                            <div className="timestamp mt-1">{timeAgo}</div>
                        </div>
                    </div>
                </Link>
            </div>
        );
    }

    // OPINION VARIANT
    if (variant === "opinion") {
        return (
            <div className="mb-6 group border-b border-gray-100 pb-4 last:border-0">
                <Link to={`/article/${id}`}>
                    <div className="flex gap-4 items-start">
                        {image_url && showImage && (
                            <div className="w-16 h-16 rounded-full overflow-hidden flex-shrink-0 border border-gray-200">
                                <img src={image_url} alt="" className="w-full h-full object-cover grayscale" />
                            </div>
                        )}
                        <div>
                            <span className="kicker text-gray-500">Opinion</span>
                            <h3 className="font-headline text-lg italic leading-tight group-hover:text-[#0274b6] mb-1">
                                {headline}
                            </h3>
                            <p className="font-sans text-xs uppercase font-bold text-gray-400">
                                {article.author || "The Editors"}
                            </p>
                        </div>
                    </div>
                </Link>
            </div>
        );
    }

    // STANDARD VARIANT (Default)
    return (
        <div className="mb-6 group flex gap-4 border-b border-gray-100 pb-6 last:border-0">
            <div className="flex-1">
                <Link to={`/article/${id}`}>
                    <div className="flex items-center gap-2 mb-1">
                        <span className="kicker">{cat}</span>
                        <span className="timestamp">{timeAgo}</span>
                    </div>
                    <h3 className="font-headline text-xl lg:text-2xl font-bold leading-tight mb-2 group-hover:text-[#0274b6] transition-colors">
                        {headline}
                    </h3>
                    <p className="font-body text-sm text-gray-600 line-clamp-2 leading-relaxed">
                        {meta_description}
                    </p>
                </Link>
            </div>
            {image_url && showImage && (
                <div className="w-1/3 max-w-[120px] lg:max-w-[150px] aspect-square flex-shrink-0">
                    <Link to={`/article/${id}`}>
                        <img
                            src={image_url}
                            alt={headline}
                            className="w-full h-full object-cover border border-gray-100 grayscale hover:grayscale-0 transition-all duration-500"
                        />
                    </Link>
                </div>
            )}
        </div>
    );
};

export default StoryCard;
