# Stock Intrinsic Value Calculator

A multi-model stock valuation tool that blends four approaches with conditional weighting:

- **DCF** — Discounted Cash Flow (5-year projection + terminal value)
- **DDM** — Dividend Discount Model (Gordon Growth)
- **P/E Multiple** — Forward earnings × target multiple
- **Graham Number** — Benjamin Graham's defensive value

Models are automatically enabled/disabled based on the stock's characteristics (dividend payer, sector, earnings sign) and weights are renormalized accordingly.

## Features

- Real-time recalculation as you adjust inputs
- Margin of Safety indicator
- DCF breakdown (projected vs terminal value)
- Sensitivity analysis (discount rate × FCF growth matrix)
- Active rules display showing which models are engaged

## Development

```bash
npm install
npm run dev
```

## Deploy to GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source** and select **GitHub Actions**
3. The included workflow (`.github/workflows/deploy.yml`) will auto-deploy on every push to `main`
4. Your app will be live at `https://<username>.github.io/stock-valuator/`

> **Important:** If your repo name is not `stock-valuator`, update the `base` field in `vite.config.js` to match: `base: '/your-repo-name/'`

## Disclaimer

This is an educational tool, not financial advice.
