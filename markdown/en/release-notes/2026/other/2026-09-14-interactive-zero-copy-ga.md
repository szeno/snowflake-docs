# Sep 14, 2026: Zero-copy support for all table formats in interactive warehouses (*General availability*)

Support for all table formats in [interactive warehouses](/user-guide/interactive) is now generally
available and is no longer in [Preview](/release-notes/preview-features).

You can use interactive warehouses to query standard tables, dynamic tables, Iceberg tables, and
hybrid tables directly, without copying or transforming your data into interactive tables. This
zero-copy approach lets you benefit from the low-latency, high-concurrency performance
characteristics of interactive warehouses on your existing data.

For more information, see [Using standard and Iceberg tables](/user-guide/interactive#label-zero-copy-interactive-analytics) with interactive analytics.
