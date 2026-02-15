import React from 'react';
import { Link } from 'react-router-dom';
import { Clock, Trash2 } from 'lucide-react';
import { formatDate, formatRelativeTime } from '../utils/dateUtils';

export default function ArticleCard({ article, featured = false, onDelete, className = "" }) {
    if (!article) return null;

    return (
        <Link to={`/article/${article.id}`} className={`group block h-full ${className}`}>
            <article className={`h-full flex flex-col relative`}>

                {/* Delete Button (Visible on Hover) */}
                {onDelete && (
                    <button
                        onClick={(e) => {
                            e.preventDefault(); // Stop navigation
                            e.stopPropagation();
                            if (window.confirm(`Are you sure you want to delete "${article.title || article.headline}"?`)) {
                                onDelete(article.id);
                            }
                        }}
                        className="absolute top-2 right-2 z-20 p-2 bg-white/90 rounded-full text-red-500 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white hover:text-red-600 shadow-sm border border-gray-200"
                        title="Delete Article"
                    >
                        <Trash2 size={16} />
                    </button>
                )}

                {/* Image Container */}
                {/* For featured articles, image is larger. For standard, it's compact. */}
                <div className={`overflow-hidden mb-4 ${featured ? 'aspect-video w-full' : 'aspect-[3/2] w-full'}`}>
                    {article.image || article.image_url ? (
                        <img
                            src={article.image || article.image_url}
                            alt={article.title || article.headline}
                            className="w-full h-full object-cover filter grayscale-[10%] contrast-[1.1] group-hover:grayscale-0 transition-all duration-500"
                        />
                    ) : (
                        <div className="w-full h-full bg-gray-100 flex items-center justify-center text-slate-300 border border-gray-100">
                            <span className="font-sans text-xs uppercase tracking-widest">No Image</span>
                        </div>
                    )}
                </div>

                {/* Content */}
                <div className="flex flex-col flex-grow">
                    <div className="flex items-center space-x-2 mb-2">
                        <span className="text-[10px] font-bold font-sans uppercase tracking-widest text-indigo-700 dark:text-indigo-400">
                            {article.category || 'General'}
                        </span>
                        <span className="text-gray-300">•</span>
                        <span className="text-[10px] font-medium font-sans text-gray-500 uppercase tracking-wider">
                            {formatRelativeTime(article.date || article.published_at)}
                        </span>
                    </div>

                    <h2 className={`${featured ? 'text-3xl md:text-4xl' : 'text-xl'} font-serif font-bold text-slate-900 dark:text-white leading-tight mb-3 group-hover:text-indigo-800 dark:group-hover:text-indigo-300 transition-colors line-clamp-3`}>
                        {article.title || article.headline}
                    </h2>

                    <p className={`font-serif text-slate-600 dark:text-slate-300 leading-relaxed ${featured ? 'text-lg line-clamp-4' : 'text-sm line-clamp-3'}`}>
                        {article.summary}
                    </p>
                </div>
            </article>
        </Link>
    );
}
