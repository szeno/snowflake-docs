# Jul 30, 2026: Adaptive refresh mode for dynamic tables (*General availability*)

ADAPTIVE refresh mode for dynamic tables is now generally available.

ADAPTIVE refresh uses incremental refresh by default but automatically reinitializes the dynamic table
when internal heuristics detect that the volume of upstream changes makes an incremental refresh
significantly more expensive than a full refresh. After reinitialization, incremental refreshes resume.

Use ADAPTIVE refresh mode as your preferred refresh mode for all incremental workloads.

For more information, see [ADAPTIVE refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-adaptive).
