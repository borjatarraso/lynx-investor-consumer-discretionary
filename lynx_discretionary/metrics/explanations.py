"""Metric explanations for Lynx Consumer Discretionary Analysis."""

from __future__ import annotations
from lynx_discretionary.models import MetricExplanation

METRIC_EXPLANATIONS: dict[str, MetricExplanation] = {}


def _add(key, full_name, description, why_used, formula, category):
    METRIC_EXPLANATIONS[key] = MetricExplanation(
        key=key, full_name=full_name, description=description,
        why_used=why_used, formula=formula, category=category,
    )


# Valuation
_add("pe_trailing", "Price-to-Earnings Ratio (TTM)",
     "Compares stock price to trailing 12-month earnings per share.",
     "Primary consumer-discretionary valuation metric. Most sector names trade "
     "in the 15-25x range; franchise / luxury names earn a premium.",
     "P/E = Price / EPS (TTM)", "valuation")
_add("pe_forward", "Forward P/E",
     "Price divided by consensus forward earnings.",
     "Forward-looking comparable. Useful during cyclical troughs when trailing "
     "earnings are depressed.", "Forward P/E = Price / Forward EPS", "valuation")
_add("pb_ratio", "Price-to-Book Ratio",
     "Compares stock price to book value per share.",
     "Useful for asset-heavy names (big-box retail, homebuilders). Less relevant "
     "for asset-light brands and franchise models.",
     "P/B = Price / Book Value per Share", "valuation")
_add("ps_ratio", "Price-to-Sales Ratio",
     "Compares stock price to revenue per share.",
     "Core metric for emerging consumer brands and DTC growth names where "
     "earnings are suppressed by reinvestment. <1x is cheap for mature retail; "
     "3-6x for high-growth brands.",
     "P/S = Market Cap / Revenue", "valuation")
_add("p_fcf", "Price-to-Free-Cash-Flow",
     "Compares market cap to free cash flow.",
     "Best valuation anchor for mature consumer operators — harder to manipulate "
     "than EPS. Target <20x for healthy mature operators.",
     "P/FCF = Market Cap / Free Cash Flow", "valuation")
_add("ev_ebitda", "Enterprise Value / EBITDA",
     "Capital-structure-neutral valuation.",
     "Preferred cross-sector comp for consumer discretionary. Mature retail: "
     "8-12x. Franchise / QSR: 14-20x. Luxury: 15-25x.",
     "EV/EBITDA = (Market Cap + Debt - Cash) / EBITDA", "valuation")
_add("ev_revenue", "Enterprise Value / Revenue",
     "EV divided by trailing revenue.",
     "Useful for unprofitable scaling operators. <1x is cheap; >3x requires "
     "strong growth / margin expansion.",
     "EV/Revenue = EV / Revenue", "valuation")
_add("peg_ratio", "PEG Ratio",
     "P/E adjusted by growth rate.",
     "PEG < 1 suggests undervaluation relative to growth. Especially useful "
     "for DEVELOPER-stage scaling operators.",
     "PEG = P/E / Annual EPS Growth Rate", "valuation")
_add("dividend_yield", "Dividend Yield",
     "Annual dividend as percentage of price.",
     "Many mature operators return capital via dividends. Franchise and mature "
     "retailers can sustain 2-5% yields; watch for payout ratio risk.",
     "Yield = Annual Dividends / Price", "valuation")
_add("earnings_yield", "Earnings Yield",
     "Inverse of P/E ratio.",
     "Compare to treasury yields for a relative-attractiveness read.",
     "Earnings Yield = EPS / Price", "valuation")
_add("ev_per_store", "EV per Store / Location",
     "Enterprise value per physical location (when disclosed).",
     "A per-unit valuation for retailers and restaurant chains. "
     "Comparable across chains within the same sub-segment.",
     "EV / Store Count", "valuation")
_add("price_to_tangible_book", "Price / Tangible Book",
     "Price vs tangible book value per share.",
     "Useful for asset-heavy retail and homebuilders.",
     "P/TBV = Price / (Equity - Intangibles) / Shares", "valuation")
