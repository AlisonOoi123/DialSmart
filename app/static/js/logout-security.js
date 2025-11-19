/**
 * DialSmart Authentication Security
 * Handles logout cleanup and login page security
 * Version: 2.0
 */
(function() {
    'use strict';

    // ============================================================================
    // CONFIGURATION
    // ============================================================================
    
    const AuthSecurity = {
        currentPage: null,
        isAuthenticated: false,
        logoutUrl: null,

        /**
         * Initialize authentication security
         * Call this from your HTML with appropriate parameters
         */
        init: function(pageType, isAuth, logoutEndpoint) {
            this.currentPage = pageType; // 'login' or 'logout'
            this.isAuthenticated = isAuth;
            this.logoutUrl = logoutEndpoint;

            console.log(`Auth Security initialized: ${pageType} page`);

            if (pageType === 'logout') {
                this.handleLogoutPage();
            } else if (pageType === 'login') {
                this.handleLoginPage();
            }
        },

        // ========================================================================
        // LOGOUT PAGE SECURITY
        // ========================================================================

        handleLogoutPage: function() {
            console.log('Logout security: Clearing browser storage');

            // Clear all session storage immediately
            sessionStorage.clear();
            localStorage.removeItem('auth_page_loaded');
            localStorage.removeItem('last_access_time');
            localStorage.removeItem('login_submit');

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
            this.preventBackNavigation();

            console.log('Logout security: Browser storage cleared');
        },

        // ========================================================================
        // LOGIN PAGE SECURITY
        // ========================================================================

        handleLoginPage: function() {
            // Clear any leftover session data from previous login
            sessionStorage.clear();

            if (this.isAuthenticated) {
                // User is already logged in but navigated to login page
                this.handleAuthenticatedUserOnLoginPage();
            } else {
                // User is not authenticated - normal login page access
                this.handleUnauthenticatedUserOnLoginPage();
            }
        },

        handleAuthenticatedUserOnLoginPage: function() {
            console.log('User already authenticated on login page - logging out for security');

            // Clear all browser storage
            sessionStorage.clear();
            localStorage.clear();

            // Redirect to logout endpoint
            if (this.logoutUrl) {
                window.location.replace(this.logoutUrl);
            }
        },

        handleUnauthenticatedUserOnLoginPage: function() {
            console.log('Login page security: Preventing unauthorized navigation');

            // Clear forward history
            window.history.replaceState(null, document.title, window.location.href);
            window.history.pushState(null, document.title, window.location.href);

            // Prevent ALL back/forward navigation from login page
            window.addEventListener('popstate', function(event) {
                window.history.pushState(null, document.title, window.location.href);
                console.log('Navigation blocked on login page - please login to continue');
            });

            // Handle form submission
            this.setupFormSubmitHandler();
        },

        // ========================================================================
        // HELPER FUNCTIONS
        // ========================================================================

        preventBackNavigation: function() {
            window.history.forward();
            
            function noBack() {
                window.history.forward();
            }
            
            window.onload = noBack;
            window.onpageshow = function(evt) {
                if (evt.persisted) noBack();
            };
        },

        setupFormSubmitHandler: function() {
            const form = document.querySelector('form');
            if (form) {
                form.addEventListener('submit', function() {
                    // Mark that we're intentionally submitting the form
                    sessionStorage.setItem('login_submit', 'true');
                });
            }
        },

        // ========================================================================
        // UTILITY FUNCTIONS
        // ========================================================================

        clearAllStorage: function() {
            sessionStorage.clear();
            localStorage.clear();
            console.log('All browser storage cleared');
        },

        preventCaching: function() {
            // Set cache control headers via meta tags (if needed)
            const meta = document.createElement('meta');
            meta.httpEquiv = 'Cache-Control';
            meta.content = 'no-cache, no-store, must-revalidate';
            document.head.appendChild(meta);
        }
    };

    // ============================================================================
    // EXPOSE TO GLOBAL SCOPE
    // ============================================================================

    window.DialSmartAuth = AuthSecurity;

    // Auto-initialize if data attributes are present
    document.addEventListener('DOMContentLoaded', function() {
        const pageType = document.body.dataset.authPage;
        const isAuth = document.body.dataset.authenticated === 'true';
        const logoutUrl = document.body.dataset.logoutUrl;

        if (pageType) {
            AuthSecurity.init(pageType, isAuth, logoutUrl);
        }
    });

})();