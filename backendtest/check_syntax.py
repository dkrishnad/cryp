import ast

try:
    with open('ultra_fast_endpoints.py', 'r') as f:
        content = f.read()
    ast.parse(content)
    print("✅ Syntax is valid")
except SyntaxError as e:
    print(f"❌ Syntax error at line {e.lineno}: {e.msg}")
    print(f"Text: {e.text}")
except IndentationError as e:
    print(f"❌ Indentation error at line {e.lineno}: {e.msg}")
    print(f"Text: {e.text}")
