import os

file_path = "e:/Antigravity/Gundammap/templates/maps/index.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CSS
css_old = """        #info-panel {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            border-top: 1px solid var(--glass-border);
            padding: 15px 20px;
            z-index: 999;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        #info-panel.show {
            max-height: 300px;
            overflow-y: auto;
        }"""

css_new = """        #info-panel {
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: var(--glass-bg);
            backdrop-filter: blur(16px);
            border-top: 1px solid var(--glass-border);
            padding: 10px 20px;
            z-index: 2000;
            max-height: 40px; /* Minimized height */
            overflow: hidden;
            transition: max-height 0.3s ease;
            user-select: text; /* Allow text selection for copy-paste */
        }

        #info-panel.show {
            max-height: 500px;
        }

        .info-panel-header {
            display: flex;
            justify-content: flex-end; /* Align toggle and close to the right */
            align-items: center;
            height: 30px;
            margin-bottom: 5px;
        }

        .info-panel-title {
            display: none; /* Removed as requested */
        }

        .header-btns {
            display: flex;
            gap: 12px;
            align-items: center;
        }

        .info-toggle-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: #253858;
            padding: 2px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.75rem;
            font-weight: 600;
            transition: all 0.2s;
        }

        .info-toggle-btn:hover {
            background: rgba(255, 255, 255, 0.4);
        }

        .info-panel-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: var(--text-muted);
            padding: 0;
            line-height: 1;
        }"""

# 2. Update HTML
html_old = """    <div id="info-panel">
        <div class="info-panel-header">
            <div class="info-panel-title">토지 정보</div>
            <button class="info-panel-close" onclick="closeInfoPanel()">×</button>
        </div>
        <div id="info-content">
            <p style="text-align: center; color: #64748b;">정보를 불러오는 중...</p>
        </div>
    </div>"""

html_new = """    <div id="info-panel">
        <div class="info-panel-header">
            <div class="header-btns">
                <button class="info-toggle-btn" onclick="toggleInfoPanel()">접기/펴기</button>
                <button class="info-panel-close" onclick="closeInfoPanel()">×</button>
            </div>
        </div>
        <div id="info-content">
            <p style="text-align: center; color: #64748b;">정보를 불러오는 중...</p>
        </div>
    </div>"""

# 3. Update Function
func_start = "        async function showLandInfo(pnu) {"
func_end = "        function closeInfoPanel() {" # We'll replace up to here

# We'll use a more flexible replacement for the function due to its length
import re

func_pattern = re.compile(r"async function showLandInfo\(pnu\).*?function closeInfoPanel\(\) \{", re.DOTALL)

new_func_code = """async function showLandInfo(pnu) {
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
                            val = val.split(',')[0].split('(')[0].trim();
                        }

                        // Format numbers with commas if they are land prices
                        if (['2025', '2024', '2023', '2022'].includes(k) && val) {
                            const num = val.replace(/[^0-9]/g, '');
                            if (num) {
                                val = Number(num).toLocaleString();
                            }
                        }
                        // Format area with commas
                        if (k === '면적' && val) {
                            const num = val.replace(/[^0-9.]/g, '');
                            if (num) {
                                val = Number(num).toLocaleString('ko-KR', { maximumFractionDigits: 2 });
                            }
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
                        if (k === '사용승인일' && val && val.length === 8) {
                            val = val.substring(0, 4) + '-' + val.substring(4, 6) + '-' + val.substring(6, 8);
                        }

                        // Format numbers with commas for area fields
                        if (['연면적', '용적연면적', '건축면적', '대지'].includes(k) && val) {
                            const num = val.replace(/[^0-9.]/g, '');
                            if (num) {
                                val = Number(num).toLocaleString('ko-KR', { maximumFractionDigits: 2 });
                            }
                        }
                        // Format height, 건폐율, 용적률
                        if (['높이', '건폐율', '용적률'].includes(k) && val) {
                            const num = val.replace(/[^0-9.]/g, '');
                            if (num) {
                                val = Number(num).toLocaleString('ko-KR', { maximumFractionDigits: 2 });
                            }
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

# Apply changes
# Normalize to help with matching
content_norm = content.replace('\\r\\n', '\\n')
css_old_norm = css_old.replace('\\r\\n', '\\n')
html_old_norm = html_old.replace('\\r\\n', '\\n')

if css_old in content:
    content = content.replace(css_old, css_new)
elif css_old_norm in content_norm:
    # This is trickier if we want to preserve original line endings, but let's try direct replace on norm
    content = content_norm.replace(css_old_norm, css_new).replace('\\n', os.linesep)

if html_old in content:
    content = content.replace(html_old, html_new)
elif html_old_norm in content_norm:
    content = content_norm.replace(html_old_norm, html_new).replace('\\n', os.linesep)

content = func_pattern.sub(new_func_code, content)

with open(file_path, 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Replacement successful")
