"""Consumer-discretionary-focused report synthesis engine."""

from __future__ import annotations

import math

from lynx_discretionary.models import AnalysisConclusion, AnalysisReport, CompanyStage, CompanyTier, JurisdictionTier


def _safe(val, default: float = 0.0) -> float:
    if val is None or isinstance(val, bool):
        return default
    try:
        f = float(val)
        return default if (math.isnan(f) or math.isinf(f)) else f
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Category weights per (stage, tier)
#
# Weights are (valuation, profitability, solvency, growth, business_quality).
# For consumer discretionary we generally weight profitability and business
# quality more heavily than for mining, because consumer companies are
# cash-generative and brand/unit-economics driven rather than cash-survival
# driven. For early-stage / emerging operators we still emphasize solvency
# and dilution.
# ---------------------------------------------------------------------------

_WEIGHTS = {
    # Mature operators — balanced, with emphasis on profitability and quality
    (CompanyStage.PRODUCER, CompanyTier.MEGA): (0.20, 0.25, 0.10, 0.20, 0.25),
    (CompanyStage.PRODUCER, CompanyTier.LARGE): (0.20, 0.25, 0.10, 0.20, 0.25),
    (CompanyStage.PRODUCER, CompanyTier.MID): (0.20, 0.25, 0.15, 0.15, 0.25),
    (CompanyStage.PRODUCER, CompanyTier.SMALL): (0.15, 0.20, 0.20, 0.20, 0.25),
    (CompanyStage.PRODUCER, CompanyTier.MICRO): (0.15, 0.15, 0.25, 0.20, 0.25),
    (CompanyStage.PRODUCER, CompanyTier.NANO): (0.10, 0.15, 0.30, 0.20, 0.25),
    # Scaling operators — growth weighted
    (CompanyStage.DEVELOPER, CompanyTier.LARGE): (0.15, 0.20, 0.15, 0.25, 0.25),
    (CompanyStage.DEVELOPER, CompanyTier.MID): (0.15, 0.20, 0.15, 0.25, 0.25),
    (CompanyStage.DEVELOPER, CompanyTier.SMALL): (0.10, 0.15, 0.25, 0.25, 0.25),
    (CompanyStage.DEVELOPER, CompanyTier.MICRO): (0.10, 0.10, 0.30, 0.25, 0.25),
    (CompanyStage.DEVELOPER, CompanyTier.NANO): (0.05, 0.10, 0.35, 0.25, 0.25),
    # Emerging brands — balance sheet and growth dominate
    (CompanyStage.EXPLORER, CompanyTier.SMALL): (0.10, 0.10, 0.30, 0.25, 0.25),
    (CompanyStage.EXPLORER, CompanyTier.MICRO): (0.10, 0.05, 0.35, 0.25, 0.25),
    (CompanyStage.EXPLORER, CompanyTier.NANO): (0.05, 0.05, 0.40, 0.25, 0.25),
    # Early stage / pre-profit — solvency dominates
    (CompanyStage.GRASSROOTS, CompanyTier.MICRO): (0.05, 0.05, 0.40, 0.20, 0.30),
    (CompanyStage.GRASSROOTS, CompanyTier.NANO): (0.05, 0.05, 0.45, 0.15, 0.30),
    # Franchise / asset-light — profitability and quality dominate
    (CompanyStage.ROYALTY, CompanyTier.SMALL): (0.20, 0.30, 0.10, 0.15, 0.25),
    (CompanyStage.ROYALTY, CompanyTier.MID): (0.20, 0.30, 0.10, 0.15, 0.25),
    (CompanyStage.ROYALTY, CompanyTier.LARGE): (0.20, 0.30, 0.10, 0.15, 0.25),
    (CompanyStage.ROYALTY, CompanyTier.MEGA): (0.20, 0.30, 0.10, 0.15, 0.25),
}
_DEFAULT_WEIGHTS = (0.15, 0.20, 0.20, 0.20, 0.25)


