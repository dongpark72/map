with open("e:/Antigravity/Gundammap/land_det_debug.html", "r", encoding='utf-8') as f:
    content = f.read()

import re
scripts = re.findall(r'<script.*?>.*?</script>', content, re.DOTALL)
for i, s in enumerate(scripts):
    if "RelYearJigaList" in s:
        print(f"--- Script {i} ---")
        print(s[:500])
        print("...")
        print(s[-500:])
