"""Single source of truth for the dataset.
Run:  python build_data.py
Writes data/credits.json and assets/data.js (kept identical on purpose)."""
import json, pathlib

meta = {
    "title": "Clean Energy Credit Finder",
    "subtitle": "Which IRA clean-energy tax credits you still qualify for \u2014 and how much time is left.",
    "law_context": "The Inflation Reduction Act (IRA) created these credits; the One Big Beautiful Bill Act (OBBBA), signed July 4, 2025, cut most of their timelines short.",
    "data_as_of": "2026-06",
    "disclaimer": "This is an educational summary, not tax or legal advice. Dates, dollar values, and eligibility rules are simplified. Confirm current rules with the IRS and a qualified tax professional before acting.",
    "sources": "IRS OBBBA FAQs; Steptoe; Grant Thornton; CESA; Arnold & Porter; McGuireWoods; Holland & Knight; Third Way; Columbia Climate Law Blog; Clifford Chance; USGBC; Nossaman (2025\u20132026).",
}

personas = [
    {"key": "homeowner",   "label": "Homeowner",                          "blurb": "Upgrading or powering the home you live in."},
    {"key": "ev",          "label": "Car buyer / EV driver",              "blurb": "Buying a clean vehicle or installing a charger."},
    {"key": "homebuilder", "label": "Home builder",                       "blurb": "Building or substantially reconstructing homes to sell or lease."},
    {"key": "commercial",  "label": "Commercial building owner or designer","blurb": "Owning, developing, or designing commercial buildings."},
    {"key": "fleet",       "label": "Business fleet operator",            "blurb": "Buying electric or fuel-cell commercial vehicles."},
    {"key": "utility",     "label": "Utility-scale power developer",      "blurb": "Developing grid-scale generation or storage."},
    {"key": "industrial",  "label": "Industrial facility / manufacturer", "blurb": "Manufacturing components or decarbonizing an industrial site."},
    {"key": "fuels",       "label": "Clean fuel or hydrogen producer",    "blurb": "Producing clean hydrogen or low-carbon transportation fuel."},
    {"key": "carbon",      "label": "Carbon capture operator",            "blurb": "Capturing and storing or using CO\u2082."},
]

