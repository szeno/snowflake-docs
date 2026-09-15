# Aug 3, 2026: Inline Stored Procedures for hybrid tables (*Public preview*)

Inline Stored Procedures for hybrid tables are now available in public preview. Inline Stored Procedures are a new type of Snowflake stored procedure designed for operational workloads on hybrid tables. The entire procedure body runs as a single atomic unit pushed directly to the query processing layer, which reduces per-statement overhead and delivers significantly lower latency for OLTP-style workloads.

This preview is available on any Snowflake account and warehouse. For the best performance, set the `ENABLE_USE_STABLE_PATH` parameter to `TRUE` on the warehouse that runs your Inline Stored Procedures.

For more information, see [Inline Stored Procedures for hybrid tables](/user-guide/hybrid-tables-inline-stored-procedures).
