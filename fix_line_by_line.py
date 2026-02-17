import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = 0
for i in range(len(lines)):
    if skip > 0:
        skip -= 1
        continue
    
    line = lines[i]
    
    # Check for the mangled title element
    if '<div class="info-panel-title">토지 정보</div>' in line:
        new_lines.append(line.replace('<div class="info-panel-title">토지 정보</div>', ''))
        continue

    # Check for the mangled CSS
    if 'justify-content: space-between;' in line and '.info-panel-header' in lines[i-1 if i>0 else 0]:
        new_lines.append(line.replace('justify-content: space-between;', 'justify-content: flex-end;'))
        continue

    # Check for the mangled JS split
    # 1482:                             val = val.split(',')[0].split('<')[0].split('(')[0].split('
    # 1483: ')[0].split('  ')[0].trim();
    if ".split('(')[0].split('" in line and i + 1 < len(lines) and "')[0].split('  ')[0].trim();" in lines[i+1]:
        # Fix the split logic
        indent = line[:line.find("val =")]
        new_lines.append(f"{indent}val = val.split(',')[0].split('<')[0].split('(')[0].split('\\\\n')[0].split('  ')[0].trim();\n")
        skip = 1
        continue
        
    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)

print("Title removed and JS syntax fixed (Line by line).")
