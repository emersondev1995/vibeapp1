#!/usr/bin/env python3
"""
Simple syntax check for main.py
"""

import ast
import sys

def check_syntax(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to parse the file
        ast.parse(content)
        print(f"✅ {filename} - Syntax is correct!")
        return True
        
    except SyntaxError as e:
        print(f"❌ {filename} - Syntax Error:")
        print(f"  Line {e.lineno}: {e.text}")
        print(f"  Error: {e.msg}")
        return False
    except IndentationError as e:
        print(f"❌ {filename} - Indentation Error:")
        print(f"  Line {e.lineno}: {e.text}")
        print(f"  Error: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filename} - Other Error: {e}")
        return False

if __name__ == "__main__":
    if check_syntax("main.py"):
        print("\n🎉 File is ready to run!")
        print("💡 You can now run: python main.py")
    else:
        print("\n🔧 Please fix the errors above")
