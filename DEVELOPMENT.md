# Development Guide

## Architecture

The application follows the shared Lince Investor Suite architecture with
consumer-discretionary-specific adaptations. Cross-agent plumbing lives in
the `lynx-investor-core` package; only sector-specific logic lives here.

### Data Flow

```
User Input (ticker/ISIN/name)
    ↓
CLI/Interactive/TUI/GUI → cli.py
    ↓
analyzer.py: run_progressive_analysis()
    ↓
ticker.py: resolve_identifier() → (ticker, isin)
    ↓
storage.py: check cache → return if cached
    ↓
fetcher.py: yfinance data (profile + financials)
    ↓
models.py: classify_stage / classify_segment / classify_jurisdiction
    ↓
analyzer.py: _validate_sector (consumer-discretionary gate)
    ↓
calculator.py: calc_valuation / profitability / solvency / growth / efficiency
    ↓
calculator.py: calc_share_structure + calc_business_quality
    ↓
calculator.py: calc_market_intelligence (insider, analyst, short, technicals, XLY + peer ETF)
    ↓
calculator.py: calc_intrinsic_value
    ↓
[parallel] reports.py + news.py
    ↓
conclusion.py: generate_conclusion() → verdict + consumer screening
    ↓
storage.py: save_analysis_report()
    ↓
display.py / tui/app.py / gui/app.py → render
```

### Key Design Decisions

1. **Stage > Tier**: Consumer-discretionary operator maturity is the primary
   analysis axis, not market cap tier. Mature operators (MCD, HD) and
   emerging brands (early-stage DTC) demand entirely different metric sets.

2. **Cyclical Tagging**: Business-quality scoring does **not** penalize
   cyclical sub-segments (autos, homes, travel, luxury, leisure) — it
   simply surfaces the exposure as a qualitative tag so investors can size
   positions appropriately.

3. **Lease-Adjusted Leverage**: Brick-and-mortar retail and restaurants
   have material off-balance-sheet lease commitments. We capitalize rent
   at 8× and include it in a lease-adjusted Debt/EBITDAR ratio alongside
   the raw Debt/EBITDA.

4. **Relevance-Driven Display**: All 4 UI modes use `get_relevance()` to
   determine which metrics to highlight, dim, or hide. For consumer
   operators this means gross margin stays Critical across every stage,
   while cash runway only surfaces for Early Stage / Emerging operators.

5. **Same-Store Sales Proxy**: Most filings don't expose comparable-store
   sales directly. We approximate productivity by subtracting asset growth
   from revenue growth — positive values indicate the existing base is
   producing more.

6. **Consumer Disclaimers**: Every analysis includes stage-specific risk
   disclosures around cyclical spending, fashion/trend reversal, and
   franchise-system dependency.

### Adding New Metrics

1. Add field to the appropriate dataclass in `models.py`
2. Calculate in `calculator.py` (in the relevant `calc_*` function)
3. Add relevance entry in `relevance.py` (_STAGE_OVERRIDES and tier tables)
4. Add explanation in `explanations.py`
5. Add display row in `display.py`, `tui/app.py`, `gui/app.py`

### Adding New Consumer Sub-Segments

1. Add to `Segment` enum in `models.py`
2. Add keywords to `_SEGMENT_KEYWORDS`
3. Add sector-ETF mapping in `_CONSUMER_PROXIES` in `calculator.py`
4. Optionally classify as cyclical in `_CYCLICAL_SEGMENTS` in `calculator.py`
5. Add industry insight in `sector_insights.py`

### Adding New Stages

1. Add to `CompanyStage` enum
2. Add keywords to `_STAGE_KEYWORDS`
3. Add weights to `_WEIGHTS` in `conclusion.py`
4. Add relevance overrides in `relevance.py`

## Running Tests

```bash
# Python unit tests
pytest tests/ -v --tb=short

# Robot Framework (requires robotframework)
pip install robotframework
robot --outputdir results robot/

# Syntax check all files
python -c "import py_compile, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('lynx_discretionary/**/*.py', recursive=True)]"
```

## Code Style

- Python 3.10+ with type hints
- Dataclasses for all data models
- Rich for console rendering
- Textual for TUI
- Tkinter for GUI
