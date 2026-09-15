# May 26, 2026: Adaptive refresh mode for dynamic tables (*Public Preview*)

Dynamic tables now support a new refresh mode: `REFRESH_MODE = ADAPTIVE`.

ADAPTIVE refresh uses incremental refresh by default but automatically reinitializes the dynamic table
when internal heuristics detect that the volume of upstream changes makes an incremental refresh
significantly more expensive than a full refresh. After reinitialization, incremental refreshes resume.

This mode is ideal for workloads where base tables normally receive small changes
but occasionally undergo bulk loads (for example, INSERT OVERWRITE).

For more information, see [ADAPTIVE refresh](/user-guide/dynamic-tables/refresh-modes#label-dynamic-tables-refresh-adaptive).
