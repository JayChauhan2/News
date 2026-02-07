import React from 'react';

const NewsGrid = ({ children }) => {
    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-0 lg:divide-x divide-gray-200 border-b border-gray-200">
            {children}
        </div>
    );
};

export const LeftColumn = ({ children }) => {
    return (
        <div className="lg:col-span-2 px-4 py-4 lg:pl-0 lg:pr-4 border-b lg:border-b-0 border-gray-100">
            {children}
        </div>
    );
};

export const CenterColumn = ({ children }) => {
    return (
        <div className="lg:col-span-7 px-4 py-4 lg:px-8 border-b lg:border-b-0 border-gray-100">
            {children}
        </div>
    );
};

export const RightColumn = ({ children }) => {
    return (
        <div className="lg:col-span-3 px-4 py-4 lg:pl-4 lg:pr-0">
            {children}
        </div>
    );
};

export default NewsGrid;
