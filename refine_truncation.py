import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update JS truncation logic with regex for better accuracy
old_js_logic = """                        // 용도지역1/용도지역2/지목 내용은 맨 처음 1개만 표시
                        if (['용도지역1', '용도지역2', '지목'].includes(k) && val) {
                            val = val.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].trim();
                        }"""

new_js_logic = """                        // 용도지역1/용도지역2/지목 내용은 맨 처음 1개만 표시
                        if (['용도지역1', '용도지역2', '지목'].includes(k) && val) {
                            // 1. 공통 구분자로 1차 분리
                            val = val.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].split('  ')[0].trim();
                            // 2. '지역', '구역', '지구' 단어 기준 첫 번째 매칭만 추출 (더 공격적인 요약)
                            const match = val.match(/.*?(지역|구역|지구|지목)/);
                            if (match) {
                                val = match[0];
                            }
                        }"""

if old_js_logic in content:
    content = content.replace(old_js_logic, new_js_logic)
else:
    # Fallback if previous replacement was slightly different
    import re
    content = re.sub(r"if \(\['용도지역1', '용도지역2', '지목'\]\.includes\(k\) && val\) \{.*?\}", new_js_logic, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("index.html refined with regex truncation")
