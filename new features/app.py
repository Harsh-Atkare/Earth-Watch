# ================================================================
#  TERRAIN GUARDIAN — Land Degradation, Deforestation & Landslide
#  Streamlit Web App using Google Earth Engine
# ================================================================

import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import json, os, sys
import plotly.graph_objects as go
import plotly.express as px

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="Terrain Guardian · Environmental Analysis",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════
#  STYLES
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;700&family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');
:root{
  --bg:#080c10;--surf:#0d1117;--surf2:#131920;--surf3:#0a0e14;
  --bdr:#1c2535;--bdr2:#243040;
  --acc:#00d4aa;--red:#ff3d5a;--amber:#f5a623;--green:#00c48c;--blue:#4da6ff;
  --txt:#dce8f0;--muted:#4a5e72;
  --mono:'JetBrains Mono',monospace;
  --display:'Bebas Neue',sans-serif;
  --body:'DM Sans',sans-serif;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,.stApp{background:var(--bg)!important;color:var(--txt);font-family:var(--body)}
#MainMenu,footer,header,[data-testid="stToolbar"]{visibility:hidden!important}
.block-container{padding:0!important;max-width:100%!important}
section[data-testid="stSidebar"]{display:none!important}
div[data-testid="stStatusWidget"]{display:none!important}
div[data-stale="true"]{opacity:1!important}
iframe{opacity:1!important}

.topbar{display:flex;align-items:center;justify-content:space-between;
  padding:0 2rem;height:56px;background:var(--surf);
  border-bottom:1px solid var(--bdr);position:sticky;top:0;z-index:1000}
.logo{font-family:var(--display);font-size:24px;letter-spacing:.12em;color:var(--acc)}
.logo em{color:var(--txt);font-style:normal}
.topbar-pills{display:flex;gap:12px;align-items:center}
.pill{font-family:var(--mono);font-size:10px;letter-spacing:.07em;
  padding:3px 10px;border-radius:20px;border:1px solid var(--bdr2);color:var(--muted)}
.pill-g{border-color:rgba(0,212,170,.3);color:var(--acc)}

.phdr{padding:.7rem 1.2rem;border-bottom:1px solid var(--bdr);
  display:flex;align-items:center;gap:8px}
.phdr-lbl{font-family:var(--mono);font-size:10px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted)}
.dot{width:7px;height:7px;border-radius:50%;background:var(--acc);
  animation:blink 2s infinite;flex-shrink:0}
.dot-r{background:var(--red)!important;animation:none!important}
.dot-g{background:var(--green)!important;animation:none!important}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}

.stTextArea textarea{background:#060a0e!important;border:1px solid var(--bdr2)!important;
  border-radius:8px!important;color:var(--acc)!important;
  font-family:var(--mono)!important;font-size:11px!important}
.stTextArea textarea:focus{border-color:rgba(0,212,170,.5)!important;
  box-shadow:0 0 0 2px rgba(0,212,170,.1)!important}
label[data-testid="stWidgetLabel"] p{font-family:var(--mono)!important;font-size:10px!important;
  color:var(--muted)!important;letter-spacing:.06em!important;text-transform:uppercase!important}
.stSelectbox>div>div{background:#060a0e!important;border:1px solid var(--bdr2)!important;
  color:var(--txt)!important;font-family:var(--mono)!important;font-size:11px!important}
.stNumberInput>div>div>input{background:#060a0e!important;border:1px solid var(--bdr2)!important;
  color:var(--acc)!important;font-family:var(--mono)!important;font-size:12px!important}

.ccard{background:rgba(0,212,170,.05);border:1px solid rgba(0,212,170,.18);
  border-radius:8px;padding:.8rem 1rem;margin:.5rem 0}
.crow{display:flex;justify-content:space-between;font-size:12px;padding:3px 0}
.ck{color:var(--muted);font-family:var(--mono);font-size:10px}
.cv{color:var(--acc);font-family:var(--mono);font-size:11px}
.cdiv{border-top:1px solid rgba(0,212,170,.15);margin:5px 0}

.stButton>button{font-family:var(--mono)!important;font-size:11px!important;
  letter-spacing:.06em!important;border-radius:7px!important;
  width:100%!important;transition:all .15s!important;padding:.55rem .8rem!important}
.stButton>button:first-child{background:var(--acc)!important;color:#060a0e!important;border:none!important}
.stButton>button:first-child:hover{background:#1fffc0!important;transform:translateY(-1px)!important}
.stButton>button:first-child:disabled{background:var(--bdr2)!important;color:var(--muted)!important}

.stat-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:.5rem}
.stat-card{background:var(--surf2);border:1px solid var(--bdr);border-radius:8px;padding:10px 12px}
.stat-val{font-family:var(--mono);font-size:18px;font-weight:700;color:var(--acc)}
.stat-lbl{font-family:var(--mono);font-size:9px;color:var(--muted);text-transform:uppercase;
  letter-spacing:.06em;margin-top:2px}

.legend{display:flex;gap:14px;padding:.5rem 1.2rem;
  border-bottom:1px solid var(--bdr);flex-wrap:wrap}
.legend-item{display:flex;align-items:center;gap:5px;
  font-family:var(--mono);font-size:9px;color:var(--muted)}
.legend-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}

.foot{text-align:center;padding:5px;border-top:1px solid var(--bdr);
  font-family:var(--mono);font-size:9px;color:var(--muted);
  letter-spacing:.06em;background:var(--surf)}

div[data-baseweb="tab-list"]{gap:0!important}
button[data-baseweb="tab"]{font-family:var(--mono)!important;font-size:11px!important;
  letter-spacing:.06em!important;color:var(--muted)!important;background:transparent!important;
  border-bottom:2px solid transparent!important;padding:10px 20px!important}
button[data-baseweb="tab"][aria-selected="true"]{color:var(--acc)!important;
  border-bottom-color:var(--acc)!important}
div[data-baseweb="tab-panel"]{padding:0!important}

.warn-box{background:rgba(245,166,35,.08);border:1px solid rgba(245,166,35,.3);
  border-radius:7px;padding:8px 12px;margin:6px 0;
  font-family:var(--mono);font-size:10px;color:var(--amber)}

::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-thumb{background:var(--bdr2);border-radius:4px}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ───────────────────────────────────────────────
for k, v in [('gj_text',''), ('parsed',None), ('draw_mode',True),
             ('deforest_result',None), ('snow_result',None), ('landslide_result',None),
             ('lulc_result',None), ('fire_result',None),
             ('overlay_tiles', None), ('overlay_name', '')]:
    if k not in st.session_state:
        st.session_state[k] = v


