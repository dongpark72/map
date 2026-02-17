
let mapKakao, mapGoogle, kakaoGeocoder, kakaoPlaces;
const vworldApiKey = window.GUNDAM_CONFIG.vworldApiKey;
const vworldDomain = window.GUNDAM_CONFIG.vworldDomain;

// Auto-logout feature removed for user convenience

function logout() {
    // Clear stored credentials
    localStorage.removeItem('gundam_saved_id');
    localStorage.removeItem('gundam_saved_pw');
    localStorage.removeItem('gundam_remember');
    sessionStorage.removeItem('gundam_auth');

    // Redirect to login page
    window.location.href = '/';
}

function checkGundamAuth() {
    const idInput = document.getElementById('gundam-userId');
    const pwInput = document.getElementById('gundam-userPw');
    const id = idInput ? idInput.value.trim() : '';
    const pw = pwInput ? pwInput.value.trim() : '';
    const status = document.getElementById('gundam-status');
    const btn = document.querySelector('.pl-access-btn');

    if (id === 'samduk' && pw === '1318') {
        if (status) {
            status.innerText = "ACCESS GRANTED. LAUNCHING SYSTEM...";
            status.className = "gundam-status status-success";
        }

        sessionStorage.setItem('gundam_auth', 'true');

        if (btn) {
            btn.disabled = true;
            btn.style.opacity = '0.7';
        }

        // Auto-logout feature removed

        console.log('Authentication successful. Hiding overlay...');
        setTimeout(() => {
            const overlay = document.getElementById('gundam-login-overlay');
            if (overlay) {
                overlay.style.transition = 'opacity 0.5s ease-out';
                overlay.style.opacity = '0';
                setTimeout(() => {
                    overlay.style.display = 'none';
                    const sidebar = document.getElementById('sidebar');
                    const tools = document.getElementById('map-tools');
                    if (sidebar) sidebar.style.display = 'flex';
                    if (tools) tools.style.display = 'flex';
                    console.log('Login overlay hidden.');
                }, 500);
            }
        }, 800);
    } else {
        if (status) {
            status.innerText = "ACCESS DENIED. INVALID CREDENTIALS.";
            status.className = "gundam-status status-error";

            // Shake effect
            status.classList.remove('pl-shake');
            void status.offsetWidth; // trigger reflow
            status.classList.add('pl-shake');
        }
    }
}

// Gundam Authentication Logic Initialization
(function initGundamAuth() {
    const isAuth = sessionStorage.getItem('gundam_auth');

    // Reset credentials just in case
    localStorage.removeItem('gundam_saved_id');
    localStorage.removeItem('gundam_saved_pw');
    localStorage.removeItem('gundam_remember');

    if (isAuth !== 'true') {
        const overlay = document.getElementById('gundam-login-overlay');
        if (overlay) overlay.style.display = 'flex';

        const sidebar = document.getElementById('sidebar');
        const tools = document.getElementById('map-tools');
        if (sidebar) sidebar.style.display = 'none';
        if (tools) tools.style.display = 'none';
    } else {
        // Already authenticated (auto-logout removed)
    }
})();


let polygonsData = []; // [{ kakao: [], google: [], markersK: [], markersG: [], badgeEl: el, landBtn: el, infoBtn: el, realBtn: el }]

let currentProvider = 'kakao';
let currentMapType = 'satellite';
let currentViewMode = 'total';

// Roadview variables
let roadview, roadviewClient, rvMinimap, rvMarker, rvMapMarker;
let isRoadviewToolActive = false;

let resultCount = 0;

// Measurement state
let currentMeasureTool = null;
let drawingLine = null;
let drawingPolygon = null;
let measureMarkers = [];
let measureOverlays = [];
let measurePath = [];
let mouseCursorMarker = null;
let areaOverlay = null;

// 패널 드래그 기능
function makeDraggable(panel, header) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    header.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        if (e.target.tagName === 'BUTTON') return;
        e.preventDefault();

        // Stop any css transitions
        panel.style.transition = 'none';

        // Anchor position to current absolute pixels
        const rect = panel.getBoundingClientRect();
        panel.style.top = rect.top + "px";
        panel.style.left = rect.left + "px";
        panel.style.bottom = "auto";
        panel.style.right = "auto";
        panel.style.transform = "none";
        panel.style.margin = "0";

        panel.setAttribute('data-dragged', 'true');

        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        panel.style.top = (panel.offsetTop - pos2) + "px";
        panel.style.left = (panel.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}


const PALETTE = [

    '#FF0000', // Red

    '#0000FF', // Blue

    '#00AA00', // Green

    '#FF8800', // Orange

    '#9900FF', // Purple

    '#FF00FF', // Pink

    '#00CCCC', // Cyan

    '#FFD700', // Yellow

    '#8B4513'  // Brown

];

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const icon = document.getElementById('toggle-icon');
    const isCollapsed = sidebar.classList.toggle('collapsed');
    icon.innerText = isCollapsed ? '▶' : '◀';
}

window.onload = function () {
    makeDraggable(document.getElementById('info-panel'), document.getElementById('info-panel-header'));
    makeDraggable(document.getElementById('price-panel'), document.getElementById('price-panel-header'));
    makeDraggable(document.getElementById('building-panel'), document.getElementById('building-panel-header'));
    makeDraggable(document.getElementById('floor-panel'), document.getElementById('floor-panel-header'));
    makeDraggable(document.getElementById('realprice-panel'), document.getElementById('realprice-panel-header'));
    makeDraggable(document.getElementById('warehouse-panel'), document.getElementById('warehouse-header'));
    makeDraggable(document.getElementById('hospital-panel'), document.getElementById('hospital-header'));
    makeDraggable(document.getElementById('auction-panel'), document.getElementById('auction-header'));

    if (window.location.protocol === 'file:') {

        document.getElementById('server-alert').style.display = 'block';

    }

    initMaps();

    kakaoGeocoder = new kakao.maps.services.Geocoder();

    kakaoPlaces = new kakao.maps.services.Places();

    // Click outside to close color picker

    document.addEventListener('click', (e) => {

        if (!e.target.closest('.badge-wrapper')) {

            document.querySelectorAll('.color-picker').forEach(p => p.classList.remove('show'));

        }

    });

    initDraggable(document.getElementById('building-panel'), document.getElementById('building-panel-header'));
    initDraggable(document.getElementById('info-panel'), document.getElementById('info-panel-header'));
    initDraggable(document.getElementById('price-panel'), document.getElementById('price-panel-header'));
};

function initDraggable(el, header) {
    if (!el || !header) return;
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    header.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e = e || window.event;
        if (e.target.tagName === 'BUTTON') return; // Don't drag when clicking buttons
        e.preventDefault();

        // If element has dynamic positioning, fix it to current absolute pixels for dragging
        if (el.id === 'info-panel' || el.id === 'price-panel') {
            const rect = el.getBoundingClientRect();
            el.style.left = rect.left + 'px';
            el.style.top = rect.top + 'px';
            el.style.bottom = 'auto';
            el.style.right = 'auto';
            el.style.transform = 'none'; // Temporarily clear transform for pixel-perfect dragging
            el.style.transition = 'none'; // Stop sliding during drag
            el.setAttribute('data-dragged', 'true');
        }

        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        el.style.top = (el.offsetTop - pos2) + "px";
        el.style.left = (el.offsetLeft - pos1) + "px";
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}


function initMaps() {

    // 서울시 종로구 우정국로 48 좌표

    const lat = 37.5732;

    const lng = 126.9840;

    const center = new kakao.maps.LatLng(lat, lng);

    mapKakao = new kakao.maps.Map(document.getElementById('map-kakao'), { center, level: 3, mapTypeId: kakao.maps.MapTypeId.HYBRID });

    mapGoogle = new google.maps.Map(document.getElementById('map-google'), { center: { lat, lng }, zoom: 18, mapTypeId: 'hybrid', mapTypeControl: false });

    kakao.maps.event.addListener(mapKakao, 'rightclick', (mouseEvent) => {
        // Clear both Warehouse and Auction markers/panels
        let clearedAny = false;
        if (window.warehouseMarkers && window.warehouseMarkers.length > 0) {
            window.warehouseMarkers.forEach(m => m.setMap(null));
            window.warehouseMarkers = [];
            closeWarehousePanel();
            clearedAny = true;
        }
        if (window.auctionMarkers && window.auctionMarkers.length > 0) {
            window.auctionMarkers.forEach(m => m.setMap(null));
            window.auctionMarkers = [];
            closeAuctionPanel();
            clearedAny = true;
        }
        if (window.hospitalMarkers && window.hospitalMarkers.length > 0) {
            window.hospitalMarkers.forEach(m => m.setMap(null));
            window.hospitalMarkers = [];
            closeHospitalPanel();
            clearedAny = true;
        }

        if (clearedAny) return; // If we cleared markers, don't add address

        // Ignore right-click if measurement tool is active
        if (currentMeasureTool) return;
        addAddressAtLocation(mouseEvent.latLng.getLat(), mouseEvent.latLng.getLng());
    });

    kakao.maps.event.addListener(mapKakao, 'click', (mouseEvent) => {
        if (isRoadviewToolActive) {
            openRoadview(mouseEvent.latLng.getLat(), mouseEvent.latLng.getLng());
            toggleRoadviewTool(); // Turn off tool after click
        }
    });

    mapGoogle.addListener('rightclick', (event) => {

        addAddressAtLocation(event.latLng.lat(), event.latLng.lng());

    });

}

function addAddressAtLocation(lat, lng) {

    const debugStatus = document.getElementById('debug-status');

    kakaoGeocoder.coord2Address(lng, lat, (result, status) => {

        if (status === kakao.maps.services.Status.OK) {

            const addr = result[0].address.address_name;

            const input = document.getElementById('address-input');

            input.value = (input.value.trim() ? input.value.trim() + '\n' : '') + addr;

            if (debugStatus) debugStatus.innerText = `주소 추가됨: ${addr}`;

            input.scrollTop = input.scrollHeight;

        }

    });

}

function switchProvider(p) {
    currentProvider = p;

    // Update UI
    document.querySelectorAll('#btn-prov-kakao, #btn-prov-google').forEach(b => b.classList.remove('active'));
    document.getElementById(`btn-prov-${p}`).classList.add('active');

    document.querySelectorAll('.map-container').forEach(m => m.classList.remove('active'));
    document.getElementById(`map-${p}`).classList.add('active');

    if (p === 'kakao' && mapKakao) mapKakao.relayout();
}

function switchMapType(t) {
    currentMapType = t;

    // Update UI
    document.querySelectorAll('#btn-map-normal, #btn-map-satellite').forEach(b => b.classList.remove('active'));
    document.getElementById(`btn-map-${t}`).classList.add('active');

    if (mapKakao) {
        if (t === 'satellite') {
            mapKakao.setMapTypeId(currentViewMode === 'total' ? kakao.maps.MapTypeId.HYBRID : kakao.maps.MapTypeId.SKYVIEW);
        } else {
            mapKakao.setMapTypeId(kakao.maps.MapTypeId.ROADMAP);
        }
    }
    if (mapGoogle) {
        if (t === 'satellite') {
            mapGoogle.setMapTypeId(currentViewMode === 'total' ? 'hybrid' : 'satellite');
        } else {
            mapGoogle.setMapTypeId('roadmap');
        }
    }
}

function switchViewMode(m) {
    currentViewMode = m;

    // Update UI
    document.querySelectorAll('#btn-view-total, #btn-view-base').forEach(b => b.classList.remove('active'));
    document.getElementById(`btn-view-${m}`).classList.add('active');

    // Refresh map type
    switchMapType(currentMapType);
}

function toggleCadastral() {
    const btn = document.getElementById('btn-cadastral');
    const isActive = btn.classList.toggle('active');

    if (mapKakao) {
        if (isActive) {
            mapKakao.addOverlayMapTypeId(kakao.maps.MapTypeId.USE_DISTRICT);
        } else {
            mapKakao.removeOverlayMapTypeId(kakao.maps.MapTypeId.USE_DISTRICT);
        }
    }
}

let districtPolygons = [];
let districtLabels = [];
let districtActive = false;
let districtCache = new Map();
let districtDebounceTimer = null;

const debouncedDistrictUpdate = () => {
    if (districtDebounceTimer) clearTimeout(districtDebounceTimer);
    districtDebounceTimer = setTimeout(() => {
        updateDistrictOverlay();
    }, 400); // 400ms debounce
};

async function toggleDistrict() {
    const btn = document.getElementById('btn-district');
    const isActive = btn.classList.toggle('active');
    districtActive = isActive;

    if (!mapKakao) {
        console.error('Kakao map not initialized');
        return;
    }


    if (isActive) {
        console.log('Activating district boundary overlay (WFS Optimized)');

        // Automatically switch to 'Base' view mode for a cleaner look
        switchViewMode('base');

        updateDistrictOverlay();

        kakao.maps.event.addListener(mapKakao, 'bounds_changed', debouncedDistrictUpdate);
        kakao.maps.event.addListener(mapKakao, 'zoom_changed', debouncedDistrictUpdate);
    } else {
        console.log('Deactivating district boundary overlay');
        districtPolygons.forEach(p => p.setMap(null));
        districtLabels.forEach(l => l.setMap(null));
        districtPolygons = [];
        districtLabels = [];

        kakao.maps.event.removeListener(mapKakao, 'bounds_changed', debouncedDistrictUpdate);
        kakao.maps.event.removeListener(mapKakao, 'zoom_changed', debouncedDistrictUpdate);
    }
}

