# Changelog

All notable changes to **Lynx Consumer Discretionary Analysis** are documented here.

## [3.0] - 2026-04-22

Part of **Lince Investor Suite v3.0** coordinated release.

### Added
- Uniform PageUp / PageDown navigation across every UI mode (GUI, TUI,
  interactive, console). Scrolling never goes above the current output
  in interactive and console mode; Shift+PageUp / Shift+PageDown remain
  reserved for the terminal emulator's own scrollback.
- Sector-mismatch warning now appends a `Suggestion: use
  'lynx-investor-<other>' instead.` line sourced from
  `lynx_investor_core.sector_registry`. The original warning text is
  preserved as-is.

### Changed
- TUI wires `lynx_investor_core.pager.PagingAppMixin` and
  `tui_paging_bindings()` into the main application.
- Graphical mode binds `<Prior>` / `<Next>` / `<Control-Home>` /
  `<Control-End>` via `bind_tk_paging()`.
- Interactive mode pages long output through `console_pager()` /
  `paged_print()`.
- Depends on `lynx-investor-core>=2.0`.

## [1.0] — 2026-04-21

Initial release as a standalone agent in the Lince Investor Suite. Forked
from `lynx-investor-basic-materials` (shared plumbing in `lynx-investor-core`)
and specialized for consumer discretionary companies.

### Added — Consumer-Discretionary Fundamental Analysis

- **Sector validator** restricts analysis to consumer-discretionary (GICS:
  "Consumer Cyclical" in Yahoo Finance taxonomy) companies, with allow-lists
  for apparel, specialty retail, home improvement, restaurants, autos,
  internet retail, lodging, leisure, luxury goods, and homebuilders.
- **Stage classifier** labels operators Early Stage / Pre-Profit, Emerging
  Brand, Scaling Operator, Mature Operator, or Franchise / Asset-Light based
  on revenue scale, operating margin, and description heuristics.
- **Sub-segment classifier** maps companies to Apparel, Specialty Retail,
  Home Improvement, Restaurants, Automotive, Lodging & Travel, Leisure,
  E-commerce, Luxury, or Homebuilding.
- **Market-exposure tier** replaces the mining "jurisdiction" axis with a
  geographic revenue-concentration read (developed / mixed / high concentration).
- **Consumer-specific metrics**:
  - Gross margin trend (expanding / stable / compressing)
  - Same-store-sales proxy (revenue growth minus asset growth)
  - Lease-adjusted leverage (Debt + 8× rent) / EBITDAR
  - SG&A as % of revenue + store-contribution margin proxy
  - Inventory turnover + days inventory
  - Working-capital intensity
  - Revenue per employee
  - CAPEX intensity
- **Business-quality scoring** over five dimensions:
  - Brand strength / margin resilience (25 pts)
  - Unit economics — ROIC + operating margin (25 pts)
  - Financial position — leverage + liquidity (20 pts)
  - Management alignment — insider ownership (15 pts)
  - Capital discipline — dilution / buybacks (15 pts)
- **Cyclical-sensitivity tagging** flags high-cyclicality sub-segments
  (autos, homebuilding, travel, luxury, leisure).
- **10-point consumer screening checklist**: positive operating margin,
  gross margin ≥ 30%, ROIC > 10%, reasonable leverage, revenue growth > 3%,
  low dilution (< 3%/yr), insider ownership ≥ 5%, positive FCF margin,
  reasonable P/E (< 25), developed-market exposure.
- **Stage-appropriate intrinsic-value methods**: DCF for mature, EV/EBITDA
  comps for scaling, EV/Revenue with margin ramp for emerging, DCF on
  royalty stream for franchise.
- **Sector context** now fetches the Consumer Discretionary Select Sector
  SPDR (XLY) as the demand proxy, plus a sub-segment peer ETF (XRT, XHB,
  EATZ, CARZ, AWAY, PEJ, ONLN, ITB).
- **Consumer-specific disclaimers** cover cyclical spending, fashion/trend
  reversal, franchise-system dependency, and unit-economics stretch during
  rapid expansion.

### Changed

- `CompanyStage` enum string values updated: `GRASSROOTS="Early Stage / Pre-Profit"`,
  `EXPLORER="Emerging Brand"`, `DEVELOPER="Scaling Operator"`,
  `PRODUCER="Mature Operator"`, `ROYALTY="Franchise / Asset-Light"`.
- `Segment` enum (formerly `Commodity`) redefined with consumer sub-segments.
- `BusinessQualityIndicators` (formerly `MiningQualityIndicators`) replaces
  geological/jurisdictional fields with brand, unit economics, channel mix,
  cyclical sensitivity, margin resilience, and customer concentration.
- `AnalysisReport.business_quality` attribute replaces `.mining_quality`.
- Scoring weights rebalanced: mature / franchise operators weight
  profitability and business quality at 25% each; emerging / early-stage
  operators keep solvency + growth dominance.
- All sector insights, metric explanations, and peer examples rewritten for
  consumer-discretionary context.

### Infrastructure

- Shared plumbing continues to come from `lynx-investor-core` (storage,
  sector gate, ticker resolution, logo, about, easter-egg renderer).
