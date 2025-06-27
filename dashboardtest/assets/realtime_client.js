/**
 * Real-Time WebSocket Client for Crypto Bot Dashboard
 * Connects to backend FastAPI WebSocket for instant price updates
 */

class RealTimePriceClient {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.prices = {};
        
        this.connect();
    }
    
    connect() {
        try {
            // Use native WebSocket (not Socket.IO) to match FastAPI backend
            this.socket = new WebSocket('ws://localhost:8000/ws/price');
            
            this.socket.onopen = () => {
                console.log('🔗 Connected to real-time price server');
                this.isConnected = true;
                this.reconnectAttempts = 0;
                
                // Update connection status
                this.updateConnectionStatus(true);
                
                // Request initial symbol data
                this.socket.send(JSON.stringify({
                    action: 'subscribe',
                    symbol: 'btcusdt'
                }));
            };
            
            this.socket.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    // Update price display in real-time
                    this.updatePriceDisplay(data);
                    this.prices[data.symbol] = data.price;
                } catch (e) {
                    console.log('📊 Received price data:', event.data);
                }
            };
            
            this.socket.onclose = () => {
                console.log('❌ Disconnected from price server');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                
                // Attempt to reconnect
                this.attemptReconnect();
            };
            
            this.socket.onerror = (error) => {
                console.log('❌ WebSocket error:', error);
                this.isConnected = false;
                this.updateConnectionStatus(false);
            };
            
        } catch (error) {
            console.log('❌ WebSocket not available, falling back to polling');
            this.fallbackToPolling();
        }
    }
    
    updatePriceDisplay(data) {
        // Update the live price display
        const priceElement = document.getElementById('live-price');
        if (priceElement) {
            const formattedPrice = data.price.toLocaleString('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 2,
                maximumFractionDigits: 8
            });
            
            // Add price change animation
            priceElement.innerHTML = `
                <div class="price-update">
                    <strong>${data.symbol.toUpperCase()}</strong><br>
                    <span class="price-value">${formattedPrice}</span><br>
                    <small class="text-muted">Updated: ${new Date().toLocaleTimeString()}</small>
                </div>
            `;
            
            // Flash effect for price changes
            priceElement.classList.add('price-flash');
            setTimeout(() => {
                priceElement.classList.remove('price-flash');
            }, 300);
        }
        
        // Update any other price displays
        this.updateAllPriceDisplays(data);
    }
    
    updateAllPriceDisplays(data) {
        // Update portfolio value, charts, etc.
        const portfolioElement = document.getElementById('portfolio-status');
        if (portfolioElement) {
            // Trigger a portfolio recalculation with new price
            this.triggerPortfolioUpdate(data);
        }
    }
    
    updateConnectionStatus(connected) {
        const statusElements = document.querySelectorAll('.connection-status');
        statusElements.forEach(element => {
            if (connected) {
                element.innerHTML = '🟢 Real-Time Connected';
                element.className = 'connection-status text-success';
            } else {
                element.innerHTML = '🔴 Disconnected (Fallback Mode)';
                element.className = 'connection-status text-warning';
            }
        });
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`🔄 Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            
            setTimeout(() => {
                this.connect();
            }, 2000 * this.reconnectAttempts); // Exponential backoff
        } else {
            console.log('❌ Max reconnect attempts reached, falling back to polling');
            this.fallbackToPolling();
        }
    }
    
    fallbackToPolling() {
        // Fallback to more frequent polling if WebSocket fails
        setInterval(() => {
            this.fetchPriceUpdate();
        }, 1000); // Poll every second as fallback
    }
    
    fetchPriceUpdate() {
        // Get current symbol from dashboard
        const symbolElement = document.querySelector('#sidebar-symbol .Select-value-label');
        const symbol = symbolElement ? symbolElement.textContent.toLowerCase() : 'btcusdt';
        
        fetch(`http://localhost:8001/price/${symbol}`)
            .then(response => response.json())
            .then(data => {
                this.updatePriceDisplay(data);
            })
            .catch(error => {
                console.log('❌ Fallback polling failed:', error);
            });
    }
    
    triggerPortfolioUpdate(priceData) {
        // Trigger Dash callback updates by dispatching custom events
        const event = new CustomEvent('price_update', {
            detail: priceData
        });
        document.dispatchEvent(event);
    }
}

// CSS for price flash animation
const style = document.createElement('style');
style.textContent = `
    .price-flash {
        animation: priceFlash 0.3s ease-in-out;
    }
    
    @keyframes priceFlash {
        0% { background-color: rgba(0, 255, 136, 0.3); }
        100% { background-color: transparent; }
    }
    
    .price-update {
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        background: linear-gradient(45deg, #1a1a1a, #2a2a2a);
        border: 1px solid #404040;
    }
    
    .price-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #00ff88;
    }
    
    .connection-status {
        font-size: 0.9em;
        margin: 5px 0;
    }
`;
document.head.appendChild(style);

// Initialize real-time client when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Initializing real-time WebSocket client...');
    window.realTimePriceClient = new RealTimePriceClient();
});

// Add method to subscribe to symbol changes
RealTimePriceClient.prototype.subscribeToSymbol = function(symbol) {
    if (this.isConnected && this.socket && this.socket.readyState === WebSocket.OPEN) {
        this.socket.send(JSON.stringify({
            action: 'subscribe',
            symbol: symbol
        }));
        console.log(`📊 Subscribed to ${symbol} price updates`);
    }
};
