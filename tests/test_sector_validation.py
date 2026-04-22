"""Tests for the consumer-discretionary sector validation gate."""

import pytest
from lynx_discretionary.core.analyzer import _validate_sector, SectorMismatchError
from lynx_discretionary.models import CompanyProfile


class TestSectorValidation:
    """Sector validation blocks non-consumer-discretionary companies."""

    def _profile(self, ticker="T", sector=None, industry=None, desc=None):
        return CompanyProfile(
            ticker=ticker, name=f"{ticker} Corp",
            sector=sector, industry=industry, description=desc,
        )

    # --- Should ALLOW ---
    def test_consumer_cyclical_sector(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Apparel Manufacturing"))

    def test_consumer_discretionary_sector(self):
        _validate_sector(self._profile(sector="Consumer Discretionary", industry="Specialty Retail"))

    def test_apparel_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Apparel Manufacturing"))

    def test_specialty_retail_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Specialty Retail"))

    def test_home_improvement_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Home Improvement Retail"))

    def test_restaurant_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Restaurants"))

    def test_auto_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Auto Manufacturers"))

    def test_lodging_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Lodging"))

    def test_internet_retail_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Internet Retail"))

    def test_luxury_goods_industry(self):
        _validate_sector(self._profile(sector="Consumer Cyclical", industry="Luxury Goods"))

    def test_same_store_sales_in_description(self):
        _validate_sector(self._profile(
            sector="Other", industry="Other",
            desc="Operator reporting same-store sales comp growth"))

    def test_franchise_in_description(self):
        _validate_sector(self._profile(
            sector="Other", industry="Other",
            desc="Global franchisor and franchisee network of restaurants"))

    def test_direct_to_consumer_in_description(self):
        _validate_sector(self._profile(
            sector="Other", industry="Other",
            desc="Direct-to-consumer apparel brand with retail stores"))

    # --- Should BLOCK ---
    def test_technology_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Technology", industry="Software"))

    def test_financial_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Financial Services", industry="Banks"))

    def test_healthcare_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Healthcare", industry="Drug Manufacturers"))

    def test_basic_materials_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Basic Materials", industry="Gold"))

    def test_energy_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Energy", industry="Oil & Gas E&P"))

    def test_real_estate_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Real Estate", industry="REIT"))

    def test_consumer_defensive_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Consumer Defensive", industry="Grocery Stores"))

    def test_all_none_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile())

    def test_empty_strings_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="", industry="", desc=""))

    def test_error_message_content(self):
        with pytest.raises(SectorMismatchError, match="outside the scope"):
            _validate_sector(self._profile(sector="Technology", industry="Software"))

    def test_error_suggests_another_agent(self):
        """Wrong-sector warning appends a 'use lynx-investor-*' line."""
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Healthcare", industry="Biotechnology"))
        message = str(exc.value)
        assert "Suggestion" in message
        assert "lynx-investor-healthcare" in message

    def test_error_never_suggests_self(self):
        """The suggestion never points back to this agent itself."""
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Energy", industry="Uranium"))
        message = str(exc.value)
        assert "use 'lynx-investor-consumer-discretionary'" not in message
