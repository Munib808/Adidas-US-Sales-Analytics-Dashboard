### Importing required modules
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# ===============================
# PAGE CONFIG (must be first)
# ===============================
st.set_page_config(
    page_title="Adidas US Sales Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CUSTOM CSS — DARK ATHLETIC THEME
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── GLOBAL ─── */
.stApp {
    background: #07080D;
    font-family: 'Outfit', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }

/* ─── ANIMATED BG ─── */
.stApp > div:first-child::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 60% 50% at 5% 10%, rgba(0, 0, 0, 0.3) 0%, transparent 50%),
        radial-gradient(ellipse 50% 60% at 95% 90%, rgba(255, 255, 255, 0.015) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0C0D14 0%, #0F1018 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.04) !important;
}
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #E2E8F0 !important;
    font-family: 'Outfit', sans-serif !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span {
    color: #94A3B8 !important;
    font-family: 'Outfit', sans-serif !important;
}
/* Sidebar title override */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1 {
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.01em !important;
    color: #F8FAFC !important;
    padding-bottom: 0.75rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.06) !important;
    margin-bottom: 1rem !important;
}
/* Sidebar radio */
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label {
    color: #CBD5E1 !important;
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 10px !important;
    padding: 0.5rem 0.85rem !important;
    margin-bottom: 4px !important;
    transition: all 0.3s ease !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] label:hover {
    border-color: rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.04) !important;
}
/* Sidebar multiselect */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {
    background: rgba(255,255,255,0.03) !important;
    border-color: rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
}
[data-testid="stSidebar"] .stMultiSelect span {
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 6px !important;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span {
    color: #E2E8F0 !important;
    font-size: 12px !important;
}

/* ─── TYPOGRAPHY ─── */
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Outfit', sans-serif !important;
    color: #F1F5F9 !important;
}
p, span, li, .stMarkdown p {
    color: #94A3B8 !important;
    font-family: 'Outfit', sans-serif !important;
}

/* Main title */
.main-title {
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 0.25rem;
    background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.main-sub {
    font-size: 0.9rem;
    color: #475569 !important;
    font-weight: 300;
}

/* ─── HERO BADGE ─── */
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #E2E8F0;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 100px;
    padding: 5px 14px;
    background: rgba(255,255,255,0.04);
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ─── METRIC CARDS ─── */
[data-testid="stMetric"] {
    background: rgba(15, 17, 26, 0.7) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.25rem !important;
    transition: all 0.3s ease !important;
    position: relative;
    overflow: hidden;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}
[data-testid="stMetric"]:hover {
    border-color: rgba(255,255,255,0.1) !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 24px rgba(0,0,0,0.3) !important;
}
[data-testid="stMetric"] label {
    color: #64748B !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #F1F5F9 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
}
[data-testid="stMetric"] [data-testid="stMetricDelta"] {
    font-family: 'JetBrains Mono', monospace !important;
}

/* ─── SECTION HEADERS ─── */
.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2rem 0 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.sh-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}
.sh-text {
    font-size: 1rem;
    font-weight: 600;
    color: #E2E8F0 !important;
}
.sh-sub {
    font-size: 0.7rem;
    color: #475569 !important;
    margin-top: 1px;
}

/* ─── DATAFRAME ─── */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* ─── TABS ─── */
[data-testid="stTabs"] button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    color: #64748B !important;
    border: none !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.3s ease !important;
    font-size: 14px !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #F1F5F9 !important;
    border-bottom: 2px solid #F1F5F9 !important;
}
[data-testid="stTabs"] button:hover {
    color: #CBD5E1 !important;
}

/* ─── EXPANDER ─── */
[data-testid="stExpander"] {
    background: rgba(15, 17, 26, 0.5) !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 14px !important;
}
[data-testid="stExpander"] summary {
    color: #CBD5E1 !important;
    font-weight: 500 !important;
}
[data-testid="stExpander"] .stMarkdown p,
[data-testid="stExpander"] .stMarkdown li {
    color: #94A3B8 !important;
    font-size: 13px !important;
    line-height: 1.8 !important;
}

/* ─── DATE INPUT ─── */
[data-testid="stDateInput"] input {
    background: rgba(15, 17, 26, 0.8) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
}
[data-testid="stDateInput"] input:focus {
    border-color: rgba(255,255,255,0.2) !important;
}
[data-testid="stDateInput"] label {
    color: #94A3B8 !important;
    font-size: 13px !important;
}

