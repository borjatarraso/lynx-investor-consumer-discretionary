*** Settings ***
Documentation    Python API tests for lynx-discretionary
Library          Process

*** Variables ***
${PYTHON}        python3

*** Keywords ***
When I Run Python Code "${code}"
    ${result}=    Run Process    ${PYTHON}    -c    ${code}    timeout=120s
    Set Test Variable    ${OUTPUT}    ${result.stdout}${result.stderr}
    Set Test Variable    ${RC}    ${result.rc}

Then The Exit Code Should Be ${expected}
    Should Be Equal As Integers    ${RC}    ${expected}

Then The Output Should Contain "${text}"
    Should Contain    ${OUTPUT}    ${text}

*** Test Cases ***
Import All Models
    [Documentation]    GIVEN the package WHEN I import models THEN all classes are available
    When I Run Python Code "from lynx_discretionary.models import AnalysisReport, CompanyProfile, CompanyStage, CompanyTier, Segment, JurisdictionTier, Relevance, MarketIntelligence, InsiderTransaction; print('OK')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Import All Calculators
    [Documentation]    GIVEN the package WHEN I import calculators THEN all functions exist
    When I Run Python Code "from lynx_discretionary.metrics.calculator import calc_valuation, calc_profitability, calc_solvency, calc_growth, calc_efficiency, calc_share_structure, calc_business_quality, calc_intrinsic_value, calc_market_intelligence; print('OK')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Classify Company Tier Mega Cap
    [Documentation]    GIVEN a large market cap WHEN I classify THEN it returns Mega Cap
    When I Run Python Code "from lynx_discretionary.models import classify_tier; print(classify_tier(500_000_000_000).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Mega Cap"

Classify Company Tier Micro Cap
    [Documentation]    GIVEN a small market cap WHEN I classify THEN it returns Micro Cap
    When I Run Python Code "from lynx_discretionary.models import classify_tier; print(classify_tier(100_000_000).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Micro Cap"

Classify Company Tier None
    [Documentation]    GIVEN None market cap WHEN I classify THEN it returns Nano Cap
    When I Run Python Code "from lynx_discretionary.models import classify_tier; print(classify_tier(None).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Nano Cap"

Classify Operator Stage Mature
    [Documentation]    GIVEN a large retailer WHEN I classify THEN Mature Operator
    When I Run Python Code "from lynx_discretionary.models import classify_stage; print(classify_stage('global retailer with comparable store sales', 25000000000, {'operatingMargins': 0.12}).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Mature Operator"

Classify Operator Stage Franchise
    [Documentation]    GIVEN a franchise description WHEN I classify THEN Franchise
    When I Run Python Code "from lynx_discretionary.models import classify_stage; print(classify_stage('global restaurant franchisor', 8000000000, {}).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Franchise"

Classify Operator Stage Scaling
    [Documentation]    GIVEN a scaling retailer WHEN I classify THEN Scaling Operator
    When I Run Python Code "from lynx_discretionary.models import classify_stage; print(classify_stage('expanding retail concept rolling out new stores', 1500000000, {'operatingMargins': 0.06}).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Scaling Operator"

Classify Operator Stage Emerging
    [Documentation]    GIVEN a small DTC brand WHEN I classify THEN Emerging Brand
    When I Run Python Code "from lynx_discretionary.models import classify_stage; print(classify_stage('emerging direct-to-consumer brand', 80000000, {'operatingMargins': -0.02}).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Emerging"

Classify Segment Apparel
    [Documentation]    GIVEN apparel text WHEN I classify THEN Apparel detected
    When I Run Python Code "from lynx_discretionary.models import classify_segment; print(classify_segment('premium athletic apparel and footwear', 'Apparel Manufacturing').value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Apparel"

Classify Segment Restaurants
    [Documentation]    GIVEN restaurant text WHEN I classify THEN Restaurants detected
    When I Run Python Code "from lynx_discretionary.models import classify_segment; print(classify_segment('quick-service restaurant chain', 'Restaurants').value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Restaurants"

Classify Segment Automotive
    [Documentation]    GIVEN auto text WHEN I classify THEN Automotive detected
    When I Run Python Code "from lynx_discretionary.models import classify_segment; print(classify_segment('electric vehicle automobile manufacturer', 'Auto Manufacturers').value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Automotive"

Classify Market Exposure Tier 1
    [Documentation]    GIVEN United States WHEN I classify THEN Tier 1
    When I Run Python Code "from lynx_discretionary.models import classify_jurisdiction; print(classify_jurisdiction('United States').value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Tier 1"

Classify Market Exposure Tier 2
    [Documentation]    GIVEN Mexico WHEN I classify THEN Tier 2
    When I Run Python Code "from lynx_discretionary.models import classify_jurisdiction; print(classify_jurisdiction('Mexico').value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Tier 2"

