"""
Dashboard Debug Logger - Comprehensive logging system for dashboard callbacks and user interactions

This module provides detailed logging for every dashboard button click, callback execution, 
API call, and error to help diagnose why dashboard features aren't working.
"""

import logging
import json
import traceback
import time
from datetime import datetime
from functools import wraps
from typing import Any, Dict, Optional

# Configure enhanced logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dashboard_debug.log'),
        logging.StreamHandler()  # Also log to console
    ]
)

# Create separate loggers for different components
callback_logger = logging.getLogger('DASHBOARD_CALLBACK')
api_logger = logging.getLogger('DASHBOARD_API')
button_logger = logging.getLogger('DASHBOARD_BUTTON')
error_logger = logging.getLogger('DASHBOARD_ERROR')

class DashboardDebugger:
    """Enhanced debugging class for dashboard interactions"""
    
    def __init__(self):
        self.session_start = datetime.now()
        self.interaction_count = 0
        self.error_count = 0
        self.api_call_count = 0
        
    def log_button_click(self, button_id: str, n_clicks: int, context: Optional[Dict] = None):
        """Log button click with context"""
        self.interaction_count += 1
        button_logger.info(f"""
=== BUTTON CLICK #{self.interaction_count} ===
Button ID: {button_id}
Click Count: {n_clicks}
Timestamp: {datetime.now().isoformat()}
Context: {json.dumps(context or {}, indent=2)}
Session Time: {(datetime.now() - self.session_start).total_seconds():.2f}s
========================================
        """)
    
    def log_callback_start(self, callback_name: str, inputs: Dict, state: Optional[Dict] = None):
        """Log callback function start"""
        callback_logger.info(f"""
>>> CALLBACK START: {callback_name} <<<
Inputs: {json.dumps(inputs, indent=2)}
State: {json.dumps(state or {}, indent=2)}
Start Time: {datetime.now().isoformat()}
        """)
    
    def log_callback_end(self, callback_name: str, outputs: Any, execution_time: float):
        """Log callback function completion"""
        callback_logger.info(f"""
<<< CALLBACK END: {callback_name} >>>
Execution Time: {execution_time:.3f}s
Outputs Type: {type(outputs).__name__}
Outputs Preview: {str(outputs)[:200]}...
End Time: {datetime.now().isoformat()}
        """)
    
    def log_api_call(self, method: str, url: str, data: Optional[Dict] = None, headers: Optional[Dict] = None):
        """Log API call details"""
        self.api_call_count += 1
        api_logger.info(f"""
=== API CALL #{self.api_call_count} ===
Method: {method}
URL: {url}
Data: {json.dumps(data or {}, indent=2)}
Headers: {json.dumps(headers or {}, indent=2)}
Timestamp: {datetime.now().isoformat()}
========================
        """)
    
    def log_api_response(self, status_code: int, response_data: Any, response_time: float):
        """Log API response details"""
        api_logger.info(f"""
=== API RESPONSE ===
Status Code: {status_code}
Response Time: {response_time:.3f}s
Response Data: {json.dumps(response_data, indent=2) if isinstance(response_data, dict) else str(response_data)[:500]}
Response Type: {type(response_data).__name__}
===================
        """)
    
    def log_error(self, error: Exception, context: str, additional_info: Optional[Dict] = None):
        """Log detailed error information"""
        self.error_count += 1
        error_logger.error(f"""
!!! ERROR #{self.error_count} in {context} !!!
Error Type: {type(error).__name__}
Error Message: {str(error)}
Additional Info: {json.dumps(additional_info or {}, indent=2)}
Traceback:
{traceback.format_exc()}
Timestamp: {datetime.now().isoformat()}
=====================================
        """)
    
    def log_dashboard_state(self, component_values: Dict):
        """Log current dashboard state"""
        callback_logger.debug(f"""
--- DASHBOARD STATE SNAPSHOT ---
Component Values: {json.dumps(component_values, indent=2)}
Total Interactions: {self.interaction_count}
Total API Calls: {self.api_call_count}
Total Errors: {self.error_count}
Session Duration: {(datetime.now() - self.session_start).total_seconds():.2f}s
-------------------------------
        """)
    
    def log_callback_result(self, callback_name: str, result: Any):
        """Log callback function result"""
        callback_logger.info(f"""
>>> CALLBACK RESULT: {callback_name} <<<
Result Type: {type(result).__name__}
Result Preview: {str(result)[:200]}...
Timestamp: {datetime.now().isoformat()}
        """)
    
    def log_callback_error(self, callback_name: str, error: Exception):
        """Log callback function error"""
        self.error_count += 1
        callback_logger.error(f"""
!!! CALLBACK ERROR: {callback_name} !!!
Error Type: {type(error).__name__}
Error Message: {str(error)}
Timestamp: {datetime.now().isoformat()}
        """)

# Global debugger instance
debugger = DashboardDebugger()

def debug_callback(callback_name: str):
    """Decorator to add comprehensive debugging to callback functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            # Log callback start
            inputs = {f"arg_{i}": arg for i, arg in enumerate(args)}
            inputs.update(kwargs)
            debugger.log_callback_start(callback_name, inputs)
            
            try:
                # Execute the callback
                result = func(*args, **kwargs)
                
                # Log successful completion
                execution_time = time.time() - start_time
                debugger.log_callback_end(callback_name, result, execution_time)
                debugger.log_callback_result(callback_name, result)  # Log the result
                
                return result
                
            except Exception as e:
                # Log error with context
                execution_time = time.time() - start_time
                debugger.log_error(e, f"Callback: {callback_name}", {
                    "execution_time": execution_time,
                    "inputs": inputs
                })
                debugger.log_callback_error(callback_name, e)  # Log the error
                
                # Return error display
                return f"Error in {callback_name}: {str(e)}"
        
        return wrapper
    return decorator

def debug_api_call(method: str, url: str, session, **kwargs):
    """Enhanced API call with comprehensive logging"""
    start_time = time.time()
    
    # Log the API call
    debugger.log_api_call(method, url, kwargs.get('json'), kwargs.get('headers'))
    
    try:
        # Make the API call
        response = getattr(session, method.lower())(url, **kwargs)
        response_time = time.time() - start_time
        
        # Try to parse JSON response
        try:
            response_data = response.json()
        except:
            response_data = response.text
        
        # Log the response
        debugger.log_api_response(response.status_code, response_data, response_time)
        
        return response
        
    except Exception as e:
        response_time = time.time() - start_time
        debugger.log_error(e, f"API Call: {method} {url}", {
            "response_time": response_time,
            "request_kwargs": kwargs
        })
        raise

# Export the main components
__all__ = ['debugger', 'debug_callback', 'debug_api_call', 'callback_logger', 'api_logger', 'button_logger', 'error_logger']