def parse_geojson(text):
    try:
        gj = json.loads(text.strip())
        if gj.get('type')=='FeatureCollection': gj=gj['features'][0]
        if gj.get('type')=='Feature': gj=gj['geometry']
        if gj.get('type') in ('Polygon','MultiPolygon'): return gj
    except Exception:
        pass
    return None

def get_bbox(geom):
    pts = geom['coordinates'][0] if geom['type']=='Polygon' \
          else [p for ring in geom['coordinates'][0] for p in ring]
    lons=[p[0] for p in pts]; lats=[p[1] for p in pts]
    return min(lons),min(lats),max(lons),max(lats)


# ═══════════════════════════════════════════════════════════════
#  TOPBAR
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div class="logo">TERRAIN<em>GUARDIAN</em></div>
  <div class="topbar-pills">
    <span class="pill">Google Earth Engine</span>
    <span class="pill">Sentinel-2 + Landsat</span>
    <span class="pill pill-g">NASADEM · Random Forest</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  LAYOUT: LEFT PANEL + MAP
# ═══════════════════════════════════════════════════════════════
col_left, col_map = st.columns([1,3], gap="small")

with col_left:
    st.markdown('<div class="phdr"><div class="dot"></div>'
                '<span class="phdr-lbl">Select Area of Interest</span></div>',
                unsafe_allow_html=True)

    # Toggle draw/text
    dc1, dc2 = st.columns(2)
    with dc1:
        if st.button("✎ DRAW ON MAP" if not st.session_state.draw_mode else "⌨ TYPE GEOJSON",
                      key="toggle_draw"):
            st.session_state.draw_mode = not st.session_state.draw_mode
            st.rerun()
    with dc2:
        if st.session_state.draw_mode:
            st.markdown('<div style="font-family:var(--mono);font-size:9px;color:var(--acc);'
                        'padding:8px 0">🖱 Draw on the map →</div>',
                        unsafe_allow_html=True)

    if st.session_state.draw_mode:
        st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--muted);'
                    'padding:6px 12px;background:rgba(0,212,170,.06);border:1px solid rgba(0,212,170,.15);'
                    'border-radius:7px;margin:4px 0">'
                    '📌 Use ▭ rectangle or ⬠ polygon tools on the map to select your area.</div>',
                    unsafe_allow_html=True)
    else:
        gj_text = st.text_area("GeoJSON", value=st.session_state.gj_text,
            height=100, label_visibility="collapsed", key="ta_input",
            placeholder='{"type":"Polygon","coordinates":[...]}\n\nPaste GeoJSON here')
        if gj_text != st.session_state.gj_text:
            st.session_state.gj_text = gj_text
            st.session_state.parsed = parse_geojson(gj_text)
            st.rerun()

    parsed = st.session_state.parsed
    if parsed:
        b = get_bbox(parsed)
        st.markdown(f"""
        <div class="ccard">
          <div class="crow"><span class="ck">LON</span>
            <span class="cv">{b[0]:.4f} → {b[2]:.4f}</span></div>
          <div class="crow"><span class="ck">LAT</span>
            <span class="cv">{b[1]:.4f} → {b[3]:.4f}</span></div>
        </div>
        """, unsafe_allow_html=True)

    bc1, bc2 = st.columns(2)
    with bc1:
        if parsed and st.button("✕  CLEAR AOI", key="clear_btn"):
            for k in ['gj_text','parsed','deforest_result','snow_result','lulc_result',
                       'landslide_result','overlay_tiles','overlay_name']:
                st.session_state[k] = '' if k=='gj_text' else None if 'result' in k else ''
            st.session_state.parsed = None
            st.rerun()
    with bc2:
        if parsed:
            gj_export = json.dumps({"type":"Feature","properties":{},"geometry":parsed}, indent=2)
            st.download_button("⬇ EXPORT AOI", data=gj_export,
                               file_name="terrain_guardian_aoi.geojson",
                               mime="application/json", key="export_aoi")


# ═══════════════════════════════════════════════════════════════
#  MAP
# ═══════════════════════════════════════════════════════════════
with col_map:
    parsed = st.session_state.parsed
    center = [22.5, 78.9]; zoom = 5
    if parsed:
        b = get_bbox(parsed)
        center = [(b[1]+b[3])/2, (b[0]+b[2])/2]; zoom = 10

    m = folium.Map(
        location=center, zoom_start=zoom,
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', control_scale=True,
    )

    # Draw controls
    if st.session_state.draw_mode:
        Draw(
            export=False, position='topleft',
            draw_options={
                'polyline': False, 'circle': False, 'circlemarker': False, 'marker': False,
                'polygon': {'shapeOptions': {'color': '#00d4aa', 'weight': 2, 'fillOpacity': 0.1}},
                'rectangle': {'shapeOptions': {'color': '#00d4aa', 'weight': 2, 'fillOpacity': 0.1}},
            },
            edit_options={'edit': False, 'remove': True},
        ).add_to(m)

    # AOI boundary
    if parsed:
        folium.GeoJson(
            {"type":"Feature","properties":{},"geometry":parsed},
            style_function=lambda x:{
                'fillColor':'#00d4aa','color':'#00d4aa',
                'weight':2,'fillOpacity':0.06,'dashArray':'6 4'}
        ).add_to(m)
        b = get_bbox(parsed)
        m.fit_bounds([[b[1],b[0]],[b[3],b[2]]])

    # Overlay tiles from analysis results
    overlay = st.session_state.overlay_tiles
    if overlay:
        folium.TileLayer(
            tiles=overlay,
            attr='GEE Analysis',
            name=st.session_state.overlay_name,
            overlay=True,
            opacity=0.7,
        ).add_to(m)
        folium.LayerControl().add_to(m)

    map_data = st_folium(m, width="100%", height=550, key="map",
                         returned_objects=["all_drawings"] if st.session_state.draw_mode else [])

    # Capture drawn geometry
    if st.session_state.draw_mode and map_data and map_data.get('all_drawings'):
        drawings = map_data['all_drawings']
        if drawings and len(drawings) > 0:
            geom = drawings[-1].get('geometry')
            if geom and geom.get('type') in ('Polygon', 'MultiPolygon'):
                gj_str = json.dumps(geom)
                if gj_str != st.session_state.gj_text:
                    st.session_state.gj_text = gj_str
                    st.session_state.parsed = geom
                    st.session_state.draw_mode = False
                    st.rerun()