/* ─── SUBHEADER STYLING ─── */
.stMarkdown h2 {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    margin-top: 1.75rem !important;
    margin-bottom: 0.75rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.04) !important;
}
.stMarkdown h3 {
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: #CBD5E1 !important;
}

/* ─── DIVIDER ─── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.04) !important;
    margin: 1.5rem 0 !important;
}

/* ─── TEXT BLOCK ─── */
.styled-text {
    font-size: 14px;
    color: #94A3B8 !important;
    line-height: 1.85;
    background: rgba(15, 17, 26, 0.5);
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 14px;
    padding: 1.5rem;
}

/* ─── CHART CONTAINERS ─── */
[data-testid="stVegaLiteChart"],
[data-testid="stPlotlyChart"] {
    background: rgba(15, 17, 26, 0.5) !important;
    border: 1px solid rgba(255,255,255,0.04) !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
    overflow: hidden !important;
}

/* ─── FOOTER ─── */
.app-footer {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    margin-top: 3rem;
    border-top: 1px solid rgba(255,255,255,0.03);
}
.ft { font-size: 0.6rem; color: #334155 !important; letter-spacing: 0.12em; text-transform: uppercase; }
.ft-tags { display: flex; justify-content: center; gap: 8px; margin-top: 0.5rem; flex-wrap: wrap; }
.ft-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.55rem;
    color: #475569;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.04);
    padding: 2px 8px;
    border-radius: 4px;
}

