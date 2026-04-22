"""Consumer-discretionary-specialized metrics calculation engine.

All calculations are both tier-aware AND stage-aware.
"""

from __future__ import annotations

import math
from typing import Optional

from datetime import datetime, timedelta

import yfinance as yf

from lynx_discretionary.models import (
    CompanyStage, CompanyTier, EfficiencyMetrics, FinancialStatement,
    GrowthMetrics, InsiderTransaction, IntrinsicValue, MarketIntelligence,
    BusinessQualityIndicators, ProfitabilityMetrics, Segment, ShareStructure,
    SolvencyMetrics, ValuationMetrics,
)


def calc_valuation(
    info: dict, statements: list[FinancialStatement],
    tier: CompanyTier, stage: CompanyStage,
) -> ValuationMetrics:
    v = ValuationMetrics()
    v.pe_trailing = info.get("trailingPE")
    v.pe_forward = info.get("forwardPE")
    v.pb_ratio = info.get("priceToBook")
    v.ps_ratio = info.get("priceToSalesTrailing12Months")
    v.peg_ratio = info.get("pegRatio")
    v.ev_ebitda = info.get("enterpriseToEbitda")
    v.ev_revenue = info.get("enterpriseToRevenue")
    v.dividend_yield = info.get("trailingAnnualDividendYield") or info.get("dividendYield")
    v.enterprise_value = info.get("enterpriseValue")
    v.market_cap = info.get("marketCap")

    if v.pe_trailing and v.pe_trailing > 0:
        v.earnings_yield = 1.0 / v.pe_trailing

    price = info.get("currentPrice") or info.get("regularMarketPrice")
    shares = info.get("sharesOutstanding")

    if price and shares and statements:
        latest = statements[0]
        if latest.free_cash_flow and latest.free_cash_flow > 0:
            v.p_fcf = (price * shares) / latest.free_cash_flow

    if tier in (CompanyTier.MICRO, CompanyTier.NANO, CompanyTier.SMALL) and statements:
        latest = statements[0]
        if latest.total_equity and latest.total_assets and price and shares:
            tbv = latest.total_equity
            if shares > 0:
                tbv_per_share = tbv / shares
                if tbv_per_share > 0:
                    v.price_to_tangible_book = price / tbv_per_share
        if latest.current_assets and latest.total_liabilities and shares and shares > 0:
            ncav = latest.current_assets - latest.total_liabilities
            ncav_ps = ncav / shares
            if ncav_ps > 0 and price:
                v.price_to_ncav = price / ncav_ps

    total_cash = info.get("totalCash")
    if total_cash and v.market_cap and v.market_cap > 0:
        v.cash_to_market_cap = total_cash / v.market_cap

    return v


def calc_profitability(
    info: dict, statements: list[FinancialStatement],
    tier: CompanyTier, stage: CompanyStage,
) -> ProfitabilityMetrics:
    p = ProfitabilityMetrics()
    p.roe = info.get("returnOnEquity")
    p.roa = info.get("returnOnAssets")
    p.gross_margin = info.get("grossMargins")
    p.operating_margin = info.get("operatingMargins")
    p.net_margin = info.get("profitMargins")

    if statements:
        s = statements[0]
        if s.operating_income is not None and s.total_assets and s.total_cash is not None:
            nopat = s.operating_income * 0.75
            invested_capital = s.total_assets - (s.total_cash or 0)
            if invested_capital > 0:
                p.roic = nopat / invested_capital
        if s.free_cash_flow and s.revenue and s.revenue > 0:
            p.fcf_margin = s.free_cash_flow / s.revenue
        if s.ebitda and s.revenue and s.revenue > 0:
            p.ebitda_margin = s.ebitda / s.revenue
        # Consumer-specific signals
        if s.selling_general_admin and s.revenue and s.revenue > 0:
            p.sga_pct_of_revenue = s.selling_general_admin / s.revenue
        if s.research_development and s.revenue and s.revenue > 0:
            p.rd_pct_of_revenue = s.research_development / s.revenue
        # Store contribution proxy: gross profit minus a rough fixed-overhead deduction
        if s.gross_profit and s.selling_general_admin and s.revenue and s.revenue > 0:
            store_contrib = s.gross_profit - s.selling_general_admin * 0.6
            p.store_contribution_margin = store_contrib / s.revenue

    # Gross margin trend across the most recent two years
    if len(statements) >= 2:
        a, b = statements[0], statements[1]
        if a.gross_profit and a.revenue and b.gross_profit and b.revenue and a.revenue > 0 and b.revenue > 0:
            gm_now = a.gross_profit / a.revenue
            gm_prev = b.gross_profit / b.revenue
            delta = gm_now - gm_prev
            if delta > 0.01:
                p.gross_margin_trend = "expanding"
            elif delta < -0.01:
                p.gross_margin_trend = "compressing"
            else:
                p.gross_margin_trend = "stable"

    return p