def generate_conclusion(report: AnalysisReport) -> AnalysisConclusion:
    c = AnalysisConclusion()
    tier, stage = report.profile.tier, report.profile.stage

    val_score = _score_valuation(report)
    prof_score = _score_profitability(report)
    solv_score = _score_solvency(report)
    grow_score = _score_growth(report)
    quality_score = _safe(report.business_quality.quality_score) if report.business_quality else 0

    c.category_scores = {"valuation": round(val_score, 1), "profitability": round(prof_score, 1),
                         "solvency": round(solv_score, 1), "growth": round(grow_score, 1),
                         "business_quality": round(quality_score, 1)}

    w = _WEIGHTS.get((stage, tier), _DEFAULT_WEIGHTS)
    c.overall_score = round(val_score * w[0] + prof_score * w[1] + solv_score * w[2] + grow_score * w[3] + quality_score * w[4], 1)
    c.verdict = _verdict(c.overall_score)
    c.category_summaries = _build_summaries(report)
    c.strengths = _find_strengths(report)
    c.risks = _find_risks(report)
    c.summary = _build_narrative(report, c)
    c.tier_note = _tier_note(tier)
    c.stage_note = _stage_note(stage)
    c.screening_checklist = _consumer_screening(report)
    return c


def _verdict(score: float) -> str:
    if score >= 75: return "Strong Buy"
    if score >= 60: return "Buy"
    if score >= 45: return "Hold"
    if score >= 30: return "Caution"
    return "Avoid"


def _score_valuation(r: AnalysisReport) -> float:
    v = r.valuation
    if v is None:
        return 50.0
    score = 50.0
    stage = r.profile.stage
    pe = _safe(v.pe_trailing, None)
    if pe is not None:
        if pe < 0:
            if stage not in (CompanyStage.GRASSROOTS, CompanyStage.EXPLORER):
                score -= 10
        elif pe < 12: score += 25
        elif pe < 18: score += 15
        elif pe < 25: score += 5
        elif pe < 35: score -= 5
        else: score -= 15
    pfcf = _safe(v.p_fcf, None)
    if pfcf is not None:
        if pfcf < 15: score += 15
        elif pfcf < 20: score += 8
        elif pfcf >= 40: score -= 10
    ev = _safe(v.ev_ebitda, None)
    if ev is not None:
        if ev < 8: score += 10
        elif ev < 12: score += 5
        elif ev >= 20: score -= 10
    pb = _safe(v.pb_ratio, None)
    if pb is not None and stage in (CompanyStage.GRASSROOTS, CompanyStage.EXPLORER):
        if pb < 1: score += 10
        elif pb < 2: score += 3
        elif pb >= 5: score -= 5
    ps = _safe(v.ps_ratio, None)
    if ps is not None:
        if ps < 1: score += 5
        elif ps >= 6: score -= 10
    return max(0, min(100, score))


def _score_profitability(r: AnalysisReport) -> float:
    if r.profile.stage == CompanyStage.GRASSROOTS:
        return 50.0
    p = r.profitability
    if p is None:
        return 50.0
    score = 50.0
    roic = _safe(p.roic, None)
    if roic is not None:
        if roic > 0.20: score += 20
        elif roic > 0.12: score += 10
        elif roic > 0.08: score += 5
        elif roic < 0: score -= 15
    roe = _safe(p.roe, None)
    if roe is not None:
        if roe > 0.25: score += 10
        elif roe > 0.15: score += 5
        elif roe < 0: score -= 10
    gm = _safe(p.gross_margin, None)
    if gm is not None:
        if gm > 0.50: score += 15
        elif gm > 0.35: score += 8
        elif gm > 0.20: score += 3
        elif gm < 0.10: score -= 10
    om = _safe(p.operating_margin, None)
    if om is not None:
        if om > 0.15: score += 10
        elif om > 0.08: score += 5
        elif om < 0: score -= 10
    fm = _safe(p.fcf_margin, None)
    if fm is not None:
        if fm > 0.10: score += 10
        elif fm > 0.05: score += 5
        elif fm < -0.05: score -= 10
    return max(0, min(100, score))