/* ─── RESPONSIVE ─── */
@media (max-width: 768px) {
    .main-title { font-size: 1.5rem; }
    [data-testid="stMetric"] { padding: 0.85rem 1rem !important; }
    [data-testid="stMetric"] [data-testid="stMetricValue"] { font-size: 1.2rem !important; }
}
</style>
""", unsafe_allow_html=True)


# ===============================
# PLOTLY THEME HELPER
# ===============================
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Outfit, sans-serif", color="#94A3B8", size=12),
    title_font=dict(family="Outfit, sans-serif", color="#E2E8F0", size=15),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
        font=dict(color="#94A3B8", size=11)
    ),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.03)",
        zerolinecolor="rgba(255,255,255,0.05)",
        tickfont=dict(color="#64748B"),
        title_font=dict(color="#94A3B8")
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.03)",
        zerolinecolor="rgba(255,255,255,0.05)",
        tickfont=dict(color="#64748B"),
        title_font=dict(color="#94A3B8")
    ),
    margin=dict(l=20, r=20, t=50, b=20),
    hoverlabel=dict(bgcolor="#1E293B", font_color="#F1F5F9", bordercolor="rgba(255,255,255,0.1)")
)

# Adidas-inspired color palette
COLORS = ["#FFFFFF", "#A3A3A3", "#64748B", "#CBD5E1", "#94A3B8", "#475569", "#E2E8F0"]
COLORS_VIVID = ["#38BDF8", "#818CF8", "#FB7185", "#34D399", "#FBBF24", "#A78BFA", "#F472B6"]


# ===============================
# DATA
# ===============================
@st.cache_data
def load_data():
    df = pd.read_csv("adidas_cleaned.xls")
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['month_name'] = pd.Categorical(df['month_name'], categories=month_order, ordered=True)
    return df

df = load_data()

# ─── SIDEBAR ───
st.sidebar.title("ADIDAS SALES DATA Analysis 2020 - 2021")
try:
    img = Image.open("logo.png")
    st.sidebar.image(img)
except:
    st.sidebar.markdown("""
    <div style="text-align:center;padding:1rem 0;">
        <span style="font-size:2.5rem;font-weight:800;color:#FFFFFF;letter-spacing:-0.05em;">adidas</span>
    </div>
    """, unsafe_allow_html=True)

side = st.sidebar.radio("Go to", ["Data Set Overview", "DashBoard"])


# ===============================
# PAGE: DATA SET OVERVIEW
# ===============================
if side == "Data Set Overview":
    st.markdown("""
    <div class="hero-badge">👟 Adidas US Sales</div>
    <div class="main-title">Sales Dashboard<br>2020 — 2021</div>
    <div class="main-sub">Comprehensive analysis of Adidas US retail performance across regions, products, and channels.</div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="section-header">
        <div class="sh-icon" style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.12);">📊</div>
        <div>
            <div class="sh-text">Dataset Overview</div>
            <div class="sh-sub">About the Adidas US sales dataset</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="styled-text">
        An Adidas sales dataset is a collection of data that includes information on the sales of Adidas products.
        This type of dataset may include details such as the number of units sold, the total sales revenue,
        the location of the sales, the type of product sold, and any other relevant information.
        Adidas sales data can be useful for a variety of purposes, such as analyzing sales trends,
        identifying successful products or marketing campaigns, and developing strategies for future sales.
        It can also be used to compare Adidas sales to those of competitors, or to analyze the effectiveness of different marketing or sales channels.
        There are a variety of sources that could potentially provide an Adidas sales dataset,
        including Adidas itself, market research firms, government agencies, or other organizations that track sales data.
        The specific data points included in an Adidas sales dataset may vary depending on the source and the purpose for which it is being used.
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-header">
        <div class="sh-icon" style="background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.12);">📋</div>
        <div>
            <div class="sh-text">Column Description</div>
            <div class="sh-sub">What each field in the dataset represents</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("Dataset Column Details"):
        st.markdown("""
        - **retailer**: Retailer selling Adidas products  
        - **region**: Geographic region in the US  
        - **state**: State where the sale happened  
        - **city**: City of the sale  

        - **product**: Product category  
        - **sales_method**: Sales channel (In-store / Online / Outlet)  

        - **price_per_unit**: Price per item  
        - **units_sold**: Number of items sold  
        - **total_sales**: Total revenue generated  
        - **operating_profit**: Profit after operating costs  
        - **operating_margin**: Profit percentage  

        - **invoice_date**: Date of transaction  
        - **year**: Year of sale  
        - **month**: Month number  
        - **month_name**: Month name
        """)

    st.markdown("""
    <div class="section-header">
        <div class="sh-icon" style="background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.12);">🗃️</div>
        <div>
            <div class="sh-text">Dataset Preview</div>
            <div class="sh-sub">First few rows of the dataset</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(df.head(), use_container_width=True)


# ===============================
# PAGE: DASHBOARD
# ===============================
if side == "DashBoard":
    option = st.sidebar.radio("Go To ", ["Univariate Analysis", "Bivariate Analysis and Multivariate Analysis"])

    if option == "Univariate Analysis":
        st.markdown("""
        <div class="hero-badge">📈 Performance Metrics</div>
        <div class="main-title">Univariate Analysis</div>
        <div class="main-sub">Key performance indicators across the full dataset and custom date ranges.</div>
        """, unsafe_allow_html=True)

        st.divider()

        df["invoice_date"] = pd.to_datetime(df["invoice_date"])
        df_2020 = df[(df["invoice_date"] >= "2020-01-01") & (df["invoice_date"] <= "2020-12-31")]
        df_2021 = df[(df["invoice_date"] >= "2021-01-01") & (df["invoice_date"] <= "2021-12-31")]

        # ─── OVERALL KPIs ───
        st.markdown("""
        <div class="section-header">
            <div class="sh-icon" style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.12);">🎯</div>
            <div>
                <div class="sh-text">Overall Performance</div>
                <div class="sh-sub">Aggregated across 2020–2021</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"${df['total_sales'].sum():,.0f}")
        col2.metric("Total Units Sold", f"{df['units_sold'].sum():,.0f}")
        col3.metric("Total Operating Profit", f"${df['operating_profit'].sum():,.0f}")

        # ─── YEAR-WISE ───
        st.markdown("""
        <div class="section-header">
            <div class="sh-icon" style="background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.12);">📅</div>
            <div>
                <div class="sh-text">Year-over-Year Comparison</div>
                <div class="sh-sub">2020 vs 2021 performance breakdown</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col4, col5 = st.columns(2)
        col4.metric("Avg Operating Margin (2020) in Percent", f"{df_2020['operating_margin'].mean():,.0f}")
        col5.metric("Avg Operating Margin (2021) in Percent", f"{df_2021['operating_margin'].mean():,.0f}")

        col6, col7, col8 = st.columns(3)
        col6.metric("Total Sales (2020)", f"${df_2020['total_sales'].sum():,.0f}")
        col7.metric("Total Sales (2021)", f"${df_2021['total_sales'].sum():,.0f}")
        col8.metric("Units Sold (2020)", f"{df_2020['units_sold'].sum():,.0f}")

        col9, col10, col11 = st.columns(3)
        col9.metric("Units Sold (2021)", f"{df_2021['units_sold'].sum():,.0f}")
        col10.metric("Operating Profit (2020)", f"${df_2020['operating_profit'].sum():,.0f}")
        col11.metric("Operating Profit (2021)", f"${df_2021['operating_profit'].sum():,.0f}")

        st.metric("Overall Avg Operating Margin in Percent", f"{df['operating_margin'].mean():,.0f}")

        # ─── DYNAMIC PERIOD ───
        st.markdown("""
        <div class="section-header">
            <div class="sh-icon" style="background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.12);">🔍</div>
            <div>
                <div class="sh-text">Dynamic Period Analysis</div>
                <div class="sh-sub">Select a custom date range to explore</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.caption("Use the date pickers below to filter metrics for any custom period.")

        d1, d2 = st.columns(2)
        with d1:
            start_date = st.date_input("Start Date", value=pd.to_datetime("2020-01-01"))
        with d2:
            end_date = st.date_input("End Date", value=pd.to_datetime("2021-12-31"))

        start_ts = pd.Timestamp(start_date)
        end_ts = pd.Timestamp(end_date)
        df_period = df[(df["invoice_date"] >= start_ts) & (df["invoice_date"] <= end_ts)]

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", f"${df_period['total_sales'].sum():,.0f}")
        col2.metric("Total Units Sold", f"{df_period['units_sold'].sum():,.0f}")
        col3.metric("Total Operating Profit", f"${df_period['operating_profit'].sum():,.0f}")

        col4, col5 = st.columns(2)
        col4.metric("Average Operating Margin", f"{df_period['operating_margin'].mean():,.0f}")


    # ===============================
    # BIVARIATE & MULTIVARIATE
    # ===============================
    if option == "Bivariate Analysis and Multivariate Analysis":

        tab1, tab2 = st.tabs(["📊 Graphs", "📋 Filtered KPIs"])

        with tab1:
            st.markdown("""
            <div class="hero-badge">📊 Deep Analysis</div>
            <div class="main-title">Bivariate & Multivariate</div>
            <div class="main-sub">Explore relationships between variables with interactive filters.</div>
            """, unsafe_allow_html=True)

            st.divider()

            # ─── SIDEBAR FILTERS ───
            region = st.sidebar.multiselect("Select Region", options=df["region"].unique(), default=df["region"].unique())
            retailer = st.sidebar.multiselect("Select Retailer", options=df["retailer"].unique(), default=df["retailer"].unique())
            product = st.sidebar.multiselect("Select Product", options=df["product"].unique(), default=df["product"].unique())
            sales_method = st.sidebar.multiselect("Select Sales Method", options=df["sales_method"].unique(), default=df["sales_method"].unique())
            year = st.sidebar.multiselect("Select Year", options=sorted(df["year"].unique()), default=sorted(df["year"].unique()))
            state = st.sidebar.multiselect("Select state", options=df["state"].unique(), default=df["state"].unique())
            city = st.sidebar.multiselect("Select city", options=df["city"].unique(), default=df["city"].unique())

            filtered_df = df[
                (df["region"].isin(region)) &
                (df["retailer"].isin(retailer)) &
                (df["product"].isin(product)) &
                (df["sales_method"].isin(sales_method)) &
                (df["year"].isin(year)) &
                (df["state"].isin(state)) &
                (df["city"].isin(city))
            ]

            # ─── FILTERED DATA ───
            st.markdown("""
            <div class="section-header">
                <div class="sh-icon" style="background:rgba(56,189,248,0.08);border:1px solid rgba(56,189,248,0.12);">🗃️</div>
                <div>
                    <div class="sh-text">Filtered Data</div>
                    <div class="sh-sub">{:,} records match current filters</div>
                </div>
            </div>
            """.format(len(filtered_df)), unsafe_allow_html=True)

            st.dataframe(filtered_df, use_container_width=True)

            # ─── SALES BY REGION & PRODUCT ───
            st.markdown("""
            <div class="section-header">
                <div class="sh-icon" style="background:rgba(168,85,247,0.08);border:1px solid rgba(168,85,247,0.12);">📊</div>
                <div>
                    <div class="sh-text">Sales Distribution</div>
                    <div class="sh-sub">By region, product, and sales channel</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                region_sales = filtered_df.groupby("region")["total_sales"].sum().reset_index()
                fig_region = px.bar(region_sales, x="region", y="total_sales",
                                    color_discrete_sequence=["#38BDF8"],
                                    title="Sales by Region")
                fig_region.update_layout(**PLOTLY_LAYOUT)
                fig_region.update_traces(marker_line_width=0, marker_cornerradius=6)
                st.plotly_chart(fig_region, use_container_width=True)

            with col2:
                product_sales = filtered_df.groupby("product")["total_sales"].sum().reset_index()
                fig_product = px.bar(product_sales, x="product", y="total_sales",
                                     color_discrete_sequence=["#818CF8"],
                                     title="Sales by Product")
                fig_product.update_layout(**PLOTLY_LAYOUT)
                fig_product.update_traces(marker_line_width=0, marker_cornerradius=6)
                st.plotly_chart(fig_product, use_container_width=True)

            # Sales by method
            method_sales = filtered_df.groupby("sales_method")["total_sales"].sum().reset_index()
            fig_method = px.bar(method_sales, x="sales_method", y="total_sales",
                                color_discrete_sequence=["#34D399"],
                                title="Sales by Sales Method")
            fig_method.update_layout(**PLOTLY_LAYOUT)
            fig_method.update_traces(marker_line_width=0, marker_cornerradius=6)
            st.plotly_chart(fig_method, use_container_width=True)

            # ─── SALES TRENDS ───
            st.markdown("""
            <div class="section-header">
                <div class="sh-icon" style="background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.12);">📈</div>
                <div>
                    <div class="sh-text">Sales Trends Over Time</div>
                    <div class="sh-sub">Daily aggregated total sales</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            sales_line = filtered_df.groupby("invoice_date")["total_sales"].sum().reset_index()
            fig_line = px.area(sales_line, x="invoice_date", y="total_sales",
                               color_discrete_sequence=["#38BDF8"],
                               title="Sales Trend")
            fig_line.update_layout(**PLOTLY_LAYOUT)
            fig_line.update_traces(line=dict(width=2), fillcolor="rgba(56,189,248,0.06)")
            st.plotly_chart(fig_line, use_container_width=True)

            # ─── TOP & BOTTOM STATES ───
            st.markdown("""
            <div class="section-header">
                <div class="sh-icon" style="background:rgba(251,191,36,0.08);border:1px solid rgba(251,191,36,0.12);">🏆</div>
                <div>
                    <div class="sh-text">Top & Bottom States</div>
                    <div class="sh-sub">By total sales revenue</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            t1, t2 = st.columns(2)
            with t1:
                region_sales_top = filtered_df.groupby("state")["total_sales"].sum().reset_index()
                region_sales_top = region_sales_top.sort_values(by="total_sales", ascending=False).head(5)
                figqq = px.bar(region_sales_top, x="state", y="total_sales",
                               color_discrete_sequence=["#34D399"],
                               title="Top 5 States")
                figqq.update_layout(**PLOTLY_LAYOUT)
                figqq.update_traces(marker_line_width=0, marker_cornerradius=6)
                st.plotly_chart(figqq, use_container_width=True)

            with t2:
                region_sales_bot = filtered_df.groupby("state")["total_sales"].sum().reset_index()
                region_sales_bot = region_sales_bot.sort_values(by="total_sales", ascending=True).head(5)
                figqq1 = px.bar(region_sales_bot, x="state", y="total_sales",
                                color_discrete_sequence=["#FB7185"],
                                title="Bottom 5 States")
                figqq1.update_layout(**PLOTLY_LAYOUT)
                figqq1.update_traces(marker_line_width=0, marker_cornerradius=6)
                st.plotly_chart(figqq1, use_container_width=True)

            # ─── MONTHLY TRENDS ───
            st.markdown("""
            <div class="section-header">
                <div class="sh-icon" style="background:rgba(251,113,133,0.08);border:1px solid rgba(251,113,133,0.12);">📅</div>
                <div>
                    <div class="sh-text">Monthly Trends</div>
                    <div class="sh-sub">Sales and units sold by month</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            mc1, mc2 = st.columns(2)
            with mc1:
                month_sales = filtered_df.groupby("month_name")["total_sales"].sum().reset_index()
                fig_ms = px.line(month_sales, x="month_name", y="total_sales",
                                 color_discrete_sequence=["#FBBF24"],
                                 title="Total Sales by Month", markers=True)
                fig_ms.update_layout(**PLOTLY_LAYOUT)
                fig_ms.update_traces(line=dict(width=2.5))
                st.plotly_chart(fig_ms, use_container_width=True)

            with mc2:
                month_units = filtered_df.groupby("month_name")["units_sold"].sum().reset_index()
                fig_mu = px.line(month_units, x="month_name", y="units_sold",
                                 color_discrete_sequence=["#A78BFA"],
                                 title="Units Sold by Month", markers=True)
                fig_mu.update_layout(**PLOTLY_LAYOUT)
                fig_mu.update_traces(line=dict(width=2.5))
                st.plotly_chart(fig_mu, use_container_width=True)

            # ─── RETAILER PERFORMANCE ───
            st.markdown("""
            <div class="section-header">
                <div class="sh-icon" style="background:rgba(129,140,248,0.08);border:1px solid rgba(129,140,248,0.12);">🏪</div>
                <div>
                    <div class="sh-text">Retailer Performance</div>
                    <div class="sh-sub">Sales and profit by retail partner</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            r1, r2 = st.columns(2)
            with r1:
                ret_sales = filtered_df.groupby("retailer")["total_sales"].sum().reset_index()
                fig_rs = px.bar(ret_sales, x="retailer", y="total_sales",
                                color_discrete_sequence=["#38BDF8"],
                                title="Total Sales by Retailer")
                fig_rs.update_layout(**PLOTLY_LAYOUT)
                fig_rs.update_traces(marker_line_width=0, marker_cornerradius=6)
                st.plotly_chart(fig_rs, use_container_width=True)

            with r2:
                ret_profit = filtered_df.groupby("retailer")["operating_profit"].sum().reset_index()
                fig_rp = px.bar(ret_profit, x="retailer", y="operating_profit",
                                color_discrete_sequence=["#34D399"],
                                title="Operating Profit by Retailer")
                fig_rp.update_layout(**PLOTLY_LAYOUT)
                fig_rp.update_traces(marker_line_width=0, marker_cornerradius=6)
                st.plotly_chart(fig_rp, use_container_width=True)

            # Product profit
            prod_profit = filtered_df.groupby("product")["operating_profit"].sum().reset_index()
            fig_pp = px.bar(prod_profit, x="product", y="operating_profit",
                            color_discrete_sequence=["#F472B6"],
                            title="Operating Profit by Product")
            fig_pp.update_layout(**PLOTLY_LAYOUT)
            fig_pp.update_traces(marker_line_width=0, marker_cornerradius=6)
            st.plotly_chart(fig_pp, use_container_width=True)

            # ─── SCATTER: SALES vs MARGIN ───
            st.markdown("""
            <div class="section-header">
                <div class="sh-icon" style="background:rgba(244,114,182,0.08);border:1px solid rgba(244,114,182,0.12);">🔬</div>
                <div>
                    <div class="sh-text">Sales vs Operating Margin</div>
                    <div class="sh-sub">Relationship between revenue and profitability</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            fig_scatter = px.scatter(
                filtered_df,
                x="total_sales",
                y="operating_margin",
                color="region",
                size="units_sold",
                hover_data=["retailer", "product", "state"],
                labels={
                    "total_sales": "Total Sales ($)",
                    "operating_margin": "Operating Margin (%)"
                },
                title="Total Sales vs Operating Margin",
                color_discrete_sequence=COLORS_VIVID
            )
            fig_scatter.update_layout(**PLOTLY_LAYOUT)
            fig_scatter.update_layout(height=500)
            st.plotly_chart(fig_scatter, use_container_width=True)


        with tab2:
            st.markdown("""
            <div class="hero-badge">📋 Filtered Metrics</div>
            <div class="main-title">Filtered KPIs</div>
            <div class="main-sub">Key metrics for the currently selected data filters.</div>
            """, unsafe_allow_html=True)

            st.divider()

            kpi1, kpi2, kpi3 = st.columns(3)
            kpi1.metric("Total Sales", f"${filtered_df['total_sales'].sum():,.0f}")
            kpi2.metric("Total Units Sold", f"{filtered_df['units_sold'].sum():,.0f}")
            kpi3.metric("Avg Margin", f"{filtered_df['operating_margin'].mean():.1f}%")


# ─── FOOTER ───
st.markdown("""
<div class="app-footer">
    <div class="ft">Adidas US Sales Dashboard — Portfolio Project</div>
    <div class="ft-tags">
        <span class="ft-tag">Streamlit</span>
        <span class="ft-tag">Plotly</span>
        <span class="ft-tag">Pandas</span>
        <span class="ft-tag">Python</span>
    </div>
</div>
""", unsafe_allow_html=True)
