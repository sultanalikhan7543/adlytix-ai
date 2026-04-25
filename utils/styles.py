# utils/styles.py — All CSS for Adlytix AI

def load_css() -> str:
    """Returns the complete CSS string for the app."""
    return """
<style>
/* ── Reset & Base ──────────────────────────────────────────── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.main .block-container {
    padding-top: 0rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

body {
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    background-color: #f0f2f6;
}

/* ── Navbar ────────────────────────────────────────────────── */
.navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 16px 32px;
    border-radius: 0 0 20px 20px;
    margin-bottom: 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
}

.navbar-brand {
    font-size: 1.6rem;
    font-weight: 800;
    color: white !important;
    letter-spacing: -0.5px;
}

.navbar-tagline {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.85);
    margin-top: 2px;
}

.navbar-badge {
    background: rgba(255,255,255,0.2);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.3);
}

/* ── Section Headers ───────────────────────────────────────── */
.section-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 4px;
    margin-top: 8px;
}

.section-subtitle {
    font-size: 0.9rem;
    color: #718096;
    margin-bottom: 20px;
}

/* ── Upload Zone ───────────────────────────────────────────── */
.upload-zone {
    background: white;
    border: 2.5px dashed #667eea;
    border-radius: 16px;
    padding: 40px 32px;
    text-align: center;
    transition: all 0.2s ease;
}

.upload-zone:hover {
    border-color: #764ba2;
    background: #fafbff;
}

.upload-icon {
    font-size: 3rem;
    margin-bottom: 12px;
}

.upload-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 8px;
}

.upload-subtitle {
    font-size: 0.88rem;
    color: #718096;
}

/* ── Metric Cards ──────────────────────────────────────────── */
.metric-card {
    background: white;
    border-radius: 14px;
    padding: 22px 16px;
    text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border-top: 4px solid #667eea;
    transition: transform 0.2s ease;
    height: 110px;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.metric-card.green { border-top-color: #48bb78; }
.metric-card.orange { border-top-color: #f6ad55; }
.metric-card.red { border-top-color: #fc5c65; }
.metric-card.purple { border-top-color: #667eea; }

.metric-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: #2d3748;
    line-height: 1;
    margin-bottom: 6px;
}

.metric-label {
    font-size: 0.78rem;
    color: #718096;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.metric-delta {
    font-size: 0.75rem;
    margin-top: 4px;
}

.delta-good { color: #48bb78; }
.delta-warn { color: #f6ad55; }
.delta-bad  { color: #fc5c65; }

/* ── Chart Container ───────────────────────────────────────── */
.chart-container {
    background: white;
    border-radius: 14px;
    padding: 8px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    margin-bottom: 16px;
}

/* ── AI Insight Cards ──────────────────────────────────────── */
.insight-wrapper {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 32px 36px;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.35);
    margin-top: 8px;
}

.insight-header {
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.insight-title {
    font-size: 1.2rem;
    font-weight: 700;
    color: white;
    margin: 0;
}

.insight-subtitle {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.75);
    margin-top: 2px;
}

.insight-content {
    color: white;
    font-size: 0.97rem;
    line-height: 1.85;
}

.insight-card {
    background: rgba(255,255,255,0.15);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border-left: 4px solid rgba(255,255,255,0.6);
}

/* ── Data Table ────────────────────────────────────────────── */
.table-container {
    background: white;
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}

/* ── Best / Worst Badges ───────────────────────────────────── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.badge-success { background: #c6f6d5; color: #276749; }
.badge-danger  { background: #fed7d7; color: #9b2c2c; }
.badge-warning { background: #fefcbf; color: #744210; }

/* ── Hero Section ──────────────────────────────────────────── */
.hero {
    text-align: center;
    padding: 40px 20px 20px;
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #2d3748;
    margin-bottom: 12px;
    line-height: 1.2;
}

.hero-title span {
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #718096;
    max-width: 520px;
    margin: 0 auto 32px;
    line-height: 1.6;
}

.feature-pills {
    display: flex;
    gap: 10px;
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: 36px;
}

.pill {
    background: white;
    border: 1.5px solid #e2e8f0;
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.85rem;
    color: #4a5568;
    font-weight: 500;
}

/* ── Footer ────────────────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 32px 16px 16px;
    color: #a0aec0;
    font-size: 0.82rem;
    border-top: 1px solid #e2e8f0;
    margin-top: 48px;
}

/* ── Success Banner ────────────────────────────────────────── */
.success-banner {
    background: linear-gradient(135deg, #48bb78, #38a169);
    color: white;
    border-radius: 12px;
    padding: 14px 20px;
    font-weight: 600;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ── Step Indicator ────────────────────────────────────────── */
.step-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 28px;
    align-items: center;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.85rem;
    font-weight: 600;
}

.step-dot {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
}

.step-dot.done {
    background: #48bb78;
    color: white;
}

.step-dot.active {
    background: #667eea;
    color: white;
}

.step-dot.pending {
    background: #e2e8f0;
    color: #a0aec0;
}

.step-line {
    flex: 1;
    height: 2px;
    background: #e2e8f0;
    border-radius: 2px;
}
</style>
"""