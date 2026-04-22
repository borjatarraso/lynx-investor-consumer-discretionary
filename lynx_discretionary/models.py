"""Data models for Lynx Consumer Discretionary — consumer-focused fundamental analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Company tier classification (market cap based)
# ---------------------------------------------------------------------------

class CompanyTier(str, Enum):
    MEGA = "Mega Cap"
    LARGE = "Large Cap"
    MID = "Mid Cap"
    SMALL = "Small Cap"
    MICRO = "Micro Cap"
    NANO = "Nano Cap"


def classify_tier(market_cap: Optional[float]) -> CompanyTier:
    if market_cap is None or market_cap <= 0:
        return CompanyTier.NANO
    if market_cap >= 200_000_000_000:
        return CompanyTier.MEGA
    if market_cap >= 10_000_000_000:
        return CompanyTier.LARGE
    if market_cap >= 2_000_000_000:
        return CompanyTier.MID
    if market_cap >= 300_000_000:
        return CompanyTier.SMALL
    if market_cap >= 50_000_000:
        return CompanyTier.MICRO
    return CompanyTier.NANO


# ---------------------------------------------------------------------------
# Consumer discretionary company stage classification
#
# Stages span the full operator life cycle from emerging concept to mature
# franchise. Member names are kept identical to other Lince agents so shared
# plumbing (relevance tables, conclusion weights) continues to work — only the
# string values are consumer-specific.
# ---------------------------------------------------------------------------

class CompanyStage(str, Enum):
    GRASSROOTS = "Early Stage / Pre-Profit"
    EXPLORER = "Emerging Brand"
    DEVELOPER = "Scaling Operator"
    PRODUCER = "Mature Operator"
    ROYALTY = "Franchise / Asset-Light"


class Segment(str, Enum):
    """Consumer discretionary sub-segment classification."""
    APPAREL = "Apparel & Footwear"
    SPECIALTY_RETAIL = "Specialty Retail"
    HOME_IMPROVEMENT = "Home Improvement"
    RESTAURANTS = "Restaurants"
    AUTOMOTIVE = "Automotive"
    LODGING_TRAVEL = "Lodging & Travel"
    LEISURE = "Leisure & Entertainment"
    ECOMMERCE = "E-commerce"
    LUXURY = "Luxury Goods"
    HOMEBUILDING = "Homebuilding"
    OTHER = "Other Consumer Discretionary"


class JurisdictionTier(str, Enum):
    """Market-exposure tier — geographic revenue concentration risk."""
    TIER_1 = "Tier 1 — Developed Markets"
    TIER_2 = "Tier 2 — Mixed Developed/Emerging"
    TIER_3 = "Tier 3 — High Concentration Risk"
    UNKNOWN = "Unknown"


class Relevance(str, Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    RELEVANT = "relevant"
    CONTEXTUAL = "contextual"
    IRRELEVANT = "irrelevant"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    WATCH = "WATCH"
    OK = "OK"
    STRONG = "STRONG"
    NA = "N/A"


# ---------------------------------------------------------------------------
# Core data models
# ---------------------------------------------------------------------------

@dataclass
class CompanyProfile:
    ticker: str
    name: str
    isin: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    market_cap: Optional[float] = None
    description: Optional[str] = None
    website: Optional[str] = None
    employees: Optional[int] = None
    tier: CompanyTier = CompanyTier.NANO
    stage: CompanyStage = CompanyStage.GRASSROOTS
    primary_segment: Segment = Segment.OTHER
    jurisdiction_tier: JurisdictionTier = JurisdictionTier.UNKNOWN
    jurisdiction_country: Optional[str] = None


@dataclass
class ValuationMetrics:
    pe_trailing: Optional[float] = None
    pe_forward: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    p_fcf: Optional[float] = None
    ev_ebitda: Optional[float] = None
    ev_revenue: Optional[float] = None
    peg_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_yield: Optional[float] = None
    enterprise_value: Optional[float] = None
    market_cap: Optional[float] = None
    price_to_tangible_book: Optional[float] = None
    price_to_ncav: Optional[float] = None
    # Consumer-discretionary-specific valuation
    ev_per_store: Optional[float] = None       # Enterprise value per physical location
    price_to_sales_growth: Optional[float] = None  # P/S normalized by revenue growth
    p_fcf_forward: Optional[float] = None
    cash_to_market_cap: Optional[float] = None


@dataclass
class ProfitabilityMetrics:
    roe: Optional[float] = None
    roa: Optional[float] = None
    roic: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    fcf_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None
    # Consumer-specific profitability signals
    sga_pct_of_revenue: Optional[float] = None       # SG&A / revenue — operating leverage
    rd_pct_of_revenue: Optional[float] = None        # R&D / revenue (brands/autos)
    store_contribution_margin: Optional[float] = None  # approx store-level margin
    gross_margin_trend: Optional[str] = None         # "expanding", "stable", "compressing"


@dataclass
class SolvencyMetrics:
    debt_to_equity: Optional[float] = None
    debt_to_ebitda: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    altman_z_score: Optional[float] = None
    net_debt: Optional[float] = None
    total_debt: Optional[float] = None
    total_cash: Optional[float] = None
    cash_burn_rate: Optional[float] = None
    cash_runway_years: Optional[float] = None
    working_capital: Optional[float] = None
    cash_per_share: Optional[float] = None
    tangible_book_value: Optional[float] = None
    ncav: Optional[float] = None
    ncav_per_share: Optional[float] = None
    quarterly_burn_rate: Optional[float] = None
    burn_as_pct_of_market_cap: Optional[float] = None
    # Consumer-discretionary-specific solvency
    lease_adjusted_debt_ratio: Optional[float] = None   # (debt + 8x rent) / EBITDAR proxy
    debt_service_coverage: Optional[float] = None       # EBITDA / interest
    capex_to_cfo: Optional[float] = None                # capex / operating cash flow


@dataclass
class GrowthMetrics:
    revenue_growth_yoy: Optional[float] = None
    revenue_cagr_3y: Optional[float] = None
    revenue_cagr_5y: Optional[float] = None
    earnings_growth_yoy: Optional[float] = None
    earnings_cagr_3y: Optional[float] = None
    earnings_cagr_5y: Optional[float] = None
    fcf_growth_yoy: Optional[float] = None
    book_value_growth_yoy: Optional[float] = None
    dividend_growth_5y: Optional[float] = None
    shares_growth_yoy: Optional[float] = None
    shares_growth_3y_cagr: Optional[float] = None
    fully_diluted_shares: Optional[float] = None
    dilution_ratio: Optional[float] = None
    production_growth_yoy: Optional[float] = None  # reused as unit/store growth proxy
    # Consumer-discretionary-specific growth
    capex_intensity: Optional[float] = None        # capex / revenue
    same_store_sales_proxy: Optional[float] = None  # revenue growth minus unit growth
    rd_intensity: Optional[float] = None            # R&D / revenue trend
    operating_leverage: Optional[float] = None      # earnings growth / revenue growth


@dataclass
class EfficiencyMetrics:
    asset_turnover: Optional[float] = None
    inventory_turnover: Optional[float] = None
    receivables_turnover: Optional[float] = None
    days_sales_outstanding: Optional[float] = None
    days_inventory: Optional[float] = None
    cash_conversion_cycle: Optional[float] = None
    # Consumer-discretionary-specific
    revenue_per_employee: Optional[float] = None
    working_capital_intensity: Optional[float] = None   # working capital / revenue


@dataclass
class BusinessQualityIndicators:
    """Consumer-discretionary business-quality indicators.

    Captures brand strength, unit economics, channel mix, balance-sheet
    alignment, and cyclical sensitivity — the qualitative factors that
    separate resilient consumer operators from cyclically exposed ones.
    """
    quality_score: Optional[float] = None
    management_quality: Optional[str] = None
    insider_ownership_pct: Optional[float] = None
    management_track_record: Optional[str] = None
    brand_strength: Optional[str] = None
    brand_strength_score: Optional[float] = None
    unit_economics_quality: Optional[str] = None
    channel_mix_quality: Optional[str] = None
    financial_position: Optional[str] = None
    dilution_risk: Optional[str] = None
    share_structure_assessment: Optional[str] = None
    cyclical_sensitivity: Optional[str] = None         # "low", "moderate", "high", "extreme"
    consumer_health_exposure: Optional[str] = None
    competitive_position: Optional[str] = None
    margin_resilience: Optional[str] = None
    customer_concentration: Optional[str] = None
    insider_alignment: Optional[str] = None
    revenue_predictability: Optional[str] = None
    asset_backing: Optional[str] = None
    near_term_catalysts: list[str] = field(default_factory=list)
    roic_history: list[Optional[float]] = field(default_factory=list)
    gross_margin_history: list[Optional[float]] = field(default_factory=list)


@dataclass
class IntrinsicValue:
    dcf_value: Optional[float] = None
    graham_number: Optional[float] = None
    lynch_fair_value: Optional[float] = None
    ncav_value: Optional[float] = None
    asset_based_value: Optional[float] = None
    nav_per_share: Optional[float] = None
    ev_resource_implied_price: Optional[float] = None  # kept for API parity (unused)
    current_price: Optional[float] = None
    margin_of_safety_dcf: Optional[float] = None
    margin_of_safety_graham: Optional[float] = None
    margin_of_safety_ncav: Optional[float] = None
    margin_of_safety_asset: Optional[float] = None
    margin_of_safety_nav: Optional[float] = None
    primary_method: Optional[str] = None
    secondary_method: Optional[str] = None


@dataclass
class ShareStructure:
    shares_outstanding: Optional[float] = None
    fully_diluted_shares: Optional[float] = None
    warrants_outstanding: Optional[float] = None
    options_outstanding: Optional[float] = None
    insider_ownership_pct: Optional[float] = None
    institutional_ownership_pct: Optional[float] = None
    float_shares: Optional[float] = None
    share_structure_assessment: Optional[str] = None
    warrant_overhang_risk: Optional[str] = None


@dataclass
class InsiderTransaction:
    """A single insider buy/sell transaction."""
    insider: str = ""
    position: str = ""
    transaction_type: str = ""
    shares: Optional[float] = None
    value: Optional[float] = None
    date: str = ""


@dataclass
class MarketIntelligence:
    """Market sentiment, insider activity, institutional holdings, and technicals.

    For consumer discretionary investors this section also tracks the sector
    ETF (XLY / VCR) and a retail peer ETF as context for relative performance.
    """
    # Insider activity
    insider_transactions: list[InsiderTransaction] = field(default_factory=list)
    net_insider_shares_3m: Optional[float] = None
    insider_buy_signal: Optional[str] = None

    # Institutional holders
    top_holders: list[str] = field(default_factory=list)
    institutions_count: Optional[int] = None
    institutions_pct: Optional[float] = None

    # Analyst consensus
    analyst_count: Optional[int] = None
    recommendation: Optional[str] = None
    target_high: Optional[float] = None
    target_low: Optional[float] = None
    target_mean: Optional[float] = None
    target_upside_pct: Optional[float] = None

    # Short interest
    shares_short: Optional[float] = None
    short_pct_of_float: Optional[float] = None
    short_ratio_days: Optional[float] = None
    short_squeeze_risk: Optional[str] = None

    # Price technicals
    price_current: Optional[float] = None
    price_52w_high: Optional[float] = None
    price_52w_low: Optional[float] = None
    pct_from_52w_high: Optional[float] = None
    pct_from_52w_low: Optional[float] = None
    price_52w_range_position: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    above_sma_50: Optional[bool] = None
    above_sma_200: Optional[bool] = None
    golden_cross: Optional[bool] = None
    beta: Optional[float] = None
    avg_volume: Optional[float] = None
    volume_10d_avg: Optional[float] = None
    volume_trend: Optional[str] = None

    # Projected dilution (for early-stage / pre-profit operators)
    projected_dilution_annual_pct: Optional[float] = None
    projected_shares_in_2y: Optional[float] = None
    financing_warning: Optional[str] = None

    # Macro context — consumer cyclicality proxies
    commodity_name: Optional[str] = None        # e.g. "Consumer Confidence", "Retail Sales"
    commodity_price: Optional[float] = None
    commodity_currency: str = "USD"
    commodity_52w_high: Optional[float] = None
    commodity_52w_low: Optional[float] = None
    commodity_52w_position: Optional[float] = None
    commodity_ytd_change: Optional[float] = None

    # Sector ETF context
    sector_etf_name: Optional[str] = None
    sector_etf_ticker: Optional[str] = None
    sector_etf_price: Optional[float] = None
    sector_etf_3m_perf: Optional[float] = None
    peer_etf_name: Optional[str] = None
    peer_etf_ticker: Optional[str] = None
    peer_etf_price: Optional[float] = None
    peer_etf_3m_perf: Optional[float] = None

    # Risk warnings
    risk_warnings: list[str] = field(default_factory=list)

    # Consumer discretionary disclaimers
    disclaimers: list[str] = field(default_factory=list)


@dataclass
class FinancialStatement:
    period: str
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_income: Optional[float] = None
    net_income: Optional[float] = None
    ebitda: Optional[float] = None
    interest_expense: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    total_equity: Optional[float] = None
    total_debt: Optional[float] = None
    total_cash: Optional[float] = None
    current_assets: Optional[float] = None
    current_liabilities: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    free_cash_flow: Optional[float] = None
    dividends_paid: Optional[float] = None
    shares_outstanding: Optional[float] = None
    eps: Optional[float] = None
    book_value_per_share: Optional[float] = None
    # Consumer-discretionary-specific line items (best effort from filings)
    selling_general_admin: Optional[float] = None
    research_development: Optional[float] = None
    inventory: Optional[float] = None


@dataclass
class AnalysisConclusion:
    overall_score: float = 0.0
    verdict: str = ""
    summary: str = ""
    category_scores: dict = field(default_factory=dict)
    category_summaries: dict = field(default_factory=dict)
    strengths: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    tier_note: str = ""
    stage_note: str = ""
    screening_checklist: dict = field(default_factory=dict)


@dataclass
class MetricExplanation:
    key: str
    full_name: str
    description: str
    why_used: str
    formula: str
    category: str


@dataclass
class Filing:
    form_type: str
    filing_date: str
    period: str
    url: str
    description: Optional[str] = None
    local_path: Optional[str] = None


@dataclass
class NewsArticle:
    title: str
    url: str
    published: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    local_path: Optional[str] = None


@dataclass
class AnalysisReport:
    profile: CompanyProfile
    valuation: Optional[ValuationMetrics] = None
    profitability: Optional[ProfitabilityMetrics] = None
    solvency: Optional[SolvencyMetrics] = None
    growth: Optional[GrowthMetrics] = None
    efficiency: Optional[EfficiencyMetrics] = None
    business_quality: Optional[BusinessQualityIndicators] = None
    intrinsic_value: Optional[IntrinsicValue] = None
    share_structure: Optional[ShareStructure] = None
    market_intelligence: Optional[MarketIntelligence] = None
    financials: list[FinancialStatement] = field(default_factory=list)
    filings: list[Filing] = field(default_factory=list)
    news: list[NewsArticle] = field(default_factory=list)
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ---------------------------------------------------------------------------
# Stage classification helpers (consumer discretionary)
# ---------------------------------------------------------------------------
#
# Stages are derived heuristically from the business description, revenue,
# and profitability signals.  The broad intuition:
#
#   GRASSROOTS: early-stage / pre-profit (persistent operating losses,
#               low revenue, or explicit "startup" language)
#   EXPLORER:   emerging brand (positive revenue, not yet consistently
#               profitable)
#   DEVELOPER:  scaling operator (rapid unit / geographic expansion,
#               meaningful revenue, expanding margins)
#   PRODUCER:   mature operator (large, stable, comp-sales focused,
#               consistent operating profits)
#   ROYALTY:    franchise / asset-light (franchise-dominant model:
#               royalties, licensing, high margins, low capex)

_STAGE_KEYWORDS = {
    CompanyStage.ROYALTY: [
        "franchise", "franchised", "franchisee", "royalty", "licensing",
        "asset-light", "asset light", "licensee", "franchisor",
    ],
    CompanyStage.PRODUCER: [
        "comparable store sales", "same-store sales", "comparable sales",
        "established", "global leader", "operates more than",
        "operates over", "nationwide", "global retailer",
    ],
    CompanyStage.DEVELOPER: [
        "expanding", "expansion", "opening new stores", "store growth",
        "rolling out", "entering new markets", "scaling",
        "international expansion",
    ],
    CompanyStage.EXPLORER: [
        "emerging", "growth stage", "early growth", "direct-to-consumer",
        "direct to consumer", "d2c", "digital native", "launched",
    ],
    CompanyStage.GRASSROOTS: [
        "early stage", "pre-revenue", "startup", "incubat",
    ],
}

_SEGMENT_KEYWORDS = {
    Segment.HOMEBUILDING: ["homebuilder", "home builder", "homebuilding", "residential construction"],
    Segment.AUTOMOTIVE: [
        "automobile", "automotive", "auto manufactur", "passenger cars",
        "vehicle manufactur", "electric vehicle", "evs", "automaker",
    ],
    Segment.LODGING_TRAVEL: [
        "hotel", "lodging", "resort", "cruise", "airline", "travel",
        "booking", "vacation", "timeshare",
    ],
    Segment.RESTAURANTS: [
        "restaurant", "quick service", "fast food", "casual dining",
        "coffee shop", "pizza",
    ],
    Segment.HOME_IMPROVEMENT: [
        "home improvement", "home center", "hardware store", "diy",
        "do-it-yourself",
    ],
    Segment.ECOMMERCE: [
        "e-commerce", "ecommerce", "online retailer", "online marketplace",
        "online store", "digital marketplace",
    ],
    Segment.APPAREL: [
        "apparel", "footwear", "athletic wear", "activewear", "sportswear",
        "clothing", "denim", "shoes", "sneaker",
    ],
    Segment.LUXURY: [
        "luxury", "high-end", "haute couture", "premium lifestyle",
    ],
    Segment.SPECIALTY_RETAIL: [
        "specialty retailer", "specialty store", "off-price",
        "discount retailer", "department store", "big-box",
    ],
    Segment.LEISURE: [
        "leisure", "gaming", "casino", "theme park", "amusement",
        "sporting goods", "fitness", "entertainment",
    ],
}

# Market-exposure tiers — consumer companies face geographic revenue
# concentration risk. Tier 1 is large diversified developed-market revenue;
# Tier 3 is heavy concentration in a single volatile market.
_TIER_1_JURISDICTIONS = {
    "united states", "canada", "united kingdom", "germany", "france",
    "australia", "japan", "switzerland", "netherlands", "sweden", "denmark",
    "norway", "finland", "ireland", "new zealand",
}

_TIER_2_JURISDICTIONS = {
    "spain", "italy", "portugal", "south korea", "taiwan", "singapore",
    "israel", "mexico", "poland", "czech republic", "greece",
}


def classify_stage(description: Optional[str], revenue: Optional[float],
                   info: Optional[dict] = None) -> CompanyStage:
    if description is None:
        description = ""
    desc_lower = description.lower()

    rev = revenue or 0
    info = info or {}
    op_margin = info.get("operatingMargins")
    profit_margin = info.get("profitMargins")

    # Franchise / asset-light keywords dominate if present
    for kw in _STAGE_KEYWORDS[CompanyStage.ROYALTY]:
        if kw in desc_lower:
            return CompanyStage.ROYALTY

    # Large mature operator: >$5B revenue AND positive operating margin
    if rev > 5_000_000_000 and (op_margin is None or op_margin > 0.03):
        for kw in _STAGE_KEYWORDS[CompanyStage.PRODUCER]:
            if kw in desc_lower:
                return CompanyStage.PRODUCER
        return CompanyStage.PRODUCER

    # Scaling operator: meaningful revenue and expansion language
    if rev > 500_000_000:
        for kw in _STAGE_KEYWORDS[CompanyStage.DEVELOPER]:
            if kw in desc_lower:
                return CompanyStage.DEVELOPER
        if op_margin is not None and op_margin > 0.05:
            return CompanyStage.PRODUCER
        return CompanyStage.DEVELOPER

    # Emerging brand
    if rev > 20_000_000:
        return CompanyStage.EXPLORER

    # Keyword match in description as tiebreaker
    for stage in [CompanyStage.DEVELOPER, CompanyStage.EXPLORER,
                  CompanyStage.GRASSROOTS]:
        for kw in _STAGE_KEYWORDS[stage]:
            if kw in desc_lower:
                return stage

    # Fallback: pre-revenue / losses
    if profit_margin is not None and profit_margin < -0.10:
        return CompanyStage.GRASSROOTS

    return CompanyStage.EXPLORER


def classify_segment(description: Optional[str],
                     industry: Optional[str] = None) -> Segment:
    import re
    text = ((description or "") + " " + (industry or "")).lower()
    scores: dict[Segment, int] = {}
    for seg, keywords in _SEGMENT_KEYWORDS.items():
        count = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if len(kw_lower) <= 3:
                if re.search(r"\b" + re.escape(kw_lower) + r"\b", text):
                    count += 1
            else:
                if kw_lower in text:
                    count += 1
        if count > 0:
            scores[seg] = count
    if scores:
        return max(scores, key=scores.get)
    return Segment.OTHER


def classify_jurisdiction(country: Optional[str],
                          description: Optional[str] = None) -> JurisdictionTier:
    if not country:
        return JurisdictionTier.UNKNOWN
    c_lower = country.lower().strip()
    desc_lower = (description or "").lower()
    for j in _TIER_1_JURISDICTIONS:
        if j in c_lower or j in desc_lower:
            return JurisdictionTier.TIER_1
    for j in _TIER_2_JURISDICTIONS:
        if j in c_lower or j in desc_lower:
            return JurisdictionTier.TIER_2
    return JurisdictionTier.TIER_3
