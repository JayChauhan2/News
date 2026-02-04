import React, { useState, useEffect } from 'react';
import ArticleCard from '../components/ArticleCard';
import AssignmentTicker from '../components/AssignmentTicker';

const HomePage = () => {
    const [articles, setArticles] = useState([]);

    useEffect(() => {
        // Poll for articles
        const fetchArticles = () => {
            fetch('http://localhost:8000/articles')
                .then(res => res.json())
                .then(data => setArticles(data))
                .catch(err => console.error("Failed to fetch articles", err));
        };

        fetchArticles();
        const interval = setInterval(fetchArticles, 10000); // Check every 10s
        return () => clearInterval(interval);
    }, []);

    return (
        <div style={{ display: 'flex', maxWidth: '1200px', margin: '0 auto', padding: '20px', gap: '40px', fontFamily: 'Inter, sans-serif' }}>
            {/* Main Content: The News Feed */}
            <main style={{ flex: 2 }}>
                <h1 style={{
                    fontSize: '2.5rem',
                    borderBottom: '4px solid #4CAF50',
                    paddingBottom: '10px',
                    marginBottom: '30px',
                    fontFamily: 'serif'
                }}>
                    The Autonomous Times
                </h1>

                {articles.length === 0 ? (
                    <div style={{ textAlign: 'center', color: '#666', marginTop: '50px' }}>
                        <p>Waiting for the Senior Reporter to publish...</p>
                        <small>(Ensure backend/watchtower/main.py is running)</small>
                    </div>
                ) : (
                    articles.map(article => (
                        <ArticleCard key={article.id} article={article} />
                    ))
                )}
            </main>

            {/* Sidebar: The Agent Brain */}
            <aside style={{ flex: 1 }}>
                <div style={{ position: 'sticky', top: '20px' }}>
                    <AssignmentTicker />

                    <div style={{
                        padding: '20px',
                        backgroundColor: '#1E1E1E',
                        borderRadius: '8px',
                        fontSize: '0.9em',
                        color: '#AAA'
                    }}>
                        <h4>System Status</h4>
                        <ul style={{ paddingLeft: '20px' }}>
                            <li>Search: <span style={{ color: '#4CAF50' }}>Active</span> (Tavily)</li>
                            <li>Writer: <span style={{ color: '#4CAF50' }}>Active</span> (Groq)</li>
                            <li>Editor: <span style={{ color: '#4CAF50' }}>Active</span> (Scikit-learn)</li>
                        </ul>
                    </div>
                </div>
            </aside>
        </div>
    );
};

export default HomePage;
