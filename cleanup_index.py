import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i in range(len(lines)):
    line = lines[i]
    # If this line is empty (or just whitespace) and the previous line was also empty, skip it
    if i > 0 and not line.strip() and not lines[i-1].strip():
        continue
    new_lines.append(line)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)

print("Cleanup successful")
