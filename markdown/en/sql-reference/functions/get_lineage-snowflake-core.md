Categories:
:   [Table functions](/sql-reference/functions-table)

# GET\_LINEAGE (SNOWFLAKE.CORE)

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Given a Snowflake object, returns data lineage information upstream or downstream from that object. Upstream means the
path of objects that led to the creation of the object; downstream means the path of objects that were created
from the object.

## Syntax

Copy code

```
SNOWFLAKE.CORE.GET_LINEAGE(
    '<object_name>',
    '<object_domain>',
    '<direction>',
    [ <max_distance>, ]
    [ '<object_version>', ]
    [ '<namespace>', ]
    [ '<object_type>', ]
    [ '<external_id>', ]
    [ '<column_name>' ]
)
```

## Arguments

**Required:**

`'object_name'`
:   Name of the object for which data lineage information is retrieved. Use the fully qualified name if the object is in a
    schema different from the current schema in the session.

`'object_domain'`
:   The domain of the object. Supported domains are ‘COLUMN’, ‘TABLE’ (which includes all table-like objects including
    views and dynamic tables), ‘SEMANTIC\_VIEW’ (for [semantic views](/user-guide/views-semantic/overview)), ‘STAGE’, and
    ‘CORTEX\_AGENT’ (for [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)).

    Specify an agent as ‘CORTEX\_AGENT’. ‘AGENT’ isn’t a valid domain, even though the object type is displayed as **Agent**
    in Snowsight.

    For ML lineage, use *TABLE* for feature views (which are dynamic tables and views internally), ‘DATASET’, or ‘MODULE’ for
    models.

    To retrieve lineage for an object that isn’t in Snowflake, use ‘EXTERNAL’, or ‘EXTERNAL\_COLUMN’ for a column of such an
    object. Both require the `namespace` argument. For more information, see
    [Lineage for objects outside Snowflake](#label-get-lineage-external-objects).

`'direction'`
:   The direction for which the lineage should be retained. Supported directions are ‘UPSTREAM’ and ‘DOWNSTREAM’.

**Optional:**

`max_distance`
:   The number of levels of lineage to retrieve. The maximum is 5; this is also the default.

`'object_version'`
:   For versioned objects, such as datasets and models, the version of the object for which lineage is retrieved. If not
    specified, the default version is used.

`'namespace'`
:   The namespace of the object, which identifies the system the object comes from. Required when `object_domain` is
    ‘EXTERNAL’ or ‘EXTERNAL\_COLUMN’, and not valid for any other domain.

`'object_type'`
:   The specific type of the object within its namespace, such as the type a data catalog assigns it. Only valid when
    `object_domain` is ‘EXTERNAL’ or ‘EXTERNAL\_COLUMN’.

`'external_id'`
:   The identifier that the originating system assigns to the object. Only valid when `object_domain` is ‘EXTERNAL’ or
    ‘EXTERNAL\_COLUMN’.

`'column_name'`
:   The name of the column to retrieve lineage for. Required when `object_domain` is ‘EXTERNAL\_COLUMN’, and not valid for
    any other domain.

## Output

The output is a table with one row per object relationship in the lineage path (that is, an edge in the lineage graph).
Relationships are between objects designated as source and target in each row. The table includes the following columns:

| Column | Type | Description |
| --- | --- | --- |
| `SOURCE_OBJECT_DATABASE` | VARCHAR | The database that contains the source object. |
| `SOURCE_OBJECT_SCHEMA` | VARCHAR | The schema that contains the source object. |
| `SOURCE_OBJECT_NAME` | VARCHAR | The unqualified name of the source object. |
| `SOURCE_OBJECT_DOMAIN` | VARCHAR | The domain of the target object. Possible values are ‘COLUMN’, ‘TABLE’, ‘SEMANTIC\_VIEW’, ‘DATASET’, ‘MODULE’ (for ML models), ‘STAGE’, and ‘CORTEX\_AGENT’. |
| `SOURCE_OBJECT_VERSION` | VARCHAR | The version of the source object, for versioned objects such as datasets and models. NULL if the source object is not versioned. |
| `SOURCE_COLUMN_NAME` | VARCHAR | The name of the source column, if the source object is a column. NULL if the source object is not a column. |
| `SOURCE_STATUS` | VARCHAR | The status of the source object. Possible values are ‘ACTIVE’ and ‘MASKED’. |
| `TARGET_OBJECT_DATABASE` | VARCHAR | The database that contains the target object. |
| `TARGET_OBJECT_SCHEMA` | VARCHAR | The schema that contains the target object. |
| `TARGET_OBJECT_NAME` | VARCHAR | The unqualified name of the target object. |
| `TARGET_OBJECT_DOMAIN` | VARCHAR | The domain of the target object. Possible values are ‘COLUMN’, ‘TABLE’, ‘SEMANTIC\_VIEW’, ‘DATASET’, ‘MODULE’ (for ML models), ‘STAGE’, and ‘CORTEX\_AGENT’. |
| `TARGET_OBJECT_VERSION` | VARCHAR | The version of the target object, for versioned objects such as datasets and models. NULL if the target object is not versioned. |
| `TARGET_COLUMN_NAME` | VARCHAR | The name of the target column, if the target object is a column. NULL if the target object is not a column. |
| `TARGET_STATUS` | VARCHAR | The status of the target object. Possible values are ‘ACTIVE’ and ‘MASKED’. |
| `DISTANCE` | INTEGER | The distance of the target object from the source object in the lineage path. A direct relationship has a distance of 1. |
| `PROCESS` | VARIANT | Provides details about how lineage between the source object and target object was established. For example, it might include the query ID of a SQL query or the name of a stored procedure that moved data from the source object to the target object. |
| `SOURCE_DETAILS` | VARIANT | Additional details about the source object. See [Object details](#label-get-lineage-object-details). |
| `TARGET_DETAILS` | VARIANT | Additional details about the target object. See [Object details](#label-get-lineage-object-details). |

Expand

Show lessSee more

## Object details

The `SOURCE_DETAILS` and `TARGET_DETAILS` columns are populated for every object in the lineage path. Keys with no value
for a given object are omitted. Each column contains the following keys:

| Key | Description |
| --- | --- |
| `dataset_type` | The specific type of the object. This is more granular than `SOURCE_OBJECT_DOMAIN` and `TARGET_OBJECT_DOMAIN`; for example, an object in the `TABLE` domain can have a `dataset_type` of `TABLE` or `VIEW`. |
| `origin` | Where the lineage for the object came from: `NATIVE` for a Snowflake object, or `OPEN_LINEAGE` for an object whose lineage was ingested from an external source. |
| `namespace` | The namespace of the object. Present for objects that aren’t Snowflake objects. |
| `external_id` | The identifier of the object in the system it originates from. Present for objects that aren’t Snowflake objects. |

Expand

Show lessSee more

## Usage notes

- You will receive an error message if the object does not exist, if the object is not accessible to the current user,
  if the object does not support data lineage, or if the object is not in the specified domain.
- The output table contains no rows if no lineage information is available for the specified object; this is not an error.
- `GET_LINEAGE` returns at most 10 million rows, each row representing an edge (relationship) in the lineage graph.
  If there are more than 10 million rows in the output, the function silently truncates output to 10 million rows.
- You can specify arguments either by position or by name, but not both in the same call. For an
  example that uses named arguments, see [Passing arguments by name](#label-get-lineage-named-args).
- For limitations and considerations that apply to using this function, see
  [Lineage limitations and considerations](/user-guide/ui-snowsight-lineage#label-lineage-limitations).

## Example

Assume you have created a table named TABLE\_B from TABLE\_A using CREATE TABLE AS SELECT, then created a table named
TABLE\_C from TABLE\_B in a similar manner. The following SQL query retrieves two steps of downstream lineage from
TABLE\_A:

Copy code

```
SELECT
    DISTANCE,
    SOURCE_OBJECT_DOMAIN,
    SOURCE_OBJECT_DATABASE,
    SOURCE_OBJECT_SCHEMA,
    SOURCE_OBJECT_NAME,
    SOURCE_STATUS,
    TARGET_OBJECT_DOMAIN,
    TARGET_OBJECT_DATABASE,
    TARGET_OBJECT_SCHEMA,
    TARGET_OBJECT_NAME,
    TARGET_STATUS,
FROM TABLE (SNOWFLAKE.CORE.GET_LINEAGE('my_database.sch.table_a', 'TABLE', 'DOWNSTREAM', 2));
```

The output is similar to the following:

```
+----------+----------------------+------------------------+----------------------+--------------------+---------------+----------------------+------------------------+----------------------+--------------------+---------------+
| DISTANCE | SOURCE_OBJECT_DOMAIN | SOURCE_OBJECT_DATABASE | SOURCE_OBJECT_SCHEMA | SOURCE_OBJECT_NAME | SOURCE_STATUS | TARGET_OBJECT_DOMAIN | TARGET_OBJECT_DATABASE | TARGET_OBJECT_SCHEMA | TARGET_OBJECT_NAME | TARGET_STATUS |
|----------+----------------------+------------------------+----------------------+--------------------+---------------+----------------------+------------------------+----------------------+--------------------+---------------|
|        1 | TABLE                | MY_DATABASE            | SCH                  | TABLE_A            | ACTIVE        | TABLE                | MY_DATABASE            | SCH                  | TABLE_B            | ACTIVE        |
|        2 | TABLE                | MY_DATABASE            | SCH                  | TABLE_B            | ACTIVE        | TABLE                | MY_DATABASE            | SCH                  | TABLE_C            | ACTIVE        |
+----------+----------------------+------------------------+----------------------+--------------------+---------------+----------------------+------------------------+----------------------+--------------------+---------------+
```

## Passing arguments by name

You can pass arguments by name instead of by position, which lets you omit the optional arguments you
don’t need. The following query returns the same lineage as the previous example:

Copy code

```
SELECT
    DISTANCE,
    SOURCE_OBJECT_NAME,
    TARGET_OBJECT_NAME
FROM TABLE (SNOWFLAKE.CORE.GET_LINEAGE(
    object_name => 'my_database.sch.table_a',
    object_domain => 'TABLE',
    direction => 'DOWNSTREAM',
    max_distance => 2));
```

## Lineage for objects outside Snowflake

Lineage isn’t limited to objects in Snowflake. For information about capturing lineage from an external system, see
[External lineage](/user-guide/external-lineage).

After that lineage is ingested into your account, `GET_LINEAGE` reports it alongside your Snowflake lineage:

- **Objects outside Snowflake appear in the output.** A lineage path that starts at a Snowflake object can continue into
  objects that aren’t in Snowflake. The `SOURCE_DETAILS` and `TARGET_DETAILS` columns identify these objects; their
  `origin` key distinguishes them from Snowflake objects. See [Object details](#label-get-lineage-object-details).
- **You can start from an object outside Snowflake.** Set `object_domain` to ‘EXTERNAL’ (or ‘EXTERNAL\_COLUMN’ for one of
  its columns) and pass the object’s `namespace` along with its name. This is useful for tracing which Snowflake objects
  an external object feeds, or what feeds it.
- **A chain of external objects takes one query per step.** Lineage can continue from one external object to another: for
  example, from a Snowflake table to an external object and then on to a second external object. To retrieve the next step
  in such a chain, run a second query anchored on the external object you reached.

For an object that isn’t in Snowflake, `SOURCE_OBJECT_DATABASE` and `SOURCE_OBJECT_SCHEMA` (and their target equivalents)
are NULL, and the object’s domain is reported as ‘EXTERNAL’ or ‘EXTERNAL\_COLUMN’.

### Example: Reaching an object outside Snowflake

Assume that TABLE\_A is exported to a file, and that lineage for the export has been ingested into your account. The
following query retrieves downstream lineage from TABLE\_A, extracting the namespace and origin of each target from
`TARGET_DETAILS`:

Copy code

```
SELECT
    DISTANCE,
    SOURCE_OBJECT_NAME,
    TARGET_OBJECT_DOMAIN,
    TARGET_OBJECT_NAME,
    TARGET_DETAILS:namespace::VARCHAR AS TARGET_NAMESPACE,
    TARGET_DETAILS:origin::VARCHAR AS TARGET_ORIGIN
FROM TABLE (SNOWFLAKE.CORE.GET_LINEAGE(
    object_name => 'my_database.sch.table_a',
    object_domain => 'TABLE',
    direction => 'DOWNSTREAM',
    max_distance => 1));
```

The output is similar to the following, in which the database and schema columns are NULL for the target because the
target isn’t a Snowflake object:

```
+----------+--------------------+----------------------+--------------------+------------------------+---------------+
| DISTANCE | SOURCE_OBJECT_NAME | TARGET_OBJECT_DOMAIN | TARGET_OBJECT_NAME | TARGET_NAMESPACE       | TARGET_ORIGIN |
|----------+--------------------+----------------------+--------------------+------------------------+---------------|
|        1 | TABLE_A            | EXTERNAL             | out/daily.parquet  | s3://analytics-exports | OPEN_LINEAGE  |
+----------+--------------------+----------------------+--------------------+------------------------+---------------+
```

### Example: Continuing from an object outside Snowflake

To retrieve the lineage of the file reached in the previous example, anchor on it: set `object_domain` to ‘EXTERNAL’ and
pass its `namespace` along with its name. Repeat this pattern to follow a chain of external objects one step at a time.

Copy code

```
SELECT
    DISTANCE,
    SOURCE_OBJECT_NAME,
    TARGET_OBJECT_DOMAIN,
    TARGET_OBJECT_NAME
FROM TABLE (SNOWFLAKE.CORE.GET_LINEAGE(
    object_name => 'out/daily.parquet',
    object_domain => 'EXTERNAL',
    direction => 'DOWNSTREAM',
    max_distance => 1,
    namespace => 's3://analytics-exports'));
```