_add("cash_to_market_cap", "Cash-to-Market-Cap Ratio",
     "How much of market cap is backed by cash.",
     "Mostly relevant for early-stage / emerging consumer brands. "
     ">20% can signal either hidden value or excessive cash burn.",
     "Cash / Market Cap = Total Cash / Market Capitalization", "valuation")

# Profitability
_add("roe", "Return on Equity",
     "Profit generated per dollar of equity.",
     "Target ROE > 15% for mature consumer operators. Franchise models often "
     "exceed 30% due to asset-light structure.",
     "ROE = Net Income / Equity", "profitability")
_add("roa", "Return on Assets",
     "Profit per dollar of assets.",
     "ROA > 8% is strong for retail. Capital-intensive models (homebuilders, "
     "hotels) naturally have lower ROA.",
     "ROA = Net Income / Total Assets", "profitability")
_add("roic", "Return on Invested Capital",
     "Return on all invested capital.",
     "THE core consumer-discretionary quality metric. ROIC > 15% suggests a "
     "durable competitive advantage (brand, network, scale).",
     "ROIC = NOPAT / Invested Capital", "profitability")
_add("gross_margin", "Gross Margin",
     "Revenue remaining after cost of goods sold.",
     "Proxy for pricing power and brand strength. Luxury: >60%. Apparel: "
     "40-55%. Specialty retail: 30-45%. Restaurants: 25-40%. Autos: 10-20%.",
     "Gross Margin = Gross Profit / Revenue", "profitability")
_add("operating_margin", "Operating Margin",
     "Revenue remaining after all operating expenses.",
     "Operating leverage indicator. Franchise models and luxury can exceed 20%; "
     "broadline retail typically 4-10%.",
     "Operating Margin = Operating Income / Revenue", "profitability")
_add("net_margin", "Net Profit Margin",
     "Revenue remaining as net profit.",
     "Bottom-line profitability after interest and tax.",
     "Net Margin = Net Income / Revenue", "profitability")
_add("fcf_margin", "Free Cash Flow Margin",
     "Revenue converted to free cash flow.",
     "Measures actual cash generation. >10% is strong for consumer operators.",
     "FCF Margin = FCF / Revenue", "profitability")
_add("ebitda_margin", "EBITDA Margin",
     "Revenue remaining as EBITDA.",
     "Approximates operating cash flow. >15% is healthy; franchise models >25%.",
     "EBITDA Margin = EBITDA / Revenue", "profitability")
_add("sga_pct_of_revenue", "SG&A as % of Revenue",
     "Selling, general, and administrative expense as a fraction of revenue.",
     "Operating-leverage indicator. As revenue scales, SG&A % should decline; "
     "rising SG&A % with flat revenue is a red flag.",
     "SG&A% = SG&A / Revenue", "profitability")
_add("store_contribution_margin", "Store Contribution Margin (proxy)",
     "Estimated store-level margin after variable store costs.",
     "Unit economics indicator. Healthy retailers and restaurants show 15-25% "
     "store-contribution margin before corporate overhead.",
     "(Gross Profit - Variable SG&A) / Revenue", "profitability")

# Solvency
_add("debt_to_equity", "Debt-to-Equity Ratio",
     "Debt financing vs equity financing.",
     "Cyclical consumer sectors should operate with moderate leverage; >2x can "
     "become dangerous in recessions.",
     "D/E = Total Debt / Equity", "solvency")
_add("debt_to_ebitda", "Debt-to-EBITDA",
     "Leverage ratio relative to operating cash flow.",
     "The primary leverage metric for consumer operators. <2x is conservative, "
     "2-4x normal, >5x stressed.",
     "Debt/EBITDA = Total Debt / EBITDA", "solvency")
_add("current_ratio", "Current Ratio",
     "Short-term asset coverage of liabilities.",
     "Retail inventories skew this metric high; >1.2 is healthy.",
     "Current Ratio = Current Assets / Current Liabilities", "solvency")
_add("quick_ratio", "Quick Ratio",
     "Liquidity excluding inventory.",
     "Important for apparel/retail where inventory can become stale.",
     "Quick Ratio = (Current Assets - Inventory) / Current Liabilities", "solvency")
