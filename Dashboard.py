import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
import folium
from pathlib import Path
from streamlit_folium import st_folium
from branca.element import MacroElement, Template

# ============================================================
# 1. KONFIGURASI HALAMAN & TEMA
# ============================================================
st.set_page_config(
    page_title="Nowcasting Produktivitas Padi Sumatera Barat",
    page_icon="🌾",
    layout="wide",
)

HIJAU = "#1F5B3A"
HIJAU_MUDA = "#6FA86B"
EMAS = "#D9A21B"
LANGIT = "#E8F1EC"
TINTA = "#16261D"
TEAL = "#2A7F6A"
TERRACOTTA = "#C0553A"

st.markdown(
    f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"], .stApp {{ font-family: 'Plus Jakarta Sans', sans-serif; color: {TINTA}; }}
.stApp {{ background: #F6F9F6; }}
.block-container {{ padding-top: 1.5rem; max-width: 1400px; }}
h1, h2, h3 {{ font-family: 'Fraunces', serif !important; color: {HIJAU}; letter-spacing: -0.01em; }}
h3 {{ font-size: 1.25rem !important; margin-top: .2rem; }}

.st-key-hero {{
    background: linear-gradient(120deg, {HIJAU} 0%, #2F7A4C 60%, #4E9461 100%);
    border-radius: 20px; padding: 2rem 2.4rem; color: #fff; margin-bottom: 1.2rem;
    position: relative; overflow: hidden;
}}
.st-key-hero::after {{
    content: "🌾"; position: absolute; right: 2rem; bottom: -1.2rem;
    font-size: 9rem; opacity: .16; transform: rotate(-12deg); pointer-events: none;
}}
.st-key-hero h1 {{ color: #fff !important; font-size: 2.2rem; margin: 0 0 .4rem 0; padding: 0; }}
.st-key-hero p {{ margin: 0; max-width: 660px; opacity: .92; line-height: 1.6; }}
.badge {{
    display: inline-block; background: rgba(255,255,255,.16); border-radius: 999px;
    padding: .25rem .8rem; font-size: .8rem; margin-bottom: .8rem;
}}

.kpi {{
    background: #fff; border-radius: 16px; padding: 1rem 1.2rem;
    border: 1px solid #DCE8DF; border-left: 6px solid {EMAS}; height: 100%;
}}
.kpi .label {{ font-size: .85rem; color: #5B6F63; }}
.kpi .nilai {{ font-family: 'Fraunces', serif; font-size: 1.8rem; font-weight: 700; color: {HIJAU}; line-height: 1.25; }}
.kpi .nilai small {{ font-family: 'Plus Jakarta Sans'; font-size: .85rem; font-weight: 500; color: #5B6F63; }}
.sub {{ color: #5B6F63; font-size: .85rem; margin: 1rem 0 .4rem; }}

div[data-testid="stSelectbox"] label, div[data-testid="stRadio"] > label {{ font-weight: 600; color: {HIJAU}; }}
.stTabs [data-baseweb="tab-list"] {{ gap: .3rem; border-bottom: 1px solid #DCE8DF; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 10px 10px 0 0; padding: .5rem 1rem; font-weight: 600; }}
.stTabs [aria-selected="true"] {{ color: {HIJAU}; background: {LANGIT}; }}
.foot {{ color:#5B6F63; font-size:.8rem; margin-top:2rem; text-align:center; }}

/* ---------- Navigasi halaman ---------- */
.st-key-nav {{ display: flex; justify-content: flex-end; position: relative; z-index: 2; }}
.st-key-nav div[role="radiogroup"] {{
    background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.28);
    border-radius: 999px; padding: .3rem; display: inline-flex; gap: .2rem;
    backdrop-filter: blur(4px);
}}
.st-key-nav div[role="radiogroup"] label {{
    border-radius: 999px; padding: .35rem 1.3rem; margin: 0;
    font-weight: 600; letter-spacing: .04em; cursor: pointer;
}}
.st-key-nav div[role="radiogroup"] label > div:first-child {{ display: none; }}
.st-key-nav div[role="radiogroup"] label p {{ color: #fff !important; font-size: .9rem; }}
.st-key-nav div[role="radiogroup"] label:has(input:checked) {{ background: #fff; }}
.st-key-nav div[role="radiogroup"] label:has(input:checked) p {{ color: {HIJAU} !important; }}

/* ---------- Halaman About ---------- */
.ab-judul {{
    font-family: 'Fraunces', serif; color: {HIJAU}; font-size: 1.7rem; font-weight: 700;
    margin: 2rem 0 .8rem; display: flex; align-items: center; gap: .6rem;
}}
.ab-judul::before {{
    content: ""; width: 6px; height: 1.6rem; background: {EMAS}; border-radius: 4px;
}}
.ab-card {{
    background: #fff; border: 1px solid #DCE8DF; border-radius: 18px;
    padding: 1.4rem 1.6rem; line-height: 1.75; color: {TINTA};
    box-shadow: 0 2px 10px rgba(31,91,58,.05);
}}
.ab-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; }}
@media (max-width: 900px) {{ .ab-grid {{ grid-template-columns: 1fr; }} }}
.ab-grid4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.2rem; }}
@media (max-width: 1100px) {{ .ab-grid4 {{ grid-template-columns: repeat(2, 1fr); }} }}
@media (max-width: 600px) {{ .ab-grid4 {{ grid-template-columns: 1fr; }} }}
.ab-grid4 .ab-box {{ min-height: 0; }}
.ab-box {{
    background: {LANGIT}; border-radius: 18px; padding: 1.6rem; min-height: 300px;
    border: 1px solid #D3E4D9; transition: transform .2s, box-shadow .2s;
}}
.ab-box:hover {{ transform: translateY(-4px); box-shadow: 0 10px 24px rgba(31,91,58,.12); }}
.ab-ikon {{
    width: 58px; height: 58px; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 1.6rem; color: #fff; margin-bottom: 1.1rem;
}}
.ab-box h4 {{
    font-family: 'Fraunces', serif; color: {HIJAU}; font-size: 1.2rem; margin: 0 0 .6rem;
}}
.ab-box p {{ margin: 0; line-height: 1.7; font-size: .97rem; }}
.ab-banner {{
    background: {HIJAU}; color: #fff; border-radius: 14px; padding: 1.1rem 1.6rem;
    margin-top: 1.2rem; font-size: .97rem; display: flex; gap: .8rem; align-items: center;
}}
.ab-info {{
    background: #E3EFE8; border-left: 6px solid {HIJAU}; border-radius: 14px;
    padding: 1.1rem 1.5rem; margin: 1.2rem 0; color: {HIJAU}; line-height: 1.7;
    display: flex; gap: .9rem; align-items: flex-start;
}}
.ab-info .em {{ font-size: 1.5rem; }}
.ab-dev {{ display: flex; gap: 1.2rem; align-items: center; flex-wrap: wrap; }}
.ab-avatar {{
    width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg,{HIJAU},{HIJAU_MUDA});
    color: #fff; display: flex; align-items: center; justify-content: center; font-size: 1.8rem;
}}
div[data-testid="stExpander"] {{
    background: #fff; border: 1px solid #DCE8DF !important; border-radius: 14px !important;
    margin-bottom: .7rem; overflow: hidden;
}}
div[data-testid="stExpander"] summary {{ font-weight: 600; color: {HIJAU}; }}
</style>
""",
    unsafe_allow_html=True,
)

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
         "Juli", "Agustus", "September", "Oktober", "November", "Desember"]


# ============================================================
# 2. LOAD DATA (4 file Excel + batas wilayah)
# ============================================================
FOLDER = Path(__file__).parent


@st.cache_data
def muat_data():
    f = "dashboard_{}_{}_2025_2026.xlsx"
    data = {
        ("Bulanan", "prov"): pd.read_excel(FOLDER / f.format("provinsi", "bulanan")),
        ("Bulanan", "kab"): pd.read_excel(FOLDER / f.format("kabkot", "bulanan")),
        ("Subround", "prov"): pd.read_excel(FOLDER / f.format("provinsi", "subround")),
        ("Subround", "kab"): pd.read_excel(FOLDER / f.format("kabkot", "subround")),
    }
    for (mode, _), d in data.items():
        if mode == "Bulanan":
            d["Label"] = d["Bulan"].map(lambda b: BULAN[b - 1]) + " " + d["Tahun"].astype(str)
            d["Urut"] = d["Tahun"] * 100 + d["Bulan"]
        else:
            d["Label"] = d["Subround"] + " " + d["Tahun"].astype(str)
            d["Urut"] = d["Tahun"] * 10 + d["Subround"].str[-1].astype(int)
    return data


@st.cache_data
def muat_geo():
    # Mendukung shapefile (.shp) maupun .json/.geojson
    kandidat = (sorted(FOLDER.glob("*.shp")) + sorted(FOLDER.glob("*.json"))
                + sorted(FOLDER.glob("*.geojson")))
    pilihan = [k for k in kandidat if "sumbar" in k.name.lower() or "batas" in k.name.lower()]
    kandidat = pilihan or kandidat
    if not kandidat:
        st.error("File peta tidak ditemukan. Letakkan 'Batas Wilayah Sumbar' (.shp/.json) "
                 "di folder yang sama dengan Dashboard.py.")
        st.stop()
    g = gpd.read_file(kandidat[0])
    if g.crs is not None and g.crs.to_epsg() != 4326:
        g = g.to_crs(epsg=4326)
    return g


data = muat_data()
geo = muat_geo()


# ============================================================
# 3. FUNGSI PETA & GRAFIK
# ============================================================
class PasKeBingkai(MacroElement):
    """Hitung ulang posisi peta setelah bingkai selesai ditampilkan,
    supaya seluruh wilayah pas di tengah (legenda diberi ruang di atas)."""

    def __init__(self, batas):
        super().__init__()
        self._name = "PasKeBingkai"
        self.batas = batas
        self._template = Template("""
        {% macro script(this, kwargs) %}
        (function () {
            var peta = {{ this._parent.get_name() }};
            var batas = {{ this.batas }};
            function pas() {
                peta.invalidateSize();
                peta.fitBounds(batas, {paddingTopLeft: [0, 60], paddingBottomRight: [0, 0]});
            }
            setTimeout(pas, 100);
            setTimeout(pas, 600);
            window.addEventListener("resize", pas);
        })();
        {% endmacro %}
        """)


def buat_peta(data_peta):
    geo_peta = geo.merge(data_peta, left_on="gaul2_name", right_on="Kabupaten", how="left")
    geo_kab = geo_peta[geo_peta["gaul2_name"] != "Danau"]
    geo_danau = geo_peta[geo_peta["gaul2_name"] == "Danau"]

    geo_map = geo_kab[["gaul2_name", "Prediksi", "geometry"]].copy()
    geo_map["Prediksi_txt"] = geo_map["Prediksi"].map(
        lambda v: f"{v:.2f} ku/ha" if pd.notna(v) else "-")

    minx, miny, maxx, maxy = geo_kab.total_bounds
    m = folium.Map(
        location=[(miny + maxy) / 2, (minx + maxx) / 2], zoom_start=8,
        min_zoom=5, max_zoom=9, zoomSnap=0.1, tiles=None,
        dragging=False, scrollWheelZoom=False, doubleClickZoom=False,
        touchZoom=False, boxZoom=False, keyboard=False, zoom_control=False,
    )
    m.get_root().html.add_child(folium.Element(
        f"<style>.leaflet-container{{background:{LANGIT};font-family:sans-serif;}}</style>"))
    batas = [[float(miny), float(minx)], [float(maxy), float(maxx)]]
    m.fit_bounds(batas, padding_top_left=(0, 60), padding_bottom_right=(0, 0))
    m.add_child(PasKeBingkai(batas))

    folium.Choropleth(
        geo_data=geo_map[["gaul2_name", "Prediksi", "geometry"]].to_json(),
        data=geo_map, columns=["gaul2_name", "Prediksi"],
        key_on="feature.properties.gaul2_name",
        fill_color="YlGn", fill_opacity=0.85, line_opacity=0.9, line_color="#ffffff",
        nan_fill_color="#D9DED9", legend_name="Prediksi produktivitas (ku/ha)",
    ).add_to(m)

    m.get_root().html.add_child(folium.Element("""
    <style>
    .legend.leaflet-control {
        transform: scale(0.8);
        transform-origin: top right;
    }
    </style>
    """))

    folium.GeoJson(
        geo_map.to_json(),
        style_function=lambda f: {"fillOpacity": 0, "weight": 0},
        highlight_function=lambda f: {"weight": 3, "color": EMAS, "fillOpacity": 0.1},
        tooltip=folium.GeoJsonTooltip(
            fields=["gaul2_name", "Prediksi_txt"], aliases=["Wilayah", "Prediksi"],
            style="font-family: sans-serif; font-size: 13px;",
        ),
    ).add_to(m)

    if not geo_danau.empty:
        folium.GeoJson(
            geo_danau[["gaul2_name", "geometry"]].to_json(),
            style_function=lambda f: {"fillColor": "#87CEEB", "fillOpacity": 0.85,
                                      "color": "#5DADE2", "weight": 1},
            tooltip="Danau",
        ).add_to(m)
    return m


def grafik_tren(df, judul):
    df = df.sort_values("Urut")
    labels = df["Label"].tolist()
    now = df[df["Aktual"].isna()]
    fig = go.Figure()
    if not now.empty:
        fig.add_vrect(
            x0=now["Label"].iloc[0], x1=labels[-1],
            fillcolor=EMAS, opacity=0.12, line_width=0,
            annotation_text="Nowcast", annotation_position="top left",
            annotation_font_color="#8A6410",
        )
    fig.add_trace(go.Scatter(
        x=labels, y=df["Aktual"], name="Aktual", mode="lines+markers",
        line=dict(color=HIJAU, width=3), marker=dict(size=6),
    ))
    fig.add_trace(go.Scatter(
        x=labels, y=df["Prediksi"], name="Prediksi / Nowcast", mode="lines+markers",
        line=dict(color=EMAS, width=3, dash="dot"), marker=dict(size=7, symbol="diamond"),
    ))
    fig.update_layout(
        title=dict(text=judul, font=dict(family="Fraunces", size=16, color=HIJAU)),
        height=400, hovermode="x unified", plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=55, b=10),
        legend=dict(orientation="h", y=1.14, x=1, xanchor="right"),
        yaxis=dict(title="Produktivitas (ku/ha)", gridcolor="#E5EEE8", zeroline=False),
        xaxis=dict(categoryorder="array", categoryarray=labels, tickangle=-35, showgrid=False),
        font=dict(family="Plus Jakarta Sans"),
    )
    return fig


# ============================================================
# 4. HALAMAN DASHBOARD
# ============================================================
def kartu(label, nilai, satuan=""):
    return (f'<div class="kpi"><div class="label">{label}</div>'
            f'<div class="nilai">{nilai} <small>{satuan}</small></div></div>')


def render(mode):
    prov = data[(mode, "prov")].sort_values("Urut").reset_index(drop=True)
    kab = data[(mode, "kab")].sort_values(["Kabupaten", "Urut"]).reset_index(drop=True)
    urutan_label = prov["Label"].tolist()
    nowcast_prov = prov[prov["Aktual"].isna()]
    awal_now = nowcast_prov["Label"].iloc[0] if not nowcast_prov.empty else urutan_label[-1]

    # ---------- Kartu nowcast (hanya Subround) ----------
    if mode == "Subround":
        st.markdown('<div class="sub">Hasil nowcasting provinsi</div>', unsafe_allow_html=True)
        kol = st.columns(max(len(nowcast_prov), 1))
        for c, (_, r) in zip(kol, nowcast_prov.iterrows()):
            c.markdown(kartu(f"Nowcast {r['Label']}", f"{r['Prediksi']:.2f}", "ku/ha"),
                       unsafe_allow_html=True)
    st.write("")

    # ---------- Peta + grafik ----------
    col_map, col_chart = st.columns([1, 1.25], gap="large")

    with col_map:
        st.markdown("### Peta nowcasting kabupaten/kota")

        # Peta hanya untuk tahun 2026
        label_peta = prov.loc[prov["Tahun"] == 2026, "Label"].tolist()
        idx_awal = label_peta.index(awal_now) if awal_now in label_peta else 0

        periode_peta = st.selectbox(
            "Pilih periode:", label_peta, index=idx_awal,
            key=f"periode_{mode}",
        )
        data_peta = kab[kab["Label"] == periode_peta].copy()
        st_folium(buat_peta(data_peta), use_container_width=True, height=460,
                  returned_objects=[], key=f"peta_{mode}")

    def grafik_kab():
        st.markdown("### Produktivitas kabupaten/kota")
        pilihan = st.selectbox("Pilih Kabupaten/Kota:", sorted(kab["Kabupaten"].unique()),
                               key=f"kab_{mode}")
        st.plotly_chart(
            grafik_tren(kab[kab["Kabupaten"] == pilihan],
                        f"Produktivitas {pilihan} ({mode.lower()})"),
            use_container_width=True, key=f"grafik_kab_{mode}",
        )

    with col_chart:
        tab_prov, tab_kab = st.tabs(["📈 Provinsi", "📍 Kabupaten/Kota"])
        with tab_prov:
            st.markdown("### Produktivitas padi provinsi")
            st.plotly_chart(
                grafik_tren(prov, f"Produktivitas Sumatera Barat ({mode.lower()})"),
                use_container_width=True, key=f"prov_{mode}",
            )
        with tab_kab:
            grafik_kab()


def halaman_dashboard():
    mode = st.radio(
        "Cakupan waktu",
        ["Subround", "Bulanan"],
        horizontal=True,
        help="Subround adalah periode empat bulanan: Subround 1 (Jan–Apr), 2 (Mei–Agu), 3 (Sep–Des).",
    )
    render(mode)


# ============================================================
# 5. HALAMAN ABOUT
# ============================================================
def halaman_about():
    # ---------- Tentang proyek ----------
    st.markdown('<div class="ab-judul">Tentang Proyek Ini</div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="ab-card">
<i>Dashboard</i> ini memvisualisasikan hasil <i>nowcasting</i> produktivitas padi Provinsi Sumatera Barat
pada level provinsi dan kabupaten/kota, dalam cakupan bulanan maupun <i>subround</i>. Tujuannya membantu
pemantauan kondisi produktivitas padi sebelum data aktual dipublikasi. <i>Dashboard</i> ini dibangun sebagai artefak
skripsi mahasiswa Politeknik Statistika STIS Program Studi D-IV Komputasi Statistik.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="ab-info">
<span class="em">💡</span>
<div>Model terbaik yang diperoleh adalah <b><i>Ridge</i></b> dengan fitur akhir EVI dan agroklimatologi 
<b><i>lag</i> 2 dengan <i>dummy</i> kabupaten/kota</b>.</div>
</div>
""",
        unsafe_allow_html=True,
    )

    k1, k2, k3 = st.columns(3)
    k1.markdown(kartu("R²", "0,726679"), unsafe_allow_html=True)
    k2.markdown(kartu("MAE", "3,718341", "ku/ha"), unsafe_allow_html=True)
    k3.markdown(kartu("RMSE", "4,626186", "ku/ha"), unsafe_allow_html=True)

    # ---------- Data dan metodologi ----------
    st.markdown('<div class="ab-judul">Data dan Metodologi</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="margin-bottom:.8rem">Data yang digunakan merupakan gabungan dari beberapa '
        'sumber dengan beberapa kandidat model <i>machine learning</i>.</div>',
        unsafe_allow_html=True,
    )

    with st.expander("🗂️  Lihat Detail Sumber Data dan Model"):
        st.markdown(
            """
**Sumber data**
- Produktivitas padi (ku/ha): BPS
- EVI: Terra-MODIS MOD13Q1.061
- Curah hujan (mm): CHIRPS
- Suhu udara (°C): ERA5-Land
- *Soil moisture* (m³/m³): ERA5-Land
- *Solar radiation* (MJ/m²): ERA5-Land

**Kandidat model**
- *Ridge Regression*
- *Lasso Regression*
- *Elastic Net*
- *Random Forest*
- XGBoost

**Evaluasi**
- R²
- RMSE
- MAE
"""
        )

# ---------- Seberapa dekat prediksi dengan aktual ----------
    st.markdown('<div class="ab-judul">Seberapa Dekat Prediksi dengan Aktual?</div>',
                unsafe_allow_html=True)
    st.markdown(
        f"""
<div class="ab-grid">
<div class="ab-box">
<div class="ab-ikon" style="background:{TEAL}">✔</div>
<h4>Mengikuti pola aktual</h4>
<p>Dharmasraya, Kota Padang, Kota Sawahlunto, Tanah Datar, Solok mengikuti pola aktual (bulanan).
Pasaman dan Kota Payakumbuh menunjukkan prediksi yang relatif mendekati nilai aktual
pada beberapa <i>subround</i>.</p>
</div>
<div class="ab-box">
<div class="ab-ikon" style="background:{EMAS}">⚖</div>
<h4>Bias antarwilayah</h4>
<p>Prediksi cenderung lebih tinggi dari aktual: Agam, Tanah Datar. Prediksi cenderung lebih rendah dari aktual:
Kepulauan Mentawai, Lima Puluh Kota.</p>
</div>
<div class="ab-box">
<div class="ab-ikon" style="background:{TERRACOTTA}">🌊</div>
<h4>Faktor di luar model</h4>
<p>Perbedaan Oktober–Desember 2025 diduga terkait cuaca ekstrem dan banjir di Sumbar
yang tidak tertangkap variabel model.</p>
</div>
</div>
<div class="ab-banner">
<span style="font-size:1.3rem">ℹ️</span>
<span>Model dengan pengintegrasian EVI dan variabel agroklimatologi (curah hujan, suhu udara,
<i>soil moisture</i>, dan <i>solar radiation</i>) belum sepenuhnya menangkap perubahan tajam
di beberapa wilayah, dengan galat yang tidak seragam antarperiode maupun antarwilayah.</span>
</div>
""",
        unsafe_allow_html=True,
    )

# ---------- Saran pengembangan ----------
    st.markdown('<div class="ab-judul">Saran Pengembangan</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
<div style="margin-bottom:.8rem">Pengembangan selanjutnya disarankan untuk mempertimbangkan:</div>
<div class="ab-grid4">
<div class="ab-box">
<div class="ab-ikon" style="background:{TEAL}">🌱</div>
<h4>Kondisi lahan</h4>
<p>Misalnya jenis tanah, irigasi, dan ketersediaan air.</p>
</div>
<div class="ab-box">
<div class="ab-ikon" style="background:{TERRACOTTA}">⛈</div>
<h4>Cuaca ekstrem</h4>
<p>Kejadian seperti banjir dan kekeringan yang memengaruhi hasil panen.</p>
</div>
<div class="ab-box">
<div class="ab-ikon" style="background:{EMAS}">🔬</div>
<h4>Variabel lingkungan lain</h4>
<p>Variabel lingkungan yang belum tercakup dalam model.</p>
</div>
<div class="ab-box">
<div class="ab-ikon" style="background:{HIJAU}">📅</div>
<h4>Karakteristik wilayah dan pola tanam</h4>
<p>Misalnya perbedaan jadwal tanam antarwilayah.</p>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

def footer():
    """Footer yang sama untuk semua halaman."""
    st.markdown(
        """
<div class="foot" style="border-top:1px solid #DCE8DF; padding-top:1rem;">
Developed by <b>Azizah Najla</b> (222212531@stis.ac.id)<br>
Supervised by Prof. Setia Pramana, S.Si, M.Sc, Ph.D.<br>
<span style="color:#C0553A; font-size:.75rem">v1.0 — September 2026</span>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# 6. HEADER + NAVIGASI
# ============================================================
with st.container(key="hero"):
    kol_judul, kol_nav = st.columns([2.2, 1])
    with kol_judul:
        st.markdown(
            """
<span class="badge">Provinsi Sumatera Barat</span>
<h1>Nowcasting Produktivitas Padi</h1>
""",
            unsafe_allow_html=True,
        )
    with kol_nav:
        halaman = st.radio(
            "Navigasi", ["Dashboard", "About"], horizontal=True,
            label_visibility="collapsed", key="nav",
        )

if halaman == "Dashboard":
    halaman_dashboard()
else:
    halaman_about()

footer()
