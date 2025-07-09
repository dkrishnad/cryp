# FastAPI WebSocket endpoint for live price streaming


from fastapi import APIRouter, WebSocket, WebSocketDisconnect, WebSocketException
import asyncio
import httpx
import json
import logging
import time
from typing import Dict, Optional

logger = logging.getLogger(__name__)

router = APIRouter()

@router.websocket("/ws/price")
async def prices_ws(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Fetch real price data here
        await websocket.send_json({"symbol": "BTCUSDT", "price": 12345.67})
        await asyncio.sleep(1)

# Global connection manager to enforce one connection per client IP
import threading
active_connections = {}
active_connections_lock = threading.Lock()

class WebSocketConnectionManager:
    """Manages WebSocket connections with automatic reconnection and error handling"""
    
    def __init__(self):
        self.connections: Dict[str, WebSocket] = {}
        self.connection_states: Dict[str, str] = {}
        self.heartbeat_intervals: Dict[str, float] = {}
        
    async def connect(self, websocket: WebSocket, client_id: str):
        """Connect and register a WebSocket client"""
        try:
            await websocket.accept()
            self.connections[client_id] = websocket
            self.connection_states[client_id] = "connected"
            self.heartbeat_intervals[client_id] = time.time()
            logger.info(f"WebSocket client {client_id} connected")
            
            # Start heartbeat
            asyncio.create_task(self.heartbeat(client_id))
            
        except Exception as e:
            logger.error(f"Failed to connect WebSocket client {client_id}: {e}")
            
    async def disconnect(self, client_id: str):
        """Disconnect and clean up WebSocket client"""
        if client_id in self.connections:
            try:
                await self.connections[client_id].close()
            except Exception as e:
                logger.warning(f"Error closing WebSocket for {client_id}: {e}")
            finally:
                self.connections.pop(client_id, None)
                self.connection_states.pop(client_id, None) 
                self.heartbeat_intervals.pop(client_id, None)
                logger.info(f"WebSocket client {client_id} disconnected")
    
    async def send_message(self, client_id: str, message: dict) -> bool:
        """Send message to WebSocket client with error handling"""
        if client_id not in self.connections:
            return False
            
        try:
            await self.connections[client_id].send_text(json.dumps(message))
            return True
        except WebSocketDisconnect:
            logger.info(f"Client {client_id} disconnected during send")
            await self.disconnect(client_id)
            return False
        except Exception as e:
            logger.error(f"Error sending message to {client_id}: {e}")
            await self.disconnect(client_id)
            return False
    
    async def heartbeat(self, client_id: str):
        """Send periodic heartbeat to maintain connection"""
        while client_id in self.connections:
            try:
                await asyncio.sleep(30)  # Heartbeat every 30 seconds
                if client_id in self.connections:
                    success = await self.send_message(client_id, {
                        "type": "heartbeat",
                        "timestamp": time.time()
                    })
                    if not success:
                        break
            except Exception as e:
                logger.error(f"Heartbeat error for {client_id}: {e}")
                break

# Global connection manager instance
connection_manager = WebSocketConnectionManager()

class PriceStreamerManager:
    def __init__(self):
        self.symbol = None
        self.price_task = None
        self.stop_event = asyncio.Event()
        self.latest_symbol = None
        self.lock = asyncio.Lock()
        self.stream_version = 0  # Increments on every symbol switch
        self.max_retries = 3
        self.retry_delay = 1.0

    async def stop_streamer(self):
        async with self.lock:
            if self.price_task is not None:
                print(f"[WS DEBUG] Stopping streamer for {self.symbol}")
                self.stop_event.set()
                try:
                    await asyncio.wait_for(self.price_task, timeout=2.0)
                except asyncio.TimeoutError:
                    print(f"[WS DEBUG] Forcibly cancelling streamer for {self.symbol}")
                    self.price_task.cancel()
                    try:
                        await self.price_task
                    except Exception:
                        pass
                await asyncio.sleep(0.2)  # Ensure all in-flight messages are cleared
                self.stop_event.clear()
                self.price_task = None
                print(f"[WS DEBUG] Stopped streamer for {self.symbol}")

    async def start_streamer(self, symbol, websocket):
        async with self.lock:
            self.symbol = symbol
            self.latest_symbol = symbol
            self.stream_version += 1
            version = self.stream_version
            print(f"[WS DEBUG] Starting streamer for {symbol} (version {version})")
            self.price_task = asyncio.create_task(self.price_streamer(symbol, websocket, version))

    async def price_streamer(self, symbol, websocket, version):
        print(f"[WS DEBUG] START price_streamer for {symbol} (version {version})")
        while True:
            if self.stop_event.is_set():
                print(f"[WS DEBUG] stop_event set, exiting streamer for {symbol} (version {version})")
                break
            # Abort if a new streamer has started (version mismatch)
            if version != self.stream_version:
                print(f"[WS DEBUG] ABORT streamer for {symbol} (version {version}), current version is {self.stream_version}")
                break
            try:
                async with httpx.AsyncClient() as client:
                    r = await client.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}")
                    price = r.json()["price"] if r.status_code == 200 else "N/A"
                # Guard: do not send if stop_event set or version changed after HTTP request
                if self.stop_event.is_set() or version != self.stream_version:
                    print(f"[WS DEBUG] ABORT send for {symbol} (version {version}) due to stop_event or version change")
                    break
                print(f"[WS DEBUG] SENDING ONLY {symbol}: {price}")
                await websocket.send_text(json.dumps({"symbol": symbol.upper(), "price": price}))
            except Exception as e:
                print(f"[WS DEBUG] Error fetching price for {symbol}: {e}")
            # Responsive sleep: check stop_event every 50ms, total 0.5s
            for _ in range(10):
                if self.stop_event.is_set():
                    break
                await asyncio.sleep(0.05)
        print(f"[WS DEBUG] STOP price_streamer for {symbol} (version {version})")