def calc_solvency(
    info: dict, statements: list[FinancialStatement],
    tier: CompanyTier, stage: CompanyStage,
) -> SolvencyMetrics:
    s = SolvencyMetrics()
    s.debt_to_equity = info.get("debtToEquity")
    if s.debt_to_equity:
        s.debt_to_equity /= 100
    s.current_ratio = info.get("currentRatio")
    s.quick_ratio = info.get("quickRatio")
    s.total_debt = info.get("totalDebt")
    s.total_cash = info.get("totalCash")

    if s.total_debt is not None and s.total_cash is not None:
        s.net_debt = s.total_debt - s.total_cash

    shares = info.get("sharesOutstanding")
    market_cap = info.get("marketCap")

    if statements:
        st = statements[0]

        if st.ebitda and st.ebitda > 0 and s.total_debt:
            s.debt_to_ebitda = s.total_debt / st.ebitda

        if st.operating_income:
            ie = abs(st.interest_expense) if st.interest_expense else None
            if ie is None and s.total_debt:
                ie = s.total_debt * 0.05
            if ie and ie > 0:
                s.interest_coverage = st.operating_income / ie

        if st.total_assets and st.total_assets > 0 and st.revenue and st.revenue > 0:
            ta = st.total_assets
            wc = 0
            if st.current_assets is not None and st.current_liabilities is not None:
                wc = st.current_assets - st.current_liabilities
            re = (st.total_equity or 0) * 0.5
            ebit = st.operating_income or 0
            mcap = info.get("marketCap", 0)
            tl = st.total_liabilities or 1
            rev = st.revenue or 0
            z = (1.2 * wc / ta + 1.4 * re / ta + 3.3 * ebit / ta +
                 0.6 * mcap / tl + 1.0 * rev / ta)
            s.altman_z_score = round(z, 2)

        if st.current_assets is not None and st.current_liabilities is not None:
            s.working_capital = st.current_assets - st.current_liabilities

        if s.total_cash and shares and shares > 0:
            s.cash_per_share = s.total_cash / shares

        if st.total_equity:
            s.tangible_book_value = st.total_equity

        if st.current_assets is not None and st.total_liabilities is not None:
            s.ncav = st.current_assets - st.total_liabilities
            if shares and shares > 0:
                s.ncav_per_share = s.ncav / shares

        if len(statements) >= 2 and st.operating_cash_flow is not None:
            ocf = st.operating_cash_flow
            if ocf < 0:
                s.cash_burn_rate = ocf
                if s.total_cash and s.total_cash > 0:
                    s.cash_runway_years = s.total_cash / abs(ocf)
                s.quarterly_burn_rate = ocf / 4
            else:
                s.cash_burn_rate = 0

        if s.cash_burn_rate and s.cash_burn_rate < 0 and market_cap and market_cap > 0:
            s.burn_as_pct_of_market_cap = abs(s.cash_burn_rate) / market_cap

        # Capex to CFO ratio — capital intensity for scaling operators
        if st.capital_expenditure and st.operating_cash_flow and st.operating_cash_flow != 0:
            s.capex_to_cfo = abs(st.capital_expenditure) / abs(st.operating_cash_flow)

        # Debt service coverage (EBITDA / interest)
        if st.ebitda and st.ebitda > 0:
            ie = abs(st.interest_expense) if st.interest_expense else 0
            if ie > 0:
                s.debt_service_coverage = st.ebitda / ie

        # Lease-adjusted leverage proxy: (total_debt + 8 * rent_proxy) / EBITDAR
        # Without explicit rent expense we approximate rent = 15% of SG&A.
        rent_proxy = (st.selling_general_admin or 0) * 0.15
        ebitdar = (st.ebitda or 0) + rent_proxy
        adjusted_debt = (s.total_debt or 0) + rent_proxy * 8
        if ebitdar > 0 and adjusted_debt > 0:
            s.lease_adjusted_debt_ratio = adjusted_debt / ebitdar

    return s


def calc_growth(
    statements: list[FinancialStatement],
    tier: CompanyTier, stage: CompanyStage,
) -> GrowthMetrics:
    g = GrowthMetrics()
    if len(statements) < 2:
        return g
    stmts = statements

    if stmts[0].revenue and stmts[1].revenue and stmts[1].revenue != 0:
        g.revenue_growth_yoy = (stmts[0].revenue - stmts[1].revenue) / abs(stmts[1].revenue)

    if stmts[0].net_income and stmts[1].net_income and stmts[1].net_income != 0:
        g.earnings_growth_yoy = (stmts[0].net_income - stmts[1].net_income) / abs(stmts[1].net_income)

    if stmts[0].free_cash_flow and stmts[1].free_cash_flow and stmts[1].free_cash_flow != 0:
        g.fcf_growth_yoy = (stmts[0].free_cash_flow - stmts[1].free_cash_flow) / abs(stmts[1].free_cash_flow)

    if stmts[0].book_value_per_share and stmts[1].book_value_per_share and stmts[1].book_value_per_share != 0:
        g.book_value_growth_yoy = (stmts[0].book_value_per_share - stmts[1].book_value_per_share) / abs(stmts[1].book_value_per_share)

    if stmts[0].shares_outstanding and stmts[1].shares_outstanding and stmts[1].shares_outstanding > 0:
        g.shares_growth_yoy = (stmts[0].shares_outstanding - stmts[1].shares_outstanding) / stmts[1].shares_outstanding

    if len(stmts) >= 4 and stmts[0].shares_outstanding and stmts[3].shares_outstanding:
        g.shares_growth_3y_cagr = _cagr(stmts[3].shares_outstanding, stmts[0].shares_outstanding, 3)

    if len(stmts) >= 4:
        g.revenue_cagr_3y = _cagr(stmts[3].revenue, stmts[0].revenue, 3)
        g.earnings_cagr_3y = _cagr(stmts[3].net_income, stmts[0].net_income, 3)

    if len(stmts) >= 5:
        g.revenue_cagr_5y = _cagr(stmts[-1].revenue, stmts[0].revenue, len(stmts) - 1)
        g.earnings_cagr_5y = _cagr(stmts[-1].net_income, stmts[0].net_income, len(stmts) - 1)

    # Capex intensity (capex as % of revenue) — unit-economic indicator
    if stmts[0].capital_expenditure and stmts[0].revenue and stmts[0].revenue > 0:
        g.capex_intensity = abs(stmts[0].capital_expenditure) / stmts[0].revenue

    # R&D intensity (apparel brands, autos, specialty retail invest heavily in product dev)
    if stmts[0].research_development and stmts[0].revenue and stmts[0].revenue > 0:
        g.rd_intensity = stmts[0].research_development / stmts[0].revenue

    # Same-store-sales proxy: revenue growth minus physical-asset growth.
    # When unit economics are healthy revenue grows faster than fixed-asset base.
    if (
        len(stmts) >= 2
        and g.revenue_growth_yoy is not None
        and stmts[0].total_assets and stmts[1].total_assets
        and stmts[1].total_assets > 0
    ):
        asset_growth = (stmts[0].total_assets - stmts[1].total_assets) / stmts[1].total_assets
        g.same_store_sales_proxy = g.revenue_growth_yoy - asset_growth

    # Operating leverage (earnings growth per unit of revenue growth)
    if g.revenue_growth_yoy and g.earnings_growth_yoy and g.revenue_growth_yoy != 0:
        g.operating_leverage = g.earnings_growth_yoy / g.revenue_growth_yoy

    return g