async function updateDistrictOverlay() {
    if (!districtActive) return;

    const bounds = mapKakao.getBounds();
    const sw = bounds.getSouthWest();
    const ne = bounds.getNorthEast();
    const level = mapKakao.getLevel();

    // 110m grid snapping for better caching
    const snap = (v, roundFunc) => roundFunc(v * 1000) / 1000;
    const xmin = snap(sw.getLng(), Math.floor);
    const ymin = snap(sw.getLat(), Math.floor);
    const xmax = snap(ne.getLng(), Math.ceil);
    const ymax = snap(ne.getLat(), Math.ceil);
    const bbox = `${xmin},${ymin},${xmax},${ymax}`;

    const oldPolygons = districtPolygons;
    const oldLabels = districtLabels;
    districtPolygons = [];
    districtLabels = [];

    const fetchLayer = async (typename, style, showLabel = false) => {
        const cacheKey = `${typename}_${bbox}`;
        let data;

        if (districtCache.has(cacheKey)) {
            data = districtCache.get(cacheKey);
        } else {
            const wfsUrl = `${window.GUNDAM_CONFIG.apiBase || ''}/proxy/wfs/?typename=${typename}&bbox=${bbox}&srsname=EPSG:4326`;
            try {
                const response = await fetch(wfsUrl);
                data = await response.json();
                if (districtCache.size > 20) districtCache.clear();
                districtCache.set(cacheKey, data);
            } catch (e) {
                console.error(`WFS fetch error (${typename}):`, e);
                return;
            }
        }

        if (data && data.features) {
            data.features.forEach(feature => {
                const geom = feature.geometry;
                if (!geom) return;

                const paths = [];
                let allCoords = [];
                if (geom.type === 'Polygon') {
                    const ring = geom.coordinates[0];
                    paths.push(ring.map(c => new kakao.maps.LatLng(c[1], c[0])));
                    allCoords = ring;
                } else if (geom.type === 'MultiPolygon') {
                    geom.coordinates.forEach(poly => {
                        const ring = poly[0];
                        paths.push(ring.map(c => new kakao.maps.LatLng(c[1], c[0])));
                        allCoords = allCoords.concat(ring);
                    });
                }

                const polygon = new kakao.maps.Polygon({
                    map: mapKakao,
                    path: paths,
                    strokeWeight: style.weight,
                    strokeColor: style.color,
                    strokeOpacity: style.opacity,
                    fillColor: style.fillColor,
                    fillOpacity: style.fillOpacity,
                    clickable: false,
                    zIndex: style.zIndex || 1
                });
                districtPolygons.push(polygon);

                if (showLabel) {
                    const properties = feature.properties || {};
                    let districtName = properties.li_kor_nm || properties.emd_kor_nm || properties.sig_kor_nm || properties.ctp_kor_nm || properties.full_nm || '';

                    if (districtName.split(' ').length > 1) {
                        const parts = districtName.split(' ');
                        districtName = parts.length >= 2 ? parts.slice(1).join(' ') : districtName;
                    }

                    if (districtName && districtName !== 'null') {
                        let latSum = 0, lngSum = 0;
                        allCoords.forEach(c => { lngSum += c[0]; latSum += c[1]; });
                        const centerLat = latSum / allCoords.length;
                        const centerLng = lngSum / allCoords.length;

                        const labelContent = document.createElement('div');
                        labelContent.className = 'district-label';
                        labelContent.style.cssText = `
                                    font-size: 10.5pt;
                                    color: #333333;
                                    font-weight: bold;
                                    text-shadow: -1.5px -1.5px 0 #fff, 1.5px -1.5px 0 #fff, -1.5px 1.5px 0 #fff, 1.5px 1.5px 0 #fff;
                                    pointer-events: none;
                                    white-space: nowrap;
                                `;
                        labelContent.innerText = districtName;

                        const label = new kakao.maps.CustomOverlay({
                            position: new kakao.maps.LatLng(centerLat, centerLng),
                            content: labelContent,
                            map: mapKakao,
                            zIndex: 10
                        });
                        districtLabels.push(label);
                    }
                }
            });
        }
    };

    const SIG_ST_THICK = { weight: 3.5, color: '#FFFF00', opacity: 0.9, fillColor: '#333333', fillOpacity: 0, zIndex: 3 };
    const SIG_ST_THIN = { weight: 1.5, color: '#FFFF00', opacity: 0.8, fillColor: '#333333', fillOpacity: 0, zIndex: 2 };
    const EMD_ST = { weight: 1.8, color: '#FFFF00', opacity: 0.8, fillColor: '#333333', fillOpacity: 0, zIndex: 1 };
    const SIDO_ST = { weight: 4.5, color: '#FFFF00', opacity: 1.0, fillColor: '#333333', fillOpacity: 0, zIndex: 4 };
    const RI_ST = { weight: 1.2, color: '#FFFF00', opacity: 0.7, fillColor: '#333333', fillOpacity: 0, zIndex: 0 };

    let requests = [];
    if (level <= 5) {
        // Show RI and EMD up to 500m (Level 5) - RI names are priority, then EMD
        requests.push(fetchLayer('lt_c_ademd_info', { ...EMD_ST, fillOpacity: 0 }, true));
        requests.push(fetchLayer('lt_c_adri_info', RI_ST, true));
    } else if (level <= 6) {
        // Show SIG and EMD at 1km (Level 6)
        requests.push(fetchLayer('lt_c_adsigg_info', { ...SIG_ST_THICK, fillOpacity: 0 }));
        requests.push(fetchLayer('lt_c_ademd_info', EMD_ST, true));
    } else if (level <= 8) {
        // Regional view: Show SIDO and SIG
        requests.push(fetchLayer('lt_c_adsido_info', { ...SIDO_ST, fillOpacity: 0 }));
        requests.push(fetchLayer('lt_c_adsigg_info', SIG_ST_THIN, true));
    } else {
        // Country view: Show SIDO
        requests.push(fetchLayer('lt_c_adsido_info', SIDO_ST, true));
    }
    try {
        await Promise.all(requests);
        oldPolygons.forEach(p => p.setMap(null));
        oldLabels.forEach(l => l.setMap(null));
    } catch (err) {
        console.error("Batch district update failed:", err);
    }
}

// ---------------------------------------------------------
// Measurement Tools Logic (Distance & Area)
// ---------------------------------------------------------
let isDrawing = false;
let measurePaths = []; // Track paths for current drawing
let measureMarkersK = []; // Points for current drawing
let measureOverlaysK = []; // Labels for current drawing
let allMeasureItems = []; // All completed shapes/overlays

function toggleMeasure(type) {
    const btnDist = document.getElementById('btn-measure-dist');
    const btnArea = document.getElementById('btn-measure-area');

    // If same tool clicked, turn off
    if (currentMeasureTool === type) {
        resetMeasureState();
        currentMeasureTool = null;
        btnDist.classList.remove('active');
        btnArea.classList.remove('active');
        removeMeasureEvents();
        return;
    }

    // Switch tool
    resetMeasureState();
    currentMeasureTool = type;
    btnDist.classList.toggle('active', type === 'dist');
    btnArea.classList.toggle('active', type === 'area');

    // Force cursor to arrow on map container
    const mapContainer = document.getElementById('map-kakao');
    if (currentMeasureTool) {
        mapContainer.style.cursor = 'default';
        const style = document.createElement('style');
        style.id = 'measure-cursor-style';
        style.innerHTML = '#map-kakao * { cursor: default !important; }';
        document.head.appendChild(style);
    } else {
        mapContainer.style.cursor = '';
        const style = document.getElementById('measure-cursor-style');
        if (style) style.remove();
    }

    // Add events
    addMeasureEvents();
}

function addMeasureEvents() {
    removeMeasureEvents(); // Clean up first
    kakao.maps.event.addListener(mapKakao, 'click', onMeasureClick);
    kakao.maps.event.addListener(mapKakao, 'mousemove', onMeasureMove);
    kakao.maps.event.addListener(mapKakao, 'rightclick', onMeasureEnd);
}

function removeMeasureEvents() {
    kakao.maps.event.removeListener(mapKakao, 'click', onMeasureClick);
    kakao.maps.event.removeListener(mapKakao, 'mousemove', onMeasureMove);
    kakao.maps.event.removeListener(mapKakao, 'rightclick', onMeasureEnd);
}

function resetMeasureState() {
    isDrawing = false;
    if (drawingLine) drawingLine.setMap(null);
    if (drawingPolygon) drawingPolygon.setMap(null);
    drawingLine = null;
    drawingPolygon = null;
    measurePath = [];
    measureMarkersK = [];
    measureOverlaysK = [];

    // Reset cursor if tool is off
    const mapContainer = document.getElementById('map-kakao');
    if (mapContainer) mapContainer.style.cursor = '';
    const style = document.getElementById('measure-cursor-style');
    if (style) style.remove();
}

function clearAllMeasurements() {
    allMeasureItems.forEach(item => {
        if (item.setMap) item.setMap(null);
        else if (item.remove) item.remove();
    });
    allMeasureItems = [];
    resetMeasureState();
}

function onMeasureClick(mouseEvent) {
    const clickPosition = mouseEvent.latLng;

    if (!isDrawing) {
        isDrawing = true;
        measurePath = [clickPosition];

        if (currentMeasureTool === 'dist') {
            drawingLine = new kakao.maps.Polyline({
                map: mapKakao,
                path: measurePath,
                strokeWeight: 3,
                strokeColor: '#00a0e9',
                strokeOpacity: 1,
                strokeStyle: 'solid'
            });
            allMeasureItems.push(drawingLine);
        } else {
            drawingPolygon = new kakao.maps.Polygon({
                map: mapKakao,
                path: measurePath,
                strokeWeight: 3,
                strokeColor: '#00a0e9',
                strokeOpacity: 1,
                strokeStyle: 'solid',
                fillColor: '#00a0e9',
                fillOpacity: 0.2
            });
            drawingLine = new kakao.maps.Polyline({
                map: mapKakao,
                path: measurePath,
                strokeWeight: 3,
                strokeColor: '#00a0e9',
                strokeOpacity: 1,
                strokeStyle: 'dashed'
            });
            allMeasureItems.push(drawingPolygon);
            allMeasureItems.push(drawingLine);
        }

        // Add start marker/dot
        displayCircleDot(clickPosition, 0);
    } else {
        measurePath.push(clickPosition);

        if (currentMeasureTool === 'dist') {
            drawingLine.setPath(measurePath);
            const distance = Math.round(drawingLine.getLength());
            displayCircleDot(clickPosition, distance);
        } else {
            drawingPolygon.setPath(measurePath);
            drawingLine.setPath(measurePath);
        }
    }
}

function onMeasureMove(mouseEvent) {
    if (!isDrawing) return;

    const mousePosition = mouseEvent.latLng;
    const path = [...measurePath, mousePosition];

    if (currentMeasureTool === 'dist') {
        drawingLine.setPath(path);
        const distance = Math.round(drawingLine.getLength());
        const content = `<div class="dotOverlay">거리 <span class="number">${distance}</span>m</div>`;
        showTempOverlay(mousePosition, content);
    } else {
        drawingPolygon.setPath(path);
        drawingLine.setPath(path);
        const area = Math.round(drawingPolygon.getArea());
        const content = `<div class="dotOverlay">면적 <span class="number">${area}</span>m<sup>2</sup></div>`;
        showTempOverlay(mousePosition, content);
    }
}

function onMeasureEnd(mouseEvent) {
    if (!isDrawing) return;

    if (currentMeasureTool === 'dist') {
        const distance = Math.round(drawingLine.getLength());
        if (distance > 0) {
            displayDistanceInfo(distance, measurePath[measurePath.length - 1]);
        }
    } else {
        const area = Math.round(drawingPolygon.getArea());
        if (area > 0) {
            displayAreaInfo(area, measurePath[measurePath.length - 1]);
        }
        drawingLine.setMap(null); // Remove dashed line
    }

    isDrawing = false;
    measurePath = [];
    if (mouseCursorMarker) mouseCursorMarker.setMap(null);
}

function displayCircleDot(position, distance) {
    const circle = new kakao.maps.Circle({
        center: position,
        radius: 1,
        strokeWeight: 1,
        strokeColor: '#000',
        strokeOpacity: 0.1,
        fillColor: '#000',
        fillOpacity: 1
    });
    circle.setMap(mapKakao);
    allMeasureItems.push(circle);

    if (distance > 0 && currentMeasureTool === 'dist') {
        // User wants to remove the segment distance labels ("거리 86m")
        // So we do nothing here
    }
}

function showTempOverlay(position, content) {
    if (mouseCursorMarker) mouseCursorMarker.setMap(null);
    mouseCursorMarker = new kakao.maps.CustomOverlay({
        content: content,
        position: position,
        yAnchor: 1
    });
    mouseCursorMarker.setMap(mapKakao);
}

function displayDistanceInfo(distance, position) {
    const content = `
                <div class="distanceInfo">
                    <div class="distanceInfo-row">
                        <div><span class="label">총거리</span><span class="number">${(distance / 1000).toFixed(2)}</span>km</div>
                        <button class="clear-measure" onclick="clearAllMeasurements()">지우기</button>
                    </div>
                </div>
            `;
    const infoOverlay = new kakao.maps.CustomOverlay({
        content: content,
        position: position,
        xAnchor: 0,
        yAnchor: 0
    });
    infoOverlay.setMap(mapKakao);
    allMeasureItems.push(infoOverlay);
}

