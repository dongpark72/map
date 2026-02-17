import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove "토지 정보" title and adjust header
# Pattern to find the title row
title_pattern = r'<div class="info-panel-title">토지 정보</div>'
content = content.replace(title_pattern, '')

# Adjust header justify-content to space-between (will move buttons to right since title is gone)
# Wait, if title is gone, justify-content: flex-end might be better for buttons. 
# But the user might want the toggle button visible.
css_header_old = ".info-panel-header {\n            display: flex;\n            justify-content: space-between;"
css_header_new = ".info-panel-header {\n            display: flex;\n            justify-content: flex-end; /* Align to right since title is removed */"
content = content.replace(css_header_old, css_header_new)

# 2. Improve truncation in JS
# Existing: val = val.split(',')[0].split('<')[0].split('(')[0].trim();
# We want to be even more aggressive if it's long and has no delimiters.
# But "first item" usually means delimited by comma or newline.
# I'll add splitting by space or dots as well if needed? No, let's keep it safe but add split('\n').

js_trunc_old = "val = val.split(',')[0].split('<')[0].split('(')[0].trim();"
js_trunc_new = "val = val.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].trim();\n                        // If still too long, take until first space or first 15 chars if it looks like a description\n                        if (['용도지역1', '지목'].includes(k) && val.length > 20) {\n                            val = val.split(' ')[0];\n                        }"

content = content.replace(js_trunc_old, js_trunc_new)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("index.html refined")