def calc_efficiency(
    info: dict, statements: list[FinancialStatement], tier: CompanyTier,
) -> EfficiencyMetrics:
    e = EfficiencyMetrics()
    if not statements:
        return e
    s = statements[0]
    if s.revenue and s.total_assets and s.total_assets > 0:
        e.asset_turnover = s.revenue / s.total_assets

    # Inventory turnover — critical for apparel, retail, restaurants
    if s.cost_of_revenue and s.inventory and s.inventory > 0:
        e.inventory_turnover = s.cost_of_revenue / s.inventory
        e.days_inventory = 365 / e.inventory_turnover

    # Working-capital intensity
    if (
        s.revenue and s.revenue > 0
        and s.current_assets is not None and s.current_liabilities is not None
    ):
        working_capital = s.current_assets - s.current_liabilities
        e.working_capital_intensity = working_capital / s.revenue

    # Revenue per employee
    employees = info.get("fullTimeEmployees")
    if employees and s.revenue:
        e.revenue_per_employee = s.revenue / employees

    return e


def calc_share_structure(
    info: dict, statements: list[FinancialStatement],
    growth: GrowthMetrics, tier: CompanyTier, stage: CompanyStage,
) -> ShareStructure:
    ss = ShareStructure()
    ss.shares_outstanding = info.get("sharesOutstanding")
    ss.float_shares = info.get("floatShares")
    ss.insider_ownership_pct = info.get("heldPercentInsiders")
    ss.institutional_ownership_pct = info.get("heldPercentInstitutions")

    implied = info.get("impliedSharesOutstanding")
    if implied:
        ss.fully_diluted_shares = implied
    elif ss.shares_outstanding:
        ss.fully_diluted_shares = ss.shares_outstanding

    if ss.shares_outstanding and ss.fully_diluted_shares and ss.shares_outstanding > 0:
        ratio = ss.fully_diluted_shares / ss.shares_outstanding
        if growth:
            growth.dilution_ratio = ratio
            growth.fully_diluted_shares = ss.fully_diluted_shares

    if ss.fully_diluted_shares:
        fd = ss.fully_diluted_shares
        if fd < 80_000_000:
            ss.share_structure_assessment = "Very Tight (<80M shares)"
        elif fd < 150_000_000:
            ss.share_structure_assessment = "Tight (80-150M shares)"
        elif fd < 300_000_000:
            ss.share_structure_assessment = "Moderate (150-300M shares)"
        elif fd < 500_000_000:
            ss.share_structure_assessment = "Heavy (300-500M shares)"
        else:
            ss.share_structure_assessment = "Bloated (>500M shares)"

    return ss


_CYCLICAL_SEGMENTS = {
    Segment.AUTOMOTIVE, Segment.HOMEBUILDING, Segment.LODGING_TRAVEL,
    Segment.LEISURE, Segment.LUXURY,
}


