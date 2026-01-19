/**
 * Blog View Counter - Client-side JavaScript
 * 
 * Add this script to blog pages to:
 * 1. Increment the view count on page load
 * 2. Display the current view count
 * 
 * Usage: <script src="/js/view-counter.js" defer></script>
 */

(function () {
    'use strict';

    const API_ENDPOINT = '/api/views';
    const STORAGE_KEY = 'viewed_pages';
    const VIEW_COOLDOWN_MS = 30 * 60 * 1000; // 30 minutes - prevent spam refreshes

    /**
     * Get the current page path (without query params)
     */
    function getPagePath() {
        return window.location.pathname.replace(/\.html$/, '').replace(/\/$/, '') || '/';
    }

    /**
     * Check if this page was recently viewed (to prevent refresh spam)
     */
    function wasRecentlyViewed(url) {
        try {
            const viewedPages = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
            const lastViewed = viewedPages[url];
            if (lastViewed && (Date.now() - lastViewed) < VIEW_COOLDOWN_MS) {
                return true;
            }
        } catch (e) {
            // localStorage not available or error
        }
        return false;
    }

    /**
     * Mark page as viewed in localStorage
     */
    function markAsViewed(url) {
        try {
            const viewedPages = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
            viewedPages[url] = Date.now();

            // Clean up old entries (older than 24 hours)
            const oneDayAgo = Date.now() - (24 * 60 * 60 * 1000);
            for (const key in viewedPages) {
                if (viewedPages[key] < oneDayAgo) {
                    delete viewedPages[key];
                }
            }

            localStorage.setItem(STORAGE_KEY, JSON.stringify(viewedPages));
        } catch (e) {
            // localStorage not available
        }
    }

    /**
     * Format view count with Polish formatting
     */
    function formatViewCount(count) {
        if (count === 1) return '1 wyświetlenie';
        if (count >= 2 && count <= 4) return `${count} wyświetlenia`;
        if (count >= 5 && count <= 21) return `${count} wyświetleń`;

        // For numbers > 21, check last digit
        const lastDigit = count % 10;
        const lastTwoDigits = count % 100;

        if (lastTwoDigits >= 12 && lastTwoDigits <= 14) {
            return `${count} wyświetleń`;
        }
        if (lastDigit >= 2 && lastDigit <= 4) {
            return `${count} wyświetlenia`;
        }
        return `${count} wyświetleń`;
    }

    /**
     * Find and update the view counter element
     */
    function updateViewDisplay(views) {
        // Look for existing view counter element
        let viewElement = document.getElementById('view-counter');

        if (!viewElement) {
            // Try to find the blog post date element and add counter next to it
            const dateElement = document.querySelector('.blog-post-date');
            if (dateElement) {
                // Append to existing date text
                const viewSpan = document.createElement('span');
                viewSpan.id = 'view-counter';
                viewSpan.style.marginLeft = '0.5em';
                viewSpan.innerHTML = `• <i data-lucide="eye" style="width: 14px; height: 14px; display: inline; vertical-align: middle;"></i> ${formatViewCount(views)}`;
                dateElement.appendChild(viewSpan);

                // Re-initialize Lucide icons if available
                if (typeof lucide !== 'undefined') {
                    lucide.createIcons();
                }
                return;
            }
        } else {
            viewElement.textContent = formatViewCount(views);
        }
    }

    /**
     * Fetch or increment view count
     */
    async function trackView() {
        const pageUrl = getPagePath();

        // Only track blog pages
        if (!pageUrl.includes('/wiedza/')) {
            return;
        }

        try {
            const shouldIncrement = !wasRecentlyViewed(pageUrl);

            if (shouldIncrement) {
                // POST to increment view count
                const response = await fetch(API_ENDPOINT, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: pageUrl })
                });

                if (response.ok) {
                    const data = await response.json();
                    updateViewDisplay(data.views);
                    markAsViewed(pageUrl);
                }
            } else {
                // GET current view count (don't increment)
                const response = await fetch(`${API_ENDPOINT}?url=${encodeURIComponent(pageUrl)}`);

                if (response.ok) {
                    const data = await response.json();
                    updateViewDisplay(data.views);
                }
            }
        } catch (error) {
            console.warn('View counter unavailable:', error.message);
            // Silently fail - don't break the page
        }
    }

    // Run on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', trackView);
    } else {
        trackView();
    }
})();
