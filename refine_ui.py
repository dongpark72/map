import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clear out excess line breaks first to make it manageable
import re
content = re.sub(r'(\n\s*)+\n', '\n\n', content)

# 2. Update CSS for info-panel
css_pattern = re.compile(r'#info-panel\s*\{.*?\}\s*#info-panel\.show\s*\{.*?\}\s*\.info-panel-header\s*\{.*?\}\s*\.info-panel-title\s*\{.*?\}\s*\.info-panel-close\s*\{.*?\}\s*\.info-table\s*\{.*?\}\s*\.info-table th\s*\{.*?\}\s*\.info-table td\s*\{.*?\}\s*\.info-table-container\s*\{.*?\}', re.DOTALL)

new_css = """#info-panel {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            border-top: 1px solid var(--glass-border);
            padding: 8px 15px;
            z-index: 2000;
            max-height: 40px; /* Minimized height */
            overflow: hidden;
            transition: max-height 0.3s ease;
            user-select: text;
        }

        #info-panel.show {
            max-height: 500px;
            overflow-y: auto;
        }

        .info-panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            height: 30px;
            margin-bottom: 5px;
        }

        .info-panel-title {
            font-size: 0.95rem;
            font-weight: 700;
            color: #2563eb; /* Blue color like the image */
        }

        .header-btns {
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .info-toggle-btn {
            background: rgba(37, 99, 235, 0.1);
            border: 1px solid rgba(37, 99, 235, 0.2);
            color: #2563eb;
            padding: 1px 8px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .info-panel-close {
            background: none;
            border: none;
            font-size: 1.4rem;
            cursor: pointer;
            color: var(--text-muted);
            line-height: 1;
        }

        .info-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8.5pt;
            background: white;
            margin-bottom: 4px;
        }

        .info-table th {
            background: #253858;
            color: white;
            font-weight: 600;
            padding: 4px 6px;
            border: 1px solid #4a5568;
            white-space: nowrap;
        }

        .info-table td {
            background: white;
            color: #1f2937;
            padding: 4px 6px;
            border: 1px solid #d1d5db;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .info-table-container {
            width: 100%;
            overflow-x: auto;
            margin-bottom: 8px;
        }"""

content = css_pattern.sub(new_css, content)

# 3. Update HTML for info-panel
html_pattern = re.compile(r'<div id="info-panel">.*?<div id="info-content">.*?</div>\s*</div>', re.DOTALL)
new_html = """<div id="info-panel">
        <div class="info-panel-header">
            <div class="info-panel-title">토지 정보</div>
            <div class="header-btns">
                <button class="info-toggle-btn" onclick="toggleInfoPanel()">접기/펴기</button>
                <button class="info-panel-close" onclick="closeInfoPanel()">×</button>
            </div>
        </div>
        <div id="info-content">
            <p style="text-align: center; color: #64748b;">정보를 불러오는 중...</p>
        </div>
    </div>"""

content = html_pattern.sub(new_html, content)

# 4. Update JS for showLandInfo
js_pattern = re.compile(r'async function showLandInfo\(pnu\).*?\}\s*function closeInfoPanel\(\)\s*\{', re.DOTALL)
new_js = """async function showLandInfo(pnu) {
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
                            val = val.split(',')[0].split('<')[0].split('(')[0].trim();
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
        }

        function toggleInfoPanel() {
            const panel = document.getElementById('info-panel');
            panel.classList.toggle('show');
        }

        function closeInfoPanel() {"""

content = js_pattern.sub(new_js, content)

with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("Replacement successful")
