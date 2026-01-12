/**
 * Footer Loader Script
 * Automatically loads the shared footer component into all pages.
 * 
 * Usage: Add this to any HTML page:
 * <div id="footer-placeholder"></div>
 * <script src="/js/footer-loader.js"></script>
 * 
 * Or replace existing footer with:
 * <footer id="footer-placeholder"></footer>
 * <script src="/js/footer-loader.js"></script>
 */

(function () {
    'use strict';

    // Determine the correct path to footer based on current page depth
    function getFooterPath() {
        const path = window.location.pathname;
        const depth = (path.match(/\//g) || []).length - 1;

        // For root level pages
        if (depth <= 1) {
            return '/components/footer.html';
        }

        // Always use absolute path for consistency
        return '/components/footer.html';
    }

    function loadFooter() {
        const placeholder = document.getElementById('footer-placeholder');

        if (!placeholder) {
            console.warn('Footer placeholder not found. Add <div id="footer-placeholder"></div> to your HTML.');
            return;
        }

        fetch(getFooterPath())
            .then(response => {
                if (!response.ok) {
                    throw new Error('Footer not found: ' + response.status);
                }
                return response.text();
            })
            .then(html => {
                placeholder.outerHTML = html;

                // Re-initialize Lucide icons if present
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
            })
            .catch(error => {
                console.error('Error loading footer:', error);
                // Fallback: keep the placeholder or show nothing
            });
    }

    // Load footer when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', loadFooter);
    } else {
        loadFooter();
    }
})();
