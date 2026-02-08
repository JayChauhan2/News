import { useState, useEffect } from 'react';

const API_BASE_URL = 'http://localhost:8000';

export async function fetchArticles() {
    try {
        const response = await fetch(`${API_BASE_URL}/articles`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch articles:", error);
        return [];
    }
}

export async function fetchAssignments() {
    try {
        const response = await fetch(`${API_BASE_URL}/assignments`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Failed to fetch assignments:", error);
        return [];
    }
}

export function useArticles() {
    const [articles, setArticles] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        async function load() {
            try {
                const data = await fetchArticles();
                // Sort by date descending if possible, assuming date string allows it
                // If data is just a list, we use it. 
                // We might need to map fields if they don't match ArticleCard expectation
                const formatted = data.map(item => ({
                    id: item.id || `article-${Math.random()}`, // Ensure ID
                    title: item.title || item.headline, // Handle potential field mismatch
                    summary: item.summary,
                    content: item.content || item.body || item.text, // Handle mismatch
                    category: item.category || "General",
                    author: item.author || "Daily Agent",
                    date: item.date || item.published_at || new Date().toISOString(),
                    image: item.image || item.image_url || null
                }));
                setArticles(formatted);
            } catch (e) {
                setError(e);
            } finally {
                setLoading(false);
            }
        }
        load();
    }, []);

    return { articles, loading, error };
}
