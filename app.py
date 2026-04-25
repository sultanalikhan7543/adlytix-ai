# app.py — Adlytix AI | Polished SaaS Dashboard
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

from config import APP_NAME, APP_TAGLINE, APP_ICON, APP_VERSION, COLORS, ROAS_GOOD, ROAS_OKAY

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{APP_NAME} — Ad Analytics",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Load CSS ───────────────────────────────────────────────────────────────────
from utils.styles import load_css
st.markdown(load_css(), unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def render_navbar():
    """Top branded navigation bar."""
    st.markdown(f"""
    <div class="navbar">
        <div>
            <div class="navbar-brand">{APP_ICON} {APP_NAME}</div>
            <div class="navbar-tagline">{APP_TAGLINE}</div>
        </div>
        <div class="navbar-badge">v{APP_VERSION} · Free Beta</div>
    </div>
    """, unsafe_allow_html=True)


def render_hero():
    """Hero section shown before file upload."""
    st.markdown("""
    <div class="hero">
        <div class="hero-title">
            Turn Ad Data Into<br><span>Instant Clarity</span>
        </div>
        <div class="hero-subtitle">
            Upload your Google Ads, Meta, or TikTok export.
            Get calculated metrics + AI insights in under 10 seconds.
            No setup. No expertise needed.
        </div>
        <div class="feature-pills">
            <span class="pill">✅ ROI & ROAS Calculator</span>
            <span class="pill">✅ AI-Powered Insights</span>
            <span class="pill">✅ Works with any CSV/Excel</span>
            <span class="pill">✅ 100% Free</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_step_bar(active_step: int):
    """Shows progress steps at the top of the workflow."""
    steps = ["Upload File", "View Metrics", "AI Insights"]
    dots = ""
    for i, label in enumerate(steps, 1):
        if i < active_step:
            cls = "done"
            icon = "✓"
        elif i == active_step:
            cls = "active"
            icon = str(i)
        else:
            cls = "pending"
            icon = str(i)

        dots += f"""
        <div class="step-item">
            <div class="step-dot {cls}">{icon}</div>
            <span style="color: {'#2d3748' if i <= active_step else '#a0aec0'}">{label}</span>
        </div>
        """
        if i < len(steps):
            dots += '<div class="step-line"></div>'

    st.markdown(
        f'<div class="step-bar">{dots}</div>',
        unsafe_allow_html=True
    )


def render_upload_zone():
    """Styled file upload section."""
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📂</div>
        <div class="upload-title">Drop your ad data file here</div>
        <div class="upload-subtitle">
            Supports CSV and Excel (.xlsx) exports from Google Ads,
            Meta Ads, TikTok Ads, and more
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        label="Upload file",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
        help="Export from your ad platform → Upload here → Done"
    )
    return uploaded_file


def get_metric_color(metric_name: str, value) -> str:
    """Returns CSS class based on metric value health."""
    try:
        v = float(value)
        if metric_name == "roas":
            if v >= ROAS_GOOD:
                return "green"
            elif v >= ROAS_OKAY:
                return "orange"
            else:
                return "red"
        elif metric_name == "roi":
            if v >= 100:
                return "green"
            elif v >= 0:
                return "orange"
            else:
                return "red"
        elif metric_name == "ctr":
            return "green" if v >= 2.0 else "orange"
        elif metric_name == "cpc":
            return "green" if v <= 3.0 else "orange"
    except:
        pass
    return "purple"


def render_metric_cards(stats: dict):
    """Renders 8 color-coded metric cards in 2 rows."""
    st.markdown(
        '<p class="section-title">📐 Performance Overview</p>'
        '<p class="section-subtitle">Key metrics calculated from your uploaded data</p>',
        unsafe_allow_html=True
    )

    def card(value, label, color="purple", delta=None):
        delta_html = ""
        if delta:
            delta_html = f'<div class="metric-delta {delta["cls"]}">{delta["text"]}</div>'
        return f"""
        <div class="metric-card {color}">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
            {delta_html}
        </div>
        """

    # Row 1
    col1, col2, col3, col4 = st.columns(4)
    cards_row1 = [
        (
            col1,
            f"${stats.get('total_spend', 0):,.0f}",
            "Total Spend",
            "purple",
            None
        ),
        (
            col2,
            f"${stats.get('total_revenue', 0):,.0f}"
            if "total_revenue" in stats else "N/A",
            "Total Revenue",
            "green" if stats.get("total_revenue", 0) >
            stats.get("total_spend", 0) else "orange",
            None
        ),
        (
            col3,
            f"{stats['avg_roas']}x" if "avg_roas" in stats else "N/A",
            "Avg ROAS",
            get_metric_color("roas", stats.get("avg_roas", 0)),
            {
                "cls": "delta-good" if stats.get("avg_roas", 0) >= ROAS_GOOD
                       else "delta-warn",
                "text": "✅ Healthy" if stats.get("avg_roas", 0) >= ROAS_GOOD
                        else "⚠️ Needs work"
            } if "avg_roas" in stats else None
        ),
        (
            col4,
            f"{stats['avg_roi']}%" if "avg_roi" in stats else "N/A",
            "Avg ROI",
            get_metric_color("roi", stats.get("avg_roi", 0)),
            None
        ),
    ]

    for col, value, label, color, delta in cards_row1:
        with col:
            st.markdown(card(value, label, color, delta), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2
    col5, col6, col7, col8 = st.columns(4)
    cards_row2 = [
        (
            col5,
            f"{stats.get('total_clicks', 0):,}",
            "Total Clicks",
            "purple",
            None
        ),
        (
            col6,
            f"{stats.get('total_impressions', 0):,}",
            "Total Impressions",
            "purple",
            None
        ),
        (
            col7,
            f"${stats['avg_cpc']}" if "avg_cpc" in stats else "N/A",
            "Avg CPC",
            get_metric_color("cpc", stats.get("avg_cpc", 0)),
            None
        ),
        (
            col8,
            f"{stats['avg_ctr']}%" if "avg_ctr" in stats else "N/A",
            "Avg CTR",
            get_metric_color("ctr", stats.get("avg_ctr", 0)),
            None
        ),
    ]

    for col, value, label, color, delta in cards_row2:
        with col:
            st.markdown(card(value, label, color, delta), unsafe_allow_html=True)


def render_best_worst(stats: dict):
    """Shows best and worst campaign side by side."""
    if "best_campaign" not in stats and "worst_campaign" not in stats:
        return

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        if "best_campaign" in stats:
            st.markdown(f"""
            <div style="background:#f0fff4; border-radius:12px; padding:20px;
                        border-left:4px solid #48bb78;">
                <p style="margin:0; font-size:0.8rem; color:#718096;
                          font-weight:600; text-transform:uppercase;">
                    🏆 Best Performer
                </p>
                <p style="margin:8px 0 4px; font-size:1.3rem; font-weight:800;
                          color:#2d3748;">
                    {stats['best_campaign']}
                </p>
                <span class="badge badge-success">
                    ROAS: {stats['best_roas']}x
                </span>
                <p style="margin:8px 0 0; font-size:0.85rem; color:#48bb78;
                          font-weight:600;">
                    ↑ Consider increasing this budget
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        if "worst_campaign" in stats:
            st.markdown(f"""
            <div style="background:#fff5f5; border-radius:12px; padding:20px;
                        border-left:4px solid #fc5c65;">
                <p style="margin:0; font-size:0.8rem; color:#718096;
                          font-weight:600; text-transform:uppercase;">
                    ⚠️ Needs Attention
                </p>
                <p style="margin:8px 0 4px; font-size:1.3rem; font-weight:800;
                          color:#2d3748;">
                    {stats['worst_campaign']}
                </p>
                <span class="badge badge-danger">
                    ROAS: {stats['worst_roas']}x
                </span>
                <p style="margin:8px 0 0; font-size:0.85rem; color:#fc5c65;
                          font-weight:600;">
                    ↓ Review targeting and creative
                </p>
            </div>
            """, unsafe_allow_html=True)


def render_charts_tabbed(df):
    """Charts organized in tabs for cleaner UX."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title">📊 Campaign Analytics</p>'
        '<p class="section-subtitle">Interactive charts — hover to explore</p>',
        unsafe_allow_html=True
    )

    from utils.charts import (
        plot_roas_bar, plot_spend_vs_revenue,
        plot_ctr_bar, plot_cpc_bar
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 ROAS",
        "💰 Spend vs Revenue",
        "🎯 CTR",
        "🖱️ CPC"
    ])

    with tab1:
        fig = plot_roas_bar(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ROAS chart requires Spend and Revenue columns.")

    with tab2:
        fig = plot_spend_vs_revenue(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Spend vs Revenue chart requires Spend column.")

    with tab3:
        fig = plot_ctr_bar(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("CTR chart requires Clicks and Impressions columns.")

    with tab4:
        fig = plot_cpc_bar(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("CPC chart requires Spend and Clicks columns.")


def render_data_table(df):
    """Clean styled data table with expander."""
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📋 View Full Campaign Data Table", expanded=False):
        st.dataframe(
            df,
            use_container_width=True,
            height=280
        )
        st.caption(f"Showing {len(df)} campaigns · "
                   f"{len(df.columns)} columns detected")


def render_ai_insights(df, stats):
    """Polished AI insights section."""
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="section-title">🤖 AI-Generated Insights</p>'
        '<p class="section-subtitle">'
        'Powered by Claude AI · Plain English analysis of your campaigns'
        '</p>',
        unsafe_allow_html=True
    )

    with st.spinner("🧠 Claude is analyzing your campaigns..."):
        from utils.ai_insights import generate_insights
        insights = generate_insights(df, stats)

    # Format insights into the styled box
    formatted = insights.replace("\n\n", "<br><br>").replace("\n", "<br>")

    st.markdown(f"""
    <div class="insight-wrapper">
        <div class="insight-header">
            <div>
                <div class="insight-title">🤖 Adlytix AI Analysis</div>
                <div class="insight-subtitle">
                    Based on {len(df)} campaigns ·
                    Generated just now
                </div>
            </div>
        </div>
        <div class="insight-content">
            {formatted}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sample_format():
    """Shows expected format when no file is uploaded."""
    import pandas as pd
    st.markdown(
        '<p class="section-title">💡 Expected File Format</p>'
        '<p class="section-subtitle">'
        'Your columns can have different names — we auto-detect them'
        '</p>',
        unsafe_allow_html=True
    )

    sample = pd.DataFrame({
        "Campaign": ["Summer Sale", "Brand Awareness", "Retargeting"],
        "Spend ($)": [500, 300, 150],
        "Clicks": [1200, 450, 800],
        "Impressions": [45000, 30000, 12000],
        "Revenue ($)": [2100, 400, 900]
    })
    st.dataframe(sample, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **✅ Required columns:**
        - Spend / Cost / Budget
        - Clicks
        - Impressions
        """)
    with col2:
        st.markdown("""
        **➕ Optional (for full analysis):**
        - Revenue / Conversion Value
        - Campaign Name
        """)
    with col3:
        st.markdown("""
        **🔄 Supported platforms:**
        - Google Ads
        - Meta / Facebook Ads
        - TikTok Ads
        - Any CSV export
        """)


def render_footer():
    """App footer."""
    st.markdown(f"""
    <div class="footer">
        <strong>{APP_NAME}</strong> · Built with ❤️ using Python + Streamlit + Claude AI<br>
        <span style="color:#cbd5e0;">
            Free to use during beta · 
            No data stored · 
            Your data never leaves your browser session
        </span>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    # Always show navbar
    render_navbar()

    # File upload section
    render_step_bar(active_step=1)
    uploaded_file = render_upload_zone()

    if uploaded_file is not None:
        # File uploaded — process it
        st.markdown(f"""
        <div class="success-banner">
            ✅ &nbsp; File uploaded successfully: <strong>{uploaded_file.name}</strong>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("⚙️ Processing your data..."):
            from utils.data_processor import load_file
            from utils.metrics import calculate_metrics, get_summary_stats

            df = load_file(uploaded_file)

        if df is not None:
            df = calculate_metrics(df)
            stats = get_summary_stats(df)

            # ── Dashboard ──────────────────────────────────────────────────
            st.markdown("---")
            render_step_bar(active_step=2)
            render_metric_cards(stats)
            render_best_worst(stats)
            render_charts_tabbed(df)
            render_data_table(df)

            st.markdown("---")
            render_step_bar(active_step=3)
            render_ai_insights(df, stats)

    else:
        # No file yet — show hero + sample format
        render_hero()
        st.markdown("---")
        render_sample_format()

    render_footer()


if __name__ == "__main__":
    main()