# May 26, 2026: Custom incremental dynamic tables (*Public Preview*)

When standard refresh modes don’t support your transformation pattern,
`CUSTOM_INCREMENTAL` refresh mode lets you write MERGE or INSERT logic that Snowflake executes on each refresh.
You define exactly how changes reach the dynamic table while Snowflake handles scheduling, retries,
and transactional guarantees. This mode supports patterns such as stream-static joins, soft-deletes,
stateful aggregation, and direct migration from streams and tasks.

For more information, see [Custom incrementalization](/user-guide/dynamic-tables/custom-incrementalization).
