import React from 'react';

export default function Footer() {
    return (
        <footer className="bg-white border-t border-gray-200 mt-12 py-8">
            <div className="container mx-auto px-4 text-center text-gray-500 text-sm">
                <p className="font-serif mb-2">&copy; {new Date().getFullYear()} The Daily Agent. All rights reserved.</p>
                <div className="flex justify-center space-x-4">
                    <a href="#" className="hover:text-black transition-colors">Privacy Policy</a>
                    <a href="#" className="hover:text-black transition-colors">Terms of Service</a>
                    <a href="#" className="hover:text-black transition-colors">Contact</a>
                </div>
            </div>
        </footer>
    );
}
