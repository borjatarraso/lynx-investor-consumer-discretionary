"""Consumer-discretionary-focused sector and industry insights."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SectorInsight:
    sector: str
    overview: str
    critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list)
    what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""


@dataclass
class IndustryInsight:
    industry: str
    sector: str
    overview: str
    critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list)
    what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""


_SECTORS: dict[str, SectorInsight] = {}
_INDUSTRIES: dict[str, IndustryInsight] = {}


def _add_sector(sector, overview, cm, kr, wtw, tv):
    _SECTORS[sector.lower()] = SectorInsight(
        sector=sector, overview=overview, critical_metrics=cm,
        key_risks=kr, what_to_watch=wtw, typical_valuation=tv,
    )


def _add_industry(industry, sector, overview, cm, kr, wtw, tv):
    _INDUSTRIES[industry.lower()] = IndustryInsight(
        industry=industry, sector=sector, overview=overview,
        critical_metrics=cm, key_risks=kr, what_to_watch=wtw,
        typical_valuation=tv,
    )


_add_sector(
    "Consumer Cyclical",
    "Consumer discretionary companies sell goods and services that consumers "
    "can defer or reallocate when budgets tighten. Demand moves with consumer "
    "confidence, disposable income, interest rates, and fashion / preference "
    "cycles. Brand strength, unit economics, and capital discipline distinguish "
    "durable franchises from cyclically exposed operators.",
    ["Same-store sales (or proxy)", "Gross margin & trend",
     "ROIC", "Inventory turnover", "Debt/EBITDA (lease-adjusted)",
     "CAPEX intensity"],
    ["Consumer spending downturn / recession", "Interest-rate pressure on big-ticket purchases",
     "Tariffs and supply-chain disruption", "Fashion / trend reversal",
     "Lease commitments stressing balance sheets",
     "Margin compression from labour and input costs"],
    ["Consumer confidence index", "Retail sales data",
     "Personal consumption expenditure (PCE)", "Credit card spending trends",
     "Inventory-to-sales ratio", "Commercial real estate rents"],
    "EV/EBITDA 8-15x for mature retail. P/FCF <20x for healthy mature. "
    "P/S 1-3x for specialty retail. Franchise / QSR trades at premium multiples.",
)

_add_sector(
    "Consumer Discretionary",
    "Alias for Consumer Cyclical — see the Consumer Cyclical entry for detail.",
    ["Same-store sales", "Gross margin", "ROIC",
     "Inventory turnover", "Debt/EBITDA"],
    ["Consumer recession", "Tariffs", "Interest rates",
     "Fashion cycle", "Lease commitments"],
    ["Consumer confidence", "Retail sales", "PCE",
     "Inventory-to-sales", "CRE rents"],
    "EV/EBITDA 8-15x. P/FCF <20x.",
)


_add_industry(
    "Apparel Manufacturing", "Consumer Cyclical",
    "Apparel and footwear brands derive value from brand equity, product "
    "innovation, channel mix, and inventory discipline. Best-in-class names "
    "(NKE, LULU) command 45-55% gross margins and high ROIC via wholesale "
    "leverage and direct-to-consumer expansion.",
    ["Gross margin (target >45%)", "Inventory days (watch for rising trend)",
     "Direct-to-consumer mix %", "ROIC", "Revenue growth",
     "Average unit retail (AUR)"],
    ["Trend / fashion reversal", "Tariffs on imported apparel",
     "Channel disintermediation", "Markdown risk",
     "Supply-chain disruption (Asia concentration)",
     "Counterfeit / IP theft"],
    ["Full-price sell-through", "Wholesale order book",
     "Direct-to-consumer growth", "International expansion ramp",
     "New product launches"],
    "EV/EBITDA 12-18x for premium brands. P/E 20-30x. P/S 2-4x. "
    "Premium brands (LULU, NKE) trade at 25-40x P/E during growth phases.",
)

_add_industry(
    "Specialty Retail", "Consumer Cyclical",
    "Specialty retailers focus on a narrow product category with deep "
    "assortment. Off-price retailers (TJX, ROST) thrive during downturns; "
    "full-price specialty (ULTA, FIVE) depends on differentiated merchandise. "
    "Comparable-store sales and inventory health are critical.",
    ["Same-store sales", "Gross margin", "Inventory turnover",
     "SG&A leverage", "New-store productivity"],
    ["E-commerce share shift", "Amazon competition",
     "Mall traffic decline", "Margin compression from promotional activity",
     "Overstocked inventory requiring markdowns"],
    ["Comparable sales trend", "Inventory growth vs revenue growth",
     "Store count and productivity", "Digital mix",
     "Markdown cadence"],
    "EV/EBITDA 8-12x. P/E 15-22x. Off-price leaders earn premium. "
    "Struggling concepts trade <6x EV/EBITDA.",
)

_add_industry(
    "Home Improvement Retail", "Consumer Cyclical",
    "Home improvement (HD, LOW) combines scale advantages, professional "
    "contractor relationships, and exposure to housing-turnover and "
    "home-price trends. High ROIC, moderate cyclicality, strong buybacks.",
    ["Same-store sales", "Pro vs DIY mix",
     "Gross margin", "Operating margin", "ROIC"],
    ["Housing turnover slowdown", "Weather disruption",
     "Input-cost inflation (lumber, appliances)",
     "Private-label commodity competition"],
    ["Housing starts & existing home sales", "Mortgage rates",
     "Home Depot / Lowe's quarterly comps", "Pro segment growth",
     "Appliance demand"],
    "EV/EBITDA 14-18x. P/E 18-25x. Dominant duopoly earns premium multiples.",
)

_add_industry(
    "Restaurants", "Consumer Cyclical",
    "Restaurants split between quick-service (MCD, CMG, DPZ, YUM) and casual "
    "dining. QSR benefits from franchise economics — asset-light, high "
    "royalty margins, recession resilience. Casual dining is more cyclical. "
    "System-wide same-store sales drive valuations.",
    ["Same-store sales", "Franchise vs company-owned mix",
     "Unit growth", "Operating margin", "Store-level margin (company-owned)",
     "Traffic vs check-average"],
    ["Labour-cost inflation", "Food-cost inflation",
     "Traffic decline", "Minimum-wage legislation",
     "Franchisee financial health"],
    ["Traffic trends", "Average check", "Unit growth",
     "Digital / delivery mix", "International expansion"],
    "QSR franchisors: EV/EBITDA 18-28x, P/E 25-35x. "
    "Casual dining: EV/EBITDA 8-12x, P/E 12-18x.",
)

_add_industry(
    "Auto Manufacturers", "Consumer Cyclical",
    "Auto manufacturers (TSLA, F, GM, STLA) are capital-intensive and highly "
    "cyclical. EV transition reshuffles the competitive set; scale, "
    "manufacturing flexibility, and balance-sheet strength determine "
    "survival. Interest rates impact affordability materially.",
    ["Operating margin by segment", "CAPEX intensity",
     "R&D as % of revenue", "Inventory days", "Vehicle mix & ASP",
     "Debt/EBITDA (watch auto-finance arm separately)"],
    ["Interest-rate sensitivity (vehicle financing)",
     "EV transition investment", "Labour disruption (UAW)",
     "Tariffs & trade policy", "Chinese EV competition",
     "Residual-value risk in auto finance"],
    ["US auto SAAR", "ASP trends", "EV adoption curve",
     "Affordability / monthly payments", "Dealer inventory"],
    "Traditional automakers: EV/EBITDA 4-8x (cyclical trough) to 8-12x (peak). "
    "Tesla premium trades at technology-company multiples.",
)

_add_industry(
    "Lodging", "Consumer Cyclical",
    "Hotels and resorts (MAR, HLT, H) operate mostly asset-light franchise "
    "models that earn royalty and incentive fees on system-wide RevPAR. "
    "Highly cyclical with travel demand; recovery from 2020-21 COVID downturn "
    "has been strong. Loyalty programs and business mix matter.",
    ["RevPAR (revenue per available room)", "Occupancy",
     "Asset-light fee income %", "Unit growth (pipeline)",
     "Operating margin", "Free cash flow conversion"],
    ["Business travel structural decline",
     "Recession cutting leisure travel", "Airbnb / alternative accommodation",
     "Currency and international exposure", "Labour inflation"],
    ["RevPAR month-over-month", "Pipeline of new properties",
     "International openings", "Business mix (group vs transient)",
     "Loyalty program penetration"],
    "Franchise hotels: EV/EBITDA 18-25x, P/E 25-35x. "
    "Owned hotels and REITs trade lower.",
)

_add_industry(
    "Internet Retail", "Consumer Cyclical",
    "E-commerce pure-plays (AMZN, EBAY, ETSY) scale on software-like "
    "economics. Amazon's retail is a capital-intensive juggernaut; AWS "
    "earnings dwarf retail. Marketplaces (ETSY, EBAY) earn take-rate on GMV.",
    ["Gross merchandise value (GMV) growth", "Take rate / margin",
     "Active buyers and retention", "Fulfillment cost trends",
     "Operating margin"],
    ["Amazon competitive encroachment", "Fulfillment cost inflation",
     "Traffic acquisition cost rising", "Marketplace seller attrition",
     "Regulatory scrutiny (antitrust, sales tax)"],
    ["GMV growth", "Active buyer growth", "Take rate trend",
     "Contribution margin", "Advertising revenue growth"],
    "E-commerce marketplaces: EV/EBITDA 12-20x. P/S 2-5x. "
    "Amazon trades on sum-of-parts (AWS + retail + ads).",
)

_add_industry(
    "Residential Construction", "Consumer Cyclical",
    "Homebuilders (DHI, LEN, TOL) are highly cyclical with mortgage rates "
    "and housing-starts trends. Margin and cash flow swing dramatically "
    "across the cycle. Book value and land position dominate valuation.",
    ["Home orders / closings growth", "Gross margin",
     "Book value per share", "Land inventory (years of supply)",
     "Cancellation rate"],
    ["Mortgage-rate increases", "Land-inventory write-downs",
     "Construction-cost inflation", "Labor shortages",
     "Regional housing downturns"],
    ["Housing starts", "Mortgage rates", "New home inventory",
     "Homebuilder order trends", "Builder sentiment (NAHB)"],
    "Homebuilders: P/B 0.8-1.5x through the cycle, P/E 8-15x. "
    "Premium builders (TOL) earn higher multiples.",
)

_add_industry(
    "Luxury Goods", "Consumer Cyclical",
    "Luxury companies (EL, RL, TPR, plus European majors LVMH, Hermès) earn "
    "premium margins on brand equity and customer loyalty. Chinese consumer "
    "demand is a critical swing factor. Travel recovery and wealth-effect "
    "cycles drive short-term performance.",
    ["Gross margin (target >65%)", "Organic growth",
     "China revenue %", "Wholesale vs DTC mix", "Brand portfolio depth"],
    ["Chinese consumer slowdown", "Currency translation",
     "Counterfeit / grey-market leakage",
     "Key-money (flagship lease) inflation",
     "Wealth-effect / equity market corrections"],
    ["China same-store sales", "Wholesale order book",
     "DTC comparable sales", "New store openings",
     "Cross-border travel data"],
    "Luxury: EV/EBITDA 15-25x, P/E 22-35x. "
    "Hermès trades at 40-60x P/E due to pricing power.",
)


def get_sector_insight(sector: str | None) -> SectorInsight | None:
    return _SECTORS.get(sector.lower()) if sector else None


def get_industry_insight(industry: str | None) -> IndustryInsight | None:
    return _INDUSTRIES.get(industry.lower()) if industry else None


def list_sectors() -> list[str]:
    return sorted(s.sector for s in _SECTORS.values())


def list_industries() -> list[str]:
    return sorted(i.industry for i in _INDUSTRIES.values())