# kind: "credit" (federal tax credit/deduction) or "program" (grant/rebate/loan program)
# deadline_date: the operative near-term cutoff (ISO) used to compute days-left; null if no near deadline.
items = [
    {
        "code": "25C", "name": "Energy Efficient Home Improvement Credit", "kind": "credit",
        "sector": "Buildings", "personas": ["homeowner"],
        "value": "30% of project costs, up to $3,200 per year",
        "ira_end": 2032, "obbba_end": 2025, "status": "Repealed early",
        "deadline_label": "Ends Dec 31, 2025", "deadline_date": "2025-12-31",
        "eligibility": "Homeowners making qualifying efficiency upgrades to an existing primary U.S. home \u2014 insulation, air sealing, exterior doors and windows, heat pumps, and home energy audits. Claimed on your federal return for the year the improvement is placed in service.",
        "notes": "No credit for property placed in service after Dec 31, 2025.",
    },
    {
        "code": "25D", "name": "Residential Clean Energy Credit", "kind": "credit",
        "sector": "Buildings", "personas": ["homeowner"],
        "value": "30% of system cost, no dollar cap",
        "ira_end": 2034, "obbba_end": 2025, "status": "Repealed early",
        "deadline_label": "Ends Dec 31, 2025", "deadline_date": "2025-12-31",
        "eligibility": "Homeowners installing rooftop solar, battery storage (3 kWh+), solar water heating, geothermal heat pumps, or small wind at a U.S. residence. Credit equals 30% of installed cost.",
        "notes": "System must be installed and placed in service by Dec 31, 2025.",
    },
    {
        "code": "25E", "name": "Previously Owned Clean Vehicle Credit", "kind": "credit",
        "sector": "Transport", "personas": ["ev"],
        "value": "Up to $4,000 (30% of sale price)",
        "ira_end": 2032, "obbba_end": 2025, "status": "Repealed early",
        "deadline_label": "Ended Sep 30, 2025", "deadline_date": "2025-09-30",
        "eligibility": "Buyers of a qualifying used EV or plug-in hybrid (at least 2 model years old, sale price \u2264 $25,000) purchased from a dealer, with income under $75k single / $150k joint. One credit per buyer every three years.",
        "notes": "Per IRS guidance, the vehicle must be 'acquired' \u2014 a written binding contract plus a payment \u2014 on or before Sep 30, 2025. It may be placed in service later and the credit still applies.",
    },
    {
        "code": "30C", "name": "Alternative Fuel Vehicle Refueling Property Credit", "kind": "credit",
        "sector": "Transport infrastructure", "personas": ["ev", "fleet", "commercial"],
        "value": "6\u201330% of cost; up to $1,000 (home) or $100,000 (business)",
        "ira_end": 2032, "obbba_end": 2026, "status": "Repealed early",
        "deadline_label": "Ends Jun 30, 2026", "deadline_date": "2026-06-30",
        "eligibility": "Homeowners and businesses installing EV chargers or alternative-fuel dispensers in eligible (low-income or non-urban) census tracts. 30% for businesses meeting wage and apprenticeship rules; capped at $1,000 for homeowners.",
        "notes": "Property must be placed in service by Jun 30, 2026.",
    },
    {
        "code": "30D", "name": "New Clean Vehicle Credit", "kind": "credit",
        "sector": "Transport", "personas": ["ev"],
        "value": "Up to $7,500",
        "ira_end": 2032, "obbba_end": 2025, "status": "Repealed early",
        "deadline_label": "Ended Sep 30, 2025", "deadline_date": "2025-09-30",
        "eligibility": "Buyers of a qualifying new EV or plug-in hybrid meeting battery-sourcing and final-assembly rules, under MSRP caps ($55k cars / $80k SUVs and trucks) and income caps ($150k single / $300k joint).",
        "notes": "Per IRS guidance, the vehicle must be 'acquired' \u2014 a written binding contract plus a payment \u2014 on or before Sep 30, 2025. It may be placed in service later and the credit still applies.",
    },
    {
        "code": "45L", "name": "New Energy Efficient Home Credit", "kind": "credit",
        "sector": "Buildings", "personas": ["homebuilder"],
        "value": "$2,500\u2013$5,000 per home",
        "ira_end": 2032, "obbba_end": 2026, "status": "Repealed early",
        "deadline_label": "Ends Jun 30, 2026", "deadline_date": "2026-06-30",
        "eligibility": "Eligible contractors who build or substantially reconstruct qualifying ENERGY STAR or Zero Energy Ready homes that are then sold or leased as a residence. Claimed by the builder, not the buyer.",
        "notes": "Home must be acquired by Jun 30, 2026.",
    },
    {
        "code": "45Q", "name": "Carbon Oxide Sequestration Credit", "kind": "credit",
        "sector": "Industry", "personas": ["carbon", "industrial", "utility"],
        "value": "Up to $85/ton stored ($180/ton direct air capture)",
        "ira_end": 2033, "obbba_end": 2033, "status": "Improved",
        "deadline_label": "Runway through 2033", "deadline_date": None,
        "eligibility": "Owners of qualified carbon-capture equipment at industrial or power facilities, and direct-air-capture projects, that capture and durably store or use CO\u2082. OBBBA raised the utilization / enhanced-oil-recovery rate to $85/ton to match geologic storage.",
        "notes": "Largely preserved and improved. New: FEOC (foreign-entity-of-concern) restrictions apply \u2014 supply-chain diligence is now a qualifying requirement.",
    },
    {
        "code": "45U", "name": "Zero-Emission Nuclear Power Production Credit", "kind": "credit",
        "sector": "Power", "personas": ["utility"],
        "value": "Up to 1.5\u00a2/kWh",
        "ira_end": 2032, "obbba_end": 2032, "status": "Preserved",
        "deadline_label": "Runway through 2032", "deadline_date": None,
        "eligibility": "Owners of existing zero-emission nuclear plants, paid per kWh of electricity produced and sold. Bonus rate requires prevailing-wage compliance.",
        "notes": "Largely unchanged through 2032. FEOC restrictions now apply.",
    },
    {
        "code": "45V", "name": "Clean Hydrogen Production Credit", "kind": "credit",
        "sector": "Industry", "personas": ["fuels", "industrial"],
        "value": "Up to $3.00/kg",
        "ira_end": 2032, "obbba_end": 2027, "status": "Shortened",
        "deadline_label": "Begin construction by Dec 31, 2027", "deadline_date": "2027-12-31",
        "eligibility": "Producers of clean hydrogen at facilities meeting lifecycle carbon-intensity tiers. The full $3.00/kg requires the lowest carbon-intensity tier plus prevailing-wage and apprenticeship compliance.",
        "notes": "Construction must begin by Dec 31, 2027 (shortened from 2032).",
    },
    {
        "code": "45W", "name": "Commercial Clean Vehicle Credit", "kind": "credit",
        "sector": "Transport", "personas": ["fleet"],
        "value": "Up to $7,500 (\u2264 14k lb) or $40,000 (heavier)",
        "ira_end": 2032, "obbba_end": 2025, "status": "Repealed early",
        "deadline_label": "Ended Sep 30, 2025", "deadline_date": "2025-09-30",
        "eligibility": "Businesses and tax-exempt organizations buying qualifying electric or fuel-cell commercial vehicles. Credit is the lesser of 30% of cost or the incremental cost versus a comparable gas vehicle, capped by weight class.",
        "notes": "Per IRS guidance, the vehicle must be 'acquired' \u2014 a written binding contract plus a payment \u2014 on or before Sep 30, 2025. It may be placed in service later and the credit still applies.",
    },
    {
        "code": "45X", "name": "Advanced Manufacturing Production Credit", "kind": "credit",
        "sector": "Manufacturing", "personas": ["industrial"],
        "value": "Component-specific, per unit produced",
        "ira_end": 2032, "obbba_end": 2027, "status": "Mixed",
        "deadline_label": "Wind parts end 2027; others phase out 2030\u201332", "deadline_date": "2027-12-31",
        "eligibility": "U.S. manufacturers producing eligible components \u2014 solar and wind parts, inverters, battery cells and modules, and critical minerals \u2014 sold to unrelated buyers. The credit amount varies by component.",
        "notes": "Wind components end 2027; others phase down 2030\u20132032. FEOC restrictions apply.",
    },
    {
        "code": "45Y", "name": "Clean Electricity Production Credit (tech-neutral PTC)", "kind": "credit",
        "sector": "Power", "personas": ["utility"],
        "value": "Up to 1.5\u00a2/kWh (+ bonus adders)",
        "ira_end": 2035, "obbba_end": 2027, "status": "Shortened",
        "deadline_label": "Wind/solar: begin construction by Jul 4, 2026", "deadline_date": "2026-07-04",
        "eligibility": "Owners of zero-emission generating facilities placed in service after 2024, paid per kWh produced. Full rate requires prevailing-wage and apprenticeship compliance; bonus adders for domestic content and energy communities.",
        "notes": "Wind & solar: beginning construction by Jul 4, 2026 locks in the credit with no placed-in-service deadline; projects that start later must instead be placed in service by Dec 31, 2027. (A June 6, 2026 federal court ruling vacated IRS Notice 2025-42, restoring the 5% safe harbor for proving construction start \u2014 this may be appealed.) Other technologies keep a longer runway through 2034+.",
    },
    {
        "code": "45Z", "name": "Clean Fuel Production Credit", "kind": "credit",
        "sector": "Industry / fuels", "personas": ["fuels"],
        "value": "Up to $1.00/gal ($1.75/gal sustainable aviation fuel)",
        "ira_end": 2027, "obbba_end": 2029, "status": "Extended",
        "deadline_label": "Extended through 2029", "deadline_date": None,
        "eligibility": "Producers of low-emission transportation fuel, including sustainable aviation fuel, at U.S. facilities. The credit scales with the fuel's carbon-intensity score.",
        "notes": "Extended to 2029. Feedstock restricted to U.S./Canada/Mexico; negative emissions rates disallowed.",
    },
    {
        "code": "48E", "name": "Clean Electricity Investment Credit (tech-neutral ITC)", "kind": "credit",
        "sector": "Power", "personas": ["utility", "commercial"],
        "value": "6\u201330% of project cost (+ bonus adders)",
        "ira_end": 2035, "obbba_end": 2027, "status": "Shortened",
        "deadline_label": "Wind/solar: begin construction by Jul 4, 2026", "deadline_date": "2026-07-04",
        "eligibility": "Owners of zero-emission generation or storage projects, claimed as a percent of capital cost. 30% base with wage/apprenticeship compliance; +10% domestic content; +10% energy community; +10\u201320% low-income.",
        "notes": "Wind & solar: beginning construction by Jul 4, 2026 locks in the credit with no placed-in-service deadline; projects that start later must instead be placed in service by Dec 31, 2027. (A June 6, 2026 federal court ruling vacated IRS Notice 2025-42, restoring the 5% safe harbor for proving construction start \u2014 this may be appealed.) Storage and other technologies keep runway to 2035.",
    },
    {
        "code": "179D", "name": "Energy Efficient Commercial Buildings Deduction", "kind": "credit",
        "sector": "Buildings", "personas": ["commercial"],
        "value": "$0.50\u2013$5.00 per square foot",
        "ira_end": 2032, "obbba_end": 2026, "status": "Repealed early",
        "deadline_label": "Begin construction by Jun 30, 2026", "deadline_date": "2026-06-30",
        "eligibility": "Owners (or designers of government and tax-exempt buildings) that cut a building's energy use by at least 25% versus baseline. This is a deduction, not a credit; the higher rate requires prevailing-wage compliance.",
        "notes": "Construction must begin by Jun 30, 2026.",
    },
    # --- Non-tax programs (rebates / grants / loans) ---
    {
        "code": "HOMES + HEAR", "name": "Home Energy Rebates", "kind": "program",
        "sector": "Buildings", "agency": "U.S. Dept. of Energy", "personas": ["homeowner"],
        "value": "Up to $8,000 (HOMES) / $14,000 (HEAR appliances)",
        "ira_end": 2031, "obbba_end": 2031, "status": "Active",
        "deadline_label": "Active in participating states through ~2031", "deadline_date": None,
        "eligibility": "Income-qualified households in participating states. HOMES rebates whole-home efficiency retrofits by energy savings; HEAR (HEEHRA) gives point-of-sale rebates for heat pumps, heat-pump water heaters, electric stoves, panels, and wiring. Administered by your state energy office.",
        "notes": "NOT repealed by OBBBA \u2014 funded through ~mid-2031. Availability depends on your state launching its program. With 25C/25D gone, this is often the main remaining federal residential tool, and it is frequently stackable with state and utility rebates.",
    },
    {
        "code": "Clean HDV", "name": "Clean Heavy-Duty Vehicles Program", "kind": "program",
        "sector": "Transport", "agency": "EPA", "personas": ["fleet"],
        "value": "Grants & rebates (largely curtailed)",
        "ira_end": 2031, "obbba_end": 2025, "status": "Rescinded",
        "deadline_label": "Unobligated funds clawed back", "deadline_date": "2025-07-04",
        "eligibility": "Was open to fleets, school districts, and transit operators deploying zero-emission heavy-duty vehicles.",
        "notes": "OBBBA rescinded unobligated funds. Compounds the loss of the 45W commercial-vehicle credit. Shown for context \u2014 generally not actionable for new applicants.",
    },
    {
        "code": "AIFDP", "name": "Advanced Industrial Facilities Deployment Program", "kind": "program",
        "sector": "Industry", "agency": "U.S. Dept. of Energy", "personas": ["industrial"],
        "value": "Grants (rescinded)",
        "ira_end": 2031, "obbba_end": 2025, "status": "Rescinded",
        "deadline_label": "Unobligated funds clawed back", "deadline_date": "2025-07-04",
        "eligibility": "Was open to industrial facilities (steel, cement, chemicals) adopting technologies to cut greenhouse-gas emissions.",
        "notes": "OBBBA rescinded all unobligated funds. Shown for context \u2014 tax credits such as 45Q remain the primary federal lever for industrial decarbonization.",
    },
    {
        "code": "Title 17 / EDFP", "name": "DOE Loan Programs Office", "kind": "program",
        "sector": "Energy finance", "agency": "U.S. Dept. of Energy", "personas": ["utility", "industrial"],
        "value": "Loan guarantees (restructured, ~75% cut)",
        "ira_end": 2031, "obbba_end": 2026, "status": "Restructured",
        "deadline_label": "Restructured \u2014 no longer clean-energy-first", "deadline_date": None,
        "eligibility": "Federal loan guarantees for energy and infrastructure projects. The 1706 program was renamed 'Energy Dominance Financing' with the emissions mandate removed and eligibility expanded to fossil, nuclear, critical minerals, and grid-reliability projects.",
        "notes": "OBBBA rescinded ~$8.4B in credit subsidies. Existing committed loans preserved. Shown for context \u2014 still a financing avenue, but reoriented away from decarbonization.",
    },
]