function displayAreaInfo(area, position) {
    const content = `
                <div class="distanceInfo">
                    <div class="distanceInfo-row">
                        <div><span class="label">총면적</span><span class="number">${area.toLocaleString()}</span>m<sup>2</sup></div>
                        <button class="clear-measure" onclick="clearAllMeasurements()">지우기</button>
                    </div>
                    <div><span class="label"></span><span class="number">${(area / 3.3058).toFixed(2)}</span>평</div>
                </div>
            `;
    const infoOverlay = new kakao.maps.CustomOverlay({
        content: content,
        position: position,
        xAnchor: 0,
        yAnchor: 0
    });
    infoOverlay.setMap(mapKakao);
    allMeasureItems.push(infoOverlay);
}

async function handleSearch() {
    const input = document.getElementById('address-input').value.trim();
    if (!input) return;

    const debugStatus = document.getElementById('debug-status');
    if (debugStatus) debugStatus.innerText = '검색 중...';

    const addresses = input.split('\n').map(a => a.trim()).filter(a => a);
    clearPolygons();
    resultCount = 0;
    document.getElementById('result-list').innerHTML = '';

    for (const addr of addresses) {
        await performSearch(addr);
    }

    if (debugStatus) debugStatus.innerText = '검색 완료';
}

function performSearch(addr) {
    return new Promise((resolve) => {
        kakaoGeocoder.addressSearch(addr, (result, status) => {

            if (status === kakao.maps.services.Status.OK) {

                processResult(result[0], addr);

                resolve();

            } else {

                kakaoPlaces.keywordSearch(addr, (kResult, kStatus) => {

                    if (kStatus === kakao.maps.services.Status.OK) {

                        reverseAndProcess(kResult[0].y, kResult[0].x, addr).then(resolve);

                    } else {

                        logResult(`검색 실패: ${addr}`, 'red');

                        resolve();

                    }

                });

            }

        });
    });
}

function reverseAndProcess(lat, lng, addr) {

    return new Promise((resolve) => {

        kakaoGeocoder.coord2Address(lng, lat, (result, status) => {

            if (status === kakao.maps.services.Status.OK) {

                processResult(result[0], addr, lat, lng);

            } else {

                displayMarkersOnly(lat, lng);

            }

            resolve();

        });

    });

}

function processResult(kakaoRes, addr, lat, lng) {
    const fLat = lat || kakaoRes.y;
    const fLng = lng || kakaoRes.x;
    displayMarkersOnly(fLat, fLng);

    // Use official address name from kakaoRes if available, otherwise fallback to input
    const officialAddr = (kakaoRes.address ? kakaoRes.address.address_name : null) || kakaoRes.address_name || addr;

    const itemIdx = logResult(`${officialAddr}`, 'inherit', fLat, fLng);

    const jibunInfo = kakaoRes.address || kakaoRes.road_address;

    if (jibunInfo && jibunInfo.b_code) {

        fetchBoundary(jibunInfo, addr, itemIdx);

    }

    // Gyeonggi Warehouse Check
    let sigunNm = '';
    let isGyeonggi = false;
    const addrObj = kakaoRes.address || kakaoRes.road_address;

    // Extract for Auction (Sido, Sgk, Emd)
    let sido = addrObj.region_1depth_name || '';
    let sgk = addrObj.region_2depth_name || '';
    let emd = addrObj.region_3depth_name || '';

    if (addrObj && addrObj.region_1depth_name && addrObj.region_1depth_name.includes('경기')) {
        isGyeonggi = true;
        if (addrObj.region_2depth_name) {
            // E.g. "Suwon-si Paldal-gu" -> "Suwon-si"
            sigunNm = addrObj.region_2depth_name.split(' ')[0];
        }
    }

    if (isGyeonggi && sigunNm) {
        checkNearbyWarehouses(fLat, fLng, sigunNm, itemIdx);
    }

    // Check Kamco Auctions
    checkNearbyAuctions(fLat, fLng, sido, sgk, emd, itemIdx);

    // Check Hospitals
    checkNearbyHospitals(fLat, fLng, sido, itemIdx);
}

function displayMarkersOnly(lat, lng) {
    if (!lat || !lng) return;
    const centerK = new kakao.maps.LatLng(lat, lng);
    const centerG = { lat: parseFloat(lat), lng: parseFloat(lng) };

    // Use setCenter for immediate and precise positioning
    mapKakao.setCenter(centerK);
    mapKakao.setLevel(2);

    if (typeof google !== 'undefined' && mapGoogle) {
        mapGoogle.setCenter(centerG);
        mapGoogle.setZoom(19);
    }
    console.log('Maps centered to:', lat, lng);
}

function moveMapToAddr(addr) {
    if (!addr) return;
    // Remove masks like ** from jibun
    const cleanAddr = addr.replace(/\*/g, '').trim();
    console.log('Moving map to:', cleanAddr);

    if (!kakaoGeocoder) {
        console.error('Kakao Geocoder not initialized');
        return;
    }

    kakaoGeocoder.addressSearch(cleanAddr, (result, status) => {
        if (status === kakao.maps.services.Status.OK) {
            const res = result[0];
            const lat = res.y;
            const lng = res.x;

            // Check if it's a specific address (has jibun or is a building address)
            // address_type can be 'REGION_ADDR' (jibun) or 'ROAD_ADDR' (road)
            const isSpecific = (res.address && (res.address.main_address_no || res.address.main_no)) ||
                (res.road_address && (res.road_address.main_building_no || res.road_address.main_no));

            if (isSpecific) {
                console.log('Specific address found, showing boundary...');
                processResult(res, cleanAddr);
            } else {
                console.log('Region/Dong level result, moving map only...');
                displayMarkersOnly(lat, lng);
            }
            console.log('Map moved to:', lat, lng);
        } else {
            console.warn('Geocoding failed for:', cleanAddr, 'Status:', status);
            // Try searching without the last part if it fails (last jibun part)
            const parts = cleanAddr.split(' ');
            if (parts.length > 1) {
                const fallBackAddr = parts.slice(0, -1).join(' ');
                console.log('Retrying with fallback:', fallBackAddr);
                // For fallback dong search, we force displayMarkersOnly
                kakaoGeocoder.addressSearch(fallBackAddr, (fRes, fStatus) => {
                    if (fStatus === kakao.maps.services.Status.OK) {
                        displayMarkersOnly(fRes[0].y, fRes[0].x);
                    }
                });
            }
        }
    });
}

