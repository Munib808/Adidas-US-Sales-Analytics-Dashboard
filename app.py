import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Adidas US Sales Analytics",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# CUSTOM CSS — PROFESSIONAL DARK THEME
# ===============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Main App Background */
.stApp {
    background: #0B0E14;
    font-family: 'Outfit', sans-serif;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #0F1219 !important;
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Glassmorphism Cards */
div[data-testid="stMetric"], .chart-container {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

/* Typography Overrides */
h1, h2, h3 {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(90deg, #FFFFFF, #94A3B8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0rem;
}

/* Custom Metric Styling */
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.8rem !important;
}

/* Fix for Multiselect Visibility */
div[data-testid="stMultiSelect"] span {
    color: #0F172A !important;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# PLOTLY THEME
# ===============================
def apply_plotly_style(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit", color="#94A3B8"),
        margin=dict(t=40, b=0, l=0, r=0),
        hovermode="x unified"
    )
    fig.update_xaxes(showgrid=False, color="#475569")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#475569")
    return fig

# ===============================
# DATA LOADING
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

# ===============================
# SIDEBAR
# ===============================
st.sidebar.markdown("<h2 style='font-size: 1.2rem;'>ADIDAS SYSTEMS</h2>", unsafe_allow_html=True)

try:
    img = Image.open("logo.png")
    st.sidebar.image(img, use_column_width=True)
except:
    st.sidebar.info("Upload logo.png to see brand assets.")

side = st.sidebar.radio("Navigation", ["Data Overview", "Interactive Dashboard"])

# ===============================
# PAGE 1: OVERVIEW
# ===============================
if side == "Data Overview":
    st.markdown('<p class="main-title">Sales Intelligence</p>', unsafe_allow_html=True)
    st.markdown("### US Retail Operations 2020—2021")
    
    col_text, col_img = st.columns([2, 1])
    with col_text:
        st.write("""
        This dataset provides a granular view of Adidas US sales performance. 
        It tracks revenue across various retailers, geographic regions, and sales channels 
        (In-store, Online, Outlet) to identify growth drivers and profitability trends.
        """)
        
    with st.expander("Explore Schema Details"):
        st.markdown("""
        | Column | Description |
        | :--- | :--- |
        | **Retailer** | Official partner name |
        | **Total Sales** | Gross revenue (USD) |
        | **Operating Margin** | Efficiency ratio (%) |
        """)
    
    st.markdown("#### Sample Audit")
    st.dataframe(df.head(10), use_container_width=True)

# ===============================
# PAGE 2: DASHBOARD
# ===============================
if side == "Interactive Dashboard":
    st.markdown('<p class="main-title">Performance Hub</p>', unsafe_allow_html=True)
    
    # ─── SIDEBAR FILTERS ───
    st.sidebar.markdown("---")
    region = st.sidebar.multiselect("Region", options=df["region"].unique(), default=df["region"].unique())
    product = st.sidebar.multiselect("Product Category", options=df["product"].unique(), default=df["product"].unique())
    method = st.sidebar.multiselect("Channel", options=df["sales_method"].unique(), default=df["sales_method"].unique())
    
    filtered_df = df[
        (df["region"].isin(region)) & 
        (df["product"].isin(product)) & 
        (df["sales_method"].isin(method))
    ]

    # ─── TOP KPI ROW ───
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Gross Revenue", f"${filtered_df['total_sales'].sum()/1e6:.1f}M")
    k2.metric("Units Moved", f"{filtered_df['units_sold'].sum():,.0f}")
    k3.metric("Operating Profit", f"${filtered_df['operating_profit'].sum()/1e6:.1f}M")
    k4.metric("Avg Margin", f"{filtered_df['operating_margin'].mean():.1f}%")

    st.markdown("---")

    # ─── ANALYTICS TABS ───
    tab_trend, tab_geo, tab_retail = st.tabs(["📈 Time Analysis", "🌍 Geo Analysis", "🏪 Channel Performance"])

    with tab_trend:
        st.markdown("#### Sales & Unit Volume Trends")
        sales_line = filtered_df.groupby("invoice_date")["total_sales"].sum().reset_index()
        fig_line = px.area(sales_line, x="invoice_date", y="total_sales", 
                           color_discrete_sequence=["#38BDF8"])
        st.plotly_chart(apply_plotly_style(fig_line), use_container_width=True)

    with tab_geo:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Top States (Revenue)")
            state_sales = filtered_df.groupby("state")["total_sales"].sum().nlargest(5).reset_index()
            fig_state = px.bar(state_sales, x="total_sales", y="state", orientation='h', 
                               color_discrete_sequence=["#818CF8"])
            st.plotly_chart(apply_plotly_style(fig_state), use_container_width=True)
        with c2:
            st.markdown("#### Regional Contribution")
            fig_pie = px.pie(filtered_df, values="total_sales", names="region", hole=0.5,
                             color_discrete_sequence=px.colors.sequential.Slate_r)
            st.plotly_chart(apply_plotly_style(fig_pie), use_container_width=True)

    with tab_retail:
        st.markdown("#### Revenue vs. Efficiency (By Retailer)")
        fig_scatter = px.scatter(
            filtered_df, x="total_sales", y="operating_margin",
            size="units_sold", color="product", hover_name="retailer",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(apply_plotly_style(fig_scatter), use_container_width=True)

# FOOTER
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #475569; font-size: 0.8rem;">
    Adidas Analytics Engine | Proprietary Internal Tool | © 2026
</div>
""", unsafe_allow_html=True)
