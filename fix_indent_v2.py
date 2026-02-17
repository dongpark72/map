import os

file_path = "e:/Antigravity/Gundammap/maps/views.py"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i in range(len(lines)):
    line = lines[i]
    # Detect the specific block
    if "if z_text and '지정되지' not in z_text:" in line:
        new_lines.append(line)
        # Check if the next lines are under-indented
        # We expect 5 lines to be fixed
        j = i + 1
        while j < i + 6 and j < len(lines):
            next_line = lines[j]
            if next_line.strip() and not next_line.startswith("                        "):
                # Add missing 4 spaces if it's one of the targeted lines
                if any(x in next_line for x in ["# Regexp match", "import re", "v = z_text", "m = pyre", "structured_data['land']['용도지역2']"]):
                    new_lines.append("    " + next_line)
                else:
                    new_lines.append(next_line)
            else:
                new_lines.append(next_line)
            j += 1
        # Skip the lines we just handled in the main loop
        # Actually, this logic is safer:
    elif i > 0 and any(x in line for x in ["# Regexp match", "import re", "v = z_text", "m = pyre", "structured_data['land']['용도지역2']"]) and "if z_text and '지정되지' not in z_text:" in lines[i-1 if i < 222 else (i-2)]:
         # This is getting complicated. Let's just use string replace on the whole file.
         pass
    else:
        # Check if this line was already added by the 'if' block above
        # This is too complex for a quick fix.
        pass

# LET'S DO THE SIMPLEST THING:
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The pattern we saw in view_file:
# 221:                     if z_text and '지정되지' not in z_text:
# 222:                         # Regexp match for first terminology (지역, 구역, 지구)
# 223:                     import re as pyre
# 224:                     v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\n')[0].strip()
# 225:                     m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
# 226:                     structured_data['land']['용도지역2'] = m.group(0) if m else v

broken = """                    if z_text and '지정되지' not in z_text:
                        # Regexp match for first terminology (지역, 구역, 지구)
                    import re as pyre
                    v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()
                    m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                    structured_data['land']['용도지역2'] = m.group(0) if m else v"""

# Wait, view_file showed line 222 WAS indented correctly?
# 221:                     if z_text and '지정되지' not in z_text:
# 222:                         # Regexp match for first terminology (지역, 구역, 지구)
# 223:                     import re as pyre
# Oh, #222 has 24 spaces (8*3), but lines 223-226 have only 20 (8*2.5?).
# Let's count from the view_file output.
# Line 221: 20 spaces
# Line 222: 24 spaces
# Line 223: 20 spaces
# Yes, 223 is at the same level as 221.

fixed = """                    if z_text and '지정되지' not in z_text:
                        # Regexp match for first terminology (지역, 구역, 지구)
                        import re as pyre
                        v = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()
                        m = pyre.search(r'.*?(지역|구역|지구|지목)', v)
                        structured_data['land']['용도지역2'] = m.group(0) if m else v"""

content = content.replace(broken, fixed)

# Also check for other variants due to \n escaping
content = content.replace(broken.replace("\\n", "\n"), fixed.replace("\\n", "\n"))

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Fixed")
