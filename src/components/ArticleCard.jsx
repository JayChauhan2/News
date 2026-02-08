import React from 'react';
import { Link } from 'react-router-dom';
import { Clock } from 'lucide-react';

export default function ArticleCard({ article, featured = false }) {
    if (!article) return null;

    return (
        <Link to={`/article/${article.id}`} className="group block h-full">
            <article className={`h-full flex flex-col ${featured ? 'md:flex-row md:items-center md:gap-8' : ''}`}>

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
                        <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
                            {article.category}
                        </span>
                        <span className="text-slate-300">•</span>
                        <span className="text-xs font-medium text-slate-500 flex items-center">
                            <Clock size={12} className="mr-1" />
                            {new Date(article.date).toLocaleDateString()}
                        </span>
                    </div>

                    <h2 className={`${featured ? 'text-4xl' : 'text-xl'} font-bold text-slate-900 leading-tight mb-3 group-hover:text-indigo-600 transition-colors`}>
                        {article.title || article.headline}
                    </h2>

                    <p className={`text-slate-600 leading-relaxed mb-4 ${featured ? 'text-lg line-clamp-4' : 'text-sm line-clamp-3'}`}>
                        {article.summary}
                    </p>

                    <div className="mt-auto pt-4 flex items-center text-sm font-medium text-slate-900">
                        <div className="w-6 h-6 rounded-full bg-slate-200 flex items-center justify-center text-xs font-bold mr-2 text-slate-600">
                            {article.author?.[0] || 'A'}
                        </div>
                        <span>{article.author}</span>
                    </div>
                </div>
            </article>
        </Link>
    );
}
