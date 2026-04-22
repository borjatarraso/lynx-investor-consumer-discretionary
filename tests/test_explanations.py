"""Unit tests for metric explanations."""

import pytest
from lynx_discretionary.metrics.explanations import (
    get_explanation, list_metrics, get_section_explanation,
    get_conclusion_explanation, SECTION_EXPLANATIONS, CONCLUSION_METHODOLOGY,
)


class TestGetExplanation:
    def test_known_metric(self):
        e = get_explanation("cash_to_market_cap")
        assert e is not None
        assert e.full_name == "Cash-to-Market-Cap Ratio"
        assert e.category == "valuation"

    def test_unknown_metric(self):
        assert get_explanation("nonexistent") is None

    def test_all_metrics_have_required_fields(self):
        for m in list_metrics():
            assert m.key != ""
            assert m.full_name != ""
            assert m.description != ""
            assert m.formula != ""
            assert m.category != ""

    def test_consumer_specific_metrics_exist(self):
        keys = [m.key for m in list_metrics()]
        assert "gross_margin" in keys
        assert "quality_score" in keys
        assert "shares_growth_yoy" in keys
        assert "lease_adjusted_debt_ratio" in keys
        assert "inventory_turnover" in keys
        assert "brand_strength" in keys
        assert "cyclical_sensitivity" in keys

    def test_list_by_category(self):
        valuation = list_metrics("valuation")
        assert len(valuation) > 0
        assert all(m.category == "valuation" for m in valuation)


class TestSectionExplanations:
    def test_all_sections_have_title(self):
        for key, sec in SECTION_EXPLANATIONS.items():
            assert "title" in sec
            assert "description" in sec

    def test_business_quality_section_exists(self):
        sec = get_section_explanation("business_quality")
        assert sec is not None
        assert "Business Quality" in sec["title"] or "business quality" in sec["title"].lower()

    def test_share_structure_section_exists(self):
        sec = get_section_explanation("share_structure")
        assert sec is not None

    def test_unknown_section(self):
        assert get_section_explanation("nonexistent") is None


class TestConclusionMethodology:
    def test_overall_exists(self):
        ce = get_conclusion_explanation("overall")
        assert ce is not None
        assert "business quality" in ce["description"].lower()

    def test_unknown_category(self):
        assert get_conclusion_explanation("nonexistent") is None
