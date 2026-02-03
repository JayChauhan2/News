import React from 'react';

const Footer = () => {
    return (
        <footer className="border-t-4 border-black mt-16 py-12 bg-gray-50">
            <div className="max-w-6xl mx-auto px-4 grid grid-cols-1 md:grid-cols-4 gap-8 font-sans text-sm">
                <div>
                    <h4 className="font-bold uppercase mb-4 tracking-wider">The News Journal</h4>
                    <p className="text-gray-600 mb-4">
                        Essential news, expert analysis, and exclusive insights from around the globe.
                    </p>
                    <p className="text-xs text-gray-500">
                        &copy; {new Date().getFullYear()} The News Journal. All rights reserved.
                    </p>
                </div>

                {/* Placeholder links */}
                <div>
                    <h4 className="font-bold uppercase mb-4 tracking-wider">Sections</h4>
                    <ul className="space-y-2 text-gray-600">
                        <li>World</li>
                        <li>U.S.</li>
                        <li>Politics</li>
                        <li>Economy</li>
                    </ul>
                </div>

                <div>
                    <h4 className="font-bold uppercase mb-4 tracking-wider">Opinion</h4>
                    <ul className="space-y-2 text-gray-600">
                        <li>Editorials</li>
                        <li>Commentary</li>
                        <li>Letters to the Editor</li>
                    </ul>
                </div>

                <div>
                    <h4 className="font-bold uppercase mb-4 tracking-wider">Subscribe</h4>
                    <p className="text-gray-600 mb-4">
                        Get full access to The News Journal.
                    </p>
                    <button className="bg-black text-white px-6 py-2 uppercase font-bold text-xs tracking-widest hover:bg-gray-800 transition-colors">
                        Subscribe Now
                    </button>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
