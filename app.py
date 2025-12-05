import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------------------
# Page Configuration
# -----------------------------------------
st.set_page_config(
    page_title="AJIO Sales Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# Professional CSS Styling
# -----------------------------------------
custom_css = """
<style>
/* ===== ROOT VARIABLES ===== */
:root {
    --bg-primary: #0a0a0a;
    --bg-secondary: #111111;
    --bg-card: #1a1a1a;
    --bg-card-hover: #222222;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --text-muted: #666666;
    --accent-primary: #00d4ff;
    --accent-secondary: #7c3aed;
    --accent-success: #10b981;
    --accent-warning: #f59e0b;
    --accent-danger: #ef4444;
    --border-color: #2a2a2a;
    --gradient-1: linear-gradient(135deg, #00d4ff 0%, #7c3aed 100%);
    --gradient-2: linear-gradient(135deg, #10b981 0%, #00d4ff 100%);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.3);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.4);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
}

/* ===== GLOBAL STYLES ===== */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', 'Segoe UI', -apple-system, sans-serif;
}

[data-testid="stAppViewContainer"] > .main {
    background-color: var(--bg-primary);
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-color);
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: var(--text-primary);
}

/* Hide default Streamlit elements */
#MainMenu, header, footer, .stDeployButton {
    visibility: hidden !important;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-secondary);
}
::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--text-muted);
}

/* ===== HEADER SECTION ===== */
.dashboard-header {
    background: var(--gradient-1);
    padding: 30px 40px;
    border-radius: 16px;
    margin-bottom: 30px;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.dashboard-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    opacity: 0.5;
}

.dashboard-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
    position: relative;
    z-index: 1;
}

.dashboard-header p {
    margin: 8px 0 0 0;
    font-size: 1rem;
    color: rgba(255,255,255,0.85);
    position: relative;
    z-index: 1;
}

.header-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    margin-top: 12px;
    position: relative;
    z-index: 1;
}

/* ===== KPI CARDS ===== */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.kpi-card {
    background: var(--bg-card);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid var(--border-color);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-4px);
    border-color: var(--accent-primary);
    box-shadow: var(--shadow-md), 0 0 20px rgba(0, 212, 255, 0.1);
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--gradient-1);
    border-radius: 4px 0 0 4px;
}

.kpi-icon {
    font-size: 2rem;
    margin-bottom: 12px;
}

.kpi-value {
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
    line-height: 1.2;
}

.kpi-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-weight: 500;
}

.kpi-change {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.75rem;
    padding: 2px 8px;
    border-radius: 12px;
    margin-top: 8px;
}

.kpi-change.positive {
    background: rgba(16, 185, 129, 0.15);
    color: var(--accent-success);
}

.kpi-change.negative {
    background: rgba(239, 68, 68, 0.15);
    color: var(--accent-danger);
}

/* ===== CHART CONTAINERS ===== */
.chart-container {
    background: var(--bg-card);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid var(--border-color);
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.chart-container:hover {
    border-color: var(--border-color);
    box-shadow: var(--shadow-sm);
}

.chart-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.chart-title .icon {
    font-size: 1.25rem;
}

/* ===== INSIGHT CARDS ===== */
.insight-card {
    background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-card-hover) 100%);
    padding: 20px;
    border-radius: 12px;
    border-left: 4px solid var(--accent-primary);
    margin-bottom: 16px;
}

.insight-card h4 {
    margin: 0 0 8px 0;
    color: var(--accent-primary);
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.insight-card p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.9rem;
    line-height: 1.5;
}

.insight-value {
    color: var(--text-primary);
    font-weight: 600;
}

/* ===== SECTION DIVIDER ===== */
.section-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 30px 0;
}

/* ===== SIDEBAR STYLING ===== */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: var(--text-primary) !important;
    font-weight: 500;
}

[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border-color) !important;
}

/* ===== FOOTER ===== */
.dashboard-footer {
    text-align: center;
    padding: 20px;
    color: var(--text-muted);
    font-size: 0.8rem;
    border-top: 1px solid var(--border-color);
    margin-top: 40px;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 768px) {
    .dashboard-header h1 {
        font-size: 1.75rem;
    }
    .kpi-value {
        font-size: 1.75rem;
    }
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# -----------------------------------------
# Load Data
# -----------------------------------------
@st.cache_data
def load_data():
    customers = pd.read_csv("data/customer.csv")
    delivery = pd.read_csv("data/delivery.csv")
    orders = pd.read_csv("data/orders.csv")
    products = pd.read_csv("data/products.csv")
    ratings = pd.read_csv("data/ratings.csv")
    returns = pd.read_csv("data/returns.csv")
    transactions = pd.read_csv("data/transaction.csv")
    return customers, delivery, orders, products, ratings, returns, transactions

customers, delivery, orders, products, ratings, returns, transactions = load_data()

# Merge Datasets
orders_full = (orders.merge(customers, on="C_ID", how="left")
               .merge(products, on="P_ID", how="left")
               .merge(ratings, on="Or_ID", how="left")
               .merge(returns, on="Or_ID", how="left")
               .merge(transactions, on="Or_ID", how="left")
               .merge(delivery, on="DP_ID", how="left"))

orders_full["Total"] = orders_full["Qty"] * orders_full["Price"]
orders_full["Order_Date"] = pd.to_datetime(orders_full["Order_Date"], errors="coerce")

# Store original data for insights
orders_original = orders_full.copy()

# -----------------------------------------
# Sidebar Filters
# -----------------------------------------
with st.sidebar:
    st.markdown("## 🎛️ Dashboard Controls")
    st.markdown("---")

    st.markdown("### 📍 Location Filters")
    states = st.multiselect(
        "Select State(s)",
        options=sorted(orders_full["State"].dropna().unique()),
        placeholder="All States"
    )

    cities = st.multiselect(
        "Select City(s)",
        options=sorted(orders_full["City"].dropna().unique()),
        placeholder="All Cities"
    )

    st.markdown("---")
    st.markdown("### 📦 Product Filters")
    categories = st.multiselect(
        "Select Category",
        options=sorted(orders_full["Category"].dropna().unique()),
        placeholder="All Categories"
    )

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info("This dashboard provides comprehensive analytics for AJIO e-commerce sales data.")

# Apply Filters
if states:
    orders_full = orders_full[orders_full["State"].isin(states)]
if cities:
    orders_full = orders_full[orders_full["City"].isin(cities)]
if categories:
    orders_full = orders_full[orders_full["Category"].isin(categories)]

# -----------------------------------------
# HEADER SECTION
# -----------------------------------------
st.markdown(f"""
<div class="dashboard-header">
    <h1>🛒 AJIO Sales Analytics Dashboard</h1>
    <p>Real-time insights into sales performance, customer behavior, and business metrics</p>
    <span class="header-badge">📅 Last Updated: {datetime.now().strftime('%B %d, %Y')}</span>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------
# KPI METRICS SECTION
# -----------------------------------------
total_sales = orders_full["Total"].sum()
total_orders = orders_full["Or_ID"].nunique()
total_customers = orders_full["C_ID"].nunique()
avg_order_value = total_sales / total_orders if total_orders > 0 else 0
return_rate = (orders_full["Reason"].notna().sum() / len(orders_full) * 100) if len(orders_full) > 0 else 0
avg_rating = orders_full["Prod_Rating"].mean() if "Prod_Rating" in orders_full.columns else 0

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-icon">💰</div>
        <div class="kpi-value">₹{total_sales/1e6:.1f}M</div>
        <div class="kpi-label">Total Revenue</div>
        <span class="kpi-change positive">↑ Active</span>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-value">{total_orders:,}</div>
        <div class="kpi-label">Total Orders</div>
        <span class="kpi-change positive">↑ Growing</span>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-value">{total_customers:,}</div>
        <div class="kpi-label">Active Customers</div>
        <span class="kpi-change positive">↑ Engaged</span>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🧾</div>
        <div class="kpi-value">₹{avg_order_value:,.0f}</div>
        <div class="kpi-label">Avg Order Value</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-value">{avg_rating:.1f}</div>
        <div class="kpi-label">Avg Product Rating</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-icon">🔄</div>
        <div class="kpi-value">{return_rate:.1f}%</div>
        <div class="kpi-label">Return Rate</div>
        <span class="kpi-change {'negative' if return_rate > 15 else 'positive'}">{'↓ Low' if return_rate <= 15 else '↑ Monitor'}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------
# CHARTS ROW 1: Sales by State & Transaction Mode
# -----------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="icon">📍</span> Total Sales by State</div>', unsafe_allow_html=True)

    state_sales = orders_full.groupby("State")["Total"].sum().sort_values(ascending=True).tail(10).reset_index()

    fig = px.bar(
        state_sales,
        x="Total",
        y="State",
        orientation="h",
        color="Total",
        color_continuous_scale=["#1e3a5f", "#00d4ff"],
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a0a0a0"),
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
        height=350,
        xaxis=dict(gridcolor="#2a2a2a", title="Revenue (₹)"),
        yaxis=dict(gridcolor="#2a2a2a", title="")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="icon">💳</span> Revenue by Payment Mode</div>', unsafe_allow_html=True)

    mode_amt = orders_full.groupby("Transaction_Mode")["Total"].sum().reset_index()

    fig = px.pie(
        mode_amt,
        names="Transaction_Mode",
        values="Total",
        hole=0.55,
        color_discrete_sequence=["#00d4ff", "#7c3aed", "#10b981", "#f59e0b", "#ef4444"]
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a0a0a0"),
        margin=dict(l=0, r=0, t=10, b=0),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2)
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# CHARTS ROW 2: Top Products & Return Reasons
# -----------------------------------------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="icon">🏆</span> Top 10 Products by Sales</div>', unsafe_allow_html=True)

    prod_sales = orders_full.groupby("P_Name")["Total"].sum().sort_values(ascending=True).tail(10).reset_index()

    fig = px.bar(
        prod_sales,
        x="Total",
        y="P_Name",
        orientation="h",
        color="Total",
        color_continuous_scale=["#10b981", "#00d4ff"],
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a0a0a0"),
        showlegend=False,
        coloraxis_showscale=False,
        margin=dict(l=0, r=0, t=10, b=0),
        height=350,
        xaxis=dict(gridcolor="#2a2a2a", title="Revenue (₹)"),
        yaxis=dict(gridcolor="#2a2a2a", title="")
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title"><span class="icon">🔄</span> Return Reasons Analysis</div>', unsafe_allow_html=True)

    return_data = orders_full[orders_full["Reason"].notna()]
    if len(return_data) > 0:
        return_reason = return_data["Reason"].value_counts().reset_index()
        return_reason.columns = ["Reason", "Count"]

        fig = px.pie(
            return_reason,
            names="Reason",
            values="Count",
            hole=0.55,
            color_discrete_sequence=["#ef4444", "#f59e0b", "#7c3aed", "#00d4ff", "#10b981"]
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#a0a0a0"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=350,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No return data available for selected filters.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------
# MONTHLY SALES TREND
# -----------------------------------------
st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-title"><span class="icon">📈</span> Monthly Sales Trend</div>', unsafe_allow_html=True)

orders_full["Month"] = orders_full["Order_Date"].dt.to_period("M").astype(str)
monthly_sales = orders_full.groupby("Month")["Total"].sum().reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=monthly_sales["Month"],
    y=monthly_sales["Total"],
    mode='lines+markers',
    line=dict(color='#00d4ff', width=3),
    marker=dict(size=10, color='#00d4ff'),
    fill='tozeroy',
    fillcolor='rgba(0, 212, 255, 0.1)'
))
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#a0a0a0"),
    margin=dict(l=0, r=0, t=10, b=0),
    height=300,
    xaxis=dict(gridcolor="#2a2a2a", title="Month"),
    yaxis=dict(gridcolor="#2a2a2a", title="Revenue (₹)")
)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------
# INSIGHTS SECTION
# -----------------------------------------
st.markdown("## 💡 Key Business Insights")

col_ins1, col_ins2, col_ins3 = st.columns(3)

with col_ins1:
    top_state = orders_full.groupby("State")["Total"].sum().idxmax() if len(orders_full) > 0 else "N/A"
    top_state_sales = orders_full.groupby("State")["Total"].sum().max() if len(orders_full) > 0 else 0
    st.markdown(f"""
    <div class="insight-card">
        <h4>🏆 Top Performing State</h4>
        <p><span class="insight-value">{top_state}</span> leads with <span class="insight-value">₹{top_state_sales/1e6:.2f}M</span> in total sales, showing strong market presence in this region.</p>
    </div>
    """, unsafe_allow_html=True)

with col_ins2:
    top_payment = orders_full.groupby("Transaction_Mode")["Total"].sum().idxmax() if len(orders_full) > 0 else "N/A"
    payment_pct = (orders_full.groupby("Transaction_Mode")["Total"].sum().max() / total_sales * 100) if total_sales > 0 else 0
    st.markdown(f"""
    <div class="insight-card">
        <h4>💳 Preferred Payment Method</h4>
        <p><span class="insight-value">{top_payment}</span> accounts for <span class="insight-value">{payment_pct:.1f}%</span> of transactions, indicating customer preference for this payment mode.</p>
    </div>
    """, unsafe_allow_html=True)

with col_ins3:
    if orders_full["Reason"].notna().any():
        top_return = orders_full[orders_full["Reason"].notna()]["Reason"].mode().iloc[0]
    else:
        top_return = "N/A"
    st.markdown(f"""
    <div class="insight-card">
        <h4>🔄 Primary Return Reason</h4>
        <p><span class="insight-value">{top_return}</span> is the most common return reason. Consider improving product quality or descriptions to reduce returns.</p>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("""
<div class="dashboard-footer">
    <p>📊 AJIO Sales Analytics Dashboard | Built with Streamlit & Plotly | © 2024</p>
</div>
""", unsafe_allow_html=True)
