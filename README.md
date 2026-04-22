# Lynx Consumer Discretionary Analysis

> Fundamental analysis specialized for consumer discretionary companies — apparel, specialty retail, home improvement, restaurants, autos, lodging, e-commerce, and luxury.

Part of the **Lince Investor Suite**.

## Overview

Lynx Consumer Discretionary is a comprehensive fundamental analysis tool built specifically for consumer-discretionary investors. It evaluates operators across all maturity stages — from emerging direct-to-consumer brands to mature franchise systems — using consumer-specific metrics, stage-aware valuation methods, and cyclical risk assessments.

### Key Features

- **Stage-Aware Analysis**: Automatically classifies operators as Early Stage / Pre-Profit, Emerging Brand, Scaling Operator, Mature Operator, or Franchise / Asset-Light — and adapts all metrics and scoring accordingly
- **Consumer-Specific Metrics**: Gross margin trend, same-store-sales proxy, inventory turnover, lease-adjusted leverage, SG&A leverage, store-contribution proxy, and capex intensity
- **4-Level Relevance System**: Marks each metric as Critical, Relevant, Contextual, or Irrelevant based on the operator's maturity stage
- **Market Intelligence**: Insider transactions, institutional holders, analyst consensus, short interest, price technicals with golden/death cross detection, and XLY / sub-sector ETF comparisons
- **10-Point Consumer Screening Checklist**: Evaluates margin quality, ROIC, leverage, growth, dilution, insider ownership, FCF generation, and valuation discipline
- **Cyclical Sensitivity Tagging**: Flags autos, homebuilding, lodging, luxury, and leisure as high-cyclicality sub-segments
- **Sub-Segment Detection**: Automatically identifies primary consumer segment (Apparel, Specialty Retail, Restaurants, Autos, E-commerce, Lodging, Luxury, Homebuilding, etc.)
- **Multiple Interface Modes**: Console CLI, Interactive REPL, Textual TUI, Tkinter GUI
- **Export**: TXT, HTML, and PDF report generation
- **Sector & Industry Insights**: Deep context for Apparel, Specialty Retail, Home Improvement, Restaurants, Autos, Lodging, Internet Retail, Homebuilders, and Luxury Goods

### Target Companies

Designed for analyzing companies like:
- **Apparel & Footwear**: NKE, LULU, LEVI, VFC, UAA
- **Specialty Retail**: TJX, ROST, ULTA, FIVE, BURL, TGT
- **Home Improvement**: HD, LOW
- **Restaurants**: MCD, CMG, SBUX, DPZ, YUM, QSR, WEN, WING
- **Autos**: TSLA, F, GM, STLA, TM
- **Lodging & Travel**: MAR, HLT, H, BKNG, EXPE, ABNB
- **Internet Retail**: AMZN, EBAY, ETSY, W
- **Luxury**: RL, TPR, EL
- **Homebuilders**: DHI, LEN, TOL, NVR

## Installation

```bash
# Clone the repository
git clone https://github.com/borjatarraso/lynx-investor-consumer-discretionary.git
cd lynx-investor-consumer-discretionary

# Install in editable mode (creates the `lynx-discretionary` command)
pip install -e .
```

### Dependencies

| Package        | Purpose                              |
|----------------|--------------------------------------|
| yfinance       | Financial data from Yahoo Finance    |
| requests       | HTTP calls (OpenFIGI, EDGAR, etc.)   |
| beautifulsoup4 | HTML parsing for SEC filings         |
| rich           | Terminal tables and formatting       |
| textual        | Full-screen TUI framework            |
| feedparser     | News RSS feed parsing                |
| pandas         | Data analysis                        |
| numpy          | Numerical computing                  |

All dependencies are installed automatically via `pip install -e .`.

## Usage

### Direct Execution
```bash
# Via the runner script
./lynx-investor-consumer-discretionary.py -p AMZN

# Via Python
python3 lynx-investor-consumer-discretionary.py -p HD

# Via pip-installed command
lynx-discretionary -p MCD
```

### Execution Modes

| Flag | Mode | Description |
|------|------|-------------|
| `-p` | Production | Uses `data/` for persistent cache |
| `-t` | Testing | Uses `data_test/` (isolated, always fresh) |

### Interface Modes

| Flag | Interface | Description |
|------|-----------|-------------|
| (none) | Console | Progressive CLI output |
| `-i` | Interactive | REPL with commands |
| `-tui` | TUI | Textual terminal UI with themes |
| `-x` | GUI | Tkinter graphical interface |

