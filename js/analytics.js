// Google Analytics Initialization
// Add this script to all pages: <script src="/js/analytics.js"></script>

(function () {
    // Load gtag.js asynchronously
    var gtagScript = document.createElement('script');
    gtagScript.async = true;
    gtagScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-GNW4457ZNR';
    document.head.appendChild(gtagScript);

    // Initialize dataLayer and gtag function
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    window.gtag = gtag;

    gtag('js', new Date());
    gtag('config', 'G-GNW4457ZNR');
})();
