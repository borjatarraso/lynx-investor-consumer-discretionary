"""Unit tests for data models and classification functions."""

import pytest
from lynx_discretionary.models import (
    CompanyProfile, CompanyStage, CompanyTier, Segment,
    JurisdictionTier, Relevance, AnalysisReport,
    ValuationMetrics, SolvencyMetrics, GrowthMetrics,
    BusinessQualityIndicators, ShareStructure, MarketIntelligence,
    FinancialStatement, AnalysisConclusion,
    classify_tier, classify_stage, classify_segment, classify_jurisdiction,
)


class TestClassifyTier:
    def test_mega_cap(self):
        assert classify_tier(300_000_000_000) == CompanyTier.MEGA

    def test_large_cap(self):
        assert classify_tier(50_000_000_000) == CompanyTier.LARGE

    def test_mid_cap(self):
        assert classify_tier(5_000_000_000) == CompanyTier.MID

    def test_small_cap(self):
        assert classify_tier(1_000_000_000) == CompanyTier.SMALL

    def test_micro_cap(self):
        assert classify_tier(100_000_000) == CompanyTier.MICRO

    def test_nano_cap(self):
        assert classify_tier(10_000_000) == CompanyTier.NANO

    def test_none_returns_nano(self):
        assert classify_tier(None) == CompanyTier.NANO

    def test_zero_returns_nano(self):
        assert classify_tier(0) == CompanyTier.NANO

    def test_negative_returns_nano(self):
        assert classify_tier(-100) == CompanyTier.NANO


class TestClassifyStage:
    def test_producer_large_operator(self):
        # >$5B revenue + comparable store sales → PRODUCER
        assert classify_stage(
            "global retailer with comparable store sales",
            25_000_000_000,
            {"operatingMargins": 0.12},
        ) == CompanyStage.PRODUCER

    def test_producer_without_margin_data(self):
        # Just >$5B revenue falls to PRODUCER even without keyword
        assert classify_stage(
            "global retailer",
            15_000_000_000,
            {},
        ) == CompanyStage.PRODUCER

    def test_developer_scaling(self):
        # $500M–$5B revenue range with expansion language → DEVELOPER
        assert classify_stage(
            "expanding retail concept rolling out new stores internationally",
            1_500_000_000,
            {"operatingMargins": 0.06},
        ) == CompanyStage.DEVELOPER

    def test_explorer_emerging(self):
        # $20M–$500M revenue → EXPLORER (emerging brand)
        assert classify_stage(
            "emerging direct-to-consumer brand",
            80_000_000,
            {"operatingMargins": -0.02},
        ) == CompanyStage.EXPLORER

    def test_grassroots_early_stage(self):
        # Pre-revenue / heavy losses → GRASSROOTS
        assert classify_stage(
            "early stage startup",
            500_000,
            {"profitMargins": -0.50},
        ) == CompanyStage.GRASSROOTS

    def test_royalty(self):
        # Franchise / asset-light language dominates regardless of revenue
        assert classify_stage(
            "global restaurant franchisor with franchise system",
            8_000_000_000,
            {"operatingMargins": 0.30},
        ) == CompanyStage.ROYALTY

    def test_none_description_default(self):
        # No description and no revenue falls through to EXPLORER default
        assert classify_stage(None, None) == CompanyStage.EXPLORER

    def test_empty_description(self):
        assert classify_stage("", 0, {}) == CompanyStage.EXPLORER


class TestClassifySegment:
    def test_apparel(self):
        assert classify_segment(
            "premium athletic apparel and footwear brand",
            "Apparel Manufacturing",
        ) == Segment.APPAREL

    def test_restaurants(self):
        assert classify_segment(
            "quick-service restaurant chain",
            "Restaurants",
        ) == Segment.RESTAURANTS

    def test_home_improvement(self):
        assert classify_segment(
            "home improvement retailer with do-it-yourself products",
            "Home Improvement Retail",
        ) == Segment.HOME_IMPROVEMENT

    def test_automotive(self):
        assert classify_segment(
            "electric vehicle manufacturer producing passenger cars",
            "Auto Manufacturers",
        ) == Segment.AUTOMOTIVE

    def test_lodging_travel(self):
        assert classify_segment(
            "international hotel and resort franchise",
            "Lodging",
        ) == Segment.LODGING_TRAVEL

    def test_ecommerce(self):
        assert classify_segment(
            "online retailer operating a digital marketplace",
            "Internet Retail",
        ) == Segment.ECOMMERCE

    def test_luxury(self):
        assert classify_segment(
            "premium lifestyle luxury brand",
            "Luxury Goods",
        ) == Segment.LUXURY

    def test_homebuilding(self):
        assert classify_segment(
            "residential construction homebuilder",
            "Residential Construction",
        ) == Segment.HOMEBUILDING

    def test_specialty_retail(self):
        assert classify_segment(
            "off-price discount retailer operating a big-box format",
            "Specialty Retail",
        ) == Segment.SPECIALTY_RETAIL

    def test_other_when_no_match(self):
        assert classify_segment("generic company", None) == Segment.OTHER

    def test_none_inputs(self):
        assert classify_segment(None, None) == Segment.OTHER


class TestClassifyJurisdiction:
    def test_us_tier1(self):
        assert classify_jurisdiction("United States") == JurisdictionTier.TIER_1

    def test_uk_tier1(self):
        assert classify_jurisdiction("United Kingdom") == JurisdictionTier.TIER_1

    def test_australia_tier1(self):
        assert classify_jurisdiction("Australia") == JurisdictionTier.TIER_1

    def test_japan_tier1(self):
        assert classify_jurisdiction("Japan") == JurisdictionTier.TIER_1

    def test_mexico_tier2(self):
        assert classify_jurisdiction("Mexico") == JurisdictionTier.TIER_2

    def test_south_korea_tier2(self):
        assert classify_jurisdiction("South Korea") == JurisdictionTier.TIER_2

    def test_unknown_tier3(self):
        assert classify_jurisdiction("SomeCountry") == JurisdictionTier.TIER_3

    def test_none_unknown(self):
        assert classify_jurisdiction(None) == JurisdictionTier.UNKNOWN


class TestDataModels:
    def test_analysis_report_defaults(self):
        r = AnalysisReport(profile=CompanyProfile(ticker="TEST", name="Test"))
        assert r.valuation is None
        assert r.market_intelligence is None
        assert r.financials == []
        assert r.fetched_at != ""

    def test_company_profile_defaults(self):
        p = CompanyProfile(ticker="X", name="X Corp")
        assert p.tier == CompanyTier.NANO
        assert p.stage == CompanyStage.GRASSROOTS
        assert p.primary_segment == Segment.OTHER
        assert p.jurisdiction_tier == JurisdictionTier.UNKNOWN

    def test_solvency_metrics_defaults(self):
        s = SolvencyMetrics()
        assert s.cash_runway_years is None
        assert s.burn_as_pct_of_market_cap is None
        assert s.lease_adjusted_debt_ratio is None

    def test_market_intelligence_defaults(self):
        mi = MarketIntelligence()
        assert mi.insider_transactions == []
        assert mi.risk_warnings == []
        assert mi.disclaimers == []

    def test_business_quality_defaults(self):
        bq = BusinessQualityIndicators()
        assert bq.quality_score is None
        assert bq.brand_strength is None
        assert bq.cyclical_sensitivity is None
