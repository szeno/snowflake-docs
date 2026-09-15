# Introduction to object tagging

## What is a tag?

A tag is a schema-level object that can be assigned to another Snowflake object. Users associate a tag with an arbitrary string value when
assigning the tag to a Snowflake object. Snowflake stores the tag and its string value as a key-value pair. The tag must be unique for
your schema, and the tag value is always a string. To assign more than one string value to the same tag, use
[Multi-value tags](/user-guide/object-tagging/multi-value-tags). For common governance use cases, you can assign
[Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags) that Snowflake creates in every account.

The following are general characteristics of object tagging:

- An object can have multiple tags at the same time. For more information, see [Tag quotas](#label-object-tagging-quota).
- A single tag can be assigned to different object types at the same time (for example, a warehouse and a table simultaneously).
- At the time of assignment, the tag string value can be duplicated or remain unique. For example, multiple tables can be assigned
  the `cost_center` tag and the tag can always have the string value `sales`. Alternatively, the string value could be different
  for each table (for example, `engineering`, `marketing`, and `finance`).

After defining the tags and assigning the tags to Snowflake objects, you can query them to monitor usage on objects and facilitate data
governance operations, such as auditing and reporting.

### Highlights

Ease of use:
:   Define a tag once and apply it to as many different objects as desirable.

Tag inheritance:
:   Because tags are inherited, applying the tag to objects higher in the securable objects hierarchy results in the tag being applied to all
    child objects. For example, if a tag is set on a table, the tag will be inherited by all columns in that table.

Automatic propagation:
:   Configure a tag so it automatically propagates to target objects from a source object.

Consistent assignment with replication:
:   Snowflake replicates tags and their assignments within the primary database to the secondary database.

Centralized or decentralized management:
:   Tags support different management approaches to facilitate compliance with internal and external regulatory requirements.

    In a centralized approach, you can create a `tag_admin` custom role that creates and applies tags to Snowflake objects.

    In a decentralized approach, individual teams apply tags to Snowflake objects and the `tag_admin` custom role creates tags to ensure
    consistent tag naming.

## Using tags for data protection

Because tags can be assigned to tables, views, and columns, setting a tag and then querying the tag enables the
discovery of a multitude of database objects and columns that contain sensitive information. Upon discovery, data stewards can determine
how best to make that data available, such as selective filtering using [row access policies](/user-guide/security-row-intro), or
using [masking policies](/user-guide/security-column-intro) to determine whether the data is tokenized, fully masked, partially
masked, or unmasked.

You can also combine object tagging and masking policies to simplify the governance of data. With this approach, you assign a masking
policy to a tag, then assign that tag to a table or column. When the data type of a column matches the data type in the masking policy
signature, the tagged column is automatically protected by the masking policy. For more information, see
[Tag-based masking policies](/user-guide/tag-based-masking-policies).

## Using tags to monitor resource usage

Assigning tags to warehouses enables accurate resource usage monitoring. Querying tags on resources allows for easy resource
grouping by cost center or some other organization unit. Additionally, the tag can facilitate analyzing relatively short-term business
activities, such as projects, to provide a more granular insight into what, when, and how resources were used.

For an example of using tags to monitor resource usage, see [Setting up object tags for cost attribution](/user-guide/cost-attributing#label-cost-attribute-tag).

## How a tag gets associated with an object

A tag can be associated with an object in the following ways:

- Someone manually set the tag on the object using a CREATE <object> or ALTER <object> command. See [Set a tag](/user-guide/object-tagging/work#label-object-tagging-set).
- The object inherited the tag from an object higher up in the Snowflake securable object hierarchy. For example, a warehouse in an account
  inherits tags set on the account. See [Tag inheritance](/user-guide/object-tagging/inheritance).
- The tag was automatically propagated from one object to another. Tags can be propagated when an object depends on another object (for
  example, a view based on a tagged table) or when data moves from a tagged object to another object (for example, using a CTAS statement
  to create a table). See [Automatic tag propagation with user-defined tags](/user-guide/object-tagging/propagation).
- The tag was automatically set on a column that was classified as containing sensitive data. To learn how sensitive data
  classification uses a tag map to set these tags, see [About classification tags](/user-guide/classify-intro#label-classify-classification-tags).
- Someone used the CREATE TABLE … LIKE or CREATE TABLE … CLONE command to create a table from an existing table with tags.

### Determine how a tag was associated with an object

The following views and functions include the `apply_method` column, which shows how a tag was associated with an object.

> - View: [ACCOUNT\_USAGE.TAG\_REFERENCES](/sql-reference/account-usage/tag_references)
> - Functions:
>   - [INFORMATION\_SCHEMA.TAG\_REFERENCES](/sql-reference/functions/tag_references)
>   - [INFORMATION\_SCHEMA.TAG\_REFERENCES\_ALL\_COLUMNS](/sql-reference/functions/tag_references_all_columns)
>   - [ACCOUNT\_USAGE.TAG\_REFERENCES\_WITH\_LINEAGE](/sql-reference/functions/tag_references_with_lineage)

For example, to find whether a tag was set manually on the object or was propagated, you could execute the following command and check the
value of the `apply_method` column.

> Copy code
>
> ```
> SELECT tag_name, tag_value, apply_method, level, domain
>   FROM TABLE(my_db.INFORMATION_SCHEMA.TAG_REFERENCES('my_table', 'TABLE'));
> ```

## Tag quotas

You can set a maximum of 50 tags on a single object, including tables and views.

If you have reached the limit on tags and want to drop one, execute an ALTER <object> UNSET TAG statement.

### Separate quota for columns

You can set a maximum of 50 different tags on the columns of a single table. This is a limit on all of the columns combined.

The column limit is separate from the limit on the number of tags set on a table. For example, suppose you create the following table with
tags on both the table and its columns:

Copy code

```
CREATE TABLE t1 (
  COL1 INT WITH TAG (tag1='col1', tag2='col1'),
  COL2 INT WITH TAG (tag1='col2'),
  )
  WITH TAG (tag3='t1');
```

Snowflake allows you to do the following:

- Set 49 more tags on the table `t1`.
- Set 48 more tags on the columns of `t1`. The limit is on *different* tags, so `tag1` isn’t counted twice.

If you run a CREATE TABLE or ALTER TABLE statement to apply tags on the columns of a table, the maximum number of unique tag-entity
associations is 100, where an entity is the table or a column. For example, if you have a table with 1,000 columns and you want to associate
the same tag with every column, you need to run 10 ALTER statements.

## Capabilities that require Enterprise Edition

Creating and setting tags is available to all accounts. However, there are advanced capabilities that require Enterprise Edition or higher.
Your account must be Enterprise Edition or higher to use the following capabilities:

- [Tag propagation](/user-guide/object-tagging/propagation)
- [Tag-based masking policies](/user-guide/tag-based-masking-policies)

## Supported objects

The following table lists the supported objects for tags, including columns, based on the Snowflake securable object hierarchy.

A tag can be set on an object with a [CREATE <object>](/sql-reference/sql/create) statement or an [ALTER <object>](/sql-reference/sql/alter) statement unless
specified otherwise in the table below.

A tag can be set on a column using a CREATE TABLE, CREATE VIEW, ALTER TABLE … MODIFY COLUMN, or ALTER VIEW statement.

| Object hierarchy | Supported objects | Notes |
| --- | --- | --- |
| Organization | Account | A tag can be [set](/sql-reference/sql/alter-account) on your [current account](/sql-reference/functions/current_account) by a role with the global APPLY TAG privilege. |
| Account | Application |  |
|  | Application package |  |
|  | Compute pool |  |
|  | Database |  |
|  | Failover group |  |
|  | Integration | All [types](/sql-reference/sql/create-integration) are supported.  Use an [ALTER INTEGRATION](/sql-reference/sql/alter-integration) command to set a tag on the integration. |
|  | Network policy | Use an [ALTER NETWORK POLICY](/sql-reference/sql/alter-network-policy) command to set a tag on a network policy. |
|  | Replication group |  |
|  | Role |  |
|  | Share | Tags are set on the share by the data sharing provider. These tags are not visible to the data sharing consumer. Use an [ALTER SHARE](/sql-reference/sql/alter-share) command to set a tag on the share. |
|  | Snowflake CoWork | Use ALTER SNOWFLAKE INTELLIGENCE to set a tag on a Snowflake CoWork object. For an example, see [Resource budgets for Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork/cowork-resource-budgets). |
|  | User |  |
|  | Warehouse |  |
| Database | Database role | Use an [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role) command to set a tag on a database role. |
|  | Schema |  |
| Schema | Aggregation policy |  |
|  | Alert |  |
|  | Backup set | For [WORM backups](/user-guide/backups). Contains a set of backups for a specific database, schema, or table. |
|  | BUDGET instance | Use an [ALTER BUDGET](/sql-reference/classes/budget/commands/alter-budget) command to set a tag on an instance of the SNOWFLAKE.CORE.BUDGET class. |
|  | CLASSIFICATION instance | Use an [ALTER SNOWFLAKE.ML.CLASSIFICATION](/sql-reference/classes/classification/commands/alter-classification) command to set a tag on an instance of the SNOWFLAKE.ML.CLASSIFICATION class. |
|  | Cortex Agent | Use an [ALTER AGENT](/sql-reference/sql/alter-agent) command to set a tag on a Cortex Agent. |
|  | Cortex Search service | Use an [ALTER CORTEX SEARCH SERVICE](/sql-reference/sql/alter-cortex-search) command to set a tag on a Cortex Search service. |
|  | Dynamic table |  |
|  | Event table |  |
|  | External function and UDF | Use an [ALTER FUNCTION](/sql-reference/sql/alter-function) command to set a tag on an external function or UDF. |
|  | External table | You can create an external table with a tag using a [CREATE EXTERNAL TABLE](/sql-reference/sql/create-external-table) statement.  To manage tag assignments on an external table, use the [ALTER TABLE](/sql-reference/sql/alter-table) command. |
|  | Git repository |  |
|  | Apache Iceberg™ table |  |
|  | Image repository |  |
|  | Interactive table |  |
|  | Join policy |  |
|  | Materialized view |  |
|  | Notebook |  |
|  | Password policy |  |
|  | Pipe | Set a tag on a pipe with an [ALTER PIPE](/sql-reference/sql/alter-pipe) statement. |
|  | Policy | Set a tag on a [masking](/sql-reference/sql/alter-masking-policy), [password](/sql-reference/sql/alter-password-policy), [row access](/sql-reference/sql/alter-row-access-policy), [session](/sql-reference/sql/alter-session-policy), [aggregation](/sql-reference/sql/alter-aggregation-policy), [join](/sql-reference/sql/alter-join-policy), or [projection](/sql-reference/sql/alter-projection-policy) policy with the corresponding ALTER *<policy>* statement. |
|  | Procedure | Set a tag on a stored procedure with an [ALTER PROCEDURE](/sql-reference/sql/alter-procedure) statement. |
|  | Projection policy |  |
|  | Semantic view |  |
|  | Session policy |  |
|  | Snapshot | For [block storage volume snapshots](/developer-guide/snowpark-container-services/block-storage-volume). |
|  | Stage | Set a tag on a stage with an [ALTER STAGE](/sql-reference/sql/alter-stage) statement. |
|  | Stream |  |
|  | Streamlit |  |
|  | Table |  |
|  | Task | Set a tag on a task with an [ALTER TASK](/sql-reference/sql/alter-task) statement. |
|  | View |  |
| Table or View | Column | Includes [event tables](/sql-reference/sql/alter-table-event-table). |
| Semantic View | Logical table, dimension, fact, metric |  |

Expand

Show lessSee more

## Limitations and considerations

Future grants:
:   [Future grants](/sql-reference/sql/grant-privilege#label-grant-privilege-schema-future-grants) of privileges on tags are not supported.

    As a workaround, grant the APPLY TAG privilege to a custom role to allow that role to apply tags to another object.

Snowflake Native App:
:   Use caution when creating the setup script when tags exist in a versioned schema. For information, see
    [version schema considerations](/developer-guide/native-apps/creating-setup-script#label-setup-script-versioned-schema-failures).
