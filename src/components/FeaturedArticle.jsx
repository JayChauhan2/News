import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';
import { formatDate } from '../utils/dateUtils';

export default function FeaturedArticle({ article }) {
    if (!article) return null;
    const { id, title, summary, category, date, image, author } = article;

    return (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 mb-16 items-center border-b border-black/10 pb-12">
            <Link to={`/article/${id}`} className="relative aspect-[16/10] overflow-hidden group w-full h-full">
                <img
                    src={image || "https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&q=80&w=1600"}
                    alt={title}
                    className="object-cover w-full h-full transition-transform duration-700 group-hover:scale-105"
                />
            </Link>

            <div className="flex flex-col justify-center">
                <div className="flex items-center space-x-2 mb-4 text-xs font-bold tracking-widest uppercase text-accent">
                    <Link to={`/category/${category || "Top Story"}`} className="px-2 py-1 border border-accent text-accent hover:bg-accent hover:text-white transition-colors">
                        {category || "Top Story"}
                    </Link>
                    <span className="text-secondary dark:text-slate-400 font-medium normal-case">{formatDate(date || article.published_at)}</span>
                </div>

                <Link to={`/article/${id}`}>
                    <h2 className="text-3xl md:text-4xl lg:text-5xl font-serif font-bold leading-tight mb-6 text-slate-900 dark:text-white hover:text-accent dark:hover:text-accent transition-colors">
                        {title}
                    </h2>
                </Link>

                <p className="text-secondary dark:text-slate-300 text-lg md:text-xl leading-relaxed mb-8">
                    {summary}
                </p>

                <div className="flex items-center justify-between">
                    <Link to={`/article/${id}`} className="group flex items-center text-sm font-bold tracking-wider text-slate-900 dark:text-white hover:text-accent dark:hover:text-accent transition-colors">
                        READ FULL STORY
                        <ArrowRight size={16} className="ml-2 transform group-hover:translate-x-1 transition-transform" />
                    </Link>
                </div>
            </div>
        </div>
    );
}
