# Oct 12, 2026: LISTING\_ACCESS\_HISTORY improvements (*General availability*)

Predicate-level detail and query types in the `LISTING_ACCESS_HISTORY` view are now generally available.
These improvements help listing providers understand how consumers query their shared data:

- The `QUERY_TYPE` column identifies supported consumer query types, including data unloads.
- The `SHARE_OBJECTS_ACCESSED` column includes `groupByObjects`, `aggregateObjects`, and `filterObjects`
  arrays that identify columns used for grouping, aggregation, and filtering. For date and timestamp columns,
  filter details also include predicate values so providers can analyze how far back consumers query their data.

For more information, see [LISTING\_ACCESS\_HISTORY view](/sql-reference/data-sharing-usage/listing-access-history).