data = {"meta": meta, "personas": personas, "items": items}

# --- Per-credit source citations (verified June 2026) ---
# Default date the figures were last checked against the cited sources.
# Override per item by adding a "verified": "YYYY-MM-DD" key to that item.
VERIFIED = "2026-06-24"
IRS_FAQ = ("https://www.irs.gov/newsroom/faqs-for-modification-of-sections-25c-25d-25e-30c-30d-45l-45w-and-179d-under-public-law-119-21-139-stat-72-july-4-2025-commonly-known-as-the-one-big-beautiful-bill-obbb",
           "IRS Fact Sheet 2025-5 (FAQs)")
AP        = ("https://www.arnoldporter.com/en/perspectives/advisories/2025/07/from-ira-to-obbba-a-new-era-for-clean-energy-tax-credits",
           "Arnold & Porter: IRA to OBBBA")
RSM       = ("https://rsmus.com/insights/services/business-tax/obbba-tax-clean-energy.html",
           "RSM: OBBBA clean energy changes")
MCGUIRE   = ("https://www.mcguirewoods.com/client-resources/alerts/2026/6/federal-court-vacates-irs-notice-2025-42-restores-5-safe-harbor-for-wind-and-solar-projects/",
           "McGuireWoods (Jun 2026): beginning-of-construction ruling")
DOE       = ("https://www.energy.gov/save/home-upgrades",
           "U.S. Dept. of Energy: Home Energy Rebates")

SOURCES = {
    "25C": IRS_FAQ, "25D": IRS_FAQ, "25E": IRS_FAQ, "30C": IRS_FAQ, "30D": IRS_FAQ,
    "45L": IRS_FAQ, "45W": IRS_FAQ, "179D": IRS_FAQ,
    "45Q": RSM, "45U": RSM, "45Z": RSM,
    "45V": AP, "45X": AP,
    "45Y": MCGUIRE, "48E": MCGUIRE,
    "HOMES + HEAR": DOE,
    # Context-only programs are clearly labeled in-card; no specific citation linked.
}
for it in items:
    url, label = SOURCES.get(it["code"], (None, None))
    it["source_url"] = url
    it["source_label"] = label
    it["verified"] = it.get("verified", VERIFIED)

import re
root = pathlib.Path(__file__).parent
(root / "data").mkdir(exist_ok=True)

# 1) Raw data for programmatic reuse
(root / "data" / "credits.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))

# 2) Inject the data block into the self-contained index.html (between markers)
data_js = "window.CE_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";"
index_path = root / "index.html"
html = index_path.read_text()
block = ("/* CE_DATA_START \u2014 generated by build_data.py; do not edit by hand */\n"
         + data_js + "\n/* CE_DATA_END */")
new_html, n = re.subn(
    r"/\* CE_DATA_START.*?CE_DATA_END \*/",
    lambda m: block, html, flags=re.S)
if n != 1:
    raise SystemExit("Could not find the CE_DATA markers in index.html — "
                     "make sure the /* CE_DATA_START */ ... /* CE_DATA_END */ block is intact.")
index_path.write_text(new_html)
print("wrote", len(items), "items into data/credits.json and index.html")
