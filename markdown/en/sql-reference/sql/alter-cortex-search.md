# ALTER CORTEX SEARCH SERVICE

Suspends, resumes, or modifies the properties of an existing [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview).

## Syntax

Copy code

```
ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name>
  { SUSPEND | RESUME } [ { INDEXING | SERVING } ]

ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name> REFRESH

ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name> SET
  [ TARGET_LAG = { '<num> { seconds | minutes | hours | days }' } ]
  [ WAREHOUSE = <warehouse_name> ]
  [ PRIMARY KEY = ( <col_name> [, ... ] ) ]
  [ FULL_INDEX_BUILD_INTERVAL_DAYS = <num> ]
  [ REQUEST_LOGGING = { TRUE | FALSE } ]
  [ AUTO_SUSPEND = { <num_seconds> | NULL } ]
  [ COMMENT = '<string_literal>' ]

ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name> UNSET
  [ PRIMARY KEY ]

ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name> SET ATTRIBUTES ( <col_name> [, ... ] )

ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name> UNSET ATTRIBUTES

ALTER CORTEX SEARCH SERVICE <name>
  ADD SCORING PROFILE [ IF NOT EXISTS ] <profile_name>
  <scoring_profile>

ALTER CORTEX SEARCH SERVICE <name>
  DROP SCORING PROFILE [ IF EXISTS ] <profile_name>

ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER CORTEX SEARCH SERVICE [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Specifies the identifier for the Cortex Search service to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`{ SUSPEND | RESUME } ...`
:   Suspends or resumes the indexing, serving, or both for a Cortex Search service. You can specify one of the following keywords to indicate
    which layer to suspend or resume:

    `INDEXING`
    :   The target that indicates the indexing layer of the Cortex Search Service. For more details, see [Usage Notes](#label-cortex-search-usage-notes).

    `SERVING`
    :   The target that indicates the serving layer of the Cortex Search Service. For more details, see [Usage Notes](#label-cortex-search-usage-notes).

        If you do not specify either keyword, both the indexing and serving layers are suspended or resumed. The OPERATE privilege is required to suspend or resume a Cortex Search service.

        To suspend serving automatically after a period of inactivity instead of manually, use the
        `AUTO_SUSPEND` property described in the SET clause below. For more information, see
        [Auto-suspend serving on inactivity](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-auto-suspend-serving).

`REFRESH`
:   Triggers a manual refresh of the Cortex Search Service. The indexing service immediately checks for changes to the source data and processes
    any new or changed rows.

`SET ...`
:   Sets one or more specified properties or parameters to set for the Cortex Search service:

    `TARGET_LAG = 'num { seconds | minutes | hours | days }'`
    :   Specifies the maximum amount of time that the Cortex Search service content should lag behind updates to the base tables specified in the source query.

    `WAREHOUSE = warehouse_name`
    :   Specifies the warehouse to use for running the source query, building the search index, and keeping it refreshed per the `TARGET_LAG` target.

    `FULL_INDEX_BUILD_INTERVAL_DAYS = num`
    :   Specifies the target interval, in days, between full index rebuilds for a Cortex Search service with
        [primary keys](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) defined. This property is only applicable to services that have primary keys set.

        Services with primary keys use an optimized refresh path where each refresh cycle (governed by `TARGET_LAG`) processes
        only the rows that changed since the last refresh, rather than re-embedding all data. Over time, these incremental
        updates accumulate fragmented index segments. A full index rebuild compacts these segments into a single optimized
        index. The rebuild does not re-embed unchanged data.

        This value is a soft target. Full index rebuilds may occur more frequently than the specified interval to optimize
        serving performance based on factors such as service target lag, change rate in the service source data, and overall
        service size.

    `REQUEST_LOGGING = \{ TRUE | FALSE \}`
    :   Enables or disables request logging for the Cortex Search Service. When enabled, the service records
        information about search requests, which you can query for monitoring and analysis purposes.
        For more information, see [Monitor Cortex Search requests](/user-guide/snowflake-cortex/cortex-search/cortex-search-monitor).

        Default: `FALSE`

    `AUTO_SUSPEND = { num_seconds | NULL }`
    :   Sets the number of seconds of query inactivity after which the service’s serving compute is
        automatically suspended. Affects serving only, not indexing. The service automatically resumes
        when it receives a query. Minimum: `1800` (30 minutes). Set to `NULL` to disable
        auto-suspend. For more information, see [Auto-suspend serving on inactivity](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-auto-suspend-serving).

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the search service.

    `PRIMARY KEY = (column_name, column_name, ...)`
    :   Modifies the set of [primary key columns](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) for the Cortex Search service.
        The combination of values in the designated columns must be unique for each row; rows with duplicate primary key
        values are ignored in the resulting search index. Primary key columns must be of the
        [TEXT](/sql-reference/data-types-text) data type. Changes to primary keys take effect after the next change
        to the source data.

`UNSET ...`
:   Unsets one or more specified properties or parameters for the Cortex Search service.

    `PRIMARY KEY`
    :   Removes any [primary key columns](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-primary-keys) that were previously set for the Cortex Search service.

`SET ATTRIBUTES (col_name [, ...])`
:   Specifies the attribute (filter) columns for the Cortex Search service. Attribute columns
    enable filtering search results using the `filter` parameter in search queries. Column
    names must be present in the service source query and cannot be of the OBJECT type.
    Changes take effect after the next index refresh, as determined by the `TARGET_LAG`
    setting and the presence of changes in the underlying source data. To apply changes
    immediately, trigger a manual refresh using `ALTER CORTEX SEARCH SERVICE ... REFRESH`.

`UNSET ATTRIBUTES`
:   Removes all attribute columns from the Cortex Search service. Changes take effect after
    the next index refresh, as determined by the `TARGET_LAG` setting and the presence of
    changes in the underlying source data. To apply changes immediately, trigger a manual
    refresh using `ALTER CORTEX SEARCH SERVICE ... REFRESH`.

`ADD SCORING PROFILE profile_name [ IF NOT EXISTS ] scoring_profile`
:   Adds a named scoring profile to the Cortex Search service. Scoring profiles define custom ranking behavior for search
    results. For more information, see [Named scoring profiles](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-named-scoring-profiles).

    `profile_name`
    :   Specifies the name of the scoring profile to add. If a profile with the specified name already exists, an error occurs unless
        you specify IF NOT EXISTS. To modify an existing profile, drop it using DROP SCORING PROFILE first.

    `scoring_profile`
    :   The scoring profile definition in JSON string format. The schema is the same as a scoring configuration specified directly in a search query
        using the `scoring_config` parameter. See [Numeric boosts and time decays](/user-guide/snowflake-cortex/cortex-search/cortex-search-customize-scoring#label-cortex-search-boosts-decays) for syntax and examples.

`DROP SCORING PROFILE [ IF EXISTS ] profile_name`
:   Drops a named scoring profile from the Cortex Search service.

    `profile_name`
    :   The name of the scoring profile to drop.

`SET TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' ... ]`
:   `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET TAG tag_name [ , tag_name ... ]`
:   Specifies one or more tags to unset on the Cortex Search service:

    - `tag_name [ , tag_name ... ]`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access Control Requirements

