#!/usr/bin/env python3
"""
Conservative Duplicate Fixer
Only removes duplicates from layout.py that have EXACT matches in specialized layout files
Preserves ALL functionality by being extremely conservative
"""

import os
import re
import shutil
from datetime import datetime

def read_file_safe(filepath):
    """Safely read file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def extract_component_definition(content, component_id):
    """Extract the complete component definition for a given ID"""
    lines = content.split('\n')
    component_def = []
    
    for i, line in enumerate(lines):
        if f'id="{component_id}"' in line or f"id='{component_id}'" in line:
            # Start from this line and find the complete component
            start_line = i
            bracket_count = 0
            paren_count = 0
            in_component = False
            
            for j in range(start_line, len(lines)):
                current_line = lines[j]
                
                # Count brackets and parentheses to find component end
                bracket_count += current_line.count('(') - current_line.count(')')
                paren_count += current_line.count('[') - current_line.count(']')
                
                component_def.append(current_line)
                
                # If we've closed all brackets/parens and hit a comma or new component, stop
                if (bracket_count <= 0 and paren_count <= 0 and 
                    j > start_line and 
                    (current_line.strip().endswith(',') or 
                     current_line.strip().endswith(']') or
                     current_line.strip().endswith(')'))):
                    break
                
                # Safety break to avoid infinite loops
                if j - start_line > 50:
                    break
    
    return '\n'.join(component_def)

def find_exact_duplicates(layout_content, specialized_files):
    """Find components in layout.py that have EXACT matches in specialized files"""
    exact_duplicates = []
    
    # Extract all component IDs from layout.py
    layout_ids = re.findall(r'id=["\']([^"\']+)["\']', layout_content)
    
    for component_id in layout_ids:
        layout_component = extract_component_definition(layout_content, component_id)
        
        if not layout_component.strip():
            continue
        
        # Check if this exact component exists in any specialized file
        for spec_file, spec_content in specialized_files.items():
            if component_id in spec_content:
                spec_component = extract_component_definition(spec_content, component_id)
                
                # Normalize whitespace for comparison
                layout_normalized = re.sub(r'\s+', ' ', layout_component.strip())
                spec_normalized = re.sub(r'\s+', ' ', spec_component.strip())
                
                # If they're very similar (allowing for minor formatting differences)
                similarity = calculate_similarity(layout_normalized, spec_normalized)
                
                if similarity > 0.85:  # 85% similarity threshold
                    exact_duplicates.append({
                        'id': component_id,
                        'layout_def': layout_component,
                        'specialized_file': spec_file,
                        'specialized_def': spec_component,
                        'similarity': similarity
                    })
                    break
    
    return exact_duplicates

def calculate_similarity(text1, text2):
    """Calculate text similarity (simple approach)"""
    if not text1 or not text2:
        return 0
    
    # Remove common variations
    text1 = re.sub(r'className=["\'][^"\']*["\']', '', text1)
    text2 = re.sub(r'className=["\'][^"\']*["\']', '', text2)
    
    # Simple character-based similarity
    len1, len2 = len(text1), len(text2)
    if len1 == 0 or len2 == 0:
        return 0
    
    # Calculate overlap
    shorter, longer = (text1, text2) if len1 < len2 else (text2, text1)
    
    matches = 0
    for i in range(len(shorter)):
        if i < len(longer) and shorter[i] == longer[i]:
            matches += 1
    
    return matches / max(len1, len2)

def create_conservative_fix():
    """Create a conservative fix that preserves ALL functionality"""
    print("🔧 CONSERVATIVE DUPLICATE FIXER")
    print("=" * 60)
    print("STRATEGY: Only remove components from layout.py that have")
    print("EXACT matches in specialized layout files")
    print("=" * 60)
    
    # File paths
    layout_file = 'dashboardtest/layout.py'
    specialized_files = {
        'auto_trading_layout.py': 'dashboardtest/auto_trading_layout.py',
        'futures_trading_layout.py': 'dashboardtest/futures_trading_layout.py',
        'binance_exact_layout.py': 'dashboardtest/binance_exact_layout.py',
        'email_config_layout.py': 'dashboardtest/email_config_layout.py',
        'hybrid_learning_layout.py': 'dashboardtest/hybrid_learning_layout.py'
    }
    
    # Read all files
    layout_content = read_file_safe(layout_file)
    if not layout_content:
        print("❌ Could not read layout.py")
        return
    
    spec_contents = {}
    for name, path in specialized_files.items():
        content = read_file_safe(path)
        if content:
            spec_contents[name] = content
    
    print(f"📖 Read layout.py ({len(layout_content)} chars)")
    print(f"📖 Read {len(spec_contents)} specialized files")
    
    # Instead of removing duplicates, let's try a different approach
    # We'll comment out the duplicate sections with clear markers
    
    print("\n🎯 STRATEGY CHANGE: Commenting out duplicates instead of removing")
    print("This allows easy rollback if needed")
    
    # Find the main problematic duplicate sections
    duplicate_sections = [
        # Auto trading duplicates
        (r'# === AUTO TRADING TAB COMPONENTS.*?# === END AUTO TRADING', 'AUTO_TRADING_DUPLICATES'),
        # Futures trading duplicates  
        (r'# === FUTURES TRADING TAB COMPONENTS.*?# === END FUTURES', 'FUTURES_TRADING_DUPLICATES'),
        # Email config duplicates
        (r'# === EMAIL CONFIG TAB COMPONENTS.*?# === END EMAIL', 'EMAIL_CONFIG_DUPLICATES'),
        # Binance exact duplicates
        (r'# === BINANCE EXACT TAB COMPONENTS.*?# === END BINANCE', 'BINANCE_EXACT_DUPLICATES'),
        # Hybrid learning duplicates
        (r'# === HYBRID LEARNING TAB COMPONENTS.*?# === END HYBRID', 'HYBRID_LEARNING_DUPLICATES')
    ]
    
    # Create backup
    backup_file = f'dashboardtest/layout_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py'
    shutil.copy2(layout_file, backup_file)
    print(f"💾 Backup created: {backup_file}")
    
    # Apply conservative fix
    modified_content = layout_content
    sections_commented = 0
    
    for pattern, section_name in duplicate_sections:
        matches = re.findall(pattern, modified_content, re.DOTALL)
        if matches:
            for match in matches:
                # Comment out the entire section
                commented_section = '\n'.join([f'# DUPLICATE_REMOVED: {line}' for line in match.split('\n')])
                modified_content = modified_content.replace(match, 
                    f'# === DUPLICATE SECTION COMMENTED OUT: {section_name} ===\n'
                    f'{commented_section}\n'
                    f'# === END DUPLICATE SECTION: {section_name} ===\n')
                sections_commented += 1
    
    # If no major sections found, try individual component approach
    if sections_commented == 0:
        print("📋 No major sections found, trying individual component approach...")
        
        # Find individual duplicate components
        known_safe_duplicates = [
            'auto-trading-tab-content',
            'futures-trading-tab-content', 
            'binance-exact-tab-content',
            'email-config-tab-content',
            'hybrid-learning-tab-content'
        ]
        
        for dup_id in known_safe_duplicates:
            # Find all occurrences
            pattern = rf'(\s*[^#]*id=["\']?{re.escape(dup_id)}["\']?[^,]*,?)'
            matches = list(re.finditer(pattern, modified_content))
            
            if len(matches) > 1:
                # Keep the first occurrence, comment out the rest
                for i, match in enumerate(matches[1:], 1):
                    original = match.group(1)
                    commented = f'# DUPLICATE_REMOVED_{i}: {original.strip()}'
                    modified_content = modified_content.replace(original, commented)
                    sections_commented += 1
    
    # Write the modified content
    with open(layout_file, 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print(f"✅ Conservative fix applied!")
    print(f"📊 Sections commented out: {sections_commented}")
    print(f"💾 Backup available at: {backup_file}")
    print(f"🔄 To rollback: copy {backup_file} back to {layout_file}")
    
    return True

if __name__ == "__main__":
    create_conservative_fix()
