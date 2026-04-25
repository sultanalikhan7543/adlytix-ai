# config.py — Central place for all branding + app settings
# Change these values to rebrand the app instantly

APP_NAME = "Adlytix AI"
APP_TAGLINE = "Stop guessing. Start knowing."
APP_DESCRIPTION = (
    "Upload your ad performance data and get instant "
    "AI-powered insights in seconds."
)
APP_ICON = "📊"
APP_VERSION = "1.0.0"

# Brand Colors
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#48bb78",
    "warning": "#f6ad55",
    "danger": "#fc5c65",
    "dark": "#2d3748",
    "gray": "#718096",
    "light_gray": "#f8f9fa",
    "white": "#ffffff",
}

# Metric thresholds for color coding
ROAS_GOOD = 3.0       # Above this = green
ROAS_OKAY = 1.5       # Above this = orange, below = red
CTR_GOOD = 2.0        # Above this = green (%)
CPC_HIGH = 3.0        # Above this = warning ($)