_add("interest_coverage", "Interest Coverage",
     "Ability to pay interest from operating earnings.",
     "> 4x is comfortable for consumer operators. < 2x signals cyclical risk.",
     "Interest Coverage = Operating Income / Interest Expense", "solvency")
_add("lease_adjusted_debt_ratio", "Lease-Adjusted Leverage",
     "Debt-to-EBITDAR after capitalizing operating leases (8x rent proxy).",
     "Critical for brick-and-mortar retail and restaurants where off-balance "
     "lease commitments are large. Target <4x; >5x is stressed.",
     "(Debt + 8 × Rent) / (EBITDA + Rent)", "solvency")
_add("altman_z_score", "Altman Z-Score",
     "Bankruptcy probability predictor.",
     "Z > 2.99: Safe. 1.81-2.99: Grey zone. < 1.81: Distress risk. Apply "
     "cautiously to asset-light / franchise operators.",
     "Z = 1.2(WC/TA) + 1.4(RE/TA) + 3.3(EBIT/TA) + 0.6(MV/TL) + 1.0(Sales/TA)",
     "solvency")
_add("cash_burn_rate", "Cash Burn Rate",
     "Annual rate of cash consumption for pre-profit operators.",
     "Relevant only for emerging / early-stage consumer brands.",
     "Cash Burn = Annual Operating Cash Flow (when negative)", "solvency")
_add("cash_runway_years", "Cash Runway",
     "Years of operation at current burn rate.",
     "< 1 year = imminent financing. > 2 years = comfortable. Target for "
     "emerging consumer brands: 18+ months.",
     "Cash Runway = Total Cash / Annual Burn Rate", "solvency")
_add("debt_service_coverage", "Debt Service Coverage",
     "EBITDA coverage of interest expense.",
     "> 4x is comfortable. Consumer operators in a rising-rate environment "
     "should target > 6x.",
     "DSCR = EBITDA / Interest Expense", "solvency")

# Growth
_add("revenue_growth_yoy", "Revenue Growth (YoY)",
     "Annual revenue change.",
     "Core growth driver. For mature consumers, 3-8% is healthy; scaling "
     "operators should deliver >15%.",
     "Growth = (Rev_Current - Rev_Prior) / |Rev_Prior|", "growth")
_add("revenue_cagr_3y", "Revenue CAGR (3-Year)",
     "3-year compound revenue growth.",
     "Smooths near-term cyclicality. > 10% is strong for consumer operators.",
     "CAGR = (End/Start)^(1/3) - 1", "growth")
_add("earnings_growth_yoy", "Earnings Growth (YoY)",
     "Annual net income change.",
     "Must exceed revenue growth to validate operating leverage.",
     "Growth = (NI_Current - NI_Prior) / |NI_Prior|", "growth")
_add("capex_intensity", "CAPEX Intensity",
     "CAPEX as % of revenue.",
     "Unit-economic indicator. Asset-light / franchise: < 3%. Scaling "
     "retailers: 4-8%. Auto manufacturers: 5-10%. Hotels / resorts: >10%.",
     "CAPEX Intensity = CAPEX / Revenue", "growth")
_add("same_store_sales_proxy", "Same-Store-Sales Proxy",
     "Revenue growth minus total-asset growth.",
     "When companies don't disclose comps, this proxy separates pure-unit "
     "growth from productivity gains. Positive values suggest the existing "
     "base is producing more per dollar of assets.",
     "Rev Growth - Asset Growth", "growth")
_add("shares_growth_yoy", "Share Dilution (YoY)",
     "Annual change in shares outstanding.",
     "Consumer operators should either hold shares flat or buy back. Net "
     "dilution > 3%/yr signals capital-allocation concerns.",
     "Dilution = (Shares_Current - Shares_Prior) / Shares_Prior", "growth")
_add("shares_growth_3y_cagr", "Dilution / Buyback CAGR (3-Year)",
     "3-year compound share dilution rate.",
     "Tracks capital-discipline trend. Best-in-class consumer names deliver "
     "-2% to -5% (net buyback) CAGR.",
     "CAGR = (Shares_End / Shares_Start)^(1/3) - 1", "growth")