def _score_solvency(r: AnalysisReport) -> float:
    s = r.solvency
    if s is None:
        return 50.0
    score = 50.0
    stage = r.profile.stage
    de = _safe(s.debt_to_equity, None)
    if de is not None:
        if stage in (CompanyStage.GRASSROOTS, CompanyStage.EXPLORER):
            if de < 0.1: score += 10
            elif de > 1.0: score -= 20
        else:
            if de < 0.5: score += 10
            elif de < 1.5: score += 3
            elif de > 3: score -= 15
    de_ebitda = _safe(s.debt_to_ebitda, None)
    if de_ebitda is not None:
        if de_ebitda < 1.5: score += 10
        elif de_ebitda < 3: score += 5
        elif de_ebitda > 5: score -= 15
    cr = _safe(s.current_ratio, None)
    if cr is not None:
        if cr > 2: score += 8
        elif cr > 1.5: score += 4
        elif cr < 1: score -= 15
    ic = _safe(s.interest_coverage, None)
    if ic is not None:
        if ic > 10: score += 8
        elif ic > 4: score += 3
        elif ic < 2: score -= 15
    burn = _safe(s.cash_burn_rate, None)
    if burn is not None and burn < 0:
        runway = _safe(s.cash_runway_years, None)
        if runway is not None:
            if runway > 3: score += 5
            elif runway < 1: score -= 25
            elif runway < 1.5: score -= 15
            elif runway < 2: score -= 5
    return max(0, min(100, score))


def _score_growth(r: AnalysisReport) -> float:
    g = r.growth
    if g is None:
        return 50.0
    score = 50.0
    stage = r.profile.stage
    rg = _safe(g.revenue_growth_yoy, None)
    if rg is not None:
        if stage in (CompanyStage.DEVELOPER, CompanyStage.EXPLORER):
            if rg > 0.25: score += 20
            elif rg > 0.10: score += 10
            elif rg > 0.03: score += 3
            elif rg < -0.05: score -= 15
        else:
            if rg > 0.15: score += 15
            elif rg > 0.05: score += 5
            elif rg < -0.05: score -= 15
    rc = _safe(g.revenue_cagr_3y, None)
    if rc is not None:
        if rc > 0.15: score += 10
        elif rc > 0.05: score += 3
        elif rc < -0.03: score -= 8
    eg = _safe(g.earnings_growth_yoy, None)
    if eg is not None:
        if eg > 0.20: score += 10
        elif eg > 0.05: score += 3
        elif eg < -0.20: score -= 10
    dil = _safe(g.shares_growth_yoy, None)
    if dil is not None:
        if dil < -0.02: score += 5   # net buybacks
        elif dil < 0.02: score += 2
        elif dil > 0.10: score -= 15
        elif dil > 0.05: score -= 5
    return max(0, min(100, score))


def _consumer_screening(r: AnalysisReport) -> dict:
    """10-point consumer-discretionary screening checklist."""
    checks: dict[str, bool | None] = {}
    s, g, ss, p, v = r.solvency, r.growth, r.share_structure, r.profitability, r.valuation
    stage = r.profile.stage

    # 1. Positive operating margin (profitable core business)
    if stage == CompanyStage.GRASSROOTS:
        checks["positive_operating_margin"] = None
    else:
        om = _safe(p.operating_margin, None) if p else None
        checks["positive_operating_margin"] = om > 0 if om is not None else None

    # 2. Gross margin >= 30% (pricing power)
    gm = _safe(p.gross_margin, None) if p else None
    checks["gross_margin_30pct"] = gm >= 0.30 if gm is not None else None

    # 3. ROIC > 10% (capital efficiency)
    roic = _safe(p.roic, None) if p else None
    checks["roic_over_10pct"] = roic > 0.10 if roic is not None else None

    # 4. Debt/EBITDA < 3x (manageable leverage for cyclical sector)
    de = _safe(s.debt_to_ebitda, None) if s else None
    if de is not None:
        checks["reasonable_leverage"] = de < 3
    elif s and _safe(s.debt_to_equity, None) is not None:
        checks["reasonable_leverage"] = s.debt_to_equity < 1.5
    else:
        checks["reasonable_leverage"] = None

    # 5. Revenue growth > 3% (outpacing inflation)
    rg = _safe(g.revenue_growth_yoy, None) if g else None
    checks["revenue_growth_positive"] = rg > 0.03 if rg is not None else None

    # 6. Low dilution (<3%/yr)
    dil = _safe(g.shares_growth_yoy, None) if g else None
    checks["low_dilution"] = dil < 0.03 if dil is not None else None

    # 7. Insider ownership >= 5%
    insider = _safe(ss.insider_ownership_pct, None) if ss else None
    checks["insider_ownership"] = insider >= 0.05 if insider is not None else None

    # 8. Positive free cash flow margin
    fm = _safe(p.fcf_margin, None) if p else None
    checks["positive_fcf_margin"] = fm > 0 if fm is not None else None

    # 9. Reasonable P/E (<25) or low P/FCF (<25)
    pe = _safe(v.pe_trailing, None) if v else None
    pfcf = _safe(v.p_fcf, None) if v else None
    if pe is not None and pe > 0:
        checks["reasonable_valuation"] = pe < 25
    elif pfcf is not None and pfcf > 0:
        checks["reasonable_valuation"] = pfcf < 25
    else:
        checks["reasonable_valuation"] = None

    # 10. Developed-market exposure tier 1/2
    jt = r.profile.jurisdiction_tier
    checks["developed_market_exposure"] = (
        jt in (JurisdictionTier.TIER_1, JurisdictionTier.TIER_2)
        if jt != JurisdictionTier.UNKNOWN else None
    )

    return checks


