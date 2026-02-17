with open("e:/Antigravity/Gundammap/land_det_debug.html", "r", encoding='utf-8') as f:
    content = f.read()

if "20,360,000" in content:
    print("Found 20,360,000 in HTML")
else:
    print("NOT Found in HTML")
