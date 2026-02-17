import os

file_path = "e:/Antigravity/Gundammap/maps/views.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Land Info Extraction to be more robust
old_parsing = """                # 테이블에서 th-td 쌍으로 정보 추출
                for th in soup.find_all('th'):
                    text = th.get_text(strip=True)
                    td = th.find_next_sibling('td')
                    if not td:
                        continue
                    val = td.get_text(strip=True)
                    
                    if '소재지' in text:
                        structured_data['land']['소재지'] = val
                    elif text == '지목':
                        structured_data['land']['지목'] = val
                    elif '면적' in text and 'm' in text.lower():
                        structured_data['land']['면적'] = val.replace('㎡', '').replace('m²', '').strip()
                    elif text == '이용상황':
                        structured_data['land']['이용상황'] = val
                    elif '도로' in text:
                        structured_data['land']['도로'] = val
                    elif '형상' in text:
                        structured_data['land']['형상'] = val
                    elif '지세' in text or '지형높이' in text:
                        structured_data['land']['지세'] = val"""

new_parsing = """                # More robust extraction using IDs and specific selectors
                def get_clean_text(selector, attr=None):
                    node = soup.select_one(selector)
                    if node:
                        return node.get_text(strip=True) if not attr else node.get(attr, '').strip()
                    return ''

                # Try specific IDs first (Common in 토지이음)
                addr = soup.find(id='address') or soup.find(id='addr')
                if addr: structured_data['land']['소재지'] = addr.get_text(strip=True)
                
                # Broad attribute search
                for th in soup.find_all(['th', 'td'], class_='tit'):
                    text = th.get_text(strip=True)
                    td = th.find_next_sibling(['td', 'th'])
                    if not td: continue
                    val = td.get_text(strip=True)
                    
                    if '소재지' in text and not structured_data['land']['소재지']:
                        structured_data['land']['소재지'] = val
                    elif text == '지목':
                        structured_data['land']['지목'] = val
                    elif '면적' in text and ('m' in text.lower() or '㎡' in text):
                        structured_data['land']['면적'] = val.replace('㎡', '').replace('m²', '').strip()
                    elif '이용상황' in text:
                        structured_data['land']['이용상황'] = val
                    elif '도로건재' in text or '도로' in text:
                        structured_data['land']['도로'] = val
                    elif '지형형상' in text or '형상' in text:
                        structured_data['land']['형상'] = val
                    elif '지형높이' in text or '지세' in text:
                        structured_data['land']['지세'] = val"""

content = content.replace(old_parsing, new_parsing)

# 2. Fix Backend Truncation (Keep only first item)
old_zoning = "structured_data['land']['용도지역1'] = z_text.split(',')[0].strip() if ',' in z_text else z_text"
new_zoning = "structured_data['land']['용도지역1'] = z_text.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].strip()"

content = content.replace(old_zoning, new_zoning)
content = content.replace("z_text.split(',')[0].strip() if ',' in z_text else z_text", new_zoning) # Double check

# 3. Fix price formatting if empty (avoid returning empty string for years)
# In case Gongsi fetch returns empty, V-World NED might have filled it. 
# Make sure we don't overwrite NED data with empty strings from Gongsi fetch.
old_gongsi = """                        if year in ['2025', '2024', '2023', '2022']:
                            structured_data['land'][year] = tds[1].get_text(strip=True).replace(',', '').replace('원', '').strip()"""

new_gongsi = """                        if year in ['2025', '2024', '2023', '2022']:
                            v = tds[1].get_text(strip=True).replace(',', '').replace('원', '').strip()
                            if v: structured_data['land'][year] = v"""

content = content.replace(old_gongsi, new_gongsi)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("views.py refined")
