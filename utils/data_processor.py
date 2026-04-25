# utils/data_processor.py
# Handles reading and cleaning uploaded CSV/Excel files

import pandas as pd
import streamlit as st


# Column name variations users might have in their exports
# We map ALL of these to our standard internal names
COLUMN_MAPPINGS = {
    "spend": [
        "spend", "cost", "amount spent", "budget", "ad spend",
        "total spend", "spend ($)", "cost ($)", "amount ($)"
    ],
    "clicks": [
        "clicks", "link clicks", "total clicks", "ad clicks"
    ],
    "impressions": [
        "impressions", "impr", "total impressions", "reach"
    ],
    "revenue": [
        "revenue", "conversion value", "total revenue",
        "sales", "value", "revenue ($)", "total value",
        "purchase value", "roas value"
    ],
    "campaign": [
        "campaign", "campaign name", "ad campaign",
        "campaign id", "ad set", "ad set name"
    ]
}


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a DataFrame with any column names and maps them
    to our standard names: spend, clicks, impressions, revenue, campaign.

    Example:
        "Amount Spent" → "spend"
        "Link Clicks"  → "clicks"
    """
    # Make all column names lowercase + strip spaces for matching
    df.columns = df.columns.str.lower().str.strip()

    rename_map = {}

    for standard_name, variations in COLUMN_MAPPINGS.items():
        for col in df.columns:
            if col in variations:
                rename_map[col] = standard_name
                break  # Stop once we find a match for this standard name

    df = df.rename(columns=rename_map)
    return df


def validate_columns(df: pd.DataFrame) -> tuple[bool, list]:
    """
    Checks that the DataFrame has the minimum required columns.
    Returns (is_valid, list_of_missing_columns).
    """
    required = ["spend", "clicks", "impressions"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        return False, missing
    return True, []


def clean_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts money/number columns to proper floats.
    Handles cases like "$1,234.56" → 1234.56
    """
    numeric_cols = ["spend", "clicks", "impressions", "revenue"]

    for col in numeric_cols:
        if col in df.columns:
            # Remove $, commas, spaces then convert to number
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[$,\s]", "", regex=True)
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows where all key numeric columns are NaN
    df = df.dropna(subset=["spend", "clicks"], how="all")

    return df


def load_file(uploaded_file) -> pd.DataFrame | None:
    """
    Main function to load and clean any uploaded file.
    Handles both CSV and Excel automatically.

    Returns a clean DataFrame or None if something goes wrong.
    """
    try:
        # ── Read the file ──────────────────────────────────────────────────
        filename = uploaded_file.name.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            st.error("❌ Unsupported file type. Please upload a CSV or Excel file.")
            return None

        # ── Clean and standardize ──────────────────────────────────────────
        df = standardize_columns(df)
        df = clean_numeric_columns(df)

        # ── Validate ───────────────────────────────────────────────────────
        is_valid, missing = validate_columns(df)

        if not is_valid:
            st.error(
                f"❌ Missing required columns: **{', '.join(missing)}**\n\n"
                "Your file must contain columns for: Spend, Clicks, Impressions.\n"
                "Column names can vary (e.g. 'Cost', 'Amount Spent') — "
                "we'll detect them automatically."
            )
            return None

        return df

    except Exception as e:
        st.error(f"❌ Error reading file: {str(e)}")
        return None


def preview_data(df: pd.DataFrame, max_rows: int = 5):
    """
    Shows a clean preview of the uploaded data inside the Streamlit app.
    """
    st.markdown(f"**{len(df)} rows detected** — showing first {max_rows}:")
    st.dataframe(
        df.head(max_rows),
        use_container_width=True
    )

    # Show which columns were detected
    detected = [col for col in
                ["campaign", "spend", "clicks", "impressions", "revenue"]
                if col in df.columns]

    st.success(f"✅ Detected columns: **{', '.join(detected)}**")

    if "revenue" not in df.columns:
        st.warning(
            "⚠️ No 'Revenue' column found. "
            "ROI and ROAS won't be calculated. "
            "Add a Revenue or Conversion Value column for full analysis."
        )