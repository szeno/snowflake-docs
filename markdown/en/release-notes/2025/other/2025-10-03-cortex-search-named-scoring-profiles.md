# Oct 03, 2025: Named scoring profiles for Cortex Search Services (*General availability*)

Cortex Search Services now support *named scoring profiles*, which allow you to save and reuse scoring configurations
when querying a Cortex Search Service. A scoring configuration consists of optional boost and decay functions, as
well as an optional reranker setting.

Using a named scoring profile lets you easily use a scoring configuration across applications and queries without having
to specify the full scoring configuration each time. If you change the scoring configuration, you only need to update it
in one place, not in every query.

For more information about named scoring profiles, see [Named scoring profiles](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-named-scoring-profiles).
