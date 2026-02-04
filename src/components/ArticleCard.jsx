import React from 'react';
import { Link } from 'react-router-dom';
import { getTimeAgo } from '../utils';

const ArticleCard = ({ article }) => {
    return (
        <div className="py-8 first:pt-0 group">
            {/* Metadata */}
            <div className="flex items-center gap-2 mb-2 font-sans text-xs uppercase tracking-wider text-gray-500">
                <span className="font-bold text-black">{article.category || "General"}</span>
                <span className="text-gray-300">|</span>
                <span>{getTimeAgo(article.published_at)}</span>
            </div>

            {/* Headline Link */}
            <Link to={`/article/${article.id}`} className="block">
                <h3 className="font-serif text-3xl font-bold text-black leading-tight mb-3 group-hover:text-gray-600 transition-colors cursor-pointer">
                    {article.headline}
                </h3>
            </Link>

            {/* Content Preview */}
            <div className="font-serif text-gray-800 text-lg leading-relaxed line-clamp-3 mb-4">
                {/* 
                   We render a plain text preview to avoid partial markdown issues in the card.
                   Or we can just use the meta_description. 
                 */}
                {article.meta_description || "Click to read the full story on the autonomous press..."}
            </div>

            {/* Footer / Read More */}
            <div className="flex items-center justify-between">
                <div className="text-xs font-sans font-bold text-gray-600 uppercase">
                    By {article.author}
                </div>

                <Link
                    to={`/article/${article.id}`}
                    className="text-sm font-sans font-bold text-blue-700 hover:text-black uppercase tracking-widest transition-colors"
                >
                    Read Full Story &rarr;
                </Link>
            </div>
        </div>
    );
};

export default ArticleCard;
