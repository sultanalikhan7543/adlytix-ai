# utils/metrics.py
# Calculates all marketing metrics from the cleaned DataFrame

import pandas as pd


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a cleaned DataFrame and adds metric columns:
    - CTR  : Click-Through Rate (%)
    - CPC  : Cost Per Click ($)
    - ROAS : Return on Ad Spend (x)
    - ROI  : Return on Investment (%)

    Any metric that can't be calculated (missing column)
    is simply skipped — no crash.
    """

    # ── CTR = (Clicks / Impressions) × 100 ────────────────────────────────
    if "clicks" in df.columns and "impressions" in df.columns:
        df["CTR (%)"] = (
            (df["clicks"] / df["impressions"]) * 100
        ).round(2)

    # ── CPC = Spend / Clicks ───────────────────────────────────────────────
    if "spend" in df.columns and "clicks" in df.columns:
        df["CPC ($)"] = (
            df["spend"] / df["clicks"]
        ).round(2)

    # ── ROAS = Revenue / Spend ─────────────────────────────────────────────
    if "revenue" in df.columns and "spend" in df.columns:
        df["ROAS (x)"] = (
            df["revenue"] / df["spend"]
        ).round(2)

    # ── ROI = ((Revenue - Spend) / Spend) × 100 ───────────────────────────
    if "revenue" in df.columns and "spend" in df.columns:
        df["ROI (%)"] = (
            ((df["revenue"] - df["spend"]) / df["spend"]) * 100
        ).round(2)

    return df


def get_summary_stats(df: pd.DataFrame) -> dict:
    """
    Returns a summary dictionary with TOTALS and AVERAGES
    for all key metrics across all campaigns.

    This powers the big metric cards at the top of the dashboard.
    """
    stats = {}

    # ── Totals ─────────────────────────────────────────────────────────────
    if "spend" in df.columns:
        stats["total_spend"] = round(df["spend"].sum(), 2)

    if "clicks" in df.columns:
        stats["total_clicks"] = int(df["clicks"].sum())

    if "impressions" in df.columns:
        stats["total_impressions"] = int(df["impressions"].sum())

    if "revenue" in df.columns:
        stats["total_revenue"] = round(df["revenue"].sum(), 2)

    # ── Averages (across campaigns) ────────────────────────────────────────
    if "CTR (%)" in df.columns:
        stats["avg_ctr"] = round(df["CTR (%)"].mean(), 2)

    if "CPC ($)" in df.columns:
        stats["avg_cpc"] = round(df["CPC ($)"].mean(), 2)

    if "ROAS (x)" in df.columns:
        stats["avg_roas"] = round(df["ROAS (x)"].mean(), 2)

    if "ROI (%)" in df.columns:
        stats["avg_roi"] = round(df["ROI (%)"].mean(), 2)

    # ── Best performing campaign ───────────────────────────────────────────
    if "ROAS (x)" in df.columns and "campaign" in df.columns:
        best_idx = df["ROAS (x)"].idxmax()
        stats["best_campaign"] = df.loc[best_idx, "campaign"]
        stats["best_roas"] = df.loc[best_idx, "ROAS (x)"]

    # ── Worst performing campaign ──────────────────────────────────────────
    if "ROAS (x)" in df.columns and "campaign" in df.columns:
        worst_idx = df["ROAS (x)"].idxmin()
        stats["worst_campaign"] = df.loc[worst_idx, "campaign"]
        stats["worst_roas"] = df.loc[worst_idx, "ROAS (x)"]

    return stats