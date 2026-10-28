# Sep 18, 2026: Directed joins: Set the scan order with FIRST or LAST (*General availability*)

With this release, the read-order clause for directed joins is generally available. You can set which side of a
directed join is scanned first without rewriting the order of the tables in the `FROM` clause. After the `ON` or
`USING` clause, add `FIRST( alias )` to scan that table first, or
`LAST( alias )` to scan that table last.

This is most useful when you want to set the scan order of one join in a chain of joins. The join must include the
`DIRECTED` keyword.

For more information, see [the read-order clause](/sql-reference/constructs/join#label-join-read-order).