def calc_business_quality(
    profitability: ProfitabilityMetrics,
    growth: GrowthMetrics,
    solvency: SolvencyMetrics,
    share_structure: ShareStructure,
    statements: list[FinancialStatement],
    info: dict,
    tier: CompanyTier,
    stage: CompanyStage,
) -> BusinessQualityIndicators:
    """Consumer-discretionary business-quality scoring.

    Weights five dimensions appropriate for consumer operators:

    1. Brand strength / gross margin resilience (25 pts) — proxy for pricing power
    2. Unit economics (ROIC + operating margin) (25 pts)
    3. Financial position (leverage + liquidity) (20 pts)
    4. Management alignment (insider ownership) (15 pts)
    5. Dilution / capital discipline (15 pts)

    Plus a cyclical-sensitivity qualitative tag (no score impact) that flags
    autos, homebuilding, travel, luxury, and leisure as high-cyclicality.
    """
    m = BusinessQualityIndicators()
    score = 0.0
    max_score = 0.0

    # ── 1. Brand strength / gross margin resilience (25 pts) ─────────
    max_score += 25
    gm = profitability.gross_margin if profitability else None
    gm_trend = profitability.gross_margin_trend if profitability else None
    if gm is not None:
        if gm >= 0.55:
            m.brand_strength = "Premium brand — >55% gross margin indicates strong pricing power"
            m.brand_strength_score = 100.0
            score += 25
        elif gm >= 0.40:
            m.brand_strength = "Strong brand — 40-55% gross margin"
            m.brand_strength_score = 75.0
            score += 18
        elif gm >= 0.28:
            m.brand_strength = "Moderate brand — 28-40% gross margin"
            m.brand_strength_score = 50.0
            score += 10
        elif gm >= 0.15:
            m.brand_strength = "Thin margins — commodity-like positioning"
            m.brand_strength_score = 25.0
            score += 4
        else:
            m.brand_strength = "Very thin margins — limited pricing power"
            m.brand_strength_score = 5.0
            score += 1
        if gm_trend == "expanding":
            m.margin_resilience = "Margins expanding — positive trend"
            score += 2
        elif gm_trend == "compressing":
            m.margin_resilience = "Margins compressing — watch closely"
            score -= 3
        else:
            m.margin_resilience = "Margins stable"
    else:
        m.brand_strength = "Brand / margin data unavailable"
        score += 8

    # ── 2. Unit economics: ROIC + operating margin (25 pts) ──────────
    max_score += 25
    roic = profitability.roic if profitability else None
    om = profitability.operating_margin if profitability else None
    ue_score = 0
    if roic is not None:
        if roic >= 0.20:
            ue_score += 15
            m.unit_economics_quality = "Excellent unit economics — ROIC > 20%"
        elif roic >= 0.12:
            ue_score += 10
            m.unit_economics_quality = "Strong unit economics — ROIC 12-20%"
        elif roic >= 0.08:
            ue_score += 6
            m.unit_economics_quality = "Adequate unit economics"
        elif roic >= 0:
            ue_score += 2
            m.unit_economics_quality = "Weak unit economics"
        else:
            m.unit_economics_quality = "Value-destructive unit economics (negative ROIC)"
    if om is not None:
        if om >= 0.15:
            ue_score += 10
        elif om >= 0.08:
            ue_score += 6
        elif om >= 0.03:
            ue_score += 3
        elif om < 0 and stage != CompanyStage.GRASSROOTS:
            ue_score -= 5
    if roic is None and om is None:
        m.unit_economics_quality = "Unit-economics data unavailable"
        ue_score = 10
    score += ue_score

    # ── 3. Financial position: leverage + liquidity (20 pts) ─────────
    max_score += 20
    fp_score = 0
    de_ebitda = solvency.debt_to_ebitda if solvency else None
    current_ratio = solvency.current_ratio if solvency else None
    runway = solvency.cash_runway_years if solvency else None
    burn = solvency.cash_burn_rate if solvency else None

    if de_ebitda is not None:
        if de_ebitda < 1.5:
            fp_score += 10
            m.financial_position = "Conservative leverage (Debt/EBITDA <1.5x)"
        elif de_ebitda < 3:
            fp_score += 6
            m.financial_position = "Moderate leverage"
        elif de_ebitda < 5:
            fp_score += 2
            m.financial_position = "Elevated leverage — cyclically exposed"
        else:
            m.financial_position = "High leverage (>5x) — distress risk in downturn"
    elif runway is not None:
        if runway > 3:
            fp_score += 10
            m.financial_position = "Strong — >3 years cash runway"
        elif runway > 1.5:
            fp_score += 6
            m.financial_position = "Adequate — 1.5-3 years runway"
        else:
            m.financial_position = "Tight — under 1.5 years runway"
            fp_score += 1
    elif burn is not None and burn >= 0:
        fp_score += 10
        m.financial_position = "Cash flow positive"
    else:
        m.financial_position = "Financial-position data unavailable"
        fp_score += 5

    if current_ratio is not None:
        if current_ratio > 1.8:
            fp_score += 6
        elif current_ratio > 1.2:
            fp_score += 3
        elif current_ratio < 1:
            fp_score -= 5
    score += fp_score

    # ── 4. Management alignment (15 pts) ──────────────────────────────
    max_score += 15
    insider_pct = share_structure.insider_ownership_pct if share_structure else None
    if insider_pct is not None:
        m.insider_ownership_pct = insider_pct
        if insider_pct > 0.15:
            m.insider_alignment = "Strong alignment — >15% insider ownership"
            m.management_quality = "Founder/family operator economics"
            score += 15
        elif insider_pct > 0.05:
            m.insider_alignment = "Meaningful alignment — 5-15% insider ownership"
            m.management_quality = "Insiders materially invested"
            score += 10
        elif insider_pct > 0.01:
            m.insider_alignment = "Low insider ownership (1-5%)"
            m.management_quality = "Professional management with limited skin"
            score += 4
        else:
            m.insider_alignment = "Very low insider ownership (<1%)"
            m.management_quality = "Professional management"
            score += 2
    else:
        m.insider_alignment = "Insider data unavailable"
        score += 6

    # ── 5. Capital discipline — dilution & buybacks (15 pts) ─────────
    max_score += 15
    dil = growth.shares_growth_yoy if growth else None
    if dil is not None:
        if dil < -0.02:
            m.dilution_risk = f"Net share buybacks ({abs(dil)*100:.1f}%/yr) — capital returned"
            score += 15
        elif dil < 0.01:
            m.dilution_risk = "Minimal dilution (<1%/yr)"
            score += 12
        elif dil < 0.03:
            m.dilution_risk = "Modest dilution (1-3%/yr)"
            score += 8
        elif dil < 0.08:
            m.dilution_risk = "Moderate dilution (3-8%/yr)"
            score += 3
        else:
            m.dilution_risk = f"Heavy dilution ({dil*100:.1f}%/yr) — value destruction risk"
    else:
        m.dilution_risk = "Dilution data unavailable"
        score += 5

    if share_structure and share_structure.share_structure_assessment:
        m.share_structure_assessment = share_structure.share_structure_assessment

    # ── Qualitative tags (no score impact) ────────────────────────────
    primary_segment = None
    try:
        # best-effort: we get segment indirectly through description / industry
        from lynx_discretionary.models import classify_segment
        primary_segment = classify_segment(
            info.get("longBusinessSummary"), info.get("industry")
        )
    except Exception:
        pass

    if primary_segment in _CYCLICAL_SEGMENTS:
        m.cyclical_sensitivity = "High — cyclical sub-segment (autos/homes/travel/luxury/leisure)"
    elif primary_segment == Segment.RESTAURANTS:
        m.cyclical_sensitivity = "Moderate — staples-like for QSR, discretionary for fine dining"
    elif primary_segment in (Segment.APPAREL, Segment.SPECIALTY_RETAIL):
        m.cyclical_sensitivity = "Moderate — tied to consumer confidence"
    elif primary_segment in (Segment.HOME_IMPROVEMENT, Segment.ECOMMERCE):
        m.cyclical_sensitivity = "Low-to-moderate — more resilient through cycles"
    else:
        m.cyclical_sensitivity = "Sensitivity inferred from stage and leverage"

    # Channel mix quality proxy (online vs physical) — inferred from capex intensity
    capex_int = growth.capex_intensity if growth else None
    if capex_int is not None:
        if capex_int < 0.03:
            m.channel_mix_quality = "Asset-light / digital mix"
        elif capex_int < 0.06:
            m.channel_mix_quality = "Balanced channel mix"
        else:
            m.channel_mix_quality = "Capex-heavy physical footprint"

    # Revenue predictability by stage
    revenues = [s.revenue for s in statements if s.revenue and s.revenue > 0]
    if revenues and stage in (CompanyStage.PRODUCER, CompanyStage.ROYALTY):
        if len(revenues) >= 2 and revenues[0] > revenues[1]:
            m.revenue_predictability = f"{stage.value} with growing revenue"
        else:
            m.revenue_predictability = f"{stage.value} with stable revenue"
    elif stage == CompanyStage.DEVELOPER:
        m.revenue_predictability = "Scaling — expect revenue volatility as unit economics mature"
    elif stage == CompanyStage.EXPLORER:
        m.revenue_predictability = "Emerging — revenue growth drives valuation"
    else:
        m.revenue_predictability = "Pre-profit — revenue predictability low"

    # Consumer health exposure
    if tier in (CompanyTier.NANO, CompanyTier.MICRO):
        m.consumer_health_exposure = "Single-concept exposure — consumer health moves with the concept"
    elif primary_segment in _CYCLICAL_SEGMENTS:
        m.consumer_health_exposure = "High beta to consumer confidence / durable goods demand"
    else:
        m.consumer_health_exposure = "Diversified exposure to consumer spending"

    m.roic_history = _calc_roic_history(statements)
    m.gross_margin_history = _calc_margin_history(statements)

    m.quality_score = round(max(0.0, (score / max_score) * 100), 1) if max_score > 0 else 0
    if m.quality_score >= 75:
        m.competitive_position = "Strong Position — High-Quality Consumer Franchise"
    elif m.quality_score >= 55:
        m.competitive_position = "Viable Position — Moderate-Quality Operator"
    elif m.quality_score >= 35:
        m.competitive_position = "Challenged — Below-Average Consumer Quality"
    else:
        m.competitive_position = "High Risk — Weak Consumer Fundamentals"

    return m


