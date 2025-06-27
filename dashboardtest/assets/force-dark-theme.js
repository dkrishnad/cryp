// Force dark theme application
window.addEventListener('DOMContentLoaded', function() {
    console.log('Applying dark theme...');
    
    // Function to apply dark theme
    function applyDarkTheme() {
        // Force body background
        document.body.style.setProperty('background-color', '#2a2a2a', 'important');
        document.body.style.setProperty('color', '#e0e0e0', 'important');
        
        // Force all tabs
        const tabLinks = document.querySelectorAll('.nav-tabs .nav-link');
        tabLinks.forEach(tab => {
            tab.style.setProperty('background-color', '#404040', 'important');
            tab.style.setProperty('color', '#e0e0e0', 'important');
            tab.style.setProperty('border', '1px solid #555555', 'important');
        });
        
        // Force active tab
        const activeTab = document.querySelector('.nav-tabs .nav-link.active');
        if (activeTab) {
            activeTab.style.setProperty('background-color', '#2a2a2a', 'important');
            activeTab.style.setProperty('color', '#ffffff', 'important');
        }
        
        // Force tab content
        const tabContent = document.querySelectorAll('.tab-content, .tab-pane');
        tabContent.forEach(content => {
            content.style.setProperty('background-color', '#2a2a2a', 'important');
            content.style.setProperty('color', '#e0e0e0', 'important');
        });
        
        // Force all containers
        const containers = document.querySelectorAll('.container, .container-fluid, .row, .col, [class*="col-"]');
        containers.forEach(container => {
            container.style.setProperty('background-color', '#2a2a2a', 'important');
            container.style.setProperty('color', '#e0e0e0', 'important');
        });
        
        // Force sliders
        const sliders = document.querySelectorAll('.rc-slider, .rc-slider-rail, .rc-slider-track');
        sliders.forEach(slider => {
            if (slider.classList.contains('rc-slider-rail')) {
                slider.style.setProperty('background-color', '#555555', 'important');
            } else if (slider.classList.contains('rc-slider-track')) {
                slider.style.setProperty('background-color', '#4CAF50', 'important');
            } else {
                slider.style.setProperty('background-color', '#404040', 'important');
            }
        });
        
        const sliderHandles = document.querySelectorAll('.rc-slider-handle');
        sliderHandles.forEach(handle => {
            handle.style.setProperty('background-color', '#ffffff', 'important');
            handle.style.setProperty('border', '2px solid #4CAF50', 'important');
        });
        
        const sliderDots = document.querySelectorAll('.rc-slider-dot');
        sliderDots.forEach(dot => {
            dot.style.setProperty('background-color', '#555555', 'important');
            dot.style.setProperty('border-color', '#555555', 'important');
        });
    }
    
    // Apply immediately
    applyDarkTheme();
    
    // Apply again after a short delay to catch any dynamically loaded content
    setTimeout(applyDarkTheme, 100);
    setTimeout(applyDarkTheme, 500);
    setTimeout(applyDarkTheme, 1000);
    
    // Set up mutation observer to apply theme to new elements
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes.length > 0) {
                setTimeout(applyDarkTheme, 50);
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
