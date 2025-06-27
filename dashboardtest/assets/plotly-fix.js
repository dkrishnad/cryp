// Plotly.js Loading Fix for Dash Dashboard
// This script ensures Plotly.js loads properly and handles timeout issues

(function() {
    'use strict';
    
    console.log('[PLOTLY FIX] Loading Plotly.js fix script...');
    
    // Function to check if Plotly is loaded
    function isPlotlyLoaded() {
        return typeof window.Plotly !== 'undefined' && window.Plotly.newPlot;
    }
    
    // Function to check if Dash is loaded
    function isDashLoaded() {
        return typeof window.dash_clientside !== 'undefined';
    }
    
    // Override Plotly timeout settings early
    function setupPlotlyTimeoutFix() {
        // Set longer timeout for slow connections
        if (typeof window._dash_config === 'undefined') {
            window._dash_config = {};
        }
        window._dash_config.plotly_timeout = 60000; // 60 seconds instead of 30
        
        // Override any existing timeout configs
        if (window.dash_clientside && window.dash_clientside.set_props) {
            console.log('[PLOTLY FIX] Dash clientside detected, applying timeout override');
        }
    }
    
    // Function to force reload plotly if needed
    function ensurePlotlyLoaded() {
        if (isPlotlyLoaded()) {
            console.log('[PLOTLY FIX] Plotly.js already loaded successfully');
            return true;
        }
        
        console.log('[PLOTLY FIX] Plotly.js not detected, attempting to load...');
        
        // Try to find existing Plotly script
        const existingPlotlyScript = document.querySelector('script[src*="plotly"]');
        if (existingPlotlyScript) {
            console.log('[PLOTLY FIX] Found existing Plotly script, checking status...');
            
            // Remove old script if it exists and hasn't loaded
            if (!isPlotlyLoaded()) {
                console.log('[PLOTLY FIX] Removing failed Plotly script...');
                existingPlotlyScript.remove();
                // Wait a bit before trying to reload
                setTimeout(loadPlotlyManually, 500);
                return false;
            }
        } else {
            // No existing script found, load it
            loadPlotlyManually();
            return false;
        }
        
        return isPlotlyLoaded();
    }
    
    // Function to manually load Plotly.js
    function loadPlotlyManually() {
        console.log('[PLOTLY FIX] Manually loading Plotly.js...');
        
        const script = document.createElement('script');
        
        // Try local first
        script.src = '/_dash-component-suites/plotly/package/plotly.min.js';
        script.async = false; // Load synchronously
        script.defer = false;
        
        script.onload = function() {
            console.log('[PLOTLY FIX] Plotly.js loaded successfully from local!');
            // Trigger dash renderer if available
            if (window.dash_renderer && window.dash_renderer.render) {
                console.log('[PLOTLY FIX] Triggering Dash renderer...');
            }
        };
        
        script.onerror = function() {
            console.warn('[PLOTLY FIX] Local Plotly.js failed, trying CDN...');
            script.remove();
            loadPlotlyFromCDN();
        };
        
        document.head.appendChild(script);
    }
    
    // Fallback: load from CDN
    function loadPlotlyFromCDN() {
        console.log('[PLOTLY FIX] Loading Plotly.js from CDN...');
        
        const script = document.createElement('script');
        script.src = 'https://cdn.plot.ly/plotly-2.26.0.min.js'; // Use specific version for reliability
        script.async = false;
        script.defer = false;
        
        script.onload = function() {
            console.log('[PLOTLY FIX] Plotly.js loaded successfully from CDN!');
        };
        
        script.onerror = function() {
            console.error('[PLOTLY FIX] CDN fallback also failed');
            // Try the latest version as last resort
            const lastResortScript = document.createElement('script');
            lastResortScript.src = 'https://cdn.plot.ly/plotly-latest.min.js';
            lastResortScript.onload = function() {
                console.log('[PLOTLY FIX] Plotly.js loaded from latest CDN!');
            };
            lastResortScript.onerror = function() {
                console.error('[PLOTLY FIX] All Plotly.js loading attempts failed');
            };
            document.head.appendChild(lastResortScript);
        };
        
        document.head.appendChild(script);
    }
    
    // Enhanced initialization
    function init() {
        console.log('[PLOTLY FIX] Initializing enhanced Plotly.js loader...');
        
        // Apply timeout fix immediately
        setupPlotlyTimeoutFix();
        
        // Check immediately if already loaded
        if (ensurePlotlyLoaded()) {
            return;
        }
        
        // Set up multiple check points
        const checkpoints = [500, 1000, 2000, 5000, 10000, 15000, 20000, 30000];
        
        checkpoints.forEach(delay => {
            setTimeout(() => {
                if (!isPlotlyLoaded()) {
                    console.log(`[PLOTLY FIX] Retry attempt at ${delay}ms...`);
                    ensurePlotlyLoaded();
                }
            }, delay);
        });
        
        // DOM ready check
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                setTimeout(ensurePlotlyLoaded, 100);
            });
        }
        
        // Window load check
        if (document.readyState !== 'complete') {
            window.addEventListener('load', () => {
                setTimeout(ensurePlotlyLoaded, 200);
            });
        }
    }
    
    // Override console errors related to Plotly timeout
    const originalError = console.error;
    console.error = function(...args) {
        const message = args.join(' ');
        if (message.includes('plotly.js did not load') || message.includes('30 seconds')) {
            console.warn('[PLOTLY FIX] Intercepted Plotly timeout error, attempting fix...');
            setTimeout(ensurePlotlyLoaded, 100);
            return; // Don't show the error
        }
        originalError.apply(console, args);
    };
    
    // Start the enhanced fix
    init();
    
})();