def calc_intrinsic_value(
    info: dict, statements: list[FinancialStatement],
    growth: GrowthMetrics, solvency: SolvencyMetrics,
    tier: CompanyTier, stage: CompanyStage,
    discount_rate: float = 0.10, terminal_growth: float = 0.03,
) -> IntrinsicValue:
    iv = IntrinsicValue()
    iv.current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    shares = info.get("sharesOutstanding")

    # Consumer-discretionary stage-appropriate valuation method selection
    if stage == CompanyStage.PRODUCER:
        iv.primary_method = "DCF (FCF to Firm)"
        iv.secondary_method = "EV/EBITDA Peer Comps"
    elif stage == CompanyStage.DEVELOPER:
        iv.primary_method = "EV/EBITDA Peer Comps"
        iv.secondary_method = "DCF with explicit unit-expansion phase"
    elif stage == CompanyStage.EXPLORER:
        iv.primary_method = "EV/Revenue with forward margin ramp"
        iv.secondary_method = "P/S vs Peer"
    elif stage == CompanyStage.ROYALTY:
        iv.primary_method = "DCF (royalty stream)"
        iv.secondary_method = "EV/EBITDA (franchise premium)"
    else:
        iv.primary_method = "Cash Backing + Peer P/S"
        iv.secondary_method = "Tangible Book Value"

    if not statements:
        return iv
    latest = statements[0]

    if stage in (CompanyStage.PRODUCER, CompanyStage.ROYALTY):
        if latest.free_cash_flow and latest.free_cash_flow > 0 and shares and shares > 0:
            fcf = latest.free_cash_flow
            growth_rate = min(growth.revenue_cagr_3y or 0.05, 0.20)
            growth_rate = max(growth_rate, 0.0)
            dr = discount_rate
            if tier == CompanyTier.SMALL:
                dr = 0.12
            elif tier in (CompanyTier.MICRO, CompanyTier.NANO):
                dr = 0.15
            if dr > terminal_growth:
                total_pv = 0.0
                projected_fcf = fcf
                for year in range(1, 11):
                    yr_growth = growth_rate - (growth_rate - terminal_growth) * (year / 10)
                    projected_fcf *= (1 + yr_growth)
                    total_pv += projected_fcf / ((1 + dr) ** year)
                terminal_fcf = projected_fcf * (1 + terminal_growth)
                terminal_value = terminal_fcf / (dr - terminal_growth)
                pv_terminal = terminal_value / ((1 + dr) ** 10)
                dcf = (total_pv + pv_terminal) / shares
                if not math.isnan(dcf) and not math.isinf(dcf) and dcf > 0:
                    iv.dcf_value = round(dcf, 2)

    eps = latest.eps or (latest.net_income / shares if latest.net_income and shares else None)
    bvps = latest.book_value_per_share or info.get("bookValue")
    if eps and eps > 0 and bvps and bvps > 0:
        iv.graham_number = round(math.sqrt(22.5 * eps * bvps), 2)

    if eps and eps > 0 and growth.earnings_cagr_3y and growth.earnings_cagr_3y > 0:
        eg = min(growth.earnings_cagr_3y * 100, 100)
        if eg > 0:
            result = eps * eg
            if not math.isnan(result) and not math.isinf(result):
                iv.lynch_fair_value = round(result, 2)

    if solvency.ncav_per_share is not None:
        iv.ncav_value = round(solvency.ncav_per_share, 4)

    if latest.total_equity and shares and shares > 0:
        iv.asset_based_value = round(latest.total_equity / shares, 4)

    if iv.current_price and iv.current_price > 0:
        if iv.dcf_value:
            iv.margin_of_safety_dcf = round((iv.dcf_value - iv.current_price) / iv.dcf_value, 4)
        if iv.graham_number:
            iv.margin_of_safety_graham = round((iv.graham_number - iv.current_price) / iv.graham_number, 4)
        if iv.ncav_value and iv.ncav_value > 0:
            iv.margin_of_safety_ncav = round((iv.ncav_value - iv.current_price) / iv.ncav_value, 4)
        if iv.asset_based_value and iv.asset_based_value > 0:
            iv.margin_of_safety_asset = round((iv.asset_based_value - iv.current_price) / iv.asset_based_value, 4)
        if iv.nav_per_share and iv.nav_per_share > 0:
            iv.margin_of_safety_nav = round((iv.nav_per_share - iv.current_price) / iv.nav_per_share, 4)

    return iv


