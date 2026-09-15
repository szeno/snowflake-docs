# Mar 13, 2026: Time distribution information added to STATISTICS column in dynamic table refresh history

The STATISTICS column in [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) and
[DYNAMIC\_TABLE\_REFRESH\_HISTORY view](/sql-reference/account-usage/dynamic_table_refresh_history) now includes time distribution information for
dynamic table refreshes. The following new properties are added:

- `queuedTimeMs`: The time (in milliseconds) spent in the queued state.
- `compilationTimeMs`: The time (in milliseconds) spent compiling the refresh query.
- `executionTimeMs`: The time (in milliseconds) spent executing the refresh query.

For successful refreshes, the STATISTICS column includes both the existing row/partition statistics and the new time
distribution information. For example:

Copy code

```
{
  "numAddedPartitions": 1,
  "numCopiedRows": 0,
  "numDeletedRows": 25,
  "numInsertedRows": 36,
  "numRemovedPartitions": 1,
  "queuedTimeMs": 123,
  "compilationTimeMs": 456,
  "executionTimeMs": 789
}
```

For failed refreshes, the STATISTICS column is now populated with the time distribution information (previously it
defaulted to an empty object). For example:

Copy code

```
{
  "queuedTimeMs": 123,
  "compilationTimeMs": 456,
  "executionTimeMs": 789
}
```

For more information, see [DYNAMIC\_TABLE\_REFRESH\_HISTORY](/sql-reference/functions/dynamic_table_refresh_history) (Information Schema) and
[DYNAMIC\_TABLE\_REFRESH\_HISTORY view](/sql-reference/account-usage/dynamic_table_refresh_history) (Account Usage).
