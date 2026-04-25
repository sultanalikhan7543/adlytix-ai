# utils/charts.py
# Creates all Plotly charts for the dashboard

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# Brand colors for Adlytix AI
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#48bb78",
    "warning": "#ed8936",
    "danger": "#fc5c65",
    "palette": [
        "#667eea", "#764ba2", "#48bb78",
        "#ed8936", "#fc5c65", "#38b2ac"
    ]
}


def plot_roas_bar(df: pd.DataFrame):
    """Bar chart: ROAS by Campaign"""
    if "ROAS (x)" not in df.columns or "campaign" not in df.columns:
        return None

    fig = px.bar(
        df,
        x="campaign",
        y="ROAS (x)",
        title="📈 ROAS by Campaign",
        color="ROAS (x)",
        color_continuous_scale=["#fc5c65", "#ed8936", "#48bb78"],
        text="ROAS (x)"
    )

    # Add a reference line at ROAS = 3 (breakeven for most businesses)
    fig.add_hline(
        y=3,
        line_dash="dash",
        line_color="gray",
        annotation_text="Target: 3x ROAS",
        annotation_position="top right"
    )

    fig.update_traces(texttemplate="%{text}x", textposition="outside")
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis_title="Campaign",
        yaxis_title="ROAS (x)",
        font=dict(family="sans-serif", size=13)
    )

    return fig


def plot_spend_vs_revenue(df: pd.DataFrame):
    """Grouped bar: Spend vs Revenue by Campaign"""
    if "spend" not in df.columns or "campaign" not in df.columns:
        return None

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name="Spend ($)",
        x=df["campaign"],
        y=df["spend"],
        marker_color="#667eea"
    ))

    if "revenue" in df.columns:
        fig.add_trace(go.Bar(
            name="Revenue ($)",
            x=df["campaign"],
            y=df["revenue"],
            marker_color="#48bb78"
        ))

    fig.update_layout(
        title="💰 Spend vs Revenue by Campaign",
        barmode="group",
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis_title="Campaign",
        yaxis_title="Amount ($)",
        font=dict(family="sans-serif", size=13),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig


def plot_ctr_bar(df: pd.DataFrame):
    """Horizontal bar: CTR by Campaign"""
    if "CTR (%)" not in df.columns or "campaign" not in df.columns:
        return None

    fig = px.bar(
        df.sort_values("CTR (%)"),
        x="CTR (%)",
        y="campaign",
        orientation="h",
        title="🎯 Click-Through Rate by Campaign",
        color="CTR (%)",
        color_continuous_scale=["#fc5c65", "#ed8936", "#48bb78"],
        text="CTR (%)"
    )

    fig.update_traces(
        texttemplate="%{text}%",
        textposition="outside"
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        xaxis_title="CTR (%)",
        yaxis_title="",
        font=dict(family="sans-serif", size=13)
    )

    return fig


def plot_cpc_bar(df: pd.DataFrame):
    """Bar chart: CPC by Campaign (lower is better)"""
    if "CPC ($)" not in df.columns or "campaign" not in df.columns:
        return None

    fig = px.bar(
        df.sort_values("CPC ($)", ascending=False),
        x="campaign",
        y="CPC ($)",
        title="🖱️ Cost Per Click by Campaign (Lower = Better)",
        color="CPC ($)",
        color_continuous_scale=["#48bb78", "#ed8936", "#fc5c65"],
        text="CPC ($)"
    )

    fig.update_traces(
        texttemplate="$%{text}",
        textposition="outside"
    )
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        font=dict(family="sans-serif", size=13)
    )

    return fig