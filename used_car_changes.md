# Used Car EDA Dashboard — Changes Report

## Bug Fixes

| Bug | Cause | Fix | Status |
|---|---|---|---|
| Crash on `px.scatter(..., trendline="ols")` | `statsmodels` not installed; OLS trendline requires extra dependency | Removed `trendline="ols"` and added explicit chart title | Fixed |

## UI Redesign & Visualization Enhancement

**Palette chosen:** Scheme A — Modern Automotive Dark
- Background: `#0f172a`
- Secondary background: `#1e293b`
- Primary/accent: `#38bdf8`
- Text: `#f8fafc`
- Highlight: `#22d3ee`

**Files changed:**
- `.streamlit/config.toml` — added theme with Modern Automotive Dark palette
- `streamlit_app.py` — full layout redesign with notebook-inspired insights
- `used_car_changes.md` — this report

**Layout and visualization updates:**
- Added `@st.cache_data` for data loading
- Engineered features from raw dataset: `Max Power bhp`, `Max Power rpm`, `Max Torque Nm`, `Max Torque rpm`, `Age of Car`, `Volume`
- Restructured into tabs: **Overview / Analysis / Details**
- KPI cards with `st.metric` in responsive columns
- New visualizations based on notebook EDA:
  - Average Price by Brand
  - Average Price by Fuel Type
  - Top 5 Most Economical Brands
  - Price vs Mileage bubble chart with `Age of Car` as size
  - Average Price Trend Over Years (line chart)
  - Economical Brands Price Trend (multi-line)
  - Volume vs Price by Transmission
  - Correlation Heatmap
  - Listings by City
- Replaced deprecated `use_container_width=True` with `width="stretch"`
- Added footer with data source attribution

**Data logic preserved:**
- CSV path unchanged: `20251115_CarLoop_Dataset.csv`
- All preprocessing and feature engineering applied in code
- Charts use the same filtered dataset with consistent dark theme styling

## Verification

- `python -m py_compile streamlit_app.py` — passed
- Streamlit runtime — not available in local environment; verify on Streamlit Cloud after deployment
- Bug check: `trendline="ols"` removed — no longer triggers `statsmodels` import error

## Manual Checks

- Open deployed app and verify dark theme renders correctly
- Check chart readability on dark background
- Test filters in sidebar across all tabs
- Confirm KPI cards update when filters change
- Verify engineered features display correctly in Analysis tab
