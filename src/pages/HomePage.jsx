import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import NewsGrid, { LeftColumn, CenterColumn, RightColumn } from '../components/NewsGrid';
import StoryCard from '../components/StoryCard';

const HomePage = () => {
    const { category } = useParams();
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchArticles = () => {
            setLoading(true);
            fetch(`http://localhost:8000/articles?t=${Date.now()}`)
                .then(res => res.json())
                .then(data => {
                    let filtered = data;
                    if (category) {
                        filtered = data.filter(a => {
                            if (Array.isArray(a.category)) {
                                return a.category.includes(category);
                            }
                            return a.category === category;
                        });
                    }
                    setArticles(filtered);
                    setLoading(false);
                })
                .catch(err => {
                    console.error("Failed to fetch articles", err);
                    setLoading(false);
                });
        };

        fetchArticles();
        const interval = setInterval(fetchArticles, 10000);
        return () => clearInterval(interval);
    }, [category]);

    if (loading && articles.length === 0) {
        return (
            <div className="min-h-[50vh] flex items-center justify-center">
                <div className="font-sans text-xs uppercase tracking-widest text-gray-400 animate-pulse">
                    Updating The Edition...
                </div>
            </div>
        );
    }

    if (articles.length === 0) {
        return (
            <div className="min-h-[50vh] flex flex-col items-center justify-center text-center p-8">
                <h2 className="font-headline text-3xl text-gray-400 italic mb-2">No news in {category || "this section"} yet.</h2>
                <p className="font-sans text-xs text-gray-300 uppercase tracking-widest">The presses are running...</p>
            </div>
        );
    }

    // Sort articles by date to ensure freshness
    const sortedArticles = [...articles].sort((a, b) => new Date(b.published_at) - new Date(a.published_at));

    // Distribution Logic
    const leadStory = sortedArticles[0];
    const whatsNews = sortedArticles.slice(1, 6); // Left column rapid fire
    const centerStories = sortedArticles.slice(6, 9); // Below hero
    const rightStories = sortedArticles.slice(9, 15); // Right column (Opinion/More)

    return (
        <NewsGrid>
            {/* LEFT COLUMN: WHAT'S NEWS */}
            <LeftColumn>
                <div className="section-header">What's News</div>
                <div className="space-y-4">
                    {whatsNews.map(article => (
                        <StoryCard key={article.id} article={article} variant="compact" />
                    ))}
                </div>
            </LeftColumn>

            {/* CENTER COLUMN: HERO & MAIN NEWS */}
            <CenterColumn>
                <div className="section-header text-center w-full border-t border-black pt-1 mb-6">
                    {category ? `${category} News` : "Top Stories"}
                </div>

                {/* Hero */}
                <StoryCard article={leadStory} variant="hero" showImage={true} />

                <div className="border-t border-gray-200 my-8"></div>

                {/* Sub-Lead Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    {centerStories.map(article => (
                        <StoryCard key={article.id} article={article} variant="standard" showImage={false} />
                    ))}
                </div>
            </CenterColumn>

            {/* RIGHT COLUMN: OPINION / MARKETS */}
            <RightColumn>
                <div className="section-header">Opinion & Commentary</div>
                <div className="bg-gray-50/50 p-4 border border-gray-100 mb-6">
                    {rightStories.slice(0, 3).map(article => (
                        <StoryCard key={article.id} article={article} variant="opinion" showImage={true} />
                    ))}
                </div>

                <div className="section-header mt-8">More Headlines</div>
                <div className="space-y-4">
                    {rightStories.slice(3).map(article => (
                        <StoryCard key={article.id} article={article} variant="compact" />
                    ))}
                </div>
            </RightColumn>
        </NewsGrid>
    );
};

export default HomePage;
