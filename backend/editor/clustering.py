from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def deduplicate_news(articles, similarity_threshold=0.85):
    """
    Groups similar articles together.
    Returns a list of clusters. Each cluster is a list of articles.
    """
    if not articles:
        return []

    # 1. Prepare texts for vectorization
    # We combine title + summary for better matching
    texts = [f"{a['title']} {a['summary']}" for a in articles]
    
    # 2. Vectorize
    vectorizer = TfidfVectorizer(stop_words='english')
    try:
        tfidf_matrix = vectorizer.fit_transform(texts)
    except ValueError:
        # Happens if empty vocabulary (e.g. funny encoding or empty strings)
        return [[a] for a in articles]

    # 3. Calculate Cosine Similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)

    # 4. Cluster using a greedy approach
    # (Simple & effective for news dedup)
    clusters = []
    visited = [False] * len(articles)

    for i in range(len(articles)):
        if visited[i]:
            continue

        cluster = [articles[i]]
        visited[i] = True

        for j in range(i + 1, len(articles)):
            if not visited[j]:
                if similarity_matrix[i][j] > similarity_threshold:
                    cluster.append(articles[j])
                    visited[j] = True
        
        clusters.append(cluster)

    print(f"Watchtower: Deduplicated {len(articles)} articles into {len(clusters)} unique clusters.")
    return clusters