def _build_summaries(r: AnalysisReport) -> dict[str, str]:
    summaries: dict[str, str] = {}
    stage = r.profile.stage
    pe = _safe(r.valuation.pe_trailing, None) if r.valuation else None
    pfcf = _safe(r.valuation.p_fcf, None) if r.valuation else None
    if pe is not None and pe > 0:
        summaries["valuation"] = f"P/E of {pe:.1f}" + (f" / P/FCF {pfcf:.1f}" if pfcf else "")
    elif pfcf is not None:
        summaries["valuation"] = f"P/FCF of {pfcf:.1f}"
    else:
        summaries["valuation"] = "Limited valuation data"
    if stage == CompanyStage.GRASSROOTS:
        summaries["profitability"] = "Pre-profit — not applicable"
    else:
        om = _safe(r.profitability.operating_margin, None) if r.profitability else None
        gm = _safe(r.profitability.gross_margin, None) if r.profitability else None
        if om is not None and gm is not None:
            summaries["profitability"] = f"GM {gm*100:.0f}% / OM {om*100:.0f}%"
        elif om is not None:
            summaries["profitability"] = f"OM {om*100:.0f}%"
        else:
            summaries["profitability"] = "Limited profitability data"
    if r.solvency:
        de_ebitda = _safe(r.solvency.debt_to_ebitda, None)
        runway = _safe(r.solvency.cash_runway_years, None)
        if de_ebitda is not None:
            summaries["solvency"] = f"Debt/EBITDA {de_ebitda:.1f}x"
        elif runway is not None:
            summaries["solvency"] = f"Cash runway: {runway:.1f} years"
        elif _safe(r.solvency.cash_burn_rate, None) is not None and r.solvency.cash_burn_rate >= 0:
            summaries["solvency"] = "Cash flow positive"
        else:
            summaries["solvency"] = "Limited solvency data"
    else:
        summaries["solvency"] = "Limited solvency data"
    rg = _safe(r.growth.revenue_growth_yoy, None) if r.growth else None
    summaries["growth"] = f"Revenue growth: {rg*100:.1f}% YoY" if rg is not None else "Limited growth data"
    summaries["business_quality"] = (r.business_quality.competitive_position or "N/A") if r.business_quality else "N/A"
    return summaries


def _find_strengths(r: AnalysisReport) -> list[str]:
    strengths: list[str] = []
    if r.profitability:
        gm = _safe(r.profitability.gross_margin, None)
        if gm and gm > 0.50:
            strengths.append(f"Strong gross margin ({gm*100:.0f}%)")
        roic = _safe(r.profitability.roic, None)
        if roic and roic > 0.15:
            strengths.append(f"High ROIC ({roic*100:.0f}%)")
        om = _safe(r.profitability.operating_margin, None)
        if om and om > 0.15:
            strengths.append(f"Strong operating margin ({om*100:.0f}%)")
        fm = _safe(r.profitability.fcf_margin, None)
        if fm and fm > 0.10:
            strengths.append(f"High FCF conversion ({fm*100:.0f}%)")
    if r.growth:
        rg = _safe(r.growth.revenue_growth_yoy, None)
        if rg and rg > 0.15:
            strengths.append(f"Strong revenue growth ({rg*100:.0f}% YoY)")
        dil = _safe(r.growth.shares_growth_yoy, None)
        if dil is not None and dil < -0.02:
            strengths.append("Net share buybacks")
    if r.solvency:
        de = _safe(r.solvency.debt_to_equity, None)
        if de is not None and de < 0.3:
            strengths.append("Conservative balance sheet")
    if r.share_structure:
        insider = _safe(r.share_structure.insider_ownership_pct, None)
        if insider and insider > 0.10:
            strengths.append(f"Meaningful insider ownership ({insider*100:.0f}%)")
    if r.profile.jurisdiction_tier == JurisdictionTier.TIER_1:
        strengths.append("Developed-market geographic exposure")
    return strengths[:6]


