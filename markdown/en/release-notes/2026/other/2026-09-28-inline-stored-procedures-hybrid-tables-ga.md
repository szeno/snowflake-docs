# Sep 28, 2026: Inline Stored Procedures for hybrid tables (*General availability*)

With this release, Inline Stored Procedures for hybrid tables are generally available. Inline Stored Procedures are a type of Snowflake stored procedure designed for operational workloads on hybrid tables. The entire procedure body runs as a single atomic unit pushed directly to the query processing layer, which reduces per-statement overhead and delivers significantly lower latency for OLTP-style workloads.

For more information, see [Inline Stored Procedures for hybrid tables](/user-guide/hybrid-tables-inline-stored-procedures).
