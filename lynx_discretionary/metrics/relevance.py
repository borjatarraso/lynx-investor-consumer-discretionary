"""Metric relevance by company tier AND operator stage.

Defines which metrics are CRITICAL, RELEVANT, CONTEXTUAL, or IRRELEVANT
for each combination of company size tier and operator maturity stage.

For consumer-discretionary analysis:
  CRITICAL    — Must-check metric for this stage. Highlighted with bold star marker.
                E.g. gross margin for mature operators, cash runway for emerging brands.
  RELEVANT    — Important and displayed normally. Useful context for the analysis.
  CONTEXTUAL  — Shown dimmed. Informational only, not a primary decision driver.
  IRRELEVANT  — Not meaningful for this stage/tier. Hidden or struck-through.

The relevance system drives visual highlighting across all four interface modes
(console, interactive, TUI, GUI) to guide investors toward the metrics that
matter most for consumer-discretionary operators at each maturity stage.
"""

from __future__ import annotations

from lynx_discretionary.models import CompanyStage, CompanyTier, Relevance

C = Relevance.CRITICAL
P = Relevance.IMPORTANT   # "P" for Priority/Important
R = Relevance.RELEVANT
X = Relevance.CONTEXTUAL
I = Relevance.IRRELEVANT


def get_relevance(
    metric_key: str,
    tier: CompanyTier,
    category: str = "valuation",
    stage: CompanyStage = CompanyStage.EXPLORER,
) -> Relevance:
    """Look up relevance for a metric given tier and stage.

    Stage overrides take precedence over tier-based lookups because
    the development stage is the primary axis for Consumer Discretionary analysis.
    """
    stage_override = _STAGE_OVERRIDES.get(metric_key, {}).get(stage)
    if stage_override is not None:
        return stage_override

    table = {
        "valuation": VALUATION_RELEVANCE,
        "profitability": PROFITABILITY_RELEVANCE,
        "solvency": SOLVENCY_RELEVANCE,
        "growth": GROWTH_RELEVANCE,
        "business_quality": BUSINESS_QUALITY_RELEVANCE,
        "share_structure": SHARE_STRUCTURE_RELEVANCE,
    }.get(category, {})
    entry = table.get(metric_key, {})
    return entry.get(tier, Relevance.RELEVANT)


# ======================================================================
# Stage-based overrides (take precedence over tier-based lookups)
# ======================================================================

_STAGE_OVERRIDES: dict[str, dict[CompanyStage, Relevance]] = {
    # VALUATION
    "pe_trailing": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: I, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "pe_forward": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: I, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: P},
    "p_fcf": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: I, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "ev_ebitda": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: X, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "ev_revenue": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: X, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "peg_ratio": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: I, CompanyStage.PRODUCER: X, CompanyStage.ROYALTY: X},
    "dividend_yield": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: I, CompanyStage.PRODUCER: X, CompanyStage.ROYALTY: P},
    "earnings_yield": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: I, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "cash_to_market_cap": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: X, CompanyStage.ROYALTY: X},
    "pb_ratio": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "price_to_tangible_book": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: X},
    "price_to_ncav": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: X, CompanyStage.ROYALTY: I},
    "ps_ratio": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: I, CompanyStage.DEVELOPER: I, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    # PROFITABILITY — consumer operators generate revenue at every stage,
    # so margin metrics stay meaningful even for EXPLORER-stage brands.
    "roe": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: X, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "roa": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: X, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "roic": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "gross_margin": {CompanyStage.GRASSROOTS: R, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "operating_margin": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "net_margin": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "fcf_margin": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "ebitda_margin": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "sga_pct_of_revenue": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "store_contribution_margin": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: X},
    # SOLVENCY — consumer operators use leverage heavily; Debt/EBITDA and
    # lease-adjusted leverage are critical for mature stages.
    "cash_burn_rate": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: X, CompanyStage.ROYALTY: I},
    "cash_runway_years": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: X, CompanyStage.ROYALTY: I},
    "burn_as_pct_of_market_cap": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: I, CompanyStage.ROYALTY: I},
    "working_capital": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "cash_per_share": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: X},
    "ncav_per_share": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: X, CompanyStage.PRODUCER: X, CompanyStage.ROYALTY: I},
    "current_ratio": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "quick_ratio": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: X},
    "debt_to_equity": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "debt_to_ebitda": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "lease_adjusted_debt_ratio": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: P},
    "interest_coverage": {CompanyStage.GRASSROOTS: R, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: P},
    "altman_z_score": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: X},
    "total_cash": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: X},
    "total_debt": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "net_debt": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "debt_service_coverage": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    # GROWTH — revenue growth matters at every stage for consumer operators.
    "shares_growth_yoy": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "shares_growth_3y_cagr": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "revenue_growth_yoy": {CompanyStage.GRASSROOTS: R, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "revenue_cagr_3y": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "revenue_cagr_5y": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: R},
    "earnings_growth_yoy": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "earnings_cagr_3y": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "earnings_cagr_5y": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: X, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: R},
    "book_value_growth_yoy": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: R, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: X},
    "fcf_growth_yoy": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "capex_intensity": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: C},
    "same_store_sales_proxy": {CompanyStage.GRASSROOTS: I, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    "operating_leverage": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: R},
    # DISCRETIONARY QUALITY
    "quality_score": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "insider_alignment": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "financial_position": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "dilution_risk": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: X},
    "asset_backing": {CompanyStage.GRASSROOTS: P, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: I},
    "revenue_predictability": {CompanyStage.GRASSROOTS: X, CompanyStage.EXPLORER: X, CompanyStage.DEVELOPER: R, CompanyStage.PRODUCER: C, CompanyStage.ROYALTY: C},
    # SHARE STRUCTURE
    "shares_outstanding": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: X},
    "fully_diluted_shares": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "insider_ownership_pct": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: C, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: P},
    "institutional_ownership_pct": {CompanyStage.GRASSROOTS: R, CompanyStage.EXPLORER: P, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: P, CompanyStage.ROYALTY: R},
    "share_structure_assessment": {CompanyStage.GRASSROOTS: C, CompanyStage.EXPLORER: C, CompanyStage.DEVELOPER: P, CompanyStage.PRODUCER: R, CompanyStage.ROYALTY: X},
}