### Examples

```bash
# Analyze a mega-cap e-commerce operator
lynx-discretionary -p AMZN

# Force fresh data download
lynx-discretionary -p NKE --refresh

# Search by company name
lynx-discretionary -p "Home Depot"

# Interactive mode
lynx-discretionary -p -i

# Export HTML report
lynx-discretionary -p MCD --export html

# Explain a metric
lynx-discretionary --explain gross_margin

# Skip filings and news for faster analysis
lynx-discretionary -t TJX --no-reports --no-news
```

## Analysis Sections

1. **Company Profile** — Tier, operator stage, consumer sub-segment, market-exposure classification
2. **Sector & Industry Insights** — Consumer-specific context and benchmarks
3. **Valuation Metrics** — Traditional (P/E, P/FCF, EV/EBITDA, P/S) + consumer-specific (EV per store)
4. **Profitability Metrics** — ROE, ROIC, margins with trend, SG&A%, store-contribution proxy (hidden for pre-profit stages)
5. **Solvency & Survival** — Debt/EBITDA, lease-adjusted leverage, interest coverage, cash runway for emerging operators
6. **Growth & Capital Discipline** — Revenue / earnings growth, same-store-sales proxy, capex intensity, dilution / buyback CAGR
7. **Operating Efficiency** — Asset turnover, inventory turnover, days inventory, revenue per employee, working-capital intensity
8. **Share Structure** — Outstanding/diluted shares, insider/institutional ownership
9. **Business Quality** — Brand strength, unit economics, financial position, cyclical sensitivity, channel mix
10. **Intrinsic Value** — DCF, Graham Number, Asset-Based (method selection by stage)
11. **Market Intelligence** — Analysts, short interest, technicals, insider trades, XLY / sub-sector ETF context
12. **Financial Statements** — 5-year annual summary
13. **SEC Filings** — Downloadable regulatory filings
14. **News** — Yahoo Finance + Google News RSS
15. **Assessment Conclusion** — Weighted score, verdict, strengths/risks, screening checklist
16. **Consumer Discretionary Disclaimers** — Stage-specific risk disclosures

## Relevance System

Each metric is classified by importance for the operator's maturity stage:

| Level | Display | Meaning |
|-------|---------|---------|
| **Critical** | `*` bold cyan star | Must-check for this stage |
| **Relevant** | Normal | Important context |
| **Contextual** | Dimmed | Informational only |
| **Irrelevant** | Hidden | Not meaningful for this stage |

Example: For a Mature Operator, ROIC and Debt/EBITDA are **Critical** while Cash Runway is **Irrelevant**.

## Scoring Methodology

The overall score (0-100) is a weighted average of 5 categories, with weights adapted by both company tier AND operator stage:

| Stage                   | Valuation | Profitability | Solvency | Growth | Business Quality |
|-------------------------|-----------|---------------|----------|--------|------------------|
| Early Stage             | 5%        | 5%            | 40-45%   | 15-20% | 30%              |
| Emerging Brand          | 5-10%     | 5-10%         | 30-40%   | 25%    | 25%              |
| Scaling Operator        | 10-15%    | 10-20%        | 15-35%   | 25%    | 25%              |
| Mature Operator         | 15-20%    | 15-25%        | 10-30%   | 15-20% | 25%              |
| Franchise / Asset-Light | 20%       | 30%           | 10%      | 15%    | 25%              |

Verdicts: Strong Buy (>=75), Buy (>=60), Hold (>=45), Caution (>=30), Avoid (<30).

## Project Structure

```
lynx-investor-consumer-discretionary/
├── lynx-investor-consumer-discretionary.py  # Runner script
├── pyproject.toml                           # Build configuration
├── requirements.txt                         # Dependencies
├── img/                                     # Logo images
├── data/                                    # Production cache
├── data_test/                               # Testing cache
├── docs/                                    # Documentation
│   └── API.md                               # API reference
├── robot/                                   # Robot Framework tests
│   ├── cli_tests.robot
│   ├── api_tests.robot
│   └── export_tests.robot
├── tests/                                   # Unit tests
└── lynx_discretionary/                      # Main package
```

## Testing

```bash
# Unit tests
pytest tests/ -v

# Robot Framework acceptance tests
robot robot/
```

## License

BSD 3-Clause License. See LICENSE in source.

## Author

**Borja Tarraso** — borja.tarraso@member.fsf.org
