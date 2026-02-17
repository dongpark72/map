import os
import re

file_path = "e:/Antigravity/Gundammap/maps/views.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update Python truncation logic to be more aggressive (first item only)
def regex_replace(match):
    prefix = match.group(1)
    val_expr = match.group(2)
    # New logic: split by common delimiters and then find first terminology match
    new_logic = f"""{prefix}
                    z_text = {val_expr}
                    # Split by common delimiters first
                    v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()
                    # Regexp match for first terminology (지역, 구역, 지구)
                    import re as pyre
                    m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                    if m: v = m.group(0)
                    structured_data['land']['{prefix[-2:-1] == '1' and '용도지역1' or '용도지역2'}'] = v"""
    return new_logic

# Find zoning assignment parts
# zoning1 = soup.find(id='present_mark1')
# if zoning1:
#     z_text = zoning1.get_text(strip=True)
#     structured_data['land']['용도지역1'] = v ...

# Simple replacement for the specific lines
old_z1 = "structured_data['land']['용도지역1'] = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()"
new_z1 = """# Regexp match for first terminology (지역, 구역, 지구)
                    import re as pyre
                    v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()
                    m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                    structured_data['land']['용도지역1'] = m.group(0) if m else v"""

old_z2 = "structured_data['land']['용도지역2'] = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()"
new_z2 = """# Regexp match for first terminology (지역, 구역, 지구)
                    import re as pyre
                    v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()
                    m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                    structured_data['land']['용도지역2'] = m.group(0) if m else v"""

if old_z1 in content:
    content = content.replace(old_z1, new_z1)
if old_z2 in content:
    content = content.replace(old_z2, new_z2)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("views.py refined with regex truncation")
