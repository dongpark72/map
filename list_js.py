with open("e:/Antigravity/Gundammap/land_det_debug.html", "r", encoding='utf-8') as f:
    content = f.read()

import re
scripts = re.findall(r'<script src="(.*?)"></script>', content)
for s in scripts:
    print(s)
