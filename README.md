# Stock Intrinsic Value Calculator

A multi-model stock valuation tool that blends four approaches with conditional weighting:

- **DCF** — Discounted Cash Flow (5-year projection + terminal value)
- **DDM** — Dividend Discount Model (Gordon Growth)
- **P/E Multiple** — Forward earnings × target multiple
- **Graham Number** — Benjamin Graham's defensive value

## Deploy to GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages**
3. Under **Source**, select **Deploy from a branch**
4. Choose **main** branch and **/ (root)** folder
5. Click **Save**
6. Your app will be live at `https://<username>.github.io/<repo-name>/`

No build step needed — it's a single `index.html`.

## Original Python Script

The standalone CLI version is included as [`stock_valuator.py`](stock_valuator.py):

```bash
python stock_valuator.py
```

## Disclaimer

This is an educational tool, not financial advice.
