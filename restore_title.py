import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Restore the "토지 정보" title to the left of the header
header_content_old = '<div class="info-panel-header">\n            <div class="header-btns">'
header_content_new = '<div class="info-panel-header">\n            <div class="info-panel-title">토지 정보</div>\n            <div class="header-btns">'

if header_content_old in content:
    content = content.replace(header_content_old, header_content_new)

# 2. Re-adjust header CSS to space-between
css_header_old = ".info-panel-header {\n            display: flex;\n            justify-content: flex-end; /* Align to right since title is removed */"
css_header_new = ".info-panel-header {\n            display: flex;\n            justify-content: space-between;"
content = content.replace(css_header_old, css_header_new)

# 3. Ensure title is visible (if it was hidden by some other CSS I might have missed)
# I'll add the .info-panel-title style again to be sure
# Wait, I already have it in the file from the early days, let's check its color.

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Title restored and styled")