| Privilege | Object |
| --- | --- |
| OWNERSHIP | Cortex Search service you want to modify any properties on. |
| OPERATE | Cortex Search service you want to perform one of the following on:   - Suspend search indexing - Resume search indexing - Refresh search index - Set or change query warehouse - Set or change target lag |
| APPLY | Enables setting a tag on a Cortex Search service. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage Notes

Attention

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

### INDEXING and SERVING states

Cortex Search services have two distinct processes that can be in either the RUNNING or SUSPENDED state: INDEXING and SERVING.

- INDEXING is the target that indicates the indexing layer of the Cortex Search Service. When in the RUNNING state, changes in base tables
  referenced by the service’s source query will prompt refreshes of the materialized data stored as part of the search index. These
  refreshes incur cost in the form of warehouse compute and vector embeddings. When in the SUSPENDED state, changes in base tables will
  not trigger refreshes, nor will they be reflected in the queryable data of the Cortex Search Service.

  Note

  If indexing is suspended for longer than the data retention period of the source tables, the service may be unable to detect changes in
  the source data when indexing is resumed and could require recreation. For more information, see [DATA\_RETENTION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-data-retention-time-in-days).
- SERVING is the target that indicates the serving layer of the Cortex Search Service. This target must be in the RUNNING state for the
  service to be queryable. When in the suspended state, the Cortex Search Service will not incur billing
  in the form of Cortex Search’s serving costs.

For detailed cost considerations, see [Cost considerations](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-cost-considerations).

The INDEXING and SERVING layers of the Cortex Search Service can be managed independently. For instance, if SERVING is in the running
state while INDEXING is suspended, you can still query the service. However, the service will not reflect any changes in the base data
regardless of the `TARGET_LAG` until INDEXING is resumed and a refresh is completed successfully.

Conversely, if INDEXING is running while SERVING is suspended, the index will continue to refresh. When SERVING is resumed, the loaded
index that becomes queryable will reflect the most up-to-date source data.

When neither the SERVING nor INDEXING keywords are specified, both targets will be impacted by the specified action.

### Manual refreshes

When you manually refresh a Cortex Search Service, the service immediately checks for changes in its source data and updates the
index as needed. Trigger a manual refresh of your Cortex Search Service when you need the most up-to-date results possible — for
example, when you have just added or updated important documents and want these to be available immediately to users. You can
also use a manual refresh to ensure that results are always current at specific times, such as at the start of business.

You can trigger a manual refresh of a Cortex Search Service using the ALTER CORTEX SEARCH SERVICE … REFRESH command or in Snowsight.

### Primary keys

Altering the primary key columns of a Cortex Search Service affects only future refreshes.
That is, changes to primary keys go into effect after the next change to the source data.

## Examples

The following example changes warehouse used by the Cortex Search service named `mysvc` to `my_new_wh`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SET WAREHOUSE = my_new_wh;
```

The following example sets the comment field of the Cortex Search service named `mysvc` to `new_comment`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SET COMMENT = 'new_comment';
```

The following example changes the target refresh lag of the Cortex Search service named `mysvc` to `1 hour`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SET TARGET_LAG = '1 hour';
```

The following example sets the primary key columns of the Cortex Search service named `mysvc` to `region` and `agent_id`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SET PRIMARY KEY = (region, agent_id);
```

The following example clears the primary key columns of the Cortex Search service named `mysvc`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc UNSET PRIMARY KEY;
```

The following example sets the attribute columns of the Cortex Search service named `mysvc` to `category` and `region`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SET ATTRIBUTES (category, region);
```

The following example removes all attribute columns from the Cortex Search service named `mysvc`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc UNSET ATTRIBUTES;
```

The following example enables request logging for a Cortex Search service named `mysvc`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SET REQUEST_LOGGING = TRUE;
```

The following example suspends serving for a Cortex Search service named `mysvc`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SUSPEND SERVING;
```

The following example enables auto-suspend on a Cortex Search service named `mysvc`,
configuring it to suspend serving after 30 minutes of query inactivity:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc SET AUTO_SUSPEND = 1800;
```

The following example manually refreshes a Cortex Search service named `mysvc`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc REFRESH;
```

The following example sets tags on the Cortex Search service named `mysvc`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc
  SET TAG cost_center = 'v1', cost_center2 = 'v2';
```

The following example unsets the `cost_center` tag on the Cortex Search service named `mysvc`:

Copy code

```
ALTER CORTEX SEARCH SERVICE mysvc UNSET TAG cost_center;
```
