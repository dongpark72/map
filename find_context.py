with open("e:/Antigravity/Gundammap/land_det_debug.html", "r", encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "공시지가" in line:
        print(f"--- Line {i+1} ---")
        for j in range(max(0, i-2), min(len(lines), i+10)):
            print(lines[j].strip())
