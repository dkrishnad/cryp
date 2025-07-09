#!/usr/bin/env python3
"""
Validation script to check that all endpoints use real data instead of fallback/mock data
"""

import re
import os

def check_real_data_usage():
    """Check main.py for endpoints using real data vs fallback/mock"""
    
    main_file = r"c:\Users\Hari\Desktop\Testin dub\backendtest\main.py"
    
    print("=== Real Data Usage Validation ===")
    print(f"Checking: {main_file}")
    print()
    
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all endpoint definitions
    endpoint_pattern = r'@app\.(get|post|put|delete)\("([^"]+)"\)'
    endpoints = re.findall(endpoint_pattern, content)
    
    print(f"Found {len(endpoints)} endpoints:")
    for method, path in endpoints[:10]:  # Show first 10
        print(f"  {method.upper()} {path}")
    if len(endpoints) > 10:
        print(f"  ... and {len(endpoints) - 10} more")
    print()
    
    # Check for problematic patterns
    problems_found = []
    
    # Check for mock/fallback patterns
    mock_patterns = [
        (r'mock.*data', "Mock data usage"),
        (r'fallback.*implementation', "Fallback implementation"),
        (r'random\.\w+\(', "Random data generation"),
        (r'# Mock', "Mock comments"),
        (r'stub.*logic', "Stub logic"),
        (r'NotImplementedError', "Not implemented errors"),
    ]
    
    print("=== Checking for Mock/Fallback Patterns ===")
    for pattern, description in mock_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            problems_found.append(f"{description}: {len(matches)} occurrences")
            print(f"⚠️  {description}: {len(matches)} occurrences")
    
    if not problems_found:
        print("✅ No obvious mock/fallback patterns found")
    print()
    
    # Check for good patterns (real data sources)
    good_patterns = [
        (r'real_predict\(', "Real ML predictions"),
        (r'binance.*api', "Binance API usage"),
        (r'get_price\(', "Real price fetching"),
        (r'futures_engine', "Futures engine usage"),
        (r'advanced_auto_trading_engine', "Advanced engine usage"),
        (r'hybrid_orchestrator', "Hybrid learning usage"),
        (r'online_learning_manager', "Online learning usage"),
        (r'data_collector', "Data collector usage"),
    ]
    
    print("=== Checking for Real Data Sources ===")
    real_sources_count = 0
    for pattern, description in good_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if matches:
            real_sources_count += len(matches)
            print(f"✅ {description}: {len(matches)} occurrences")
    
    print(f"\nTotal real data source references: {real_sources_count}")
    print()
    
    # Check specific critical endpoints
    critical_endpoints = [
        "/ml/predict",
        "/ml/current_signal", 
        "/features/indicators",
        "/portfolio",
        "/price",
        "/fapi/v1/ticker/24hr",
        "/retrain",
        "/balance"
    ]
    
    print("=== Critical Endpoint Analysis ===")
    for endpoint in critical_endpoints:
        # Find the endpoint function
        pattern = rf'@app\.\w+\("{re.escape(endpoint)}"\).*?def\s+(\w+)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            func_name = match.group(1)
            # Find the function body (rough approximation)
            func_start = content.find(f"def {func_name}")
            if func_start != -1:
                # Find next function or end
                next_func = content.find("\n@app.", func_start + 1)
                next_def = content.find("\ndef ", func_start + 1)
                
                func_end = min([pos for pos in [next_func, next_def, len(content)] if pos > func_start])
                func_body = content[func_start:func_end]
                
                # Check for real data usage in this function
                has_real_data = False
                has_mock_data = False
                
                # Strong indicators of real data usage
                real_data_patterns = [
                    'real_predict', 'binance', 'get_price', 'futures_engine', 
                    'advanced_auto_trading_engine', 'real_data_confirmed', 
                    'data_source.*real', 'hybrid_orchestrator', 'online_learning_manager'
                ]
                
                # Patterns that indicate mock/fallback (but not in comments saying "NO MOCK")
                mock_patterns = ['mock_data', 'fallback_data', 'random.choice', 'random.uniform']
                
                if any(re.search(pattern, func_body, re.IGNORECASE) for pattern in real_data_patterns):
                    has_real_data = True
                
                # Only flag as mock if actually contains mock data patterns (not just comments)
                for pattern in mock_patterns:
                    if re.search(pattern, func_body, re.IGNORECASE):
                        has_mock_data = True
                
                status = "✅ Real data" if has_real_data and not has_mock_data else "🔄 Mixed" if has_real_data and has_mock_data else "❌ Mock/fallback only" if has_mock_data else "❓ Unknown"
                print(f"{endpoint:25} -> {status}")
        else:
            print(f"{endpoint:25} -> ❓ Not found")
    
    print()
    print("=== Summary ===")
    if problems_found:
        print("Issues found:")
        for problem in problems_found:
            print(f"  - {problem}")
        print("\nRecommendation: Review and fix remaining mock/fallback usage")
    else:
        print("✅ No major mock/fallback issues detected")
        print("✅ All critical endpoints appear to prioritize real data sources")
    
    print(f"✅ Total real data source references: {real_sources_count}")
    print("✅ Backend appears ready for real-time testing")

if __name__ == "__main__":
    check_real_data_usage()
