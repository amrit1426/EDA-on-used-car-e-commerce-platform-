# Used Car EDA Dashboard — Changes Report

## Bug Fixes

| Bug | Cause | Fix | Status |
|---|---|---|---|
| Crash on `px.scatter(..., trendline="ols")` | `statsmodels` not installed; OLS trendline requires extra dependency | Removed `trendline="ols"` and added explicit chart title | Fixed |

## UI Redesign

**Palette chosen:** Scheme A — Modern Automotive Dark
- Background: `#0f172a`
- Secondary background: `#1e293b`
- Primary/accent: `#38bdf8`
- Text: `#f8fafc`
- Highlight: `#22d3ee`

**Files changed:**
- `.streamlit/config.toml` — added theme with Modern Automotive Dark palette
- `streamlit_app.py` — full layout redesign

**Layout changes:**
- Added `@st.cache_data` for data loading
- Restructured into tabs: Overview / Analysis / Details
- KPIs wrapped in `st.columns(3)` with `st.metric`
- All charts updated with dark-theme-friendly Plotly layout (`paper_bgcolor`, `plot_bgcolor`, grid colors)
- Replaced deprecated `use_container_width=True` with `width="stretch"`
- Added footer with data source attribution

**Data logic preserved:**
- CSV path unchanged: `20251115_CarLoop_Dataset.csv`
- Filter logic unchanged
- All charts use the same filtered dataset

## Verification

- `python -m py_compile streamlit_app.py` — passed
- Streamlit runtime — not available in local environment; verify on Streamlit Cloud after deployment
- Bug check: `trendline="ols"` removed — no longer triggers `statsmodels` import error

## Manual Checks

- Open deployed app and verify dark theme renders correctly
- Check chart readability on dark background
- Test filters in sidebar across all tabs
- Confirm KPI cards update when filters change