async function fetchBoundary(info, originalAddr, itemIdx) {

    const bCode = (info.b_code || "").substring(0, 10);

    const san = info.mountain_yn === 'Y' ? '2' : '1';

    const extractDigit = (val) => (val || "").toString().replace(/[^0-9]/g, "");

    const bun = extractDigit(info.main_address_no || info.main_no || "").padStart(4, '0');

    const ho = extractDigit(info.sub_address_no || info.sub_no || "").padStart(4, '0');

    const pnu = `${bCode}${san}${bun}${ho}`;

    // Update Land Info Button URL and Info Button

    const data = polygonsData[itemIdx];

    if (data) {

        data.pnu = pnu; // Store PNU

        if (data.landBtn) {

            // Use pnu parameter instead of selPnu for better compatibility

            data.landBtn.href = `https://www.eum.go.kr/web/ar/lu/luLandDet.jsp?pnu=${pnu}&mode=search&isNoScr=script`;

            data.landBtn.title = `토지이용계획 확인 (PNU: ${pnu})`;

            data.landBtn.classList.remove('disabled');

        }

        if (data.infoBtn) {
            data.infoBtn.classList.remove('disabled');
        }

        if (data.gongBtn) {
            data.gongBtn.classList.remove('disabled');
        }

        // Fetch land summary for result list item
        fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/landinfo/?pnu=${pnu}`)
            .then(res => res.json())
            .then(resJson => {
                if (resJson.status === 'OK' && resJson.data && resJson.data.land) {
                    const l = resJson.data.land;

                    // Format area
                    let areaStr = l['면적'] || '-';
                    if (areaStr !== '-') {
                        const num = areaStr.toString().replace(/[^0-9.]/g, '');
                        if (num) areaStr = Number(num).toLocaleString('ko-KR', { maximumFractionDigits: 0 });
                    }

                    // Get latest price
                    const years = ['2025', '2024', '2023'];
                    let priceStr = '-';
                    for (const y of years) {
                        if (l[y]) {
                            const pVal = l[y].toString().replace(/[^0-9]/g, '');
                            if (pVal) {
                                priceStr = `${Number(pVal).toLocaleString()}원/㎡`;
                                break;
                            }
                        }
                    }

                    const parts = [
                        areaStr !== '-' ? `${areaStr}㎡` : '',
                        priceStr !== '-' ? priceStr : '',
                        l['용도지역1'] || '',
                        l['지목'] || '',
                        l['도로'] || ''
                    ].filter(p => p && p.trim() !== '');
                    const summary = parts.join(', ');

                    if (data.infoRow) {
                        data.infoRow.innerText = summary;
                    }

                    // 실거래가 유형 자동 감지 및 버튼 활성화
                    let defaultType = 'land';
                    const bjdongNm = l['소재지'] || '';
                    const jimok = l['지목'] || '';
                    const useSitu = l['이용상황'] || '';

                    // 1. 지목 및 이용상황 기반 감지 (토지/공장/창고)
                    if (jimok.includes('장') || useSitu.includes('공장') || useSitu.includes('창고')) {
                        defaultType = 'factory';
                    } else if (useSitu.includes('상업') || useSitu.includes('업무') || useSitu.includes('주사') || useSitu.includes('점포')) {
                        defaultType = 'biz';
                    }

                    // 2. 건물 주용도 기반 감지 (건축물 대장 정보가 있는 경우)
                    if (resJson.data.buildings && resJson.data.buildings.length > 0) {
                        const mainUse = resJson.data.buildings[0]['주용도'] || '';
                        if (mainUse.includes('아파트')) defaultType = 'apt';
                        else if (mainUse.includes('오피스텔')) defaultType = 'offi';
                        else if (mainUse.includes('연립') || mainUse.includes('다세대')) defaultType = 'row';
                        else if (mainUse.includes('단독') || mainUse.includes('다가구')) defaultType = 'detached';
                        else if (mainUse.includes('공장') || mainUse.includes('창고') || mainUse.includes('자원순환') || mainUse.includes('위험물')) defaultType = 'factory';
                        else if (mainUse.includes('근린') || mainUse.includes('업무') || mainUse.includes('판매') || mainUse.includes('의료')) defaultType = 'biz';
                    }

                    data.defaultRealPriceType = defaultType;
                    // 법정동명 추출 (마지막 '동', '로', '가', '리', '면', '읍'으로 끝나는 단어들)
                    const addrParts = bjdongNm.split(' ').filter(v => v);
                    const lastImportantIdx = addrParts.findLastIndex(v =>
                        v.endsWith('동') || v.endsWith('로') || v.endsWith('가') ||
                        v.endsWith('리') || v.endsWith('면') || v.endsWith('읍')
                    );

                    data.bjdongNm = lastImportantIdx !== -1 ? addrParts[lastImportantIdx] : '';
                    // 주소 접두사 (시/구/동/면 등) 저장 - 지번 제외한 전체 경로 보존
                    data.fullAddrPrefix = lastImportantIdx !== -1 ? addrParts.slice(0, lastImportantIdx + 1).join(' ') : bjdongNm;

                    if (data.realBtn) {
                        data.realBtn.classList.remove('disabled');
                        data.realBtn.title = `최근 실거래가 보기 (감지된 유형: ${defaultType})`;
                    }

                    // Show building button only if buildings exist
                    if (resJson.data.buildings && resJson.data.buildings.length > 0) {
                        if (data.buildBtn) {
                            data.buildBtn.style.display = 'inline-flex';
                            data.buildBtn.classList.remove('disabled');
                        }
                    }
                }
            })
            .catch(err => console.error('Summary fetch error:', err));
    }

    try {

        const proxyUrl = `${window.GUNDAM_CONFIG.apiBase || ''}/proxy/parcel/?pnu=${pnu}`;

        const response = await fetch(proxyUrl);

        const data = await response.json();

        if (data.response?.status === 'OK') {

            const features = data.response.result?.featureCollection?.features;

            if (features?.length > 0) {

                drawPolygonsForIdx(features[0].geometry, itemIdx);

            }

        }

    } catch (e) { console.error(e); }

}

function drawPolygonsForIdx(geom, idx) {
    const data = polygonsData[idx];
    if (!data) return;

    const color = PALETTE[0]; // 기본 빨강

    const paths = geom.type === 'Polygon' ? [geom.coordinates[0]] : geom.coordinates.map(c => c[0]);

    paths.forEach(path => {

        const kPath = path.map(c => new kakao.maps.LatLng(c[1], c[0]));

        const gPath = path.map(c => ({ lat: c[1], lng: c[0] }));

        const kPoly = new kakao.maps.Polygon({ map: mapKakao, path: kPath, strokeWeight: 1.8, strokeColor: color, strokeOpacity: 0.9, fillColor: color, fillOpacity: 0.1 });

        const gPoly = new google.maps.Polygon({ map: mapGoogle, paths: gPath, strokeColor: color, strokeOpacity: 0.9, strokeWeight: 1.8, fillColor: color, fillOpacity: 0.1 });

        data.kakao.push(kPoly);

        data.google.push(gPoly);

    });

}

function updateColor(idx, color) {

    const data = polygonsData[idx];
    if (!data) return;

    data.badgeEl.style.background = color;

    data.kakao.forEach(p => {

        p.setOptions({ strokeColor: color, fillColor: color });

    });

    data.google.forEach(p => {

        p.setOptions({ strokeColor: color, fillColor: color });

    });

    data.markersK.forEach(m => {

        const inner = m.getContent().querySelector('.map-badge');

        if (inner) inner.style.background = color;

    });

    // Google simple marker label doesn't support background color change easily without custom icons

    // So we might just keep it or use a more complex overlay for Google if needed.

}

function logResult(msg, color = 'inherit', lat, lng) {

    const idx = resultCount++;

    const num = resultCount;

    const defaultColor = PALETTE[0];

    polygonsData[idx] = { kakao: [], google: [], markersK: [], markersG: [], badgeEl: null, landBtn: null, infoBtn: null, gongBtn: null, buildBtn: null, realBtn: null, pnu: null, infoRow: null, address: msg };

    const item = document.createElement('div');

    item.className = 'result-item';

    const contentWrapper = document.createElement('div');

    contentWrapper.className = 'result-content-wrapper';

    const addrRow = document.createElement('div');

    addrRow.className = 'result-addr-row';

    const badgeWrapper = document.createElement('div');

    badgeWrapper.className = 'badge-wrapper';

    const badge = document.createElement('div');

    badge.className = 'badge';

    badge.innerText = num;

    badge.onclick = (e) => {

        e.stopPropagation();

        // Close other pickers

        document.querySelectorAll('.color-picker').forEach(p => p !== picker && p.classList.remove('show'));

        // Toggle this picker

        const isShowing = picker.classList.contains('show');

        picker.classList.toggle('show');

        // Bring parent item to front when picker is shown

        if (!isShowing) {

            item.style.zIndex = "1050";

        } else {

            item.style.zIndex = "";

        }

    };

    polygonsData[idx].badgeEl = badge;

    const picker = document.createElement('div');

    picker.className = 'color-picker';

    PALETTE.forEach(c => {

        const dot = document.createElement('div');

        dot.className = 'color-dot';

        dot.style.background = c;

        dot.onclick = (e) => {

            e.stopPropagation();

            updateColor(idx, c);

            picker.classList.remove('show');

        };

        picker.appendChild(dot);

    });

    badgeWrapper.appendChild(badge);

    badgeWrapper.appendChild(picker);

    addrRow.appendChild(badgeWrapper);

    addrRow.appendChild(document.createTextNode(` ${msg}`));

    const actionRow = document.createElement('div');

    actionRow.className = 'result-action-row';

    const landBtn = document.createElement('a');

    landBtn.className = 'land-info-btn disabled';

    landBtn.innerText = '토';

    landBtn.target = '_blank';

    landBtn.title = '토지이용계획 (토지이음)';

    landBtn.onclick = (e) => e.stopPropagation();

    polygonsData[idx].landBtn = landBtn;

    actionRow.appendChild(landBtn);

    // Info Button ('정')

    const infoBtn = document.createElement('button');

    infoBtn.className = 'info-btn disabled';

    infoBtn.innerText = '정';

    infoBtn.title = '토지 정보 보기';

    infoBtn.onclick = (e) => {

        e.stopPropagation();

        if (!infoBtn.classList.contains('disabled')) {

            showLandInfo(idx);

        }

    };

    polygonsData[idx].infoBtn = infoBtn;
    polygonsData[idx].listItem = item;

    actionRow.appendChild(infoBtn);

    // Gong Button ('공')
    const gongBtn = document.createElement('button');
    gongBtn.className = 'gong-btn disabled';
    gongBtn.innerText = '공';
    gongBtn.title = '공시지가 보기';
    gongBtn.onclick = (e) => {
        e.stopPropagation();
        if (!gongBtn.classList.contains('disabled')) {
            showPriceTable(idx);
        }
    };
    polygonsData[idx].gongBtn = gongBtn;
    actionRow.appendChild(gongBtn);

    // Building Button ('건')
    const buildBtn = document.createElement('button');
    buildBtn.className = 'build-btn disabled';
    buildBtn.style.display = 'none';
    buildBtn.innerText = '건';
    buildBtn.title = '건축물 정보 보기';
    buildBtn.onclick = (e) => {
        e.stopPropagation();
        if (!buildBtn.classList.contains('disabled')) {
            showBuildingDetail(idx);
        }
    };
    polygonsData[idx].buildBtn = buildBtn;
    actionRow.appendChild(buildBtn);

    // Real Price Button ('실')
    const realBtn = document.createElement('button');
    realBtn.className = 'real-btn disabled';
    realBtn.innerText = '실';
    realBtn.title = '실거래가 정보 보기';
    realBtn.onclick = (e) => {
        e.stopPropagation();
        if (!realBtn.classList.contains('disabled')) {
            showRealPrice(idx, polygonsData[idx].defaultRealPriceType);
        }
    };
    polygonsData[idx].realBtn = realBtn;
    actionRow.appendChild(realBtn);

    // Roadview Button ('로드')
    const roadBtn = document.createElement('button');
    roadBtn.className = 'road-btn';
    roadBtn.innerText = '로';
    roadBtn.title = '로드뷰 보기';
    roadBtn.onclick = (e) => {
        e.stopPropagation();
        openRoadview(lat, lng);
    };
    polygonsData[idx].roadBtn = roadBtn;
    actionRow.appendChild(roadBtn);

    const infoRow = document.createElement('div');
    infoRow.className = 'result-info-row';
    infoRow.innerText = ''; // Initially empty
    polygonsData[idx].infoRow = infoRow;

    contentWrapper.appendChild(addrRow);
    contentWrapper.appendChild(infoRow);

    contentWrapper.appendChild(actionRow);

    item.appendChild(contentWrapper);

    item.onclick = () => {

        document.querySelectorAll('.result-item').forEach(i => i.classList.remove('selected'));

        item.classList.add('selected');

        if (lat && lng) displayMarkersOnly(lat, lng);

    };

    document.getElementById('result-list').appendChild(item);

    // Add Markers to Map

    if (lat && lng) {

        // Kakao Marker

        const kContent = document.createElement('div');

        kContent.innerHTML = `<div class="map-badge" style="background: ${defaultColor}; color: white; padding: 1px 5px; border-radius: 3px; font-size: 8pt; font-weight: bold; box-shadow: 0 1px 3px rgba(0,0,0,0.3); transform: translateY(-15px);">${num}</div>`;

        const kOverlay = new kakao.maps.CustomOverlay({

            position: new kakao.maps.LatLng(lat, lng),

            content: kContent,

            map: mapKakao

        });

        polygonsData[idx].markersK.push(kOverlay);

        // Google Marker

        const gMarker = new google.maps.Marker({

            position: { lat: parseFloat(lat), lng: parseFloat(lng) },

            map: mapGoogle,

            label: {

                text: num.toString(),

                color: 'white',

                fontSize: '8pt',

                fontWeight: 'bold'

            }

        });

        polygonsData[idx].markersG.push(gMarker);

    }

    return idx;

}

async function showLandInfo(idx) {
    const data = polygonsData[idx];
    if (!data) return;
    const pnu = data.pnu;
    const panel = document.getElementById('info-panel');
    const content = document.getElementById('info-content');

    panel.classList.add('visible');
    panel.classList.add('show');
    content.innerHTML = '<p style="text-align: center; color: #64748b;">정보를 불러오는 중...</p>';

    try {
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/landinfo/?pnu=${pnu}`);
        const resJson = await response.json();

        if (resJson.status === 'OK' && resJson.data) {
            const land = resJson.data.land;
            const blds = resJson.data.buildings || [];
            console.log('Fetched Land Info:', resJson.data);

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

            // 건축물 정보 테이블 (여러 동 표시)
            console.log(`Displaying ${blds.length} buildings:`, blds);

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
            html += '</tr></thead><tbody>';

            if (blds.length > 0) {
                blds.forEach(bld => {
                    html += '<tr>';
                    bldKeys.forEach(k => {
                        let val = bld[k] || '';
                        if (k === '사용승인일' && val && val.toString().length === 8) {
                            val = val.toString().substring(0, 4) + '-' + val.toString().substring(4, 6) + '-' + val.toString().substring(6, 8);
                        }
                        if (['연면적', '용적연면적', '건축면적', '대지', '높이', '건폐율', '용적률'].includes(k) && val) {
                            const num = val.toString().replace(/[^0-9.]/g, '');
                            if (num) val = Number(num).toLocaleString('ko-KR', { maximumFractionDigits: 2 });
                        }
                        html += `<td>${val}</td>`;
                    });
                    html += '</tr>';
                });
            } else {
                html += `<tr><td colspan="${bldKeys.length}" style="color: #64748b; padding: 20px;">건축물 정보가 없습니다.</td></tr>`;
            }
            html += '</tbody></table></div>';

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

function toggleInfoPanel(e) {
    const panel = document.getElementById('info-panel');
    const btn = e.currentTarget;

    // To "hide below", we MUST anchor to the current bottom edge.
    const rect = panel.getBoundingClientRect();
    const vh = window.innerHeight;

    // Calculate current bottom position from viewport bottom
    const currentBottom = vh - rect.bottom;

    // Set styles to anchor to bottom
    panel.style.top = 'auto';
    panel.style.bottom = currentBottom + 'px';

    // Re-apply horizontal position
    if (panel.style.left && panel.style.left !== 'auto' && panel.style.left !== '16px') {
        panel.style.transform = 'none';
    } else {
        panel.style.left = '16px';
        panel.style.transform = 'none';
    }

    // Apply transition and toggle
    panel.style.transition = 'max-height 0.3s ease, bottom 0.3s ease';
    panel.classList.toggle('show');
    btn.innerText = panel.classList.contains('show') ? '▼' : '▲';
}

function closeInfoPanel() {
    const panel = document.getElementById('info-panel');
    if (panel) {
        panel.classList.remove('visible');
        panel.classList.remove('show');
        // Reset toggle button icon if it exists
        const toggleBtn = panel.querySelector('.info-toggle-btn');
        if (toggleBtn) toggleBtn.innerText = '▲';
    }
}

async function showPriceTable(idx) {
    const data = polygonsData[idx];
    if (!data) return;
    const pnu = data.pnu;
    const panel = document.getElementById('price-panel');
    const content = document.getElementById('price-content');
    const toggleBtn = panel.querySelector('.price-panel-toggle');

    panel.style.display = 'block'; // Ensure block display
    panel.style.transition = 'right 0.3s ease, transform 0.3s ease';
    panel.classList.add('active');
    panel.classList.remove('minimized');
    if (toggleBtn) toggleBtn.innerText = '▶'; // Reset to "Hide" icon

    // Reset transform if it was minimized
    if (!panel.style.top || panel.style.top === 'auto') {
        panel.style.transform = '';
    } else {
        panel.style.transform = 'none';
    }

    content.innerHTML = '<p style="text-align: center; color: #64748b; font-size: 8pt;">불러오는 중...</p>';

    try {
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/landinfo/?pnu=${pnu}`);
        const resJson = await response.json();

        if (resJson.status === 'OK' && resJson.data && resJson.data.land) {
            const land = resJson.data.land;
            const years = ['2025', '2024', '2023', '2022'];

            let html = '<div class="price-grid">';

            // Column 1: Year
            html += '<div class="price-col"><div class="price-cell header">연도</div>';
            years.forEach(y => html += `<div class="price-cell">${y}</div>`);
            html += '</div>';

            // Column 2: M2
            html += '<div class="price-col"><div class="price-cell header">공시지가(㎡)</div>';
            years.forEach(y => html += `<div class="price-cell">${land[y] || '-'}</div>`);
            html += '</div>';

            // Column 3: Pyung
            html += '<div class="price-col"><div class="price-cell header">공시지가(평)</div>';
            years.forEach(y => {
                let pM2 = land[y] || '-';
                let pPyung = '-';
                if (pM2 !== '-') {
                    const val = parseInt(pM2.replace(/,/g, ''));
                    if (!isNaN(val)) pPyung = Math.round(val * 3.3058).toLocaleString();
                }
                html += `<div class="price-cell">${pPyung}</div>`;
            });
            html += '</div>';

            html += '</div>';
            content.innerHTML = html;
        } else {
            content.innerHTML = '<p style="text-align: center; color: #ef4444; font-size: 8pt;">데이터 없음</p>';
        }
    } catch (error) {
        console.error('Price search error:', error);
        content.innerHTML = '<p style="text-align: center; color: #ef4444; font-size: 8pt;">오류 발생</p>';
    }
}

function togglePricePanel(e) {
    const panel = document.getElementById('price-panel');
    const btn = e.currentTarget;
    panel.style.transition = 'right 0.3s ease, transform 0.3s ease';
    const isMinimized = panel.classList.toggle('minimized');
    btn.innerText = isMinimized ? '◀' : '▶';

    if (panel.style.top && panel.style.top !== 'auto') {
        // Dragged state: add/remove translateX while keeping top
        panel.style.transform = isMinimized ? 'translateX(220px)' : 'none';
    } else {
        // Default state: handle transition via CSS class toggle
        if (!isMinimized) panel.style.transform = '';
    }
}

function closePricePanel() {
    const panel = document.getElementById('price-panel');
    if (!panel) return;
    panel.style.transition = 'right 0.3s ease, transform 0.3s ease';
    panel.classList.remove('active');
    panel.classList.remove('minimized');
    const toggleBtn = panel.querySelector('.price-panel-toggle');
    if (toggleBtn) toggleBtn.innerText = '▶';
    // Completely hide after transition
    setTimeout(() => {
        if (!panel.classList.contains('active')) {
            panel.style.display = 'none';
        }
    }, 300);
}

// Unused functions removed to avoid confusion

async function showBuildingDetail(idx) {
    const data = polygonsData[idx];
    if (!data) return;
    const pnu = data.pnu;
    const panel = document.getElementById('building-panel');
    const content = document.getElementById('building-detail-content');

    panel.style.display = 'block';
    panel.classList.remove('minimized');
    content.innerHTML = '<p style="text-align: center; color: #64748b; font-size: 8pt; padding: 20px;">정보를 불러오는 중...</p>';

    try {
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/building-detail/?pnu=${pnu}`);
        const resData = await response.json();

        if (resData.status === 'OK' && resData.data) {
            const recap = resData.data.recap || {};
            const titles = resData.data.titles || [];

            // Update Panel Title
            const titleText = panel.querySelector('.bld-panel-title-text');
            if (titleText) {
                titleText.innerText = "건축물대장 총괄표제부";
            }

            if (Object.keys(recap).length === 0 && titles.length === 0) {
                content.innerHTML = '<p style="text-align: center; color: #ef4444; font-size: 8pt; padding: 20px;">건축물 정보가 없습니다.</p>';
                return;
            }

            let html = '<table class="bld-table">';

            // Helper for rows
            const row = (l1, k1, l2, k2) => {
                return `<tr>
                            <th>${l1}</th><td>${recap[k1] || '-'}</td>
                            <th>${l2}</th><td>${recap[k2] || '-'}</td>
                        </tr>`;
            };

            // Row 1: 대지위치
            html += `<tr><th>대지위치</th><td colspan="3">${recap['대지위치'] || '-'}</td></tr>`;
            // Row 2: 도로명주소
            html += `<tr><th>도로명주소</th><td colspan="3">${recap['도로명주소'] || '-'}</td></tr>`;
            // Row 3: 건물명
            html += `<tr><th>건물명</th><td colspan="3">${recap['건물명'] || '-'}</td></tr>`;
            // Row 4: 관련지번
            html += `<tr><th>관련지번</th><td colspan="3">${recap['관련지번'] || '-'}</td></tr>`;

            html += row('대지면적(㎡)', '대지면적', '연면적(㎡)', '연면적');
            html += row('건축면적(㎡)', '건축면적', '용적면적(㎡)', '용적면적');
            html += row('건폐율(%)', '건폐율', '용적률(%)', '용적률');
            html += row('주건물수', '주건물수', '부속건물수', '부속건물수');
            html += row('호/가구/세대', '호가구세대', '주용도', '주용도');
            html += row('자주식주차', '자주식주차', '기계식주차', '기계식주차');
            html += row('허가일', '허가일', '사용승인일', '사용승인일');

            html += '</table>';

            // Building Titles List
            if (titles.length > 0) { // Always show header if we have data structure
                html += '<div class="bld-sub-header" style="margin-top: 10px; margin-bottom: 5px; font-weight: bold; color: #2563eb; text-align:center;">건축물현황</div>';
                html += '<table class="bld-list-table" style="width:100%; border-collapse: collapse; font-size: 7.5pt;"><thead><tr style="background: #f1f5f9; color: #475569;">';
                ['구분', '명칭', '구조/지붕', '층수', '용도', '면적(㎡)'].forEach(h => html += `<th style="padding: 4px; border: 1px solid #e2e8f0;">${h}</th>`);
                html += '</tr></thead><tbody>';

                titles.forEach(t => {
                    const dongName = t['명칭'] || '-';
                    const dongPK = t['PK'] || '';
                    const isClickable = dongName !== '-' && dongName !== '총괄표제부';

                    // 행 자체에 클릭 이벤트 추가 및 클래스 적용
                    const trAttr = isClickable
                        ? `class="bld-row-clickable" onclick="showFloorInfo('${pnu}', '${dongName}', '${dongPK}')"`
                        : '';

                    html += `<tr ${trAttr}>
                                <td style="text-align:center; padding: 4px; border: 1px solid #e2e8f0;">${t['구분']}</td>
                                <td style="text-align:center; padding: 4px; border: 1px solid #e2e8f0;">${dongName}</td>
                                <td style="text-align:center; padding: 4px; border: 1px solid #e2e8f0;">${t['구조']} ${t['지붕']}</td>
                                <td style="text-align:center; padding: 4px; border: 1px solid #e2e8f0;">${t['층수']}</td>
                                <td style="text-align:center; padding: 4px; border: 1px solid #e2e8f0;">${t['용도']}</td>
                                <td style="text-align:right; padding: 4px; border: 1px solid #e2e8f0;">${t['면적'] ? Number(t['면적']).toLocaleString() : '-'}</td>
                             </tr>`;
                });
                html += '</tbody></table>';
            }

            content.innerHTML = html;
        } else {
            content.innerHTML = `<p style="text-align: center; color: #ef4444; font-size: 8pt; padding: 20px;">데이터 없음: ${resData.message || ''}</p>`;
        }
    } catch (error) {
        console.error('Building search error:', error);
        content.innerHTML = '<p style="text-align: center; color: #ef4444; font-size: 8pt; padding: 20px;">오류 발생</p>';
    }
}

function toggleBuildingPanel(e) {
    const panel = document.getElementById('building-panel');
    const btn = e.currentTarget;

    // To "fold up", anchor to current top edge
    const rect = panel.getBoundingClientRect();
    panel.style.top = rect.top + "px";
    panel.style.bottom = "auto";

    panel.style.transition = 'max-height 0.3s ease, top 0.3s ease';
    panel.classList.toggle('minimized');
    btn.innerText = panel.classList.contains('minimized') ? '▼' : '▲';
}

function closeBuildingPanel() {
    const panel = document.getElementById('building-panel');
    panel.style.display = 'none';
    panel.classList.remove('minimized');
    // Reset position if needed, or keep it where it was dragged
}

// 층별 정보 표시 함수
async function showFloorInfo(pnu, dongNm, pk) {
    const panel = document.getElementById('floor-panel');
    const content = document.getElementById('floor-content');
    const titleText = panel.querySelector('.floor-panel-title-text');

    panel.style.display = 'block';
    panel.classList.remove('minimized');
    content.innerHTML = '<p style="text-align: center; color: #64748b; font-size: 8pt; padding: 20px;">정보를 불러오는 중...</p>';

    // 패널 제목 업데이트
    if (titleText) {
        titleText.innerText = `층별 정보 - ${dongNm}`;
    }

    try {
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/floor-info/?pnu=${pnu}&dongNm=${encodeURIComponent(dongNm)}&pk=${pk}`);
        const resData = await response.json();

        if (resData.status === 'OK' && resData.data && resData.data.floors) {
            const floors = resData.data.floors;

            if (floors.length === 0) {
                content.innerHTML = '<p style="text-align: center; color: #ef4444; font-size: 8pt; padding: 20px;">층별 정보가 없습니다.</p>';
                return;
            }

            let html = '<table class="floor-table">';
            html += '<thead><tr>';
            ['구분', '층별', '구조', '용도', '면적(㎡)'].forEach(h => html += `<th>${h}</th>`);
            html += '</tr></thead><tbody>';

            floors.forEach(f => {
                const area = f['면적'] ? Number(f['면적']).toLocaleString('ko-KR', { maximumFractionDigits: 2 }) : '-';
                html += `<tr>
                            <td>${f['구분']}</td>
                            <td>${f['층별']}</td>
                            <td>${f['구조']}</td>
                            <td>${f['용도']}</td>
                            <td>${area}</td>
                        </tr>`;
            });

            html += '</tbody></table>';
            content.innerHTML = html;
        } else {
            content.innerHTML = `<p style="text-align: center; color: #ef4444; font-size: 8pt; padding: 20px;">데이터 없음: ${resData.message || ''}</p>`;
        }
    } catch (error) {
        console.error('Floor info fetch error:', error);
        content.innerHTML = '<p style="text-align: center; color: #ef4444; font-size: 8pt; padding: 20px;">오류 발생</p>';
    }
}

function toggleFloorPanel(e) {
    const panel = document.getElementById('floor-panel');
    const btn = e.currentTarget;

    // To "fold up", anchor to current top edge
    const rect = panel.getBoundingClientRect();
    panel.style.top = rect.top + "px";
    panel.style.bottom = "auto";

    panel.style.transition = 'max-height 0.3s ease, top 0.3s ease';
    panel.classList.toggle('minimized');
    btn.innerText = panel.classList.contains('minimized') ? '▼' : '▲';
}

function closeFloorPanel() {
    const panel = document.getElementById('floor-panel');
    panel.style.display = 'none';
    panel.classList.remove('minimized');
}

async function showRealPrice(idx, type) {
    const data = polygonsData[idx];
    if (!data) return;
    const pnu = data.pnu;
    if (!pnu) return;

    const sigunguCd = pnu.substring(0, 5);
    const bjdongCd = pnu.substring(5, 10);
    const bjdongNm = data.bjdongNm || '';

    const panel = document.getElementById('realprice-panel');
    const content = document.getElementById('realprice-content');

    panel.style.display = 'block';
    panel.classList.remove('minimized');
    const toggleBtn = panel.querySelector('.realprice-toggle');
    if (toggleBtn) toggleBtn.innerText = '▶';

    // Reset transform if it was minimized
    if (!panel.style.top || panel.style.top === 'auto') {
        panel.style.transform = '';
    } else {
        // If dragged, we might want to keep the position but remove any slide-out translation
        panel.style.transform = 'none';
    }

    content.innerHTML = '<p style="text-align: center; padding: 20px; color: #64748b;">데이터를 불러오는 중...</p>';

    // Base address for geocoding
    // 1. Try address from land info (fullAddrPrefix)
    // 2. Try address from search result (address)
    let addrPrefix = data.fullAddrPrefix || '';
    if (!addrPrefix && data.address) {
        addrPrefix = data.address.split(' ').slice(0, -1).join(' ');
    }

    // 탭 활성화
    document.querySelectorAll('.realprice-tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.type === type);
        tab.onclick = () => showRealPrice(idx, tab.dataset.type);
    });

    try {
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/real-price/?sigunguCd=${sigunguCd}&bjdongCd=${bjdongCd}&bjdongNm=${encodeURIComponent(bjdongNm)}&type=${type}`);
        const resJson = await response.json();

        if (resJson.status === 'OK') {
            if (resJson.data.length === 0) {
                content.innerHTML = '<p style="text-align: center; padding: 20px; color: #64748b;">최근 2년 내 실거래가 데이터가 없습니다.</p>';
                return;
            }

            let html = '<table class="realprice-table"><thead><tr>';
            const items = resJson.data;

            const toPyung = (m2) => {
                if (!m2 || m2 === '-') return '-';
                const val = parseFloat(m2.toString().replace(/,/g, ''));
                if (isNaN(val)) return '-';
                return Math.round(val * 0.3025).toLocaleString();
            };

            if (type === 'factory') {
                html += '<th style="width:55px;">계약일</th><th style="min-width:45px;">지번</th><th style="width:50px;">유형</th><th style="min-width:60px;">용도</th><th style="width:25px;">층</th><th style="width:40px;">건축</th><th style="width:65px;">금액(만)</th><th style="width:45px;">대지(평)</th><th style="width:45px;">건물(평)</th><th style="width:70px;">토지(건물)<br>평단가(만)</th>';
            } else if (type === 'biz') {
                html += '<th style="width:55px;">계약일</th><th style="min-width:70px;">지번</th><th style="width:25px;">층</th><th style="min-width:70px;">용도</th><th style="width:40px;">건축</th><th style="width:65px;">금액(만)</th><th style="width:45px;">대지(평)</th><th style="width:45px;">건물(평)</th><th style="width:70px;">건물평단가<br>(만)</th>';
            } else if (type === 'land') {
                html += '<th style="width:55px;">계약일</th><th style="min-width:80px;">지번</th><th style="width:35px;">지목</th><th style="min-width:80px;">용도</th><th style="width:65px;">금액(만)</th><th style="width:45px;">면적(평)</th><th style="width:70px;">토지평단가<br>(만)</th>';
            } else if (type === 'apt' || type === 'offi') {
                html += '<th style="width:55px;">계약일</th><th style="min-width:90px;">명칭</th><th style="width:50px;">지번</th><th style="width:25px;">층</th><th style="width:40px;">건축</th><th style="width:65px;">금액(만)</th><th style="width:50px;">전용면적<br>(평)</th><th style="width:70px;">전용평단가<br>(만)</th>';
            } else if (type === 'row') {
                html += '<th style="width:55px;">계약일</th><th style="min-width:80px;">명칭</th><th style="width:50px;">지번</th><th style="width:25px;">층</th><th style="width:40px;">건축</th><th style="width:65px;">금액(만)</th><th style="width:50px;">대지권(평)</th><th style="width:50px;">전용(평)</th><th style="width:70px;">전용평단가<br>(만)</th>';
            } else if (type === 'detached') {
                html += '<th style="width:55px;">계약일</th><th style="min-width:70px;">지번</th><th style="width:40px;">유형</th><th style="width:40px;">건축</th><th style="width:65px;">금액(만)</th><th style="width:45px;">대지(평)</th><th style="width:45px;">연면적(평)</th><th style="width:70px;">토지평단가<br>(만)</th>';
            }
            html += '</tr></thead><tbody>';

            items.forEach(item => {
                html += '<tr>';
                const dateStr = `${item.dealYear}.${item.dealMonth}.${item.dealDay}`;
                html += `<td>${dateStr}</td>`;

                const jibunVal = item.jibun || '-';
                // Robust address construction: 
                // If addrPrefix already ends with dong name, don't duplicate umdNm if it's the same
                let searchAddr = addrPrefix;
                const umd = (item.umdNm || '').trim();
                if (umd && !addrPrefix.includes(umd)) {
                    searchAddr += ' ' + umd;
                }
                searchAddr += ' ' + jibunVal;
                searchAddr = searchAddr.replace(/'/g, "\\'").trim();
                const jibunTd = `<td class="clickable-jibun" onclick="moveMapToAddr('${searchAddr}')">${jibunVal}</td>`;

                if (type === 'factory') {
                    const amount = parseFloat(item.dealAmount.toString().replace(/,/g, ''));
                    let unitPrice = '-';
                    if (item.buildingType === '일반') {
                        const pAr = parseFloat(item.plottageAr || 0);
                        const pyung = pAr * 0.3025;
                        if (pyung > 0 && !isNaN(amount)) unitPrice = Math.round(amount / pyung).toLocaleString();
                    } else if (item.buildingType === '집합') {
                        const bAr = parseFloat(item.buildingAr || 0);
                        const pyung = bAr * 0.3025;
                        if (pyung > 0 && !isNaN(amount)) unitPrice = Math.round(amount / pyung).toLocaleString();
                    }
                    html += `${jibunTd}<td>${item.buildingType || '-'}</td><td>${item.buildingUse || '-'}</td><td>${item.floor || '-'}</td><td>${item.buildYear || '-'}</td><td>${item.dealAmount}</td><td>${toPyung(item.plottageAr)}</td><td>${toPyung(item.buildingAr)}</td><td>${unitPrice}</td>`;
                } else if (type === 'biz') {
                    const bAr = parseFloat(item.buildingAr || 0);
                    const pyung = bAr * 0.3025;
                    const amount = parseFloat(item.dealAmount.toString().replace(/,/g, ''));
                    let unitPrice = '-';
                    if (pyung > 0 && !isNaN(amount)) {
                        unitPrice = Math.round(amount / pyung).toLocaleString();
                    }
                    html += `${jibunTd}<td>${item.floor || '-'}</td><td>${item.buildingUse || '-'}</td><td>${item.buildYear || '-'}</td><td>${item.dealAmount}</td><td>${toPyung(item.plottageAr)}</td><td>${toPyung(item.buildingAr)}</td><td>${unitPrice}</td>`;
                }
                else if (type === 'land') {
                    const lAr = parseFloat(item.area || 0);
                    const pyung = lAr * 0.3025;
                    const amount = parseFloat(item.dealAmount.toString().replace(/,/g, ''));
                    let unitPrice = '-';
                    if (pyung > 0 && !isNaN(amount)) {
                        unitPrice = Math.round(amount / pyung).toLocaleString();
                    }
                    html += `${jibunTd}<td>${item.lndcgrNm || '-'}</td><td>${item.landUse || '-'}</td><td>${item.dealAmount}</td><td>${toPyung(item.area)}</td><td>${unitPrice}</td>`;
                }
                else if (type === 'apt') {
                    const eAr = parseFloat(item.area || 0);
                    const pyung = eAr * 0.3025;
                    const amount = parseFloat(item.dealAmount.toString().replace(/,/g, ''));
                    let unitPrice = '-';
                    if (pyung > 0 && !isNaN(amount)) {
                        unitPrice = Math.round(amount / pyung).toLocaleString();
                    }
                    html += `<td>${item.name || '-'}</td>${jibunTd}<td>${item.floor || '-'}</td><td>${item.buildYear || '-'}</td><td>${item.dealAmount}</td><td>${toPyung(item.area)}</td><td>${unitPrice}</td>`;
                } else if (type === 'offi') {
                    const eAr = parseFloat(item.area || 0);
                    const pyung = eAr * 0.3025;
                    const amount = parseFloat(item.dealAmount.toString().replace(/,/g, ''));
                    let unitPrice = '-';
                    if (pyung > 0 && !isNaN(amount)) {
                        unitPrice = Math.round(amount / pyung).toLocaleString();
                    }
                    html += `<td>${item.name || '-'}</td>${jibunTd}<td>${item.floor || '-'}</td><td>${item.buildYear || '-'}</td><td>${item.dealAmount}</td><td>${toPyung(item.area)}</td><td>${unitPrice}</td>`;
                }
                else if (type === 'row') {
                    const eAr = parseFloat(item.excluUseAr || 0);
                    const pyung = eAr * 0.3025;
                    const amount = parseFloat(item.dealAmount.toString().replace(/,/g, ''));
                    let unitPrice = '-';
                    if (pyung > 0 && !isNaN(amount)) {
                        unitPrice = Math.round(amount / pyung).toLocaleString();
                    }
                    html += `<td>${item.name || '-'}</td>${jibunTd}<td>${item.floor || '-'}</td><td>${item.buildYear || '-'}</td><td>${item.dealAmount}</td><td>${toPyung(item.landAr)}</td><td>${toPyung(item.excluUseAr)}</td><td>${unitPrice}</td>`;
                }
                else if (type === 'detached') {
                    const pAr = parseFloat(item.plottageAr || 0);
                    const pyung = pAr * 0.3025;
                    const amount = parseFloat(item.dealAmount.toString().replace(/,/g, ''));
                    let unitPrice = '-';
                    if (pyung > 0 && !isNaN(amount)) {
                        unitPrice = Math.round(amount / pyung).toLocaleString();
                    }
                    html += `${jibunTd}<td>${item.houseType || '-'}</td><td>${item.buildYear || '-'}</td><td>${item.dealAmount}</td><td>${toPyung(item.plottageAr)}</td><td>${toPyung(item.totalFloorAr)}</td><td>${unitPrice}</td>`;
                }
                html += '</tr>';
            });
            html += '</tbody></table>';
            content.innerHTML = html;
        } else {
            content.innerHTML = `<p style="text-align: center; padding: 20px; color: #ef4444;">오류: ${resJson.message}</p>`;
        }
    } catch (error) {
        console.error('RealPrice fetch error:', error);
        content.innerHTML = '<p style="text-align: center; padding: 20px; color: #ef4444;">정보를 불러오는 중 오류가 발생하였습니다.</p>';
    }
}

function closeRealPricePanel() {
    const panel = document.getElementById('realprice-panel');
    panel.style.display = 'none';
    panel.classList.remove('minimized');
    const toggleBtn = panel.querySelector('.realprice-toggle');
    if (toggleBtn) toggleBtn.innerText = '▶';
}

function toggleRealPricePanel(e) {
    const panel = document.getElementById('realprice-panel');
    const btn = e.currentTarget;
    panel.style.transition = 'right 0.3s ease, transform 0.3s ease';
    const isMinimized = panel.classList.toggle('minimized');
    btn.innerText = isMinimized ? '◀' : '▶';

    if (panel.style.top && panel.style.top !== 'auto') {
        // Dragged state: add/remove translateX while keeping top/left
        panel.style.transform = isMinimized ? 'translateX(485px)' : 'none';
    } else {
        // Default state: handle transition via CSS class toggle
        // but if we are not in default transform, we might need manual reset
        if (!isMinimized) panel.style.transform = '';
    }
}

// ---------------------------------------------------------
// Roadview Logic
// ---------------------------------------------------------
function toggleRoadviewTool() {
    isRoadviewToolActive = !isRoadviewToolActive;
    const btn = document.getElementById('btn-roadview-tool');
    btn.classList.toggle('active', isRoadviewToolActive);

    const mapContainer = document.getElementById('map-kakao');
    if (isRoadviewToolActive) {
        mapContainer.classList.add('roadview-tool-cursor');
        // Reset other tools if active
        if (currentMeasureTool) toggleMeasure(currentMeasureTool);
    } else {
        mapContainer.classList.remove('roadview-tool-cursor');
    }
}

function openRoadview(lat, lng) {
    if (!lat || !lng) return;

    const container = document.getElementById('roadview-container');
    const rvMain = document.getElementById('roadview-main');
    const rvMini = document.getElementById('roadview-minimap');

    container.style.display = 'block';

    if (!roadview) {
        roadviewClient = new kakao.maps.RoadviewClient();
        roadview = new kakao.maps.Roadview(rvMain);

        // Initialize Minimap
        rvMinimap = new kakao.maps.Map(rvMini, {
            center: new kakao.maps.LatLng(lat, lng),
            level: 3,
            mapTypeId: kakao.maps.MapTypeId.HYBRID
        });

        // Custom POV Marker: Yellow cone + Blue dot
        const povContainer = document.createElement('div');
        povContainer.style.cssText = 'position: relative; width: 100px; height: 100px;';

        // 1. The Cone (SVG for precise sector)
        const coneDiv = document.createElement('div');
        coneDiv.id = 'rv-pov-cone';
        coneDiv.style.cssText = `
                    position: absolute; top:0; left:0; width:100%; height:100%;
                    background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M50 50 L10 0 A60 60 0 0 1 90 0 Z" fill="rgba(255,230,0,0.6)" stroke="white" stroke-width="1"/></svg>') no-repeat center;
                    background-size: contain;
                    transform-origin: 50% 50%;
                    z-index: 1;
                `;

        // 2. The Blue Dot
        const dotDiv = document.createElement('div');
        dotDiv.style.cssText = `
                    position: absolute; top: 50%; left: 50%; width: 16px; height: 16px;
                    background: #2563eb; border: 3px solid white; border-radius: 50%;
                    margin-top: -8px; margin-left: -8px; box-shadow: 0 0 4px rgba(0,0,0,0.5);
                    z-index: 2;
                `;

        povContainer.appendChild(coneDiv);
        povContainer.appendChild(dotDiv);

        rvMarker = new kakao.maps.CustomOverlay({
            position: new kakao.maps.LatLng(lat, lng),
            content: povContainer,
            map: rvMinimap,
            xAnchor: 0.5,
            yAnchor: 0.5
        });

        // Synchronize Roadview -> Minimap
        kakao.maps.event.addListener(roadview, 'position_changed', function () {
            const pos = roadview.getPosition();
            rvMinimap.setCenter(pos);
            rvMarker.setPosition(pos);
        });

        kakao.maps.event.addListener(roadview, 'viewpoint_changed', function () {
            const viewpoint = roadview.getViewpoint();
            const coneElement = document.getElementById('rv-pov-cone');
            if (coneElement) {
                // Kakao pan is in degrees. Adjust rotation as needed
                coneElement.style.transform = `rotate(${viewpoint.pan}deg)`;
            }
        });

        // Synchronize Minimap -> Roadview
        kakao.maps.event.addListener(rvMinimap, 'click', function (mouseEvent) {
            const position = mouseEvent.latLng;
            roadviewClient.getNearestPanoId(position, 50, function (panoId) {
                if (panoId) {
                    roadview.setPanoId(panoId, position);
                }
            });
        });

        // Standard map controls for minimap
        rvMinimap.addControl(new kakao.maps.ZoomControl(), kakao.maps.ControlPosition.RIGHT);
    }

    // Find nearest Roadview for given coords
    const position = new kakao.maps.LatLng(lat, lng);
    roadviewClient.getNearestPanoId(position, 50, function (panoId) {
        if (panoId) {
            roadview.setPanoId(panoId, position);
            rvMinimap.setCenter(position);
            rvMarker.setPosition(position);
        } else {
            alert('이 위치 근처에는 로드뷰 정보가 없습니다.');
            closeRoadview();
        }
    });
}

function toggleRvMinimapSize() {
    const map = document.getElementById('roadview-minimap');
    map.classList.toggle('large');
    setTimeout(() => { if (rvMinimap) rvMinimap.relayout(); }, 350);
}

function toggleRvMinimapVisibility() {
    const map = document.getElementById('roadview-minimap');
    const btn = document.getElementById('rv-hide-btn');
    const isHidden = map.classList.toggle('hidden-map');

    btn.innerText = isHidden ? '↗' : '↙';

    setTimeout(() => { if (rvMinimap) rvMinimap.relayout(); }, 350);
}

function closeRoadview() {
    document.getElementById('roadview-container').style.display = 'none';
}

function clearPolygons() {

    polygonsData.forEach(data => {

        if (!data) return;

        data.kakao.forEach(p => p.setMap(null));

        data.google.forEach(p => p.setMap(null));

        data.markersK.forEach(m => m.setMap(null));

        data.markersG.forEach(m => m.setMap(null));

    });

    polygonsData = [];

    closeInfoPanel();
    closePricePanel();
    closeBuildingPanel();
    closeFloorPanel();
    closeRealPricePanel();
    closeWarehousePanel();
}

// 페이지 로드 시 드래그 기능 활성화
document.addEventListener('DOMContentLoaded', function () {
    const buildingPanel = document.getElementById('building-panel');
    const buildingHeader = document.getElementById('building-panel-header');
    const floorPanel = document.getElementById('floor-panel');
    const floorHeader = document.getElementById('floor-panel-header');

});



// ---------------------------------------------------------
// Warehouse Logic
// ---------------------------------------------------------
async function checkNearbyWarehouses(lat, lng, sigunNm, itemIdx) {
    try {
        // Fetch more warehouses to ensure we don't miss any nearby ones
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/warehouse/?sigun=${encodeURIComponent(sigunNm)}&pSize=3000`);
        const data = await response.json();
        const nearbyWarehouses = [];

        if (data.LogisticsWarehouse && data.LogisticsWarehouse[1] && data.LogisticsWarehouse[1].row) {
            const rows = data.LogisticsWarehouse[1].row;
            const limitDeg = 0.10; // ~11km radius - greatly expanded

            rows.forEach(w => {
                try {
                    if (w.REFINE_WGS84_LAT && w.REFINE_WGS84_LOGT) {
                        const wLat = parseFloat(w.REFINE_WGS84_LAT);
                        const wLng = parseFloat(w.REFINE_WGS84_LOGT);

                        if (!isNaN(wLat) && !isNaN(wLng)) {
                            // Also check if non-zero
                            if (Math.abs(wLat) > 1 && Math.abs(wLng) > 1) {
                                if (Math.abs(lat - wLat) < limitDeg && Math.abs(lng - wLng) < limitDeg) {
                                    w.distance = Math.sqrt(Math.pow(lat - wLat, 2) + Math.pow(lng - wLng, 2));
                                    nearbyWarehouses.push(w);
                                }
                            }
                        }
                    }
                } catch (err) {
                    // ignore bad row
                }
            });
        }

        if (nearbyWarehouses.length > 0) {
            nearbyWarehouses.sort((a, b) => a.distance - b.distance);
            const data = polygonsData[itemIdx];
            if (data && data.listItem) {
                data.warehouses = nearbyWarehouses;

                // Check if button already exists to prevent dupes
                if (data.listItem.querySelector('.warehouse-btn')) return;

                const btn = document.createElement('button');
                btn.className = 'warehouse-btn';
                btn.innerText = '창';
                btn.title = `인근 물류창고 ${nearbyWarehouses.length}개 발견`;
                btn.style.cssText = `
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            width: 15px;
                            height: 15px;
                            background: #8b5cf6;
                            color: white !important;
                            border-radius: 3px;
                            font-size: 7pt;
                            font-weight: bold;
                            border: none;
                            margin-top: 4px;
                            cursor: pointer;
                            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                        `;
                btn.onclick = (e) => {
                    e.stopPropagation();
                    showWarehouseOnMap(nearbyWarehouses);
                };
                const actionRow = data.listItem.querySelector('.result-action-row');
                if (actionRow) actionRow.appendChild(btn);
            }
        }
    } catch (e) {
        console.error("Warehouse check error:", e);
    }
}


function updateWarehousePanel(w, totalCount) {
    const panel = document.getElementById('warehouse-panel');
    const content = document.getElementById('warehouse-content');
    if (!panel || !content) return;

    // Unhide if needed
    panel.style.display = 'block';
    panel.classList.remove('minimized');
    if (!panel.getAttribute('data-dragged')) {
        panel.style.left = '50%';
        panel.style.transform = 'translateX(-50%)';
        panel.style.top = 'auto';
        panel.style.bottom = '30px';
    }

    const titleEl = panel.querySelector('.warehouse-panel-title');
    if (titleEl) titleEl.innerText = `📦 물류창고: ${w.BIZPLC_NM}`;

    let html = '<div class="info-table-container" style="border:none;"><table class="info-table" style="font-size: 8pt; width:100%; border-collapse: collapse;"><tbody>';

    const addRow = (label, val) => {
        html += `<tr><th style="width:100px; padding: 6px 8px; background:#f8fafc; color:#64748b; border: 1px solid #e2e8f0; font-weight:600;">${label}</th><td style="text-align:left; padding: 6px 8px; border: 1px solid #e2e8f0;">${val || '-'}</td></tr>`;
    };
    const toPy = (val) => {
        const num = parseFloat(val);
        if (isNaN(num)) return val || '-';
        return `${Math.round(num * 0.3025).toLocaleString()}평`;
    };

    addRow('사업장명', w.BIZPLC_NM);
    addRow('인허가일자', w.LICENSG_DE);
    addRow('영업상태', w.BSN_STATE_NM);
    addRow('주소', w.REFINE_LOTNO_ADDR || w.REFINE_ROADNM_ADDR);

    const genCnt = w.GENRL_WAREHS_BUILDG_CNT || '0';
    const genAr = toPy(w.GENRL_WAREHS_AR_INFO);
    addRow('일반창고', `${genCnt}동 (${genAr})`);

    const coldCnt = w.COLDSTRG_WAREHS_BUILDG_CNT || '0';
    const coldAr = toPy(w.COLDSTRG_WAREHS_AR);
    addRow('냉동냉장창고', `${coldCnt}동 (${coldAr})`);

    addRow('시설장비 현황', w.FACLT_EQUP_STUS);

    addRow('보관요율', w.CUSTODY_TARIFF_RT || '-');

    let bizNm = w.BIZCOND_CUSTODY_ND_WAREHS_NM;
    if (bizNm === '1' || bizNm === 'null') bizNm = '-';
    addRow('업태명', bizNm || '-');

    html += '</tbody></table></div>';

    if (totalCount && totalCount > 1) {
        html += `<div style="padding:8px; font-size:7.5pt; color:#64748b; background:#f8fafc; border-top:1px solid #e2e8f0; text-align:center;">
                         외 인근 ${totalCount - 1}개 창고 표시됨
                    </div>`;
    }
    content.innerHTML = html;
}

// ---------------------------------------------------------
// Hospital Logic (HIRA API - Radius Search)
// ---------------------------------------------------------
async function showHospitalsOnMap(lat, lng) {
    // Remove existing hospital overlays
    hospitalOverlays.forEach(o => o.setMap(null));
    hospitalOverlays = [];

    try {
        // HIRA V2 Radius Search Proxy Call
        // Use larger radius (10000m = 10km) to ensure coverage
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/hospital/list/?x=${lng}&y=${lat}&radius=10000`);
        const resData = await response.json();

        if (resData.status === 'OK' && resData.items) {
            const hospitals = resData.items;
            if (hospitals.length === 0) {
                alert('인근 병원 정보가 없습니다.');
                return;
            }

            hospitals.forEach(h => {
                // Create Custom Overlay for Hospital
                const content = document.createElement('div');
                content.style.cssText = `
                            padding: 6px 10px; background: white; border-radius: 20px;
                            border: 2px solid #059669; color: #059669; font-weight: bold; font-size: 11px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.2); cursor: pointer; display: flex; align-items: center; gap: 4px;
                            white-space: nowrap; transition: transform 0.2s;
                        `;
                content.innerHTML = `<span style="font-size:12px;">🏥</span> ${h.yadmNm}`;

                // Hover effect
                content.onmouseenter = () => {
                    content.style.zIndex = '9999';
                    content.style.transform = 'scale(1.1)';
                };
                content.onmouseleave = () => {
                    content.style.zIndex = '1';
                    content.style.transform = 'scale(1.0)';
                };

                content.onclick = () => {
                    showHospitalDetail(h.yadmNm, h.addr, h.telno, h.clCdNm, h.hospUrl, h.estbDd, h.drTotCnt);
                };

                const pos = new kakao.maps.LatLng(h.lat, h.lng);
                const overlay = new kakao.maps.CustomOverlay({
                    map: map,
                    position: pos,
                    content: content,
                    yAnchor: 1.4 // Slightly above the point
                });

                hospitalOverlays.push(overlay);
            });

            // Show notification
            const notification = document.createElement('div');
            notification.innerHTML = `<span style="color:#059669; font-weight:bold;">${hospitals.length}</span>개의 병원이 표시되었습니다.`;
            notification.style.cssText = `
                        position: fixed; bottom: 80px; left: 50%; transform: translateX(-50%);
                        background: rgba(0, 0, 0, 0.7); color: white; padding: 8px 16px;
                        border-radius: 20px; font-size: 12px; z-index: 9999;
                        animation: fadeOut 3s forwards; pointer-events: none;
                    `;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 3000);

        } else {
            alert('병원 정보를 불러오는데 실패했습니다.');
        }

    } catch (e) {
        console.error("Hospital API Error:", e);
        alert('병원 정보를 불러오는 중 오류가 발생했습니다.');
    }
}

