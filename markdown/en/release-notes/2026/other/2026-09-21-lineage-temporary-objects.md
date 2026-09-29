# Sep 21, 2026: Lineage preservation through temporary tables and views (*General availability*)

[Preserving data lineage through temporary tables and views](/user-guide/lineage-temporary-objects) is now generally
available.

Many pipelines use temporary tables and views as intermediate steps. After those objects are dropped, either explicitly
or automatically at the end of a session, Snowflake now preserves the lineage between their upstream sources and
downstream tables when the temporary object is a genuine bridge (it has both an upstream source and a downstream table),
at both the object and column levels. Lineage graphs in Snowsight and results from
[GET\_LINEAGE](/sql-reference/functions/get_lineage-snowflake-core) continue to show how data moved, even after the
intermediate temporary objects are gone.

This feature requires Enterprise Edition (or higher).

For more information, see [Preserving data lineage through temporary tables and views](/user-guide/lineage-temporary-objects).