# ═══════════════════════════════════════════════════════════════
#  ANALYSIS TABS
# ═══════════════════════════════════════════════════════════════
st.markdown('<hr style="border:none;border-top:1px solid #1c2535;margin:0">', unsafe_allow_html=True)

tab_lulc, tab_deforest, tab_fire, tab_snow, tab_landslide, tab_overview = st.tabs([
    "🗺️  LULC", "🌳  DEFORESTATION", "🔥  FOREST FIRE", "❄️  SNOW & ICE", "⛰️  LANDSLIDE RISK", "📊  OVERVIEW"
])


# ── TAB 0: LULC ──────────────────────────────────────────────
with tab_lulc:
    st.markdown('<div class="phdr"><div class="dot dot-g"></div>'
                '<span class="phdr-lbl">Land Use Land Cover — Google Dynamic World (10m)</span></div>',
                unsafe_allow_html=True)

    lc1, lc2 = st.columns([1,1])
    with lc1:
        lulc_year = st.number_input("Year", min_value=2017, max_value=2025, value=2024, key="lulc_year")
    with lc2:
        lulc_season = st.selectbox("Season", ['annual', 'kharif', 'rabi', 'dry', 'wet'], index=0, key="lulc_season")

    def _cached_lulc(geojson_dict, year, season):
        """Permanent disk cache — saves results as JSON so repeat scans are instant."""
        import json, hashlib, os
        cache_dir = os.path.join(os.path.dirname(__file__), '.cache', 'lulc')
        os.makedirs(cache_dir, exist_ok=True)
        key = hashlib.md5(json.dumps({'g': geojson_dict, 'y': year, 's': season},
                                      sort_keys=True).encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{key}.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        from analysis.lulc import analyze_lulc
        result = analyze_lulc(geojson_dict, year, season)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f)
        return result

    if st.button("🗺️  CLASSIFY LAND USE", disabled=(parsed is None), key="run_lulc"):
        with st.spinner("Fetching Dynamic World LULC from GEE... (1-2 min)"):
            try:
                result = _cached_lulc(parsed, lulc_year, lulc_season)
                st.session_state.lulc_result = result
                st.session_state.overlay_tiles = result['lulc_tiles']
                st.session_state.overlay_name = 'LULC Classification'
                st.rerun()
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                import traceback; traceback.print_exc()

    result = st.session_state.lulc_result
    if result:
        s = result['stats']
        classes = result['classes']
        areas = s['class_areas_km2']
        pcts = s['class_percentages']

        # Stats grid — class areas
        grid_html = '<div class="stat-grid">'
        for cls_val, cls_info in classes.items():
            name = cls_info['name']
            area = areas.get(name, 0)
            pct = pcts.get(name, 0)
            color = cls_info['color']
            grid_html += f'''<div class="stat-card">
              <div class="stat-val" style="color:{color}">{area} km²</div>
              <div class="stat-lbl">{name} ({pct}%)</div></div>'''
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)

        # Info card
        st.markdown(f'''
        <div class="ccard">
          <div class="crow"><span class="ck">SOURCE</span>
            <span class="cv" style="color:#00c48c">{s['source']}</span></div>
          <div class="crow"><span class="ck">RESOLUTION</span>
            <span class="cv">{s['resolution']}</span></div>
          <div class="cdiv"></div>
          <div class="crow"><span class="ck">YEAR</span>
            <span class="cv">{s['year']}</span></div>
          <div class="crow"><span class="ck">SEASON</span>
            <span class="cv">{s['season'].upper()}</span></div>
          <div class="crow"><span class="ck">IMAGES USED</span>
            <span class="cv">{s['images_used']}</span></div>
          <div class="crow"><span class="ck">DOMINANT CLASS</span>
            <span class="cv">{s['dominant_class']}</span></div>
          <div class="crow"><span class="ck">TOTAL AREA</span>
            <span class="cv">{s['total_area_km2']} km²</span></div>
        </div>''', unsafe_allow_html=True)

        # Donut chart
        labels = list(areas.keys())
        values = list(areas.values())
        colors = [info['color'] for info in classes.values()]
        fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.5,
                               marker=dict(colors=colors),
                               textfont=dict(family='JetBrains Mono', size=10)))
        fig.update_layout(
            title='Land Use Distribution',
            template='plotly_dark', paper_bgcolor='#0d1117', plot_bgcolor='#0a0e14',
            font=dict(family='JetBrains Mono', size=10, color='#dce8f0'),
            height=300, margin=dict(l=20,r=20,t=40,b=20),
            legend=dict(font=dict(size=9)),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Legend
        legend_html = '<div class="legend">'
        for cls_info in classes.values():
            legend_html += f'<div class="legend-item"><div class="legend-dot" style="background:{cls_info["color"]}"></div>{cls_info["name"]}</div>'
        legend_html += '</div>'
        st.markdown(legend_html, unsafe_allow_html=True)

        # Layer switch — Row 1: base layers
        st.markdown('<div style="font-family:var(--mono);font-size:9px;color:var(--muted);'
                    'letter-spacing:.1em;text-transform:uppercase;padding:8px 0 4px">MAP LAYERS</div>',
                    unsafe_allow_html=True)
        lc1, lc2, lc3, lc4, lc5 = st.columns(5)
        with lc1:
            if st.button("🗺 LULC", key="sw_lulc"):
                st.session_state.overlay_tiles = result['lulc_tiles']
                st.session_state.overlay_name = 'LULC Classification'
                st.rerun()
        with lc2:
            if st.button("🛰 RGB", key="sw_rgb"):
                st.session_state.overlay_tiles = result['rgb_tiles']
                st.session_state.overlay_name = 'RGB Composite'
                st.rerun()
        with lc3:
            if st.button("🌿 NDVI", key="sw_ndvi_lulc"):
                st.session_state.overlay_tiles = result['ndvi_tiles']
                st.session_state.overlay_name = 'NDVI'
                st.rerun()
        with lc4:
            if st.button("🏗 NDBI", key="sw_ndbi"):
                st.session_state.overlay_tiles = result['ndbi_tiles']
                st.session_state.overlay_name = 'Built-up Index'
                st.rerun()
        with lc5:
            if st.button("💧 MNDWI", key="sw_mndwi"):
                st.session_state.overlay_tiles = result['mndwi_tiles']
                st.session_state.overlay_name = 'Water Index'
                st.rerun()

        # Layer switch — Row 2: probability heatmaps
        st.markdown('<div style="font-family:var(--mono);font-size:9px;color:var(--muted);'
                    'letter-spacing:.1em;text-transform:uppercase;padding:4px 0">PROBABILITY HEATMAPS</div>',
                    unsafe_allow_html=True)
        lp1, lp2, lp3 = st.columns(3)
        with lp1:
            if st.button("🏘 Built Area", key="sw_built_prob"):
                st.session_state.overlay_tiles = result['built_prob_tiles']
                st.session_state.overlay_name = 'Built Area Probability'
                st.rerun()
        with lp2:
            if st.button("🌳 Trees", key="sw_trees_prob"):
                st.session_state.overlay_tiles = result['trees_prob_tiles']
                st.session_state.overlay_name = 'Trees Probability'
                st.rerun()
        with lp3:
            if st.button("🌾 Crops", key="sw_crops_prob"):
                st.session_state.overlay_tiles = result['crops_prob_tiles']
                st.session_state.overlay_name = 'Crops Probability'
                st.rerun()


# ── TAB 1: DEFORESTATION ─────────────────────────────────────
with tab_deforest:
    st.markdown('<div class="phdr"><div class="dot dot-g"></div>'
                '<span class="phdr-lbl">Global Forest Watch Change Analysis (Hansen)</span></div>',
                unsafe_allow_html=True)

    dc1, dc2, dc3 = st.columns([1,1,1])
    with dc1:
        d_start = st.number_input("Start Year", min_value=2001, max_value=2024, value=2010, key="d_start")
    with dc2:
        d_end = st.number_input("End Year", min_value=2001, max_value=2024, value=2024, key="d_end")
    with dc3:
        d_thresh = st.number_input("Min Canopy (%)", min_value=10, max_value=100, value=20, step=5, key="d_thresh")

    # Year validation
    if d_end <= d_start:
        st.markdown('<div class="warn-box">⚠ End year must be greater than start year</div>',
                    unsafe_allow_html=True)

    def _cached_deforest(geojson_dict, start_year, end_year, min_canopy):
        """Permanent disk cache for deforestation analysis."""
        import json, hashlib, os
        cache_dir = os.path.join(os.path.dirname(__file__), '.cache', 'deforest')
        os.makedirs(cache_dir, exist_ok=True)
        key = hashlib.md5(json.dumps({'g': geojson_dict, 'sy': start_year, 'ey': end_year, 'mc': min_canopy},
                                      sort_keys=True).encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{key}.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        from analysis.deforestation import analyze_deforestation
        result = analyze_deforestation(geojson_dict, start_year, end_year, min_canopy)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(result, f)
        return result

    can_run = parsed is not None and d_end > d_start
    if st.button("🌳  ANALYZE DEFORESTATION", disabled=(not can_run), key="run_deforest"):
        with st.spinner("Analyzing forest cover change via GEE... (1-2 min)"):
            try:
                result = _cached_deforest(parsed, d_start, d_end, d_thresh)
                st.session_state.deforest_result = result
                st.session_state.overlay_tiles = result.get('combined_tiles', result['forest_loss_tiles'])
                st.session_state.overlay_name = 'Forest & Loss Combined'
                st.rerun()
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                import traceback; traceback.print_exc()

    result = st.session_state.deforest_result
    if result:
        s = result['stats']

        # Stats grid
        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-card">
            <div class="stat-val" style="color:#00c48c">{s['base_forest_area_ha']} ha</div>
            <div class="stat-lbl">Base Forest Area (Year 2000)</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#ff3d5a">{s['loss_area_ha']} ha</div>
            <div class="stat-lbl">Forest Loss ({s['start_year']}-{s['end_year']})</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Net change / Loss Percentage
        st.markdown(f"""
        <div class="ccard" style="border-color:#ff3d5a40">
          <div class="crow"><span class="ck">FOREST LOSS PERCENTAGE</span>
            <span class="cv" style="color:#ff3d5a">{s['loss_percentage']}%</span></div>
        </div>""", unsafe_allow_html=True)

        # Info card
        st.markdown(f'''
        <div class="ccard">
          <div class="crow"><span class="ck">SOURCE</span>
            <span class="cv" style="color:#00c48c">{s['source']}</span></div>
          <div class="crow"><span class="ck">MIN CANOPY COVER</span>
            <span class="cv">{s['min_canopy']}%</span></div>
        </div>''', unsafe_allow_html=True)

        # Legend
        st.markdown("""
        <div class="legend">
          <div class="legend-item"><div class="legend-dot" style="background:#2d6a2d"></div>Base Forest (Year 2000)</div>
          <div class="legend-item"><div class="legend-dot" style="background:#FF2222"></div>Forest Loss</div>
        </div>""", unsafe_allow_html=True)

        # Layer switch
        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            if st.button("🗺️ Combined Mask", key="sw_combined"):
                st.session_state.overlay_tiles = result.get('combined_tiles', result['forest_loss_tiles'])
                st.session_state.overlay_name = 'Combined Forest & Loss'
                st.rerun()
        with lc2:
            if st.button("🔥 Forest Loss Only", key="sw_change"):
                st.session_state.overlay_tiles = result['forest_loss_tiles']
                st.session_state.overlay_name = 'Forest Loss'
                st.rerun()
        with lc3:
            if st.button("🌲 Base Forest Only", key="sw_base"):
                st.session_state.overlay_tiles = result['base_forest_tiles']
                st.session_state.overlay_name = 'Base Forest'
                st.rerun()

# ── TAB 1.5: FOREST FIRE ─────────────────────────────────────
with tab_fire:
    st.markdown('<div class="phdr"><div class="dot" style="background:#ff6b35"></div>'
                '<span class="phdr-lbl">Burn Severity Analysis — Sentinel-2 dNBR (10m)</span></div>',
                unsafe_allow_html=True)

    from datetime import date, timedelta
    fire_c1, fire_c2 = st.columns(2)
    with fire_c1:
        st.markdown('<span style="font-size:11px;color:var(--muted)">PRE-FIRE PERIOD</span>',
                    unsafe_allow_html=True)
        fp1, fp2 = st.columns(2)
        with fp1:
            f_pre_start = st.date_input("Pre Start", value=date(2024, 10, 1), key="f_pre_s",
                                         label_visibility="collapsed")
        with fp2:
            f_pre_end = st.date_input("Pre End", value=date(2024, 12, 31), key="f_pre_e",
                                       label_visibility="collapsed")
    with fire_c2:
        st.markdown('<span style="font-size:11px;color:var(--muted)">POST-FIRE PERIOD</span>',
                    unsafe_allow_html=True)
        fp3, fp4 = st.columns(2)
        with fp3:
            f_post_start = st.date_input("Post Start", value=date(2025, 1, 1), key="f_post_s",
                                          label_visibility="collapsed")
        with fp4:
            f_post_end = st.date_input("Post End", value=date(2025, 3, 1), key="f_post_e",
                                        label_visibility="collapsed")

    # Validation
    if f_pre_end >= f_post_start:
        st.markdown('<div class="warn-box">⚠ Pre-fire period must end before post-fire period starts</div>',
                    unsafe_allow_html=True)

    def _cached_fire(geojson_dict, pre_s, pre_e, post_s, post_e):
        """Permanent disk cache for burn severity analysis."""
        import json as _json, hashlib, os
        cache_dir = os.path.join(os.path.dirname(__file__), '.cache', 'forest_fire')
        os.makedirs(cache_dir, exist_ok=True)
        key = hashlib.md5(_json.dumps({'g': geojson_dict, 'ps': pre_s, 'pe': pre_e,
                                        'os': post_s, 'oe': post_e},
                                       sort_keys=True).encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{key}.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return _json.load(f)
        from analysis.forest_fire import analyze_burn_severity
        result = analyze_burn_severity(geojson_dict, pre_s, pre_e, post_s, post_e)
        with open(cache_file, 'w', encoding='utf-8') as f:
            _json.dump(result, f)
        return result

    can_run_fire = parsed is not None and f_pre_end < f_post_start
    if st.button("🔥  ANALYZE BURN SEVERITY", disabled=(not can_run_fire), key="run_fire"):
        with st.spinner("Analyzing burn severity via Sentinel-2 dNBR... (1-2 min)"):
            try:
                result = _cached_fire(parsed,
                                      str(f_pre_start), str(f_pre_end),
                                      str(f_post_start), str(f_post_end))
                st.session_state.fire_result = result
                st.session_state.overlay_tiles = result.get('severity_tiles')
                st.session_state.overlay_name = 'Burn Severity (dNBR)'
                st.rerun()
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                import traceback; traceback.print_exc()

    fire_result = st.session_state.fire_result
    if fire_result:
        fs = fire_result['stats']

        # Stats grid
        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-card">
            <div class="stat-val" style="color:#fee08b">{fs['low_severity_ha']} ha</div>
            <div class="stat-lbl">Low Severity</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#fc8d59">{fs['moderate_severity_ha']} ha</div>
            <div class="stat-lbl">Moderate Severity</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#d73027">{fs['high_severity_ha']} ha</div>
            <div class="stat-lbl">High Severity</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Total burned
        burn_color = '#d73027' if fs['total_burned_ha'] > 0 else '#00c48c'
        st.markdown(f"""
        <div class="ccard" style="border-color:#ff6b3540">
          <div class="crow"><span class="ck">TOTAL BURNED AREA</span>
            <span class="cv" style="color:{burn_color}">{fs['total_burned_ha']} ha</span></div>
          <div class="crow"><span class="ck">SOURCE</span>
            <span class="cv" style="color:#00c48c">{fs['source']}</span></div>
          <div class="crow"><span class="ck">PRE-FIRE IMAGES</span>
            <span class="cv">{fs['pre_images']}</span></div>
          <div class="crow"><span class="ck">POST-FIRE IMAGES</span>
            <span class="cv">{fs['post_images']}</span></div>
        </div>""", unsafe_allow_html=True)

        # Legend
        st.markdown("""
        <div class="legend">
          <div class="legend-item"><div class="legend-dot" style="background:#1a9850"></div>Unburned</div>
          <div class="legend-item"><div class="legend-dot" style="background:#fee08b"></div>Low</div>
          <div class="legend-item"><div class="legend-dot" style="background:#fc8d59"></div>Moderate</div>
          <div class="legend-item"><div class="legend-dot" style="background:#d73027"></div>High</div>
        </div>""", unsafe_allow_html=True)

        # Layer switches
        fc1, fc2, fc3, fc4 = st.columns(4)
        with fc1:
            if st.button("🗺️ Severity Map", key="sw_severity"):
                st.session_state.overlay_tiles = fire_result['severity_tiles']
                st.session_state.overlay_name = 'Burn Severity (dNBR)'
                st.rerun()
        with fc2:
            if st.button("🔥 Burned Mask", key="sw_burned"):
                st.session_state.overlay_tiles = fire_result['burned_mask_tiles']
                st.session_state.overlay_name = 'Burned Area Mask'
                st.rerun()
        with fc3:
            if st.button("🟢 Pre-Fire RGB", key="sw_pre_rgb"):
                st.session_state.overlay_tiles = fire_result['pre_rgb_tiles']
                st.session_state.overlay_name = 'Pre-Fire RGB'
                st.rerun()
        with fc4:
            if st.button("🔴 Post-Fire RGB", key="sw_post_rgb"):
                st.session_state.overlay_tiles = fire_result['post_rgb_tiles']
                st.session_state.overlay_name = 'Post-Fire RGB'
                st.rerun()


# ── TAB 2: SNOW & ICE COVER ──────────────────────────────────
with tab_snow:
    st.markdown('<div class="phdr"><div class="dot dot-b"></div>'
                '<span class="phdr-lbl">Snow & Ice Cover — Landsat 8/9 NDSI Analysis</span></div>',
                unsafe_allow_html=True)

    st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--muted);'
                'padding:6px 12px">NDSI = (Green − SWIR1) / (Green + SWIR1) · Threshold > 0.4 for snow</div>',
                unsafe_allow_html=True)

    snow_year = st.slider("Select Year", min_value=2014, max_value=2026, value=2024, key="snow_year")

    def _cached_snow(geojson_dict, yr):
        """Permanent disk cache for snow analysis."""
        import json as _json, hashlib, os
        cache_dir = os.path.join(os.path.dirname(__file__), '.cache', 'snow')
        os.makedirs(cache_dir, exist_ok=True)
        key = hashlib.md5(_json.dumps({'g': geojson_dict, 'y': yr}, sort_keys=True).encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{key}.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return _json.load(f)
        from analysis.snow_cover import analyze_snow_cover
        result = analyze_snow_cover(geojson_dict, yr)
        with open(cache_file, 'w', encoding='utf-8') as f:
            _json.dump(result, f)
        return result

    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("❄️  MAP SNOW COVER", disabled=(parsed is None), key="run_snow"):
            with st.spinner(f"Analyzing snow cover for {snow_year} via Landsat + GEE... (1-2 min)"):
                try:
                    result = _cached_snow(parsed, snow_year)
                    st.session_state.snow_result = result
                    st.session_state.overlay_tiles = result['snow_tiles']
                    st.session_state.overlay_name = 'Snow Cover Mask'
                    st.rerun()
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
                    import traceback; traceback.print_exc()
    with sc2:
        if st.button("📈  SNOW TREND (2014-2025)", disabled=(parsed is None), key="run_snow_trend"):
            with st.spinner("Computing multi-year snow trend... (3-5 min)"):
                try:
                    from analysis.snow_cover import get_snow_trend
                    trend = get_snow_trend(parsed, 2014, 2025)
                    st.session_state.snow_trend = trend
                    st.rerun()
                except Exception as e:
                    st.error(f"Trend failed: {e}")
                    import traceback; traceback.print_exc()

    result = st.session_state.snow_result
    if result:
        s = result['stats']

        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-card">
            <div class="stat-val" style="color:#87CEEB">{s['snow_area_km2']} km²</div>
            <div class="stat-lbl">Snow Covered</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#8B4513">{s['non_snow_area_km2']} km²</div>
            <div class="stat-lbl">Non-Snow</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#00bfff">{s['snow_coverage_pct']}%</div>
            <div class="stat-lbl">Snow Coverage</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#dce8f0">{s['total_area_km2']} km²</div>
            <div class="stat-lbl">Total AOI</div></div>
        </div>
        """, unsafe_allow_html=True)

        # NDSI stats card
        st.markdown(f"""
        <div class="ccard">
          <div class="crow"><span class="ck">ANALYSIS YEAR</span>
            <span class="cv">{s['year']}</span></div>
          <div class="crow"><span class="ck">MEAN NDSI</span>
            <span class="cv">{s['ndsi_mean']}</span></div>
          <div class="crow"><span class="ck">NDSI STD DEV</span>
            <span class="cv">{s['ndsi_std']}</span></div>
          <div class="cdiv"></div>
          <div class="crow"><span class="ck">SNOW THRESHOLD</span>
            <span class="cv">NDSI > 0.4</span></div>
          <div class="crow"><span class="ck">SENSOR</span>
            <span class="cv">Landsat 8/9 (30m)</span></div>
        </div>""", unsafe_allow_html=True)

        # Donut chart
        labels = ['Snow / Ice', 'Land / Water']
        values = [s['snow_area_km2'], s['non_snow_area_km2']]
        colors = ['#87CEEB', '#8B4513']
        fig = go.Figure(go.Pie(labels=labels, values=values, hole=0.5,
                               marker=dict(colors=colors),
                               textfont=dict(family='JetBrains Mono', size=10)))
        fig.update_layout(
            template='plotly_dark', paper_bgcolor='#0d1117', plot_bgcolor='#0a0e14',
            font=dict(family='JetBrains Mono', size=10, color='#dce8f0'),
            height=280, margin=dict(l=20,r=20,t=20,b=20),
            legend=dict(font=dict(size=9)),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Legend
        st.markdown("""
        <div class="legend">
          <div class="legend-item"><div class="legend-dot" style="background:#87CEEB"></div>Snow / Ice</div>
          <div class="legend-item"><div class="legend-dot" style="background:#8B4513"></div>Land / Water</div>
        </div>""", unsafe_allow_html=True)

        # Layer switch
        lc1, lc2, lc3 = st.columns(3)
        with lc1:
            if st.button("❄️ Snow Mask", key="sw_snow"):
                st.session_state.overlay_tiles = result['snow_tiles']
                st.session_state.overlay_name = 'Snow Cover Mask'
                st.rerun()
        with lc2:
            if st.button("🌈 NDSI Map", key="sw_ndsi"):
                st.session_state.overlay_tiles = result['ndsi_tiles']
                st.session_state.overlay_name = 'NDSI Heatmap'
                st.rerun()
        with lc3:
            if st.button("🛰 True Color", key="sw_snow_rgb"):
                st.session_state.overlay_tiles = result['rgb_tiles']
                st.session_state.overlay_name = 'Landsat True Color'
                st.rerun()

    # Multi-year trend chart
    if hasattr(st.session_state, 'snow_trend') and st.session_state.snow_trend:
        trend = st.session_state.snow_trend
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=[d['year'] for d in trend],
            y=[d['area_km2'] for d in trend],
            mode='lines+markers', name='Snow Area',
            line=dict(color='#00bfff', width=2),
            marker=dict(size=6, color='#87CEEB'),
            fill='tozeroy', fillcolor='rgba(0,191,255,0.1)',
        ))
        fig_trend.update_layout(
            title='Snow Covered Area Over Years (Landsat 8/9)',
            xaxis_title='Year', yaxis_title='Snow Area (km²)',
            template='plotly_dark',
            paper_bgcolor='#0d1117', plot_bgcolor='#0a0e14',
            font=dict(family='JetBrains Mono', size=10, color='#dce8f0'),
            height=300, margin=dict(l=50,r=20,t=40,b=40),
        )
        st.plotly_chart(fig_trend, use_container_width=True)


# ── TAB 3: LANDSLIDE SUSCEPTIBILITY ──────────────────────────
with tab_landslide:
    st.markdown('<div class="phdr"><div class="dot dot-r"></div>'
                '<span class="phdr-lbl">Random Forest Landslide Susceptibility Mapping</span></div>',
                unsafe_allow_html=True)

    st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--muted);'
                'padding:6px 12px">RF Variables (9): Elevation · Slope · Aspect · Hillshade · '
                'Flow Accumulation · HAND · TPI · Distance to Drainage · NDVI<br>'
                'Overlay Layers: Annual Precipitation (CHIRPS) · Temperature (MODIS LST)</div>',
                unsafe_allow_html=True)

    def _cached_landslide(geojson_dict):
        """Permanent disk cache for landslide analysis."""
        import json as _json, hashlib, os
        cache_dir = os.path.join(os.path.dirname(__file__), '.cache', 'landslide')
        os.makedirs(cache_dir, exist_ok=True)
        key = hashlib.md5(_json.dumps({'g': geojson_dict}, sort_keys=True).encode()).hexdigest()
        cache_file = os.path.join(cache_dir, f'{key}.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                return _json.load(f)
        from analysis.landslide import analyze_landslide
        result = analyze_landslide(geojson_dict)
        with open(cache_file, 'w', encoding='utf-8') as f:
            _json.dump(result, f)
        return result

    if st.button("⛰️  MAP LANDSLIDE RISK", disabled=(parsed is None), key="run_landslide"):
        with st.spinner("Building 13-variable terrain stack + training RF classifier via GEE... (2-4 min)"):
            try:
                result = _cached_landslide(parsed)
                st.session_state.landslide_result = result
                st.session_state.overlay_tiles = result['class_tiles']
                st.session_state.overlay_name = 'Landslide Risk Classes'
                st.rerun()
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                import traceback; traceback.print_exc()

    result = st.session_state.landslide_result
    if result:
        s = result['stats']

        st.markdown(f"""
        <div class="stat-grid">
          <div class="stat-card">
            <div class="stat-val" style="color:#00c48c">{s['low_risk_km2']} km²</div>
            <div class="stat-lbl">Low Risk</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#f5d623">{s['moderate_risk_km2']} km²</div>
            <div class="stat-lbl">Moderate Risk</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#f5a623">{s['high_risk_km2']} km²</div>
            <div class="stat-lbl">High Risk</div></div>
          <div class="stat-card">
            <div class="stat-val" style="color:#ff3d5a">{s['very_high_risk_km2']} km²</div>
            <div class="stat-lbl">Very High Risk</div></div>
        </div>
        """, unsafe_allow_html=True)

        # Model metrics card
        st.markdown(f"""
        <div class="ccard">
          <div class="crow"><span class="ck">MODEL ACCURACY</span>
            <span class="cv">{s['accuracy']}%</span></div>
          <div class="crow"><span class="ck">ROC AUC</span>
            <span class="cv" style="color:{'#00c48c' if s.get('auc',0)>0.7 else '#f5a623'}">{s.get('auc', 'N/A')}</span></div>
          <div class="cdiv"></div>
          <div class="crow"><span class="ck">PRECISION</span>
            <span class="cv">{s.get('precision', 'N/A')}</span></div>
          <div class="crow"><span class="ck">RECALL</span>
            <span class="cv">{s.get('recall', 'N/A')}</span></div>
          <div class="crow"><span class="ck">F1 SCORE</span>
            <span class="cv">{s.get('f1', 'N/A')}</span></div>
          <div class="cdiv"></div>
          <div class="crow"><span class="ck">TRAINING SAMPLES</span>
            <span class="cv">{s['num_training_samples']}</span></div>
          <div class="crow"><span class="ck">TEST SAMPLES</span>
            <span class="cv">{s['num_test_samples']}</span></div>
          <div class="crow"><span class="ck">TOTAL AREA</span>
            <span class="cv">{s['total_km2']} km²</span></div>
        </div>""", unsafe_allow_html=True)

        # Variable importance chart
        if result.get('importance'):
            imp = result['importance']
            sorted_imp = dict(sorted(imp.items(), key=lambda x: x[1], reverse=True))
            fig = go.Figure(go.Bar(
                x=list(sorted_imp.values()),
                y=list(sorted_imp.keys()),
                orientation='h',
                marker=dict(color='#00d4aa'),
                text=[f'{v}%' for v in sorted_imp.values()],
                textposition='outside',
                textfont=dict(family='JetBrains Mono', size=9, color='#dce8f0'),
            ))
            fig.update_layout(
                title='Variable Importance (%)',
                template='plotly_dark', paper_bgcolor='#0d1117', plot_bgcolor='#0a0e14',
                font=dict(family='JetBrains Mono', size=10, color='#dce8f0'),
                height=350, margin=dict(l=100,r=60,t=40,b=20),
                xaxis=dict(title='Importance %', range=[0, max(sorted_imp.values()) + 5]),
            )
            st.plotly_chart(fig, use_container_width=True)

        # Legend
        st.markdown("""
        <div class="legend">
          <div class="legend-item"><div class="legend-dot" style="background:#00c48c"></div>Low Risk</div>
          <div class="legend-item"><div class="legend-dot" style="background:#f5d623"></div>Moderate</div>
          <div class="legend-item"><div class="legend-dot" style="background:#f5a623"></div>High Risk</div>
          <div class="legend-item"><div class="legend-dot" style="background:#ff3d5a"></div>Very High</div>
        </div>""", unsafe_allow_html=True)

        # Layer switch
        st.markdown('<div style="font-family:var(--mono);font-size:9px;color:var(--muted);'
                    'letter-spacing:.1em;text-transform:uppercase;padding:8px 0 4px">RISK & TERRAIN LAYERS</div>',
                    unsafe_allow_html=True)
        lc1, lc2, lc3, lc4 = st.columns(4)
        with lc1:
            if st.button("🗺 Risk Map", key="sw_class"):
                st.session_state.overlay_tiles = result['class_tiles']
                st.session_state.overlay_name = 'Risk Classes'
                st.rerun()
        with lc2:
            if st.button("🔥 Susceptibility Prob", key="sw_prob"):
                st.session_state.overlay_tiles = result['probability_tiles']
                st.session_state.overlay_name = 'Susceptibility Probability'
                st.rerun()
        with lc3:
            if st.button("📐 Slope", key="sw_slope"):
                st.session_state.overlay_tiles = result['slope_tiles']
                st.session_state.overlay_name = 'Slope'
                st.rerun()
        with lc4:
            if st.button("🏔 Elev", key="sw_elev"):
                st.session_state.overlay_tiles = result['elevation_tiles']
                st.session_state.overlay_name = 'Elevation'
                st.rerun()

        st.markdown('<div style="font-family:var(--mono);font-size:9px;color:var(--muted);'
                    'letter-spacing:.1em;text-transform:uppercase;padding:4px 0">TRIGGER & MOISTURE FACTORS</div>',
                    unsafe_allow_html=True)
        lt1, lt2, lt3 = st.columns(3)
        with lt1:
            if result.get('precip_tiles') and st.button("🌧️ Rainfall (CHIRPS)", key="sw_precip"):
                st.session_state.overlay_tiles = result['precip_tiles']
                st.session_state.overlay_name = 'Annual Precipitation'
                st.rerun()
        with lt2:
            if result.get('temp_tiles') and st.button("🌡️ LST (MODIS)", key="sw_temp"):
                st.session_state.overlay_tiles = result['temp_tiles']
                st.session_state.overlay_name = 'Land Surface Temperature'
                st.rerun()
        with lt3:
            if result.get('hand_tiles') and st.button("💧 HAND", key="sw_hand"):
                st.session_state.overlay_tiles = result['hand_tiles']
                st.session_state.overlay_name = 'Height Above Nearest Drainage'
                st.rerun()


# ── TAB 4: OVERVIEW ──────────────────────────────────────────
with tab_overview:
    st.markdown('<div class="phdr"><div class="dot"></div>'
                '<span class="phdr-lbl">Combined Analysis Overview</span></div>',
                unsafe_allow_html=True)

    lur = st.session_state.lulc_result
    dr = st.session_state.deforest_result
    gr = st.session_state.snow_result
    lr = st.session_state.landslide_result

    has_any = lur or dr or gr or lr

    if not has_any:
        st.markdown('<div style="font-family:var(--mono);font-size:11px;color:var(--muted);'
                    'padding:2rem;text-align:center">'
                    '📊 Run at least one analysis to see the combined overview.</div>',
                    unsafe_allow_html=True)
    else:
        ov_cols = st.columns(4)

        with ov_cols[0]:
            st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--acc);'
                        'letter-spacing:.1em;text-transform:uppercase;padding:8px 12px;'
                        'border-bottom:1px solid var(--bdr)">🗺️ LULC</div>',
                        unsafe_allow_html=True)
            if lur:
                lus = lur['stats']
                dominant = max(lus['class_areas_km2'].items(), key=lambda x: x[1])
                st.markdown(f'''
                <div class="ccard">
                  <div class="crow"><span class="ck">DOMINANT CLASS</span>
                    <span class="cv">{dominant[0]}</span></div>
                  <div class="crow"><span class="ck">DOMINANT AREA</span>
                    <span class="cv">{dominant[1]} km²</span></div>
                  <div class="crow"><span class="ck">SOURCE</span>
                    <span class="cv">{lus.get('source', 'Dynamic World')}</span></div>
                  <div class="crow"><span class="ck">IMAGES</span>
                    <span class="cv">{lus.get('images_used', 'N/A')}</span></div>
                </div>''', unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--muted);'
                            'padding:12px">Not yet analyzed</div>', unsafe_allow_html=True)

        with ov_cols[1]:
            st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--acc);'
                        'letter-spacing:.1em;text-transform:uppercase;padding:8px 12px;'
                        'border-bottom:1px solid var(--bdr)">🌳 Deforestation</div>',
                        unsafe_allow_html=True)
            if dr:
                ds = dr['stats']
                color = '#ff3d5a' if float(ds['loss_percentage']) > 0 else '#00c48c'
                st.markdown(f"""
                <div class="ccard">
                  <div class="crow"><span class="ck">LOSS PERCENT</span>
                    <span class="cv" style="color:{color}">{ds['loss_percentage']}%</span></div>
                  <div class="crow"><span class="ck">LOSS AREA</span>
                    <span class="cv" style="color:#ff3d5a">{ds['loss_area_ha']} ha</span></div>
                  <div class="crow"><span class="ck">BASE AREA</span>
                    <span class="cv" style="color:#00c48c">{ds['base_forest_area_ha']} ha</span></div>
                  <div class="crow"><span class="ck">PERIOD</span>
                    <span class="cv">{ds['start_year']}–{ds['end_year']}</span></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--muted);'
                            'padding:12px">Not yet analyzed</div>', unsafe_allow_html=True)

        with ov_cols[2]:
            st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--acc);'
                        'letter-spacing:.1em;text-transform:uppercase;padding:8px 12px;'
                        'border-bottom:1px solid var(--bdr)">❄️ Snow & Ice</div>',
                        unsafe_allow_html=True)
            if gr:
                gs = gr['stats']
                st.markdown(f"""
                <div class="ccard">
                  <div class="crow"><span class="ck">SNOW AREA</span>
                    <span class="cv" style="color:#87CEEB">{gs['snow_area_km2']} km²</span></div>
                  <div class="crow"><span class="ck">COVERAGE</span>
                    <span class="cv" style="color:#00bfff">{gs['snow_coverage_pct']}%</span></div>
                  <div class="crow"><span class="ck">MEAN NDSI</span>
                    <span class="cv">{gs['ndsi_mean']}</span></div>
                  <div class="crow"><span class="ck">YEAR</span>
                    <span class="cv">{gs['year']}</span></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--muted);'
                            'padding:12px">Not yet analyzed</div>', unsafe_allow_html=True)

        with ov_cols[3]:
            st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--acc);'
                        'letter-spacing:.1em;text-transform:uppercase;padding:8px 12px;'
                        'border-bottom:1px solid var(--bdr)">⛰️ Landslide Risk</div>',
                        unsafe_allow_html=True)
            if lr:
                ls = lr['stats']
                st.markdown(f"""
                <div class="ccard">
                  <div class="crow"><span class="ck">HIGH + VERY HIGH</span>
                    <span class="cv" style="color:#ff3d5a">{ls['high_risk_km2'] + ls['very_high_risk_km2']} km²</span></div>
                  <div class="crow"><span class="ck">MODERATE</span>
                    <span class="cv" style="color:#f5a623">{ls['moderate_risk_km2']} km²</span></div>
                  <div class="crow"><span class="ck">ACCURACY</span>
                    <span class="cv">{ls['accuracy']}%</span></div>
                  <div class="crow"><span class="ck">AUC</span>
                    <span class="cv" style="color:{'#00c48c' if ls.get('auc',0)>0.7 else '#f5a623'}">{ls.get('auc', 'N/A')}</span></div>
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div style="font-family:var(--mono);font-size:10px;color:var(--muted);'
                            'padding:12px">Not yet analyzed</div>', unsafe_allow_html=True)

        # Combined export
        if has_any:
            export_data = {}
            if lur: export_data['lulc'] = lur['stats']
            if dr: export_data['deforestation'] = dr['stats']
            if gr: export_data['snow_cover'] = gr['stats']
            if lr: export_data['landslide'] = lr['stats']
            st.download_button("⬇ EXPORT ALL STATS (JSON)",
                               data=json.dumps(export_data, indent=2),
                               file_name="terrain_guardian_results.json",
                               mime="application/json", key="export_all")


# ═══════════════════════════════════════════════════════════════
#  FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="foot">
  TERRAIN GUARDIAN · Google Earth Engine · Sentinel-2 + Landsat + NASADEM ·
  NDVI · NDSI · Random Forest · Snow Cover + Deforestation + Landslide Susceptibility
</div>
""", unsafe_allow_html=True)