Relevance Emerging Cash Runway Critical
    [Documentation]    GIVEN emerging brand WHEN I check cash runway THEN critical
    When I Run Python Code "from lynx_discretionary.metrics.relevance import get_relevance; from lynx_discretionary.models import CompanyTier, CompanyStage; print(get_relevance('cash_runway_years', CompanyTier.MICRO, 'solvency', CompanyStage.EXPLORER).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "critical"

Relevance Mature EV EBITDA Critical
    [Documentation]    GIVEN mature operator WHEN I check EV/EBITDA THEN critical
    When I Run Python Code "from lynx_discretionary.metrics.relevance import get_relevance; from lynx_discretionary.models import CompanyTier, CompanyStage; print(get_relevance('ev_ebitda', CompanyTier.MID, 'valuation', CompanyStage.PRODUCER).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "critical"

Relevance Mature ROIC Critical
    [Documentation]    GIVEN mature operator WHEN I check ROIC THEN critical
    When I Run Python Code "from lynx_discretionary.metrics.relevance import get_relevance; from lynx_discretionary.models import CompanyTier, CompanyStage; print(get_relevance('roic', CompanyTier.MID, 'profitability', CompanyStage.PRODUCER).value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "critical"

Get Metric Explanation
    [Documentation]    GIVEN metric key WHEN I get explanation THEN details returned
    When I Run Python Code "from lynx_discretionary.metrics.explanations import get_explanation; e = get_explanation('gross_margin'); print(e.full_name)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "Gross Margin"

Get Unknown Metric Returns None
    [Documentation]    GIVEN bad key WHEN I get explanation THEN None
    When I Run Python Code "from lynx_discretionary.metrics.explanations import get_explanation; print(get_explanation('nonexistent'))"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "None"

Get Sector Insight
    [Documentation]    GIVEN Consumer Cyclical WHEN I get insight THEN data returned
    When I Run Python Code "from lynx_discretionary.metrics.sector_insights import get_sector_insight; s = get_sector_insight('Consumer Cyclical'); print('OK' if s else 'FAIL')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Get Industry Insight Apparel
    [Documentation]    GIVEN Apparel Manufacturing WHEN I get insight THEN data returned
    When I Run Python Code "from lynx_discretionary.metrics.sector_insights import get_industry_insight; i = get_industry_insight('Apparel Manufacturing'); print('OK' if i else 'FAIL')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Get Industry Insight Restaurants
    [Documentation]    GIVEN Restaurants WHEN I get insight THEN data returned
    When I Run Python Code "from lynx_discretionary.metrics.sector_insights import get_industry_insight; i = get_industry_insight('Restaurants'); print('OK' if i else 'FAIL')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Storage Mode Switching
    [Documentation]    GIVEN storage WHEN I switch modes THEN it works
    When I Run Python Code "from lynx_discretionary.core.storage import set_mode, get_mode, is_testing; set_mode('testing'); assert is_testing(); set_mode('production'); assert not is_testing(); print('OK')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Storage Invalid Mode Raises Error
    [Documentation]    GIVEN storage WHEN I set invalid mode THEN error
    When I Run Python Code "from lynx_discretionary.core.storage import set_mode; set_mode('invalid')"
    Then The Exit Code Should Be 1
    Then The Output Should Contain "ValueError"

Export Formats Available
    [Documentation]    GIVEN export module WHEN I check formats THEN all exist
    When I Run Python Code "from lynx_discretionary.export import ExportFormat; print(ExportFormat.TXT.value, ExportFormat.HTML.value, ExportFormat.PDF.value)"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "txt html pdf"

About Text Has All Fields
    [Documentation]    GIVEN package WHEN I get about THEN all fields present
    When I Run Python Code "from lynx_discretionary import get_about_text; a = get_about_text(); assert all(k in a for k in ['name','suite','version','author','license','description']); print('OK')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Conclusion Generation
    [Documentation]    GIVEN minimal report WHEN I generate conclusion THEN a verdict is produced
    When I Run Python Code "from lynx_discretionary.models import AnalysisReport, CompanyProfile; from lynx_discretionary.core.conclusion import generate_conclusion; r = AnalysisReport(profile=CompanyProfile(ticker='TEST', name='Test')); c = generate_conclusion(r); assert c.verdict in ['Strong Buy','Buy','Hold','Caution','Avoid']; print('OK')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"

Consumer Metrics In Explanations
    [Documentation]    GIVEN explanations WHEN I list THEN consumer metrics present
    When I Run Python Code "from lynx_discretionary.metrics.explanations import list_metrics; keys = [m.key for m in list_metrics()]; assert 'gross_margin' in keys; assert 'quality_score' in keys; assert 'lease_adjusted_debt_ratio' in keys; assert 'brand_strength' in keys; print('OK')"
    Then The Exit Code Should Be 0
    Then The Output Should Contain "OK"