# ======================================================================
# Tier-based relevance tables (fallback when no stage override exists)
# ======================================================================

VALUATION_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "pe_trailing":           {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "pb_ratio":              {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "ps_ratio":              {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: R, CompanyTier.SMALL: R, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "p_fcf":                 {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "ev_ebitda":             {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "cash_to_market_cap":    {CompanyTier.MEGA: I, CompanyTier.LARGE: I, CompanyTier.MID: X, CompanyTier.SMALL: P, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "price_to_tangible_book":{CompanyTier.MEGA: X, CompanyTier.LARGE: X, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "price_to_ncav":         {CompanyTier.MEGA: I, CompanyTier.LARGE: I, CompanyTier.MID: X, CompanyTier.SMALL: P, CompanyTier.MICRO: C, CompanyTier.NANO: C},
}

PROFITABILITY_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "roe":              {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "roic":             {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
    "gross_margin":     {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: P, CompanyTier.NANO: X},
    "fcf_margin":       {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: P, CompanyTier.SMALL: P, CompanyTier.MICRO: X, CompanyTier.NANO: I},
}

SOLVENCY_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "debt_to_equity":    {CompanyTier.MEGA: C, CompanyTier.LARGE: C, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "current_ratio":     {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "cash_burn_rate":    {CompanyTier.MEGA: I, CompanyTier.LARGE: I, CompanyTier.MID: X, CompanyTier.SMALL: P, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "cash_runway_years": {CompanyTier.MEGA: I, CompanyTier.LARGE: I, CompanyTier.MID: X, CompanyTier.SMALL: P, CompanyTier.MICRO: C, CompanyTier.NANO: C},
}

GROWTH_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "shares_growth_yoy":      {CompanyTier.MEGA: X, CompanyTier.LARGE: X, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "revenue_growth_yoy":     {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: C, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
}

BUSINESS_QUALITY_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "quality_score":          {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "insider_alignment":      {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
}

SHARE_STRUCTURE_RELEVANCE: dict[str, dict[CompanyTier, Relevance]] = {
    "shares_outstanding":       {CompanyTier.MEGA: X, CompanyTier.LARGE: X, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "fully_diluted_shares":     {CompanyTier.MEGA: X, CompanyTier.LARGE: X, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
    "insider_ownership_pct":    {CompanyTier.MEGA: P, CompanyTier.LARGE: P, CompanyTier.MID: P, CompanyTier.SMALL: C, CompanyTier.MICRO: C, CompanyTier.NANO: C},
}
