#!/usr/bin/env python3
"""
Script para corrigir problemas de indentação no main.py
"""

def fix_indentation(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixed_lines = []
    in_function = False
    in_class = False
    current_indent = 0
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            fixed_lines.append(line)
            continue
        
        # Skip comments that are properly indented
        if stripped.startswith('#'):
            fixed_lines.append(line)
            continue
        
        # Count leading spaces
        leading_spaces = len(line) - len(line.lstrip())
        
        # Detect class definitions
        if stripped.startswith('class ') and stripped.endswith(':'):
            in_class = True
            current_indent = leading_spaces
            fixed_lines.append(line)
            continue
            
        # Detect function definitions  
        if stripped.startswith('def ') and stripped.endswith(':'):
            in_function = True
            fixed_lines.append(line)
            continue
            
        # End of class/function (dedent to 0 or to class level)
        if not line.startswith(' ') and not stripped.startswith('@'):
            in_class = False
            in_function = False
            current_indent = 0
            fixed_lines.append(line)
            continue
        
        # Fix common indentation problems
        if in_class and not in_function:
            # Class members should be indented by 4 spaces
            if leading_spaces == 8 and not any(keyword in stripped for keyword in ['try:', 'except', 'if ', 'for ', 'while ', 'with ', 'return ', 'raise ', 'continue', 'break']):
                # This might be a wrongly indented class member
                if not stripped.startswith('"""') and not stripped.startswith("'''"):
                    fixed_line = '    ' + stripped + '\n'
                    fixed_lines.append(fixed_line)
                    continue
        
        # Fix Config class indentation
        if stripped.startswith('class Config:'):
            fixed_lines.append(line)
            continue
            
        if stripped == 'from_attributes = True' and leading_spaces == 4:
            fixed_lines.append('        from_attributes = True\n')
            continue
            
        if stripped.startswith('json_encoders = {') and leading_spaces == 4:
            fixed_lines.append('        json_encoders = {\n')
            continue
            
        # Fix function body indentation issues
        if stripped in ['yield db', 'db.close()', 'expire = datetime.utcnow() + expires_delta', 'expire = datetime.utcnow() + timedelta(minutes=15)'] and leading_spaces == 4:
            fixed_lines.append('        ' + stripped + '\n')
            continue
            
        # Default: keep the line as is
        fixed_lines.append(line)
    
    # Write the fixed file
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed indentation in {filename}")

if __name__ == "__main__":
    fix_indentation("main_broken.py")
    print("Indentation fixed!")
