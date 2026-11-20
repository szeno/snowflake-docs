# Nov 20, 2026: AUTO refresh mode for dynamic tables resolves to ADAPTIVE

When you create a dynamic table with `REFRESH_MODE = AUTO` (the default), Snowflake now resolves
the refresh mode to ADAPTIVE instead of INCREMENTAL when the definition supports incremental refresh.
If the definition isn’t compatible with incremental refresh, AUTO still resolves to FULL.

Existing dynamic tables aren’t affected. Tables already created with AUTO keep their previously
resolved refresh mode.

To use INCREMENTAL refresh without adaptive reinitialization, set `REFRESH_MODE = INCREMENTAL`
explicitly.

For more information, see [AUTO refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-auto).
