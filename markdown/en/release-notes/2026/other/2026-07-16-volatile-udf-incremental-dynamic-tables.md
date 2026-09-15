# July 16, 2026: VOLATILE scalar UDFs are supported with dynamic table incremental refresh (*General availability*)

VOLATILE scalar user-defined functions (UDFs) are now supported with dynamic table incremental refresh in INCREMENTAL,
AUTO, and ADAPTIVE refresh modes. This applies to scalar UDFs written in Python, Java, Scala, JavaScript, and SQL.
For incremental refresh, VOLATILE UDFs are supported only in the SELECT clause.

For a complete list of supported queries and functions, see [Supported queries for dynamic tables](/user-guide/dynamic-tables/supported-queries).
