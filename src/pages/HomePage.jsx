import React, { useState, useEffect } from 'react';
import ArticleGrid from '../components/ArticleGrid';
import { fetchArticles } from '../api/client';

export default function HomePage() {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        async function load() {
            const data = await fetchArticles();
            setArticles(data);
            setLoading(false);
        }
        load();
    }, []);

    if (loading) {
        return <div className="text-center py-20 font-serif text-lg">Loading the presses...</div>;
    }

    return (
        <div>
            <ArticleGrid articles={articles} />
        </div>
    );
}
