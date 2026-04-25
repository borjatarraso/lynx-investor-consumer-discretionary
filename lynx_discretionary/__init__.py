"""Lynx Consumer Discretionary — Fundamental analysis for consumer discretionary companies."""

from pathlib import Path

# Suite-level constants come from lynx-investor-core (shared across every agent).
from lynx_investor_core import (
    LICENSE_NAME,
    LICENSE_TEXT,
    LICENSE_URL,
    SUITE_LABEL,
    SUITE_NAME,
    SUITE_VERSION,
    __author__,
    __author_email__,
    __license__,
    __year__,
)
from lynx_investor_core import storage as _core_storage

# Initialize the shared storage layer with this agent's project root so
# data/ and data_test/ live beside *this* package.
_core_storage.set_base_dir(Path(__file__).resolve().parent.parent)

# ---------------------------------------------------------------------------
# Agent-specific identity
# ---------------------------------------------------------------------------

__version__ = "6.0.0"  # lynx-investor-consumer-discretionary version (independent of core)

APP_NAME = "Lynx Consumer Discretionary Analysis"
APP_SHORT_NAME = "Consumer Discretionary Analysis"
APP_TAGLINE = "Consumer Discretionary Fundamental Analysis"
APP_SCOPE = "consumer discretionary companies"
PROG_NAME = "lynx-discretionary"
PACKAGE_NAME = "lynx_discretionary"
USER_AGENT_PRODUCT = "LynxDiscretionary"
NEWS_SECTOR_KEYWORD = "consumer discretionary stock"

TICKER_SUGGESTIONS = (
    "  - For US mega-cap retailers, try: AMZN, HD, MCD, NKE, LOW, SBUX",
    "  - For specialty retail, try: TJX, ROST, ULTA, LULU, TGT",
    "  - For restaurants, try: CMG, DPZ, YUM, QSR",
    "  - For autos, try: TSLA, F, GM, STLA",
    "  - For lodging/travel, try: BKNG, MAR, HLT, ABNB",
    "  - You can also type the full company name: 'Home Depot'",
)

DESCRIPTION = (
    "Fundamental analysis specialized for consumer discretionary "
    "companies — apparel & footwear, specialty retail, home improvement, "
    "restaurants, automotive, lodging & leisure, and e-commerce. "
    "Evaluates operators across all maturity stages from emerging brands "
    "to mature franchises using consumer-specific metrics: same-store "
    "sales growth, gross margin, inventory turnover, cash conversion "
    "cycle, CAPEX intensity, ROIC, brand strength, and consumer "
    "cyclicality exposure.\n\n"
    "Part of the Lince Investor Suite."
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_logo_ascii() -> str:
    """Load the ASCII logo from img/logo_ascii.txt."""
    from lynx_investor_core.logo import load_logo_ascii
    return load_logo_ascii(Path(__file__).resolve().parent)


def get_about_text() -> dict:
    """Return structured about information (uniform across agents)."""
    from lynx_investor_core.about import AgentMeta, build_about
    meta = AgentMeta(
        app_name=APP_NAME,
        short_name=APP_SHORT_NAME,
        tagline=APP_TAGLINE,
        package_name=PACKAGE_NAME,
        prog_name=PROG_NAME,
        version=__version__,
        description=DESCRIPTION,
        scope_description=APP_SCOPE,
    )
    return build_about(meta, logo_ascii=_load_logo_ascii())
