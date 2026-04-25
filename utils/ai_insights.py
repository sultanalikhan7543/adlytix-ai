# utils/ai_insights.py
# Sends metrics to Claude API and returns plain-English insights

import os
import anthropic


def build_prompt(df, stats: dict) -> str:
    """
    Builds a clear, structured prompt to send to Claude.
    The better the prompt, the better the insights.
    """

    # Build campaign-level summary text
    campaign_lines = []

    for _, row in df.iterrows():
        line = []

        if "campaign" in df.columns:
            line.append(f"Campaign: {row.get('campaign', 'Unknown')}")
        if "spend" in df.columns:
            line.append(f"Spend: ${row.get('spend', 0)}")
        if "clicks" in df.columns:
            line.append(f"Clicks: {int(row.get('clicks', 0))}")
        if "CTR (%)" in df.columns:
            line.append(f"CTR: {row.get('CTR (%)', 0)}%")
        if "CPC ($)" in df.columns:
            line.append(f"CPC: ${row.get('CPC ($)', 0)}")
        if "ROAS (x)" in df.columns:
            line.append(f"ROAS: {row.get('ROAS (x)', 0)}x")
        if "ROI (%)" in df.columns:
            line.append(f"ROI: {row.get('ROI (%)', 0)}%")

        campaign_lines.append(" | ".join(line))

    campaigns_text = "\n".join(campaign_lines)

    # Build overall summary
    summary_parts = []
    if "total_spend" in stats:
        summary_parts.append(f"Total Spend: ${stats['total_spend']}")
    if "total_revenue" in stats:
        summary_parts.append(f"Total Revenue: ${stats['total_revenue']}")
    if "avg_roas" in stats:
        summary_parts.append(f"Average ROAS: {stats['avg_roas']}x")
    if "avg_roi" in stats:
        summary_parts.append(f"Average ROI: {stats['avg_roi']}%")
    if "avg_ctr" in stats:
        summary_parts.append(f"Average CTR: {stats['avg_ctr']}%")
    if "avg_cpc" in stats:
        summary_parts.append(f"Average CPC: ${stats['avg_cpc']}")

    summary_text = " | ".join(summary_parts)

    prompt = f"""You are a senior digital marketing analyst reviewing ad campaign performance data.

Here is the campaign-level data:
{campaigns_text}

Overall Summary:
{summary_text}

Please provide a concise analysis with these exact sections:

1. OVERALL PERFORMANCE (2-3 sentences): How is the account performing overall? Is the average ROAS healthy? (A ROAS above 3x is generally good for most businesses.)

2. BEST CAMPAIGN (1-2 sentences): Which campaign is performing best and why is it working?

3. NEEDS ATTENTION (1-2 sentences): Which campaign is underperforming and what specific action should the advertiser take?

4. TOP RECOMMENDATION (1-2 sentences): The single most impactful change they can make right now.

Use simple, plain English. Avoid jargon. Write as if explaining to a small business owner who is not a marketing expert. Be specific with numbers."""

    return prompt


def generate_insights(df, stats: dict) -> str:
    """
    Main function that calls Claude API and returns insights as a string.
    Falls back to a rule-based insight if API call fails.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")

    # ── Fallback if no API key ─────────────────────────────────────────────
    if not api_key:
        return generate_fallback_insights(stats)

    try:
        client = anthropic.Anthropic(api_key=api_key)
        prompt = build_prompt(df, stats)

        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=600,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return message.content[0].text

    except Exception as e:
        # If API fails for any reason, use rule-based fallback
        return generate_fallback_insights(stats) + \
               f"\n\n_(AI service temporarily unavailable: {str(e)})_"


def generate_fallback_insights(stats: dict) -> str:
    """
    Rule-based insights when Claude API is unavailable.
    Still gives useful feedback based on the numbers.
    """
    insights = []

    # ROAS analysis
    if "avg_roas" in stats:
        roas = stats["avg_roas"]
        if roas >= 4:
            insights.append(
                f"✅ **Overall Performance:** Excellent! "
                f"Your average ROAS of {roas}x means you're earning "
                f"${roas} for every $1 spent on ads."
            )
        elif roas >= 2:
            insights.append(
                f"⚠️ **Overall Performance:** Moderate. "
                f"Your average ROAS of {roas}x is profitable but has "
                f"room for improvement. Aim for 3x or higher."
            )
        else:
            insights.append(
                f"🔴 **Overall Performance:** Your ROAS of {roas}x "
                f"means you may be losing money. Immediate optimization needed."
            )

    # Best campaign
    if "best_campaign" in stats:
        insights.append(
            f"🏆 **Best Campaign:** '{stats['best_campaign']}' "
            f"with {stats['best_roas']}x ROAS. "
            f"Consider increasing its budget."
        )

    # Worst campaign
    if "worst_campaign" in stats:
        insights.append(
            f"📉 **Needs Attention:** '{stats['worst_campaign']}' "
            f"has the lowest ROAS at {stats['worst_roas']}x. "
            f"Review its targeting and creative."
        )

    # CPC analysis
    if "avg_cpc" in stats:
        cpc = stats["avg_cpc"]
        if cpc > 3:
            insights.append(
                f"💰 **Cost Alert:** Your average CPC of ${cpc} is high. "
                f"Try refining your audience targeting to lower this."
            )

    return "\n\n".join(insights)