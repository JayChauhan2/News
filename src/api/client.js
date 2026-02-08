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

export async function fetchArticle(id) {
    const articles = await fetchArticles();
    return articles.find(a => a.id === id);
}
