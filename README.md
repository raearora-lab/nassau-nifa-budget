# Nassau County Budget vs NIFA, 2017–2026

Static site comparing Nassau County's Major Funds budgets and tax levy with the Nassau County Interim Finance Authority's (NIFA) reviews, FY2017–FY2027: latest news, upcoming NIFA/Legislature meetings, NIFA's seven FY2027 recommendations, every figure NIFA cites (with document and page), conclusions with derived levy math, a ten-year chart and data downloads.

- Live: https://nassau-nifa-budget.pages.dev/ (canonical: https://whorunsny.org/nifa/)
- Build: `python3 scripts/build.py` (content in `scripts/data.py`) writes `public/index.html`; `python3 scripts/og.py` writes `public/og.png`.
- Deploy: GitHub Actions (`.github/workflows/deploy.yml`) runs `wrangler pages deploy public` to Cloudflare Pages project `nassau-nifa-budget` on every push to `main`. Needs repo secrets `CLOUDFLARE_API_KEY` and `CLOUDFLARE_EMAIL`.

Last updated Nov 14, 2026.