def calc_market_intelligence(
    info: dict, ticker_obj, solvency: SolvencyMetrics,
    share_structure: ShareStructure, growth: GrowthMetrics,
    tier: CompanyTier, stage: CompanyStage,
) -> MarketIntelligence:
    """Aggregate market sentiment, insider activity, technicals, and risk warnings."""
    mi = MarketIntelligence()
    price = info.get("currentPrice") or info.get("regularMarketPrice")
    shares_outstanding = info.get("sharesOutstanding")
    mi.price_current = price

    # ── 1. Insider transactions ──────────────────────────────────────
    try:
        insider_df = ticker_obj.insider_transactions
        if insider_df is not None and not insider_df.empty:
            top_rows = insider_df.head(10)
            for _, row in top_rows.iterrows():
                txn = InsiderTransaction(
                    insider=str(row.get("Insider", row.get("insider", ""))),
                    position=str(row.get("Position", row.get("position", ""))),
                    transaction_type=str(row.get("Transaction", row.get("transaction", ""))),
                    shares=row.get("Shares", row.get("shares")),
                    value=row.get("Value", row.get("value")),
                    date=str(row.get("Start Date", row.get("startDate", row.get("date", "")))),
                )
                mi.insider_transactions.append(txn)

            # Net shares in last 3 months
            cutoff = datetime.now() - timedelta(days=90)
            net_shares = 0.0
            buy_count = 0
            sell_count = 0
            for _, row in insider_df.iterrows():
                date_val = row.get("Start Date", row.get("startDate", row.get("date")))
                try:
                    if hasattr(date_val, "to_pydatetime"):
                        txn_date = date_val.to_pydatetime()
                    elif isinstance(date_val, str) and date_val:
                        txn_date = datetime.strptime(date_val[:10], "%Y-%m-%d")
                    else:
                        continue
                    if txn_date.tzinfo is not None:
                        txn_date = txn_date.replace(tzinfo=None)
                    if txn_date < cutoff:
                        continue
                except (ValueError, TypeError):
                    continue

                txn_type = str(row.get("Transaction", row.get("transaction", ""))).lower()
                shares_val = row.get("Shares", row.get("shares", 0)) or 0

                if any(kw in txn_type for kw in ("acquisition", "exercise", "purchase", "buy")):
                    net_shares += abs(shares_val)
                    buy_count += 1
                elif any(kw in txn_type for kw in ("disposition", "sale", "sell")):
                    net_shares -= abs(shares_val)
                    sell_count += 1

            mi.net_insider_shares_3m = net_shares

            if net_shares > 0 and buy_count > 3:
                mi.insider_buy_signal = "Strong insider buying"
            elif net_shares < 0:
                mi.insider_buy_signal = "Insider selling"
            else:
                mi.insider_buy_signal = "Mixed/Neutral"
    except Exception:
        mi.insider_buy_signal = "Data unavailable"

    # ── 2. Institutional holders ─────────────────────────────────────
    try:
        inst_df = ticker_obj.institutional_holders
        if inst_df is not None and not inst_df.empty:
            holder_col = "Holder" if "Holder" in inst_df.columns else (
                "holder" if "holder" in inst_df.columns else None
            )
            if holder_col:
                mi.top_holders = inst_df[holder_col].head(5).tolist()
    except Exception:
        pass
    mi.institutions_count = info.get("institutionsCount")
    mi.institutions_pct = share_structure.institutional_ownership_pct if share_structure else None

    # ── 3. Analyst consensus ─────────────────────────────────────────
    mi.target_high = info.get("targetHighPrice")
    mi.target_low = info.get("targetLowPrice")
    mi.target_mean = info.get("targetMeanPrice")
    mi.recommendation = info.get("recommendationKey")
    mi.analyst_count = info.get("numberOfAnalystOpinions")

    if mi.target_mean and price and price > 0:
        mi.target_upside_pct = (mi.target_mean - price) / price

    # ── 4. Short interest ────────────────────────────────────────────
    mi.shares_short = info.get("sharesShort")
    short_pct_raw = info.get("shortPercentOfFloat")
    if short_pct_raw is not None:
        mi.short_pct_of_float = short_pct_raw * 100
    mi.short_ratio_days = info.get("shortRatio")

    short_pct = mi.short_pct_of_float or 0
    short_ratio = mi.short_ratio_days or 0
    if short_pct > 15 and short_ratio > 5:
        mi.short_squeeze_risk = "High squeeze potential"
    elif short_pct > 8:
        mi.short_squeeze_risk = "Elevated short interest"
    else:
        mi.short_squeeze_risk = "Normal"

    # ── 5. Price technicals ──────────────────────────────────────────
    mi.price_52w_high = info.get("fiftyTwoWeekHigh")
    mi.price_52w_low = info.get("fiftyTwoWeekLow")
    mi.sma_50 = info.get("fiftyDayAverage")
    mi.sma_200 = info.get("twoHundredDayAverage")
    mi.beta = info.get("beta")
    mi.avg_volume = info.get("averageVolume")
    mi.volume_10d_avg = info.get("averageDailyVolume10Day")

    if price and mi.price_52w_high and mi.price_52w_high > 0:
        mi.pct_from_52w_high = (price - mi.price_52w_high) / mi.price_52w_high
    if price and mi.price_52w_low and mi.price_52w_low > 0:
        mi.pct_from_52w_low = (price - mi.price_52w_low) / mi.price_52w_low
    if price and mi.price_52w_high and mi.price_52w_low is not None:
        range_span = mi.price_52w_high - mi.price_52w_low
        if range_span > 0:
            mi.price_52w_range_position = (price - mi.price_52w_low) / range_span

    if price and mi.sma_50:
        mi.above_sma_50 = price > mi.sma_50
    if price and mi.sma_200:
        mi.above_sma_200 = price > mi.sma_200
    if mi.sma_50 and mi.sma_200:
        mi.golden_cross = mi.sma_50 > mi.sma_200

    if mi.volume_10d_avg and mi.avg_volume and mi.avg_volume > 0:
        vol_ratio = mi.volume_10d_avg / mi.avg_volume
        if vol_ratio > 1.25:
            mi.volume_trend = "Increasing"
        elif vol_ratio < 0.75:
            mi.volume_trend = "Decreasing"
        else:
            mi.volume_trend = "Stable"

    # --- Consumer discretionary macro & sector context ---
    # For consumer operators the "commodity" slot is used for a consumer-demand
    # proxy (the broad consumer-discretionary sector ETF) rather than a physical
    # commodity. We also fetch a sub-segment peer ETF so investors can compare
    # relative performance.
    _CONSUMER_PROXIES = {
        Segment.APPAREL:           [("XRT", "SPDR S&P Retail"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.SPECIALTY_RETAIL:  [("XRT", "SPDR S&P Retail"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.HOME_IMPROVEMENT:  [("XHB", "SPDR S&P Homebuilders"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.RESTAURANTS:       [("EATZ", "AdvisorShares Restaurant"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.AUTOMOTIVE:        [("CARZ", "First Trust S-Network Future Vehicles & Tech"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.LODGING_TRAVEL:    [("AWAY", "ETFMG Travel Tech"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.LEISURE:           [("PEJ", "Invesco Dynamic Leisure & Entertainment"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.ECOMMERCE:         [("ONLN", "ProShares Online Retail"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.LUXURY:            [("GLUX.PA", "Amundi S&P Global Luxury"), ("XLY", "Consumer Discretionary Select Sector SPDR")],
        Segment.HOMEBUILDING:      [("XHB", "SPDR S&P Homebuilders"), ("ITB", "iShares U.S. Home Construction")],
        Segment.OTHER:             [("XLY", "Consumer Discretionary Select Sector SPDR"), ("VCR", "Vanguard Consumer Discretionary")],
    }

    # Detect sub-segment from the business description / industry
    company_segment = Segment.OTHER
    try:
        from lynx_discretionary.models import classify_segment
        desc = info.get("longBusinessSummary", "")
        industry = info.get("industry", "")
        company_segment = classify_segment(desc, industry)
    except Exception:
        pass

    # Fetch a broad consumer-demand proxy (Consumer Discretionary sector ETF)
    # stored in the legacy "commodity" slot for template parity across agents.
    try:
        demand_proxy = yf.Ticker("XLY")
        pi = demand_proxy.info or {}
        mi.commodity_name = "Consumer Discretionary (XLY)"
        mi.commodity_price = pi.get("regularMarketPrice") or pi.get("previousClose")
        mi.commodity_52w_high = pi.get("fiftyTwoWeekHigh")
        mi.commodity_52w_low = pi.get("fiftyTwoWeekLow")
        if mi.commodity_price and mi.commodity_52w_high and mi.commodity_52w_low:
            rng = mi.commodity_52w_high - mi.commodity_52w_low
            if rng > 0:
                mi.commodity_52w_position = (mi.commodity_price - mi.commodity_52w_low) / rng
    except Exception:
        pass

    _SECTOR_ETFS = _CONSUMER_PROXIES

    # Fetch sector ETF performance
    try:
        etf_list = _SECTOR_ETFS.get(company_segment, _SECTOR_ETFS[Segment.OTHER])
        if len(etf_list) >= 1:
            etf_ticker, etf_name = etf_list[0]
            et = yf.Ticker(etf_ticker)
            ei = et.info or {}
            mi.sector_etf_name = etf_name
            mi.sector_etf_ticker = etf_ticker
            mi.sector_etf_price = ei.get("regularMarketPrice") or ei.get("previousClose")
            try:
                hist = et.history(period="3mo")
                if hist is not None and len(hist) > 1:
                    mi.sector_etf_3m_perf = (hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1)
            except Exception:
                pass
        if len(etf_list) >= 2:
            etf_ticker2, etf_name2 = etf_list[1]
            et2 = yf.Ticker(etf_ticker2)
            ei2 = et2.info or {}
            mi.peer_etf_name = etf_name2
            mi.peer_etf_ticker = etf_ticker2
            mi.peer_etf_price = ei2.get("regularMarketPrice") or ei2.get("previousClose")
            try:
                hist2 = et2.history(period="3mo")
                if hist2 is not None and len(hist2) > 1:
                    mi.peer_etf_3m_perf = (hist2["Close"].iloc[-1] / hist2["Close"].iloc[0] - 1)
            except Exception:
                pass
    except Exception:
        pass

    # ── 6. Projected dilution (early-stage / emerging operators) ─────
    pre_profit_stages = (CompanyStage.GRASSROOTS, CompanyStage.EXPLORER)
    if stage in pre_profit_stages:
        runway = solvency.cash_runway_years if solvency else None
        burn = solvency.cash_burn_rate if solvency else None
        if runway is not None and runway < 3 and burn is not None and burn < 0:
            if price and price > 0 and shares_outstanding and shares_outstanding > 0:
                new_shares = abs(burn) * 2 / price
                mi.projected_dilution_annual_pct = new_shares / shares_outstanding
                mi.projected_shares_in_2y = shares_outstanding + new_shares

        if runway is not None:
            if runway < 1:
                mi.financing_warning = (
                    "Critical: cash runway under 1 year. "
                    "Imminent dilutive financing expected."
                )
            elif runway < 1.5:
                mi.financing_warning = (
                    "Warning: cash runway under 18 months. "
                    "Dilutive financing likely within next year."
                )
            elif runway < 3:
                mi.financing_warning = (
                    "Note: cash runway under 3 years. "
                    "Future financing probable; monitor cash position."
                )

    # ── 7. Risk warnings ────────────────────────────────────────────
    warnings: list[str] = []

    if mi.beta and mi.beta > 2.0:
        warnings.append(
            f"High volatility (beta {mi.beta:.1f}) "
            "— price swings of 2-3x market moves"
        )

    if short_pct > 10:
        warnings.append(
            f"Elevated short interest ({short_pct:.1f}%) "
            "— negative sentiment or squeeze setup"
        )

    if not mi.analyst_count or mi.analyst_count == 0:
        warnings.append("No analyst coverage — higher information asymmetry")

    if mi.pct_from_52w_low is not None and mi.pct_from_52w_low < 0.20:
        warnings.append(
            "Trading near 52-week low — potential capitulation or value"
        )

    if mi.insider_buy_signal == "Insider selling":
        warnings.append("Recent insider selling detected")

    if solvency and solvency.cash_runway_years is not None and solvency.cash_runway_years < 1.5:
        warnings.append("Cash runway under 18 months — dilutive financing likely")

    if share_structure and share_structure.fully_diluted_shares:
        if share_structure.fully_diluted_shares > 500_000_000:
            warnings.append("Bloated share structure limits per-share upside")

    if stage in pre_profit_stages and solvency and solvency.total_debt and solvency.total_debt > 0:
        warnings.append("Debt in pre-profit company — unusual for emerging consumer operators")

    mi.risk_warnings = warnings

    # ── 8. Consumer-discretionary disclaimers ────────────────────────
    disclaimers: list[str] = [
        "Consumer discretionary spending is cyclical. Current margins may compress during recessions.",
        "Same-store sales are lagging indicators — monitor unit growth and channel mix.",
        "Fashion cycles and consumer preferences shift rapidly; trend exposure can reverse.",
    ]
    if stage in (CompanyStage.GRASSROOTS, CompanyStage.EXPLORER):
        disclaimers.append(
            "This company is early-stage. Brand durability is unproven and many emerging "
            "concepts fail before reaching scale."
        )
    if stage == CompanyStage.DEVELOPER:
        disclaimers.append(
            "Rapid unit expansion often stretches unit economics. Watch new-store "
            "productivity and pre-opening expense trends."
        )
    if stage == CompanyStage.ROYALTY:
        disclaimers.append(
            "Franchise models depend on franchisee health; system-wide same-store sales "
            "matter more than corporate-owned performance."
        )
    disclaimers.extend([
        "Past performance and insider activity do not guarantee future results.",
        "This analysis is for informational purposes only and does not constitute investment advice.",
    ])
    mi.disclaimers = disclaimers

    return mi


def _calc_roic_history(statements: list[FinancialStatement]) -> list[Optional[float]]:
    vals = []
    for s in statements:
        if s.operating_income is not None and s.total_assets and s.total_cash is not None:
            nopat = s.operating_income * 0.75
            ic = s.total_assets - (s.total_cash or 0)
            if ic > 0:
                vals.append(nopat / ic)
    return vals


def _calc_margin_history(statements: list[FinancialStatement]) -> list[Optional[float]]:
    margins = []
    for s in statements:
        if s.gross_profit and s.revenue and s.revenue > 0:
            margins.append(s.gross_profit / s.revenue)
    return margins


def _cagr(start: Optional[float], end: Optional[float], years: int) -> Optional[float]:
    if not start or not end or start <= 0 or end <= 0 or years <= 0:
        return None
    try:
        result = (end / start) ** (1 / years) - 1
        if math.isnan(result) or math.isinf(result):
            return None
        return result
    except (ValueError, OverflowError, ZeroDivisionError):
        return None
