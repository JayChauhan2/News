import React from 'react';

import { Link } from 'react-router-dom';
import { Clock, Trash2 } from 'lucide-react';
import { formatDate, formatRelativeTime } from '../utils/dateUtils';

export default function ArticleCard({ article, featured = false, onDelete }) {
    if (!article) return null;

    return (
        <Link to={`/article/${article.id}`} className="group block h-full">
            <article className={`h-full flex flex-col ${featured ? 'md:flex-row md:items-center md:gap-8' : ''} relative`}>

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
                        className="absolute top-2 right-2 z-20 p-2 bg-white/90 rounded-full text-red-500 opacity-0 group-hover:opacity-100 transition-opacity hover:bg-white hover:text-red-600 shadow-sm"
                        title="Delete Article"
                    >
                        <Trash2 size={16} />
                    </button>
                )}

                {/* Image Container */}
                <div className={`overflow-hidden rounded-2xl bg-slate-100 ${featured ? 'md:w-2/3 md:h-96' : 'h-56 mb-4'}`}>
                    {article.image || article.image_url ? (
                        <img
                            src={article.image || article.image_url}
                            alt={article.title || article.headline}
                            className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500"
                        />
                    ) : (
                        <div className="w-full h-full flex items-center justify-center text-slate-300">
                            <span>No Image</span>
                        </div>
                    )}
                </div>

                {/* Content */}
                <div className={`flex flex-col ${featured ? 'md:w-1/3 py-4' : 'flex-grow'}`}>
                    <div className="flex items-center space-x-2 mb-3">
                        <Link to={`/category/${article.category}`} className="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wider hover:text-indigo-800 dark:hover:text-indigo-300 transition-colors">
                            {article.category}
                        </Link>
                        <span className="text-slate-300 dark:text-slate-600">•</span>
                        <span className="text-xs font-medium text-slate-500 dark:text-slate-400 flex items-center">
                            <Clock size={12} className="mr-1" />
                            {formatRelativeTime(article.date || article.published_at)}
                        </span>
                    </div>

                    <h2 className={`${featured ? 'text-4xl' : 'text-xl'} font-bold text-slate-900 dark:text-white leading-tight mb-3 group-hover:text-indigo-600 dark:group-hover:text-indigo-400 transition-colors`}>
                        {article.title || article.headline}
                    </h2>

                    <p className={`text-slate-600 dark:text-slate-300 leading-relaxed mb-4 ${featured ? 'text-lg line-clamp-4' : 'text-sm line-clamp-3'}`}>
                        {article.summary}
                    </p>
                </div>
            </article>
        </Link>
    );
}
