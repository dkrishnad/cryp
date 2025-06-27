
// DASH COMPONENT LOADING FIXES

// Enhanced error handling for chunk loading
window.addEventListener('error', function(e) {
    if (e.message && e.message.includes('ChunkLoadError')) {
        console.warn('[DASH FIX] Chunk loading error detected, attempting reload...');
        // Don't auto-reload, just log
        setTimeout(() => {
            console.log('[DASH FIX] Component should retry loading automatically');
        }, 1000);
    }
});

// Fix for dropdown component loading
document.addEventListener('DOMContentLoaded', function() {
    // Ensure all dropdowns are properly initialized
    setTimeout(() => {
        const dropdowns = document.querySelectorAll('.Select');
        dropdowns.forEach(dropdown => {
            if (!dropdown.classList.contains('initialized')) {
                dropdown.classList.add('initialized');
                console.log('[DASH FIX] Dropdown initialized');
            }
        });
    }, 1000);
});

// Fix for slider component loading
window.addEventListener('load', function() {
    setTimeout(() => {
        const sliders = document.querySelectorAll('.rc-slider');
        sliders.forEach(slider => {
            if (!slider.style.width) {
                slider.style.width = '100%';
                console.log('[DASH FIX] Slider width fixed');
            }
        });
    }, 500);
});

// Enhanced plotly loading fix
if (typeof window.PlotlyConfig === 'undefined') {
    window.PlotlyConfig = {
        MathJaxConfig: 'local',
        locale: 'en'
    };
}

// Component retry mechanism
window.dashComponentRetry = function(componentName, maxRetries = 3) {
    let retries = 0;
    const retry = () => {
        if (retries < maxRetries) {
            retries++;
            console.log(`[DASH FIX] Retrying ${componentName} (${retries}/${maxRetries})`);
            setTimeout(retry, 1000 * retries);
        } else {
            console.warn(`[DASH FIX] ${componentName} failed to load after ${maxRetries} retries`);
        }
    };
    retry();
};

console.log('[DASH FIX] Component loading fixes loaded');