async function showWarehouseOnMap(warehouses) {
    if (!warehouses || warehouses.length === 0) return;

    if (window.warehouseMarkers) {
        window.warehouseMarkers.forEach(m => m.setMap(null));
        window.warehouseMarkers = [];
    }


    // Create CustomOverlays with '창' text
    for (const warehouse of warehouses) {
        try {
            const wLat = parseFloat(warehouse.REFINE_WGS84_LAT);
            const wLng = parseFloat(warehouse.REFINE_WGS84_LOGT);
            if (isNaN(wLat) || isNaN(wLng)) continue;

            const wPos = new kakao.maps.LatLng(wLat, wLng);

            // Create Content
            const content = document.createElement('div');
            // Styling to look like a small distinct marker (Yellow)
            content.style.cssText = `
                        background-color: #FCD34D; /* Yellow-400 */
                        border: 2px solid #d97706; /* Amber-600 */
                        color: #78350F; /* Amber-900 */
                        width: 24px;
                        height: 24px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 11px;
                        font-weight: bold;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                        cursor: pointer;
                        user-select: none;
                        transition: transform 0.1s;
                     `;
            content.innerHTML = '창';

            content.onmouseover = () => { content.style.transform = 'scale(1.1)'; };
            content.onmouseout = () => { content.style.transform = 'scale(1.0)'; };
            content.onclick = () => {
                updateWarehousePanel(warehouse, warehouses.length);
            };

            const overlay = new kakao.maps.CustomOverlay({
                position: wPos,
                content: content,
                map: mapKakao,
                yAnchor: 0.5 // Center aligned
            });

            if (!window.warehouseMarkers) window.warehouseMarkers = [];
            window.warehouseMarkers.push(overlay);
        } catch (e) { console.error(e); }
    }

}