@router.websocket("/ws/price")
async def websocket_price(websocket: WebSocket):
    print(f"[WS DEBUG] WebSocket connection opened: {websocket.client}")
    await websocket.accept()
    client_ip = websocket.client.host if hasattr(websocket, 'client') and websocket.client else None
    print(f"[WS DEBUG] Client IP: {client_ip}")
    manager = PriceStreamerManager()
    # Enforce only one connection per client IP
    if client_ip:
        old_manager = None
        with active_connections_lock:
            old_manager = active_connections.get(client_ip)
        if old_manager:
            print(f"[WS DEBUG] Closing previous connection for {client_ip} (awaiting stop)")
            # Await the old manager's streamer to fully stop before replacing
            await old_manager.stop_streamer()
        with active_connections_lock:
            active_connections[client_ip] = manager
        first_symbol_received = False
        # Start with default symbol immediately to prevent timeout
        default_symbol = "BTCUSDT"
        print(f"[WS DEBUG] Starting with default symbol: {default_symbol}")
        await manager.start_streamer(default_symbol, websocket)
        first_symbol_received = True
        try:
            while True:
                try:
                    print(f"[WS DEBUG] Waiting for symbol message from client {client_ip}...")
                    msg = await asyncio.wait_for(websocket.receive_text(), timeout=10)  # Reduced timeout
                    print(f"[WS DEBUG] Received message: {msg}")
                    
                    # Handle both JSON and plain text messages
                    symbol = msg
                    try:
                        # Try to parse as JSON first
                        parsed_msg = json.loads(msg)
                        if isinstance(parsed_msg, dict) and 'symbol' in parsed_msg:
                            symbol = parsed_msg['symbol']
                        elif isinstance(parsed_msg, str):
                            symbol = parsed_msg
                        print(f"[WS DEBUG] Parsed symbol from JSON: {symbol}")
                    except json.JSONDecodeError:
                        # If not JSON, treat as plain text symbol
                        symbol = msg.strip()
                        print(f"[WS DEBUG] Using plain text symbol: {symbol}")
                    
                    if symbol and symbol != manager.symbol:
                        print(f"[WS DEBUG] Switching from {manager.symbol} to {symbol}")
                        # Atomically stop/start streamer
                        await manager.stop_streamer()
                        await manager.start_streamer(symbol, websocket)
                except asyncio.TimeoutError:
                    # Continue with current symbol instead of closing
                    print(f"[WS DEBUG] No new symbol received, continuing with {manager.symbol}")
                    continue
        except WebSocketDisconnect:
            print(f"[WS DEBUG] WebSocket disconnected for {client_ip}.")
            await manager.stop_streamer()
        except Exception as e:
            print(f"[WS DEBUG] Exception for {client_ip}: {e}")
            await manager.stop_streamer()
        finally:
            # Remove from active connections on disconnect
            if client_ip:
                with active_connections_lock:
                    if active_connections.get(client_ip) is manager:
                        del active_connections[client_ip]
            print(f"[WS DEBUG] WebSocket handler finished for {client_ip}")
