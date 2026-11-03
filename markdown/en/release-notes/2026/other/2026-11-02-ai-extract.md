# Nov 02, 2026: AI\_EXTRACT updates (Public Preview)

AI\_EXTRACT now delivers a **12.8% relative improvement in average extraction accuracy** compared with the previous version in our evaluations. Extract fields, lists, and tables more accurately from complex documents, including forms, handwritten content, dense tables, and charts.

With cross-region inference enabled, these improvements apply automatically—with **no SQL changes and no change in price.**

This update includes:

- **8× higher document page limit:** Extract from documents with up to 1,000 pages, up from 125 pages.
- **More reliable multi-field extraction:** AI\_EXTRACT handles requests with many fields more robustly and returns one combined result.
- **`scale_factor` no longer needed:** AI\_EXTRACT now delivers improved extraction quality without manual scaling adjustments. Existing calls continue to work unchanged; any `scale_factor` value is ignored.

Cross-region inference is required to receive this update. Without it, AI\_EXTRACT continues to use the previous version.

For more information, see [AI\_EXTRACT](/sql-reference/functions/ai_extract).
