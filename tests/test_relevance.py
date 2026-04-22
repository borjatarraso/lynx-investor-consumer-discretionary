"""Unit tests for the relevance system."""

import pytest
from lynx_discretionary.models import CompanyStage, CompanyTier, Relevance
from lynx_discretionary.metrics.relevance import get_relevance


class TestStageOverrides:
    """Stage overrides take precedence over tier-based lookups."""

    def test_explorer_pe_irrelevant(self):
        assert get_relevance("pe_trailing", CompanyTier.MEGA, "valuation", CompanyStage.EXPLORER) == Relevance.IRRELEVANT

    def test_explorer_cash_runway_critical(self):
        assert get_relevance("cash_runway_years", CompanyTier.MICRO, "solvency", CompanyStage.EXPLORER) == Relevance.CRITICAL

    def test_grassroots_cash_to_mcap_critical(self):
        assert get_relevance("cash_to_market_cap", CompanyTier.NANO, "valuation", CompanyStage.GRASSROOTS) == Relevance.CRITICAL

    def test_producer_ev_ebitda_critical(self):
        assert get_relevance("ev_ebitda", CompanyTier.MID, "valuation", CompanyStage.PRODUCER) == Relevance.CRITICAL

    def test_producer_cash_burn_contextual(self):
        assert get_relevance("cash_burn_rate", CompanyTier.MID, "solvency", CompanyStage.PRODUCER) == Relevance.CONTEXTUAL

    def test_explorer_gross_margin_critical(self):
        # For consumer operators gross margin stays meaningful at every stage
        assert get_relevance(
            "gross_margin", CompanyTier.MICRO, "profitability", CompanyStage.EXPLORER
        ) == Relevance.CRITICAL

    def test_grassroots_profitability_muted(self):
        # Pre-profit stage still surfaces ROE as contextual, not critical
        for key in ["roe", "roa", "roic"]:
            rel = get_relevance(key, CompanyTier.MICRO, "profitability", CompanyStage.GRASSROOTS)
            assert rel in (Relevance.IRRELEVANT, Relevance.CONTEXTUAL, Relevance.RELEVANT)

    def test_producer_profitability_relevant(self):
        assert get_relevance(
            "roic", CompanyTier.MID, "profitability", CompanyStage.PRODUCER
        ) == Relevance.CRITICAL

    def test_dilution_critical_for_emerging_operators(self):
        for stage in [CompanyStage.GRASSROOTS, CompanyStage.EXPLORER]:
            assert get_relevance(
                "shares_growth_yoy", CompanyTier.MICRO, "growth", stage
            ) == Relevance.CRITICAL

    def test_lease_adjusted_leverage_critical_for_mature(self):
        assert get_relevance(
            "lease_adjusted_debt_ratio", CompanyTier.MID, "solvency", CompanyStage.PRODUCER
        ) == Relevance.CRITICAL

    def test_debt_to_ebitda_critical_for_mature(self):
        assert get_relevance(
            "debt_to_ebitda", CompanyTier.LARGE, "solvency", CompanyStage.PRODUCER
        ) == Relevance.CRITICAL

    def test_insider_ownership_critical_for_juniors(self):
        assert get_relevance("insider_ownership_pct", CompanyTier.MICRO, "share_structure", CompanyStage.EXPLORER) == Relevance.CRITICAL

    def test_royalty_fcf_critical(self):
        assert get_relevance("fcf_margin", CompanyTier.SMALL, "profitability", CompanyStage.ROYALTY) == Relevance.CRITICAL


class TestTierFallback:
    """When no stage override exists, tier-based lookup is used."""

    def test_unknown_metric_defaults_relevant(self):
        assert get_relevance("some_unknown_metric", CompanyTier.MID, "valuation", CompanyStage.PRODUCER) == Relevance.RELEVANT

    def test_pb_ratio_critical_for_small(self):
        # Stage override for PRODUCER pb_ratio = IMPORTANT
        assert get_relevance("pb_ratio", CompanyTier.SMALL, "valuation", CompanyStage.PRODUCER) in [Relevance.CRITICAL, Relevance.IMPORTANT, Relevance.RELEVANT]
