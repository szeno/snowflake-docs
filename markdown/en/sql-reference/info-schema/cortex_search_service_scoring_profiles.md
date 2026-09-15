# CORTEX\_SEARCH\_SERVICE\_SCORING\_PROFILES view

This Information Schema view displays a row for each Cortex Search Service named scoring profile in the current or specified database.

For more information about named scoring profiles, see [Named scoring profiles](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-named-scoring-profiles).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SERVICE\_CATALOG | VARCHAR | The database in which the service is defined. |
| SERVICE\_SCHEMA | VARCHAR | The schema in which the service is defined. |
| SERVICE\_NAME | VARCHAR | The name of the search service to which the profile belongs. |
| PROFILE\_NAME | VARCHAR | The name of the scoring profile. |
| SCORING\_PROFILE | VARCHAR | The scoring profile configuration as a JSON-format string. |

Expand

Show lessSee more

## Example

The following statement lists the named scoring profiles that are in the current database.

Copy code

```
SELECT * FROM INFORMATION_SCHEMA.CORTEX_SEARCH_SERVICE_SCORING_PROFILES;
```
