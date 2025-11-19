// Logout Security Script
// This script clears browser storage after logout to prevent forward button access

(function() {
    'use strict';

    // Clear all session storage immediately
    sessionStorage.clear();
    localStorage.removeItem('auth_page_loaded');
    localStorage.removeItem('last_access_time');

    // Clear browser cache for this session
    if ('caches' in window) {
        caches.keys().then(function(names) {
            names.forEach(function(name) {
                caches.delete(name);
            });
        });
    }

    // Prevent browser from caching this logout page
    window.addEventListener('beforeunload', function() {
        sessionStorage.clear();
    });

    // Prevent back button from working after logout
    window.history.forward();
    function noBack() {
        window.history.forward();
    }
    window.onload = noBack;
    window.onpageshow = function(evt) {
        if (evt.persisted) noBack();
    };

    console.log('Logout security: Browser storage cleared');
})();