_add("operating_leverage", "Operating Leverage",
     "Earnings growth relative to revenue growth.",
     "> 2x signals scaling margin expansion; < 1x suggests margin compression.",
     "Op Leverage = Earnings Growth / Revenue Growth", "growth")

# Efficiency
_add("inventory_turnover", "Inventory Turnover",
     "How many times per year inventory is sold.",
     "Apparel: 3-6x. Specialty retail: 4-8x. Restaurants (very high): 50x+. "
     "Declining turnover is an early stress signal for retailers.",
     "Inventory Turnover = COGS / Average Inventory", "efficiency")
_add("days_inventory", "Days Inventory",
     "Average days required to sell inventory.",
     "Apparel: 60-120 days. Home improvement: 80-120 days. Declining days = "
     "healthier; rising days = potential markdown risk.",
     "Days Inventory = 365 / Inventory Turnover", "efficiency")
_add("working_capital_intensity", "Working-Capital Intensity",
     "Working capital as % of revenue.",
     "Franchise and e-commerce models often run with negative WC "
     "(favorable). Inventory-heavy retailers: 10-25%.",
     "WC Intensity = Working Capital / Revenue", "efficiency")
_add("revenue_per_employee", "Revenue per Employee",
     "Top-line revenue divided by headcount.",
     "Labour-productivity proxy. Digital-native: >$500K. Restaurants: "
     "$50-80K. Specialty retail: $150-250K.",
     "Revenue / Full-Time Employees", "efficiency")

# Business quality
_add("quality_score", "Consumer Business Quality Score",
     "Composite quality score (0-100).",
     "Evaluates brand strength, unit economics, financial position, "
     "management alignment, and capital discipline. >70 is high quality, "
     "<35 is weak.",
     "Weighted sum of brand strength, unit economics, financial position, "
     "insider alignment, dilution", "business_quality")
_add("brand_strength", "Brand Strength",
     "Qualitative assessment of pricing power.",
     "Derived primarily from gross margin level and trend. Premium brands "
     "sustain >50% gross margin with stable pricing.",
     "Inferred from Gross Margin level + trend", "business_quality")
_add("cyclical_sensitivity", "Cyclical Sensitivity",
     "Exposure to consumer-confidence and macro cycles.",
     "Autos, homes, luxury, travel, leisure are most cyclical. Home "
     "improvement and e-commerce are more resilient.",
     "Inferred from sub-segment classification", "business_quality")
_add("unit_economics_quality", "Unit Economics Quality",
     "Combined ROIC + operating margin assessment.",
     "Strong unit economics is the single most reliable long-term "
     "performance indicator for consumer operators.",
     "Composite of ROIC and Operating Margin", "business_quality")
_add("channel_mix_quality", "Channel Mix Quality",
     "Qualitative read on digital vs physical mix.",
     "Digital-led operators have more favorable capex profiles. "
     "Inferred from CAPEX intensity.",
     "Inferred from CAPEX / Revenue", "business_quality")


