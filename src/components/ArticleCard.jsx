import React from 'react';

const ArticleCard = ({ article }) => {
    return (
        <div style={{
            border: '1px solid #333',
            borderRadius: '8px',
            padding: '20px',
            marginBottom: '20px',
            backgroundColor: '#1E1E1E',
            color: '#E0E0E0'
        }}>
            <h2 style={{ marginTop: 0, color: '#4CAF50' }}>{article.headline}</h2>
            <div style={{ fontSize: '0.8em', color: '#888', marginBottom: '10px' }}>
                {article.published_at} | By {article.author}
            </div>

            {/* Simulation of where the Hero Image would go */}
            <div style={{
                backgroundColor: '#000',
                height: '200px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                border: '1px dashed #555',
                marginBottom: '15px',
                color: '#555',
                fontSize: '0.9em',
                fontStyle: 'italic',
                padding: '20px',
                textAlign: 'center'
            }}>
                [Hero Image Prompt: {article.image_prompt}]
            </div>

            <p style={{ lineHeight: '1.6' }}>{article.meta_description}</p>

            <div style={{ marginTop: '15px' }}>
                {article.seo_tags && article.seo_tags.map(tag => (
                    <span key={tag} style={{
                        display: 'inline-block',
                        backgroundColor: '#333',
                        color: '#888',
                        padding: '2px 8px',
                        borderRadius: '4px',
                        fontSize: '0.8em',
                        marginRight: '8px'
                    }}>
                        {tag}
                    </span>
                ))}
            </div>

            <details style={{ marginTop: '15px', cursor: 'pointer', color: '#64B5F6' }}>
                <summary>Read Full Article</summary>
                <div style={{
                    marginTop: '10px',
                    color: '#CCC',
                    whiteSpace: 'pre-wrap',
                    textAlign: 'left',
                    fontFamily: 'monospace'
                }}>
                    {article.content}
                </div>
            </details>
        </div>
    );
};

export default ArticleCard;
