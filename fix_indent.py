import os

file_path = "e:/Antigravity/Gundammap/maps/views.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
skip = False
for i, line in enumerate(lines):
    # Check for the corrupted block
    if "if z_text and '지정되지' not in z_text:" in line:
        output_lines.append(line)
        # Look ahead for corrupted indentation
        if i + 1 < len(lines) and "# Regexp match" in lines[i+1]:
             # We need to indent the next 4 lines
             output_lines.append("                        # Regexp match for first terminology (지역, 구역, 지구)\n")
             output_lines.append("                        import re as pyre\n")
             output_lines.append("                        v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()\n")
             output_lines.append("                        m = pyre.search(r'.*?(지역|구역|지구|지목)', v)\n")
             output_lines.append("                        structured_data['land']['용도지역2'] = m.group(0) if m else v\n")
             # Skip the next 5 lines of the original file (the comment + 4 code lines)
             skip_count = 5
             # Let's count how many lines to skip exactly based on what we saw in view_file
             # 222: # Regexp match...
             # 223: import re...
             # 224: v = ...
             # 225: m = ...
             # 226: structured_data...
             continue 
    
    if skip_count > 0:
        skip_count -= 1
        continue
    
    output_lines.append(line)

# Since range-based skipping is tricky with line numbers, let's just do a clean replacement of the whole block.
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern matching for the broken part
broken_part = """                    if z_text and '지정되지' not in z_text:
                        # Regexp match for first terminology (지역, 구역, 지구)
                    import re as pyre
                    v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()
                    m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                    structured_data['land']['용도지역2'] = m.group(0) if m else v"""

fixed_part = """                    if z_text and '지정되지' not in z_text:
                        # Regexp match for first terminology (지역, 구역, 지구)
                        import re as pyre
                        v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()
                        m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                        structured_data['land']['용도지역2'] = m.group(0) if m else v"""

if broken_part in content:
    content = content.replace(broken_part, fixed_part)
else:
    # Use regex if exact match fails due to line endings
    import re
    content = re.sub(r"if z_text and '지정되지' not in z_text:\s+# Regexp match.*?\n\s+import re as pyre\n\s+v = .*?\n\s+m = .*?\n\s+structured_data\['land'\]\['용도지역2'\] = m\.group\(0\) if m else v", fixed_part, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Indentation fixed")