function closeWarehousePanel() {
    const panel = document.getElementById('warehouse-panel');
    if (panel) panel.style.display = 'none';
}

function toggleWarehousePanel(e) {
    const panel = document.getElementById('warehouse-panel');
    const btn = e.currentTarget;
    panel.classList.toggle('minimized');
    btn.innerText = panel.classList.contains('minimized') ? '▲' : '▼';
}


// ---------------------------------------------------------
// Kamco Auction Logic
// ---------------------------------------------------------

window.auctionMarkers = [];

async function checkNearbyAuctions(lat, lng, sido, sgk, emd, itemIdx) {
    if (!sido || !sgk) return;

    try {
        const query = `sido=${encodeURIComponent(sido)}&sgk=${encodeURIComponent(sgk)}`;
        const response = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/auction/?${query}`);
        const resJson = await response.json();

        if (resJson.status === 'OK' && resJson.items && resJson.items.length > 0) {
            const items = resJson.items;
            const data = polygonsData[itemIdx];

            if (data && data.listItem) {
                data.auctions = items;
                data.searchLat = lat;
                data.searchLng = lng;

                // Add '캠' Button to the action row, similar to '창'
                const actionRow = data.listItem.querySelector('.result-action-row');
                if (actionRow) {
                    // Prevent duplicates
                    if (actionRow.querySelector('.auction-btn')) return;

                    const btn = document.createElement('button');
                    btn.className = 'auction-btn';
                    btn.innerText = '캠';
                    btn.title = `인근 공매 물건 발견`;
                    btn.style.cssText = `
                                display: inline-flex;
                                align-items: center;
                                justify-content: center;
                                width: 15px;
                                height: 15px;
                                background: #ef4444;
                                color: white !important;
                                border-radius: 3px;
                                font-size: 7pt; font-weight: bold; border: none;
                                margin-top: 4px; cursor: pointer;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                            `;
                    btn.onclick = (e) => {
                        e.stopPropagation();
                        displayAuctionMarkers(items, lat, lng, emd);
                    };
                    actionRow.appendChild(btn);
                }
            }
        }
    } catch (err) {
        console.error("Auction check error:", err);
    }
}

async function displayAuctionMarkers(items, centerLat, centerLng, emdName) {
    if (window.auctionMarkers) {
        window.auctionMarkers.forEach(m => m.setMap(null));
    }
    window.auctionMarkers = [];

    if (!window.kakaoGeocoder) {
        window.kakaoGeocoder = new kakao.maps.services.Geocoder();
    }

    const limitDeg = 0.09; // Approx 10km

    // 1. Filter and prioritize items
    // First, items containing the specific EMD name, then others
    let prioritizedItems = [];
    let otherItems = [];

    if (emdName) {
        const cleanEmd = emdName.replace(/[0-9]/g, '').trim(); // Remove digits like '미음동1' -> '미음동'
        items.forEach(item => {
            const addr = item.NMRD_ADRS || item.LDNM_ADRS || '';
            if (addr.includes(cleanEmd)) prioritizedItems.push(item);
            else otherItems.push(item);
        });
    } else {
        otherItems = items;
    }

    // Limit total geocoding to reasonable amount (e.g., 50 prioritized + 30 others)
    const targetItems = prioritizedItems.slice(0, 80).concat(otherItems.slice(0, 40));

    console.log(`Geocoding ${targetItems.length} auction items (EMD: ${emdName || 'N/A'})`);

    // 2. Geocode with small delay to prevent overwhelming
    for (let i = 0; i < targetItems.length; i++) {
        const item = targetItems[i];
        const addr = item.NMRD_ADRS || item.LDNM_ADRS;
        if (!addr) continue;

        // Simple concurrency control: wait a bit every 10 items
        if (i > 0 && i % 10 === 0) await new Promise(r => setTimeout(r, 100));

        window.kakaoGeocoder.addressSearch(addr, (result, status) => {
            if (status === kakao.maps.services.Status.OK) {
                const mLat = parseFloat(result[0].y);
                const mLng = parseFloat(result[0].x);

                // Distance check (Approx)
                if (centerLat && centerLng) {
                    const dLat = Math.abs(centerLat - mLat);
                    const dLng = Math.abs(centerLng - mLng);
                    if (dLat > limitDeg || dLng > limitDeg) return;
                }

                const coords = new kakao.maps.LatLng(mLat, mLng);
                const content = document.createElement('div');
                content.className = 'auction-marker';
                content.innerText = '캠';
                content.style.cssText = `
                            cursor: pointer;
                            background: #ef4444;
                            color: white;
                            border-radius: 50%;
                            width: 24px;
                            height: 24px;
                            line-height: 24px;
                            text-align: center;
                            font-size: 10px;
                            font-weight: bold;
                            border: 2px solid white;
                            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
                        `;
                content.onclick = (e) => {
                    e.stopPropagation();
                    updateAuctionPanel(item);
                };

                const overlay = new kakao.maps.CustomOverlay({
                    position: coords,
                    content: content,
                    yAnchor: 1
                });

                overlay.setMap(mapKakao);
                window.auctionMarkers.push(overlay);
            }
        });
    }
}

function updateAuctionPanel(item) {
    const panel = document.getElementById('auction-panel');
    const content = document.getElementById('auction-content');
    if (!panel || !content) return;

    const formatPrice = (val) => {
        if (!val) return '-';
        const num = Number(val);
        return isNaN(num) ? val : num.toLocaleString() + '원';
    };

    const toPy = (val) => {
        if (!val) return '-';
        const m2 = parseFloat(val);
        if (isNaN(m2)) return val;
        const py = Math.round(m2 * 0.3025);
        return `${py.toLocaleString()}평 (${m2.toLocaleString()}㎡)`;
    };

    const fields = [
        { label: '물건명', val: item.CLTR_NM },
        { label: '물건상태', val: item.PBCT_CLTR_STAT_NM || '-' },
        { label: '물건소재지(지번)', val: item.LDNM_ADRS },
        { label: '용도', val: item.CTGR_FULL_NM || '-' },
        { label: '토지면적', val: toPy(item.LAND_SQMS) },
        { label: '건물면적', val: toPy(item.BLD_SQMS) },
        { label: '입찰시작가', val: formatPrice(item.MIN_BID_PRC) },
        { label: '입찰 회수', val: item.BID_PRGN_NFT ? item.BID_PRGN_NFT + '회' : '-' }
    ];

    // Use same table styling as Warehouse Panel (8pt font, grey background headers)
    let html = '<div class="info-table-container" style="border:none;"><table class="info-table" style="font-size: 8pt; width:100%; border-collapse: collapse;"><tbody>';

    fields.forEach(f => {
        html += `
                    <tr>
                        <th style="width:110px; padding: 6px 8px; background:#f8fafc; color:#64748b; border: 1px solid #e2e8f0; font-weight:600; text-align:left;">${f.label}</th>
                        <td style="text-align:left; padding: 6px 8px; border: 1px solid #e2e8f0; color:#334155;">${f.val || '-'}</td>
                    </tr>
                `;
    });
    html += '</tbody></table></div>';

    content.innerHTML = html;
    panel.style.display = 'block';
    panel.classList.remove('minimized');
}

function closeAuctionPanel() {
    const panel = document.getElementById('auction-panel');
    if (panel) panel.style.display = 'none';
}

function toggleAuctionPanel(e) {
    const panel = document.getElementById('auction-panel');
    const btn = e.currentTarget;
    if (panel) {
        panel.classList.toggle('minimized');
        btn.innerText = panel.classList.contains('minimized') ? '▲' : '▼';
    }
}

// ---------------------------------------------------------
// Hospital Info & Statistics Logic
// ---------------------------------------------------------

window.hospitalMarkers = [];

async function checkNearbyHospitals(lat, lng, sido, itemIdx) {
    if (!kakaoPlaces) kakaoPlaces = new kakao.maps.services.Places();

    // HP8 is the category code for hospitals
    kakaoPlaces.categorySearch('HP8', (results, status) => {
        if (status === kakao.maps.services.Status.OK) {
            if (results && results.length > 0) {
                addHospitalButton(itemIdx, results, lat, lng, sido);
            }
        }
    }, {
        location: new kakao.maps.LatLng(lat, lng),
        radius: 10000 // 10km radius
    });
}

function addHospitalButton(itemIdx, results, lat, lng, sido) {
    const data = polygonsData[itemIdx];
    if (!data || !data.listItem) return;

    data.hospitals = results;

    const actionRow = data.listItem.querySelector('.result-action-row');
    if (actionRow) {
        if (actionRow.querySelector('.hospital-btn')) return;

        const btn = document.createElement('button');
        btn.className = 'hospital-btn';
        btn.innerText = '병';
        btn.title = `인근 ${results.length}개의 병/의원 발견 (10km)`;
        btn.style.cssText = `
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 15px;
                    height: 15px;
                    background: #10b981; /* Green-500 */
                    color: white !important;
                    border-radius: 3px;
                    font-size: 7pt;
                    font-weight: bold;
                    border: none;
                    margin-top: 4px;
                    cursor: pointer;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                `;
        btn.onclick = (e) => {
            e.stopPropagation();
            showHospitalOnMap(results, sido, itemIdx);
        };
        actionRow.appendChild(btn);
    }
}

function showHospitalOnMap(hospitals, centerSido, itemIdx) {
    if (window.hospitalMarkers) {
        window.hospitalMarkers.forEach(m => m.setMap(null));
    }
    window.hospitalMarkers = [];

    hospitals.forEach(h => {
        const hPos = new kakao.maps.LatLng(h.y, h.x);
        const content = document.createElement('div');
        content.style.cssText = `
                    background-color: #10b981; /* Green-500 */
                    border: 2px solid white;
                    color: white;
                    width: 24px;
                    height: 24px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 11px;
                    font-weight: bold;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                    cursor: pointer;
                    user-select: none;
                `;
        content.innerHTML = '병';
        content.onclick = () => {
            // Check if it's a Kakao object (has place_name) or HIRA object (has yadmNm)
            const info = {
                yadmNm: h.yadmNm || h.place_name,
                addr: h.addr || h.road_address_name || h.address_name,
                telno: h.telno || h.phone,
                clCdNm: h.clCdNm, // Kakao doesn't have this, will be "-" initially
                hospUrl: h.hospUrl || h.place_url,
                estbDd: h.estbDd,
                drTotCnt: h.drTotCnt,
                ykiho: h.ykiho
            };
            updateHospitalPanel(info);
        };

        const overlay = new kakao.maps.CustomOverlay({
            position: hPos,
            content: content,
            map: mapKakao,
            yAnchor: 0.5
        });
        window.hospitalMarkers.push(overlay);
    });

    // 마커들이 보이도록 지도 이동 (선택적)
    // if (hospitals.length > 0) {
    //     const bounds = new kakao.maps.LatLngBounds();
    //     hospitals.forEach(h => bounds.extend(new kakao.maps.LatLng(h.y, h.x)));
    //     mapKakao.setBounds(bounds);
    // }
}

async function updateHospitalPanel(info, addrArg, telnoArg, clCdNmArg, hospUrlArg, estbDdArg, drTotCntArg) {
    let yadmNm, addr, telno, clCdNm, hospUrl, estbDd, drTotCnt, ykiho;

    if (typeof info === 'string') {
        // Legacy call signature
        yadmNm = info;
        addr = addrArg;
        telno = telnoArg;
        clCdNm = clCdNmArg;
        hospUrl = hospUrlArg;
        estbDd = estbDdArg;
        drTotCnt = drTotCntArg;
    } else {
        // New object signature
        ({ yadmNm, addr, telno, clCdNm, hospUrl, estbDd, drTotCnt, ykiho } = info || {});
    }
    const panel = document.getElementById('hospital-panel');
    const content = document.getElementById('hospital-content');
    if (!panel || !content) return;

    content.innerHTML = '<div style="padding:20px; text-align:center; font-size:9pt; color:#64748b;">정보를 불러오는 중...</div>';
    panel.style.display = 'block';
    panel.classList.remove('minimized');

    const renderHeader = (data) => {
        return `
                    <div style="padding: 15px; background: #fff; border-bottom: 2px solid #10b981; margin-bottom: 10px;">
                        <div style="font-size: 13pt; font-weight: 800; color: #1e293b; margin-bottom: 5px;">${data.yadmNm}</div>
                        <div style="font-size: 8.5pt; color: #64748b; margin-bottom: 8px;">${data.clCdNm || '-'}</div>
                        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 9pt;">
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <span style="color: #10b981; font-weight: bold; min-width: 60px;">주소</span>
                                <span style="color: #334155;">${data.addr || '-'}</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <span style="color: #10b981; font-weight: bold; min-width: 60px;">개설일자</span>
                                <span style="color: #334155;">${data.estbDd ? (data.estbDd.toString().slice(0, 4) + '.' + data.estbDd.toString().slice(4, 6) + '.' + data.estbDd.toString().slice(6, 8)) : '-'}</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <span style="color: #10b981; font-weight: bold; min-width: 60px;">의사총수</span>
                                <span style="color: #334155;">${data.drTotCnt ? data.drTotCnt + '명' : '-'}</span>
                            </div>
                             <div style="display: flex; align-items: center; gap: 6px;">
                                <span style="color: #10b981; font-weight: bold; min-width: 60px;">전화</span>
                                <span style="color: #334155;">${data.telno || '-'}</span>
                            </div>
                        </div>
                        <div style="margin-top: 10px;">
                            ${data.hospUrl ? `<a href="${data.hospUrl}" target="_blank" style="display: inline-block; padding: 4px 10px; background: #d1fae5; color: #065f46; text-decoration: none; border-radius: 4px; font-size: 8pt; font-weight: bold; border: 1px solid #a7f3d0;">홈페이지</a>` : ''}
                        </div>
                    </div>
                `;
    };

    // Initial Render with available info
    let currentInfo = { yadmNm, addr, telno, clCdNm, hospUrl, estbDd, drTotCnt };

    try {
        // Fetch details
        let query = `name=${encodeURIComponent(yadmNm)}`;
        if (ykiho) {
            query += `&ykiho=${encodeURIComponent(ykiho)}`;
        }
        const responseDetail = await fetch(`${window.GUNDAM_CONFIG.apiBase || ''}/proxy/hospital/detail/?${query}`);
        const resJson = await responseDetail.json();

        if (resJson.status === 'OK') {
            // Update header with HIRA basis info if available
            if (resJson.basis) {
                const b = resJson.basis;
                currentInfo = {
                    yadmNm: b.yadmNm || currentInfo.yadmNm,
                    addr: b.addr || currentInfo.addr,
                    telno: b.telno || currentInfo.telno,
                    clCdNm: b.clCdNm || currentInfo.clCdNm,
                    hospUrl: b.hospUrl || currentInfo.hospUrl,
                    estbDd: b.estbDd || currentInfo.estbDd,
                    drTotCnt: b.drTotCnt || currentInfo.drTotCnt
                };
            }

            const headerHtml = renderHeader(currentInfo);

            if (resJson.detail) {
                const detail = resJson.detail;
                let html = '<div class="info-table-container" style="border:none; padding:10px;"><table class="info-table" style="font-size: 8.5pt; width:100%; border-collapse: collapse;">';

                html += `<thead style="background:#1e293b;">
                                    <tr>
                                        <th style="padding:8px; border:1px solid #334155; color:#ffffff;">구분</th>
                                        <th style="padding:8px; border:1px solid #334155; color:#ffffff;">시설 정보 (병상수)</th>
                                    </tr>
                                 </thead><tbody>`;

                const addRow = (label, val) => {
                    const displayVal = (val !== undefined && val !== null && val !== '-') ? Number(val).toLocaleString() : '-';
                    html += `<tr>
                                    <th style="width:140px; padding: 6px 12px; background:#f8fafc; color:#64748b; border: 1px solid #e2e8f0; font-weight:600; text-align:left;">${label}</th>
                                    <td style="text-align:right; padding: 6px 12px; border: 1px solid #e2e8f0; color:#334155; font-weight:700;">${displayVal}${displayVal !== '-' ? '개' : ''}</td>
                                 </tr>`;
                };

                addRow('상급 병상', detail.hghrSickbdCnt);
                addRow('일반 병상', detail.stdSickbdCnt);
                addRow('중환자실 병상', detail.icu_cnt);
                addRow('응급실 병상', detail.emymCnt);
                addRow('격리 병실', detail.isnrSbdCnt);
                addRow('무균 치료실', detail.anvirTrrmSbdCnt);
                addRow('분만실 수', detail.partumCnt);
                addRow('수술실 수', detail.soprmCnt);
                addRow('정신과 폐쇄 병상', detail.psydeptClsHigSbdCnt || detail.psydeptClsGnlSbdCnt);

                html += '</tbody></table></div>';
                html += `<div style="padding:10px; font-size:7.5pt; color:#94a3b8; text-align:center;">※ 건강보험심사평가원(HIRA) 실시간 시설 정보</div>`;

                content.innerHTML = headerHtml + html;
            }
        } else {
            const errorMsg = resJson.message || '병원 상세 정보를 찾을 수 없습니다.';
            content.innerHTML = renderHeader(currentInfo) + `<div style="padding:20px; text-align:center; font-size:9pt; color:#ef4444;">${errorMsg}</div>`;
        }
    } catch (err) {
        console.error("Hospital detail fetch error:", err);
        content.innerHTML = renderHeader(currentInfo) + '<div style="padding:20px; text-align:center; font-size:9pt; color:#ef4444;">데이터 요청 중 오류가 발생했습니다.</div>';
    }
}

function closeHospitalPanel() {
    const panel = document.getElementById('hospital-panel');
    if (panel) panel.style.display = 'none';
}

function toggleHospitalPanel(e) {
    const panel = document.getElementById('hospital-panel');
    const btn = e.currentTarget;
    if (panel) {
        panel.classList.toggle('minimized');
        btn.innerText = panel.classList.contains('minimized') ? '▲' : '▼';
    }
}