def _find_risks(r: AnalysisReport) -> list[str]:
    risks: list[str] = []
    if r.profitability:
        om = _safe(r.profitability.operating_margin, None)
        if om is not None and om < 0.03 and r.profile.stage != CompanyStage.GRASSROOTS:
            risks.append(f"Thin operating margin ({om*100:.1f}%)")
        fm = _safe(r.profitability.fcf_margin, None)
        if fm is not None and fm < 0:
            risks.append("Negative free cash flow margin")
    if r.solvency:
        de = _safe(r.solvency.debt_to_ebitda, None)
        if de is not None and de > 4:
            risks.append(f"High leverage (Debt/EBITDA {de:.1f}x)")
        runway = _safe(r.solvency.cash_runway_years, None)
        if runway is not None and runway < 1.5:
            risks.append(f"Limited cash runway ({runway:.1f} years)")
        ic = _safe(r.solvency.interest_coverage, None)
        if ic is not None and ic < 2:
            risks.append(f"Low interest coverage ({ic:.1f}x)")
    if r.growth:
        rg = _safe(r.growth.revenue_growth_yoy, None)
        if rg is not None and rg < -0.05:
            risks.append(f"Revenue declining ({rg*100:.1f}% YoY)")
        dil = _safe(r.growth.shares_growth_yoy, None)
        if dil is not None and dil > 0.08:
            risks.append(f"Heavy dilution ({dil*100:.1f}%/yr)")
    if r.profile.jurisdiction_tier == JurisdictionTier.TIER_3:
        risks.append("Tier 3 market exposure — high concentration risk")
    if r.profile.stage == CompanyStage.GRASSROOTS:
        risks.append("Early-stage / pre-profit — binary outcome risk")
    return risks[:6]


def _build_narrative(r: AnalysisReport, c: AnalysisConclusion) -> str:
    parts = [f"{r.profile.name} ({r.profile.tier.value}, {r.profile.stage.value}) scores {c.overall_score:.0f}/100 — '{c.verdict}'."]
    if c.strengths:
        parts.append(f"Strengths: {c.strengths[0].lower()}" + (f" and {c.strengths[1].lower()}" if len(c.strengths) > 1 else "") + ".")
    if c.risks:
        parts.append(f"Risks: {c.risks[0].lower()}" + (f" and {c.risks[1].lower()}" if len(c.risks) > 1 else "") + ".")
    return " ".join(parts)


def _tier_note(tier: CompanyTier) -> str:
    return {
        CompanyTier.MEGA: "Full traditional analysis. DCF and ROIC primary. Liquidity and coverage uniform.",
        CompanyTier.LARGE: "Full traditional analysis. All metrics reliable.",
        CompanyTier.MID: "Blended analysis. Growth and margin trajectory weighted heavily.",
        CompanyTier.SMALL: "Balance sheet and unit economics critical. Cyclical sensitivity matters.",
        CompanyTier.MICRO: "Survival and working-capital efficiency dominate. Limited analyst coverage.",
        CompanyTier.NANO: "Speculative. Asset-based valuation and cash position only. High risk.",
    }.get(tier, "")


def _stage_note(stage: CompanyStage) -> str:
    return {
        CompanyStage.PRODUCER: "Mature Operator: ROIC, operating margin, same-store sales, FCF conversion.",
        CompanyStage.DEVELOPER: "Scaling Operator: unit growth, new-store productivity, CAPEX intensity, margin trajectory.",
        CompanyStage.EXPLORER: "Emerging Brand: revenue growth, gross margin, dilution, cash runway.",
        CompanyStage.GRASSROOTS: "Early Stage: cash runway, burn rate, founder ownership. Binary outcome risk.",
        CompanyStage.ROYALTY: "Franchise / Asset-Light: royalty margins, system-wide sales, franchisee health, low capex.",
    }.get(stage, "")
