import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the "토지 정보" title element
content = content.replace('<div class="info-panel-title">토지 정보</div>', '')

# 2. Adjust header CSS
old_css = ".info-panel-header {\n            display: flex;\n            justify-content: space-between;"
new_css = ".info-panel-header {\n            display: flex;\n            justify-content: flex-end;"
content = content.replace(old_css, new_css)

# 3. Fix the mangled JS in showLandInfo
# We need to find the specific mangled block. 
# Based on view_file:
# val = val.split(',')[0].split('<')[0].split('(')[0].split('
# ')[0].split('  ')[0].trim();

# I'll use a broad replacement for the whole function to be absolutely sure.
clean_show_land_info = """        async function showLandInfo(pnu) {
            const panel = document.getElementById('info-panel');
            const content = document.getElementById('info-content');

            panel.classList.add('show');
            content.innerHTML = '<p style="text-align: center; color: #64748b;">정보를 불러오는 중...</p>';
            currentInfoPnu = pnu;

            try {
                const response = await fetch(`/proxy/landinfo/?pnu=${pnu}`);
                const data = await response.json();

                if (data.status === 'OK' && data.data) {
                    const land = data.data.land;
                    const bld = data.data.building;

                    let html = '<div class="info-table-container">';

                    // 토지 정보 테이블
                    html += '<table class="info-table"><thead><tr>';
                    const landKeys = ['소재지', '용도지역1', '용도지역2', '지목', '이용상황', '면적', '도로', '형상', '지세', '2025', '2024', '2023', '2022'];
                    landKeys.forEach(k => {
                        let label = k;
                        if (k === '면적') label = '면적(m²)';
                        html += `<th>${label}</th>`;
                    });
                    html += '</tr></thead><tbody><tr>';
                    landKeys.forEach(k => {
                        let val = land[k] || '';
                        
                        // 용도지역1/용도지역2/지목 내용은 맨 처음 1개만 표시
                        if (['용도지역1', '용도지역2', '지목'].includes(k) && val) {
                            // 1. 공통 구분자로 1차 분리
                            val = val.split(',')[0].split('<')[0].split('(')[0].split('\\n')[0].split('  ')[0].trim();
                            // 2. '지역', '구역', '지구' 단어 기준 첫 번째 매칭만 추출
                            const match = val.match(/.*?(지역|구역|지구|지목)/);
                            if (match) {
                                val = match[0];
                            }
                        }

                        // Format numbers with commas
                        if (['2025', '2024', '2023', '2022'].includes(k) && val) {
                            const num = val.toString().replace(/[^0-9]/g, '');
                            if (num) val = Number(num).toLocaleString();
                        }
                        if (k === '면적' && val) {
                            const num = val.toString().replace(/[^0-9.]/g, '');
                            if (num) val = Number(num).toLocaleString('ko-KR', { maximumFractionDigits: 2 });
                        }
                        html += `<td>${val}</td>`;
                    });
                    html += '</tr></tbody></table></div>';

                    // 건축물 정보 테이블
                    html += '<div class="info-table-container">';
                    html += '<table class="info-table"><thead><tr>';
                    const bldKeys = ['건물명', '동명칭', '사용승인일', '구조', '지붕', '주용도', '지하', '지상', '연면적', '용적연면적', '건축면적', '대지', '높이', '건폐율', '용적률'];
                    bldKeys.forEach(k => {
                        let label = k;
                        if (['연면적', '용적연면적', '건축면적', '대지'].includes(k)) label += '(m²)';
                        if (k === '높이') label += '(m)';
                        if (['건폐율', '용적률'].includes(k)) label += '(%)';
                        html += `<th>${label}</th>`;
                    });
                    html += '</tr></thead><tbody><tr>';
                    bldKeys.forEach(k => {
                        let val = bld[k] || '';

                        // 사용승인일 날짜 형식 변환 (YYYYMMDD -> YYYY-MM-DD)
                        if (k === '사용승인일' && val && val.toString().length === 8) {
                            val = val.toString().substring(0, 4) + '-' + val.toString().substring(4, 6) + '-' + val.toString().substring(6, 8);
                        }

                        // Format numbers with commas
                        if (['연면적', '용적연면적', '건축면적', '대지', '높이', '건폐율', '용적률'].includes(k) && val) {
                            const num = val.toString().replace(/[^0-9.]/g, '');
                            if (num) val = Number(num).toLocaleString('ko-KR', { maximumFractionDigits: 2 });
                        }
                        html += `<td>${val}</td>`;
                    });
                    html += '</tr></tbody></table></div>';

                    content.innerHTML = html;
                }
                else {
                    content.innerHTML = `<p style="text-align: center; color: #ef4444;">정보를 불러올 수 없습니다: ${data.message || '알 수 없는 오류'}</p>`;
                }
            } catch (error) {
                console.error('Land info fetch error:', error);
                content.innerHTML = '<p style="text-align: center; color: #ef4444;">정보를 불러오는 중 오류가 발생했습니다.</p>';
            }
        }"""

import re
# Look for the start and end of the function. Use re.DOTALL to handle multiline.
mangled_pattern = re.compile(r'async function showLandInfo\(pnu\)\s*\{.*?\}\s*function toggleInfoPanel\(\)', re.DOTALL)
content = mangled_pattern.sub(clean_show_land_info + "\n\n        function toggleInfoPanel()", content)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Title removed and JS syntax fixed.")