SECTION_EXPLANATIONS = {
    "profile": {
        "title": "Company Profile",
        "description": (
            "Company identification, market cap tier, operator maturity stage, "
            "primary consumer-discretionary sub-segment (apparel, specialty "
            "retail, restaurants, autos, etc.), and geographic market-exposure tier."
        ),
    },
    "valuation": {
        "title": "Valuation Metrics",
        "description": (
            "Price-based ratios. P/E and P/FCF are the primary anchors for "
            "mature consumer operators; EV/EBITDA enables cross-comparison. "
            "For emerging brands, P/S and cash-to-market-cap are more useful."
        ),
    },
    "profitability": {
        "title": "Profitability Metrics",
        "description": (
            "Margin and return analysis. Gross margin is the proxy for pricing "
            "power; ROIC separates durable franchises from capital-destructive "
            "operators. Includes SG&A% and a store-contribution proxy."
        ),
    },
    "solvency": {
        "title": "Solvency & Survival",
        "description": (
            "Balance sheet strength. Debt/EBITDA and lease-adjusted leverage "
            "are the core metrics — operating-lease commitments are large for "
            "brick-and-mortar retail and restaurants. Cash runway only matters "
            "for pre-profit emerging operators."
        ),
    },
    "growth": {
        "title": "Growth & Capital Discipline",
        "description": (
            "Revenue/earnings growth, CAPEX intensity, and share dilution. "
            "Mature consumer operators should either hold shares flat or buy "
            "back; >3% dilution per year is a red flag in the sector."
        ),
    },
    "efficiency": {
        "title": "Operating Efficiency",
        "description": (
            "Asset turnover, inventory turnover, days inventory, working "
            "capital intensity, and revenue per employee. Inventory is "
            "especially important for apparel and specialty retail."
        ),
    },
    "share_structure": {
        "title": "Share Structure",
        "description": (
            "Shares outstanding, fully diluted, insider ownership, and "
            "institutional holdings. Founder-led consumer names with >10% "
            "insider ownership have historically outperformed."
        ),
    },
    "business_quality": {
        "title": "Consumer Business Quality Assessment",
        "description": (
            "Consumer-specific quality scoring. Evaluates brand strength, "
            "unit economics, financial position, management alignment, and "
            "capital discipline. Includes cyclical-sensitivity tagging."
        ),
    },
    "intrinsic_value": {
        "title": "Intrinsic Value Estimates",
        "description": (
            "Multiple valuation methods adapted by stage. Mature operators: "
            "DCF + EV/EBITDA comps. Scaling operators: EV/EBITDA peer comps. "
            "Emerging: EV/Revenue with margin-ramp. Franchise: DCF on royalty "
            "stream."
        ),
    },
    "conclusion": {
        "title": "Assessment Conclusion",
        "description": (
            "Weighted scoring across 5 categories with weights adapted by both "
            "tier and operator stage. Includes a 10-point consumer-discretionary "
            "screening checklist."
        ),
    },
}


CONCLUSION_METHODOLOGY = {
    "overall": {
        "title": "Conclusion Methodology",
        "description": (
            "Score is a weighted average of 5 categories (valuation, "
            "profitability, solvency, growth, business quality). Weights vary "
            "by BOTH company tier AND operator stage. Mature operators: "
            "profitability and quality weighted at 25% each. Emerging brands: "
            "solvency and growth weighted at 25-35%. Verdicts: Strong Buy "
            "(>=75), Buy (>=60), Hold (>=45), Caution (>=30), Avoid (<30)."
        ),
    },
    "valuation": {
        "title": "Valuation Score",
        "description": (
            "Starts at 50. Adjusted by P/E, P/FCF, EV/EBITDA, P/S, and P/B. "
            "Early-stage / emerging operators get a bonus for low P/B."
        ),
    },
    "profitability": {
        "title": "Profitability Score",
        "description": (
            "Starts at 50. ROIC is weighted most heavily, then gross margin, "
            "operating margin, and FCF conversion. Pre-profit operators "
            "default to 50 since margins are not meaningful yet."
        ),
    },
    "solvency": {
        "title": "Solvency Score",
        "description": (
            "Starts at 50. Debt/equity, debt/EBITDA, current ratio, interest "
            "coverage, and cash runway for pre-profit operators. Emerging "
            "brands are penalized heavily for any material debt."
        ),
    },
    "growth": {
        "title": "Growth Score",
        "description": (
            "Starts at 50. Revenue growth, 3-year CAGR, earnings growth, and "
            "share dilution. Scaling stage operators get the highest growth "
            "thresholds; net buybacks earn a bonus."
        ),
    },
    "business_quality": {
        "title": "Consumer Business Quality Score",
        "description": (
            "Composite of brand strength / gross margin (25pts), unit "
            "economics / ROIC (25pts), financial position (20pts), "
            "management alignment (15pts), and capital discipline (15pts). "
            "Includes cyclical-sensitivity tagging."
        ),
    },
}


def get_explanation(key): return METRIC_EXPLANATIONS.get(key)


def get_section_explanation(section): return SECTION_EXPLANATIONS.get(section)


def get_conclusion_explanation(category=None):
    return CONCLUSION_METHODOLOGY.get(category or "overall")


def list_metrics(category=None):
    metrics = list(METRIC_EXPLANATIONS.values())
    return [m for m in metrics if m.category == category] if category else metrics
