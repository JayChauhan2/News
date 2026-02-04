import React, { useState, useEffect } from 'react';

const AssignmentTicker = () => {
    const [assignments, setAssignments] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:8000/assignments?t=${Date.now()}`)
            .then(res => res.json())
            .then(data => setAssignments(data))
            .catch(err => console.error("Failed to fetch assignments", err));
    }, []);

    if (assignments.length === 0) return null;

    return (
        <div style={{
            border: '1px solid #444',
            borderRadius: '8px',
            padding: '15px',
            backgroundColor: '#252526',
            color: '#E0E0E0',
            marginBottom: '30px'
        }}>
            <h3 style={{ marginTop: 0, fontSize: '1em', textTransform: 'uppercase', letterSpacing: '1px' }}>
                🔴 Live Wire: The Watchtower
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                {assignments.slice(0, 5).map(ticket => ( // Show top 5
                    <li key={ticket.id} style={{
                        padding: '8px 0',
                        borderBottom: '1px solid #333',
                        fontSize: '0.9em'
                    }}>
                        <strong style={{ color: '#FFD700' }}>[{ticket.score}/10]</strong> {ticket.title}
                        <div style={{ fontSize: '0.8em', color: '#888', marginTop: '4px' }}>
                            REASON: {ticket.reasoning}
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AssignmentTicker;
