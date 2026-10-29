Schema:
:   [Data Sharing Usage](/sql-reference/data-sharing-usage)

# LISTING\_ACCESS\_HISTORY view

Preview Feature — Open

This feature is currently in preview and is available to all users. The `QUERY_TYPE` column and the `groupByObjects`, `aggregateObjects`, and `filterObjects` arrays in the `SHARE_OBJECTS_ACCESSED` column are generally available.

This view in the DATA\_SHARING\_USAGE schema can be used to explore the history of consumers’ usage of your listings.
LISTING\_ACCESS\_HISTORY provides object-level information about queries run against the data shares or Native Apps attached to your listings. For more information about the data provided by the LISTING\_ACCESS\_HISTORY view, see the [Columns](#columns) section.

Each row returned by LISTING\_ACCESS\_HISTORY represents a single time the listing was accessed by a consumer. Because the rows represent queries instead of sessions, it is likely that the same listing will appear multiple times, one row for each query.

A single consumer query can access objects from multiple listings. The QUERY\_TOKEN identifies the query that generated a row in the listing access history.
To identify a collection of listing objects accessed by a single consumer query, use the QUERY\_TOKEN.

The LISTING\_ACCESS\_HISTORY view provides selected information about consumer queries rather than their full SQL text. The view also excludes any objects that are not owned by the provider account. For example, if a consumer joins data from your listing with their own data or another provider’s data, only listing objects that you own are returned by the LISTING\_ACCESS\_HISTORY view. The view also reports supported consumer query types and information about how consumers use columns in your listing. For details, see [Columns](#label-listing-access-columns) and [SHARE\_OBJECTS\_ACCESSED array](#label-share-objects-accessed-array).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| QUERY\_TOKEN | VARCHAR | Unique ID for each query run by a consumer. A QUERY\_TOKEN does not correlate with any actual query identifier on the consumer side. |
| QUERY\_DATE | DATE | Date when the query was executed. |
| QUERY\_TYPE | VARCHAR | Consumer query type: `SELECT`, `INSERT`, `CREATE_TABLE_AS_SELECT`, `UNLOAD`, or `PARTITIONED_UNLOAD`. Other types and queries predating this column return `<redacted>`. Returns `NULL` when `IS_APPLICATION` is `TRUE`. |
| EXCHANGE\_NAME | VARCHAR | Snowflake Marketplace or the data exchange where the listing is available. |
| SNOWFLAKE\_REGION | VARCHAR | Snowflake region where the consumption occurred. |
| LISTING\_GLOBAL\_NAME | VARCHAR | Global name of the listing in the Snowflake Marketplace or data exchange that provides the share. |
| PROVIDER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the share owner. |
| PROVIDER\_ACCOUNT\_NAME | VARCHAR | Account name of the share owner. |
| SHARE\_NAME | VARCHAR | Name of the data share that consumers accessed. When IS\_SHARE is FALSE, the value is NULL. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | Account locator of the consumer. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | Account name of the consumer. |
| CONSUMER\_ACCOUNT\_ORGANIZATION | VARCHAR | Name of the organization for the consumer account. |
| REGION\_GROUP | VARCHAR | [Region group](/user-guide/admin-account-identifier#label-region-groups) where the account of the consumer is located. |
| CONSUMER\_NAME | VARCHAR | Contains the name of the consumer account that accessed, used, or requested a listing. If no name is available, such as for trial accounts, the value is NULL. |
| IS\_SHARE | BOOLEAN | TRUE if the access was on a share. When TRUE, the SHARE\_OBJECTS\_ACCESSED column provides details about the share objects accessed by the consumer query. |
| IS\_APPLICATION | BOOLEAN | TRUE if the access was on an application. When TRUE, APPLICATION\_OBJECTS\_ACCESSED column provides details about the application objects accessed by the consumer query. |
| SHARE\_OBJECTS\_ACCESSED | ARRAY | Details the share objects accessed by the consumer query. When IS\_SHARE is FALSE, the value is NULL. See [SHARE\_OBJECTS\_ACCESSED array](#label-share-objects-accessed-array) for formatting. |
| APPLICATION\_OBJECTS\_ACCESSED | ARRAY | Details the application objects accessed by the consumer query. When IS\_APPLICATION is FALSE, the value is NULL. See [APPLICATION\_OBJECTS\_ACCESSED array](#label-application-objects-accessed-array). |
| APPLICATION\_PACKAGE\_NAME | VARCHAR | The current name of the application package from which the application was installed. When IS\_APPLICATION is FALSE, the value is NULL. |
| APPLICATION\_VERSION | VARCHAR | The version of the application when the query occurred. When IS\_APPLICATION is FALSE, the value is NULL |
| APPLICATION\_PATCH\_ID | NUMBER | The application patch number when the query occurred. When IS\_APPLICATION is FALSE, the value is NULL. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 2 days.
- The data is retained for 365 days (1 year).

### SHARE\_OBJECTS\_ACCESSED array

The SHARE\_OBJECTS\_ACCESSED array provides details about the objects in a share accessed by a consumer query. The format of an item in the
array depends on the type of object that was accessed.

Functions:

Copy code

```
{
  "argumentSignature": (function_signature varchar),
  "objectName": "DATABASE_NAME.SCHEMA_NAME.FUNCTION_NAME",
  "objectID": "12345",
  "objectDomain": "Function"
}
```

Stored procedures:

Copy code

```
{
  "argumentSignature": (function_signature varchar),
  "objectName": "DATABASE_NAME.SCHEMA_NAME.PROCEDURE_NAME"
  "objectID":"12345"
  "objectDomain":"Procedure"
}
```

Tables, views, and columns:

Copy code

```
[
  {
    "Columns": [
      {
        "columnId": ######,
        "columnName": "column1_name"
      },
      {
        "columnId": ######,
        "columnName": "column2_name"
      }
    ],
    "objectDomain":"VIEW",
    "objectId": ##view_id##,
    "objectName": "DATABASE_1.PUBLIC.VIEW_1"
  },
  {
    "Columns": [
      {
        "columnId": ######,
        "columnName": "column3_name"
      },
      {
        "columnId": ######,
        "columnName": "column4_name"
      }
    ],
    "objectDomain":"TABLE",
    "objectId": ##table_id##,
    "objectName": "DATABASE_2.PUBLIC.TABLE1"
  }
]
```

For tables and views, an item can also include the following arrays, which describe how consumer queries used your columns:

| Field | Description |
| --- | --- |
| `groupByObjects` | Your columns that the consumer query grouped by. Each entry contains a `columnId` and a `columnName`. |
| `aggregateObjects` | Your columns that the consumer query passed to an aggregate function. Each entry contains a `columnId` and a `columnName`. |
| `filterObjects` | Your columns that the consumer query filtered on in a `WHERE`, `HAVING`, or `QUALIFY` clause. Each entry contains a `columnId` and a `columnName`. For date and timestamp columns compared with a constant, the entry can also contain a `columnValue` field holding the date used in the filter predicate, expressed as a UTC date (`YYYY-MM-DD`) without time-of-day information. For all other data types, the entry omits `columnValue` and doesn’t expose the filter value. |

Expand

Show lessSee more

An entry for a table or view with these arrays included looks like this:

Copy code

```
[
  {
    "Columns": [
      {
        "columnId": ######,
        "columnName": "column1_name"
      }
    ],
    "groupByObjects": [
      {
        "columnId": ######,
        "columnName": "column2_name"
      }
    ],
    "aggregateObjects": [
      {
        "columnId": ######,
        "columnName": "column3_name"
      }
    ],
    "filterObjects": [
      {
        "columnId": ######,
        "columnName": "column4_name",
        "columnValue": "2024-01-01"
      },
      {
        "columnId": ######,
        "columnName": "column5_name"
      }
    ],
    "objectDomain":"TABLE",
    "objectId": ##table_id##,
    "objectName": "DATABASE_2.PUBLIC.TABLE1"
  }
]
```

Cortex Search Services:

Copy code

```
[
  {
    "objectDomain":"Cortex Search Service",
    "objectId": 12345,
    "objectName": "DATABASE_2.PUBLIC.SHARED_CKE_NAME",
    "hashedDocumentIds": [##hashed_id1##, ##hashed_id2##],
    "hashVersion": "V1"
  }
]
```

### APPLICATION\_OBJECTS\_ACCESSED array

The APPLICATION\_OBJECTS\_ACCESSED array provides details about the objects in a Native App accessed by a consumer query. The format of an item in the array depends on the type of object that was accessed.

Unlike the SHARE\_OBJECTS\_ACCESSED column array results, APPLICATION\_OBJECTS\_ACCESSED results containing object IDs are unavailable and database names are masked.

Functions:

Copy code

```
{
  "argumentSignature": (function_signature varchar),
  "objectName": "23662386A408C571B77FDC53691793E4992D1C12.SCHEMA_NAME.FUNCTION_NAME",
  "objectDomain": "Function"
}
```

Stored procedures:

Copy code

```
{
  "argumentSignature": (function_signature varchar),
  "objectName": "23662386A408C571B77FDC53691793E4992D1C12.SCHEMA_NAME.PROCEDURE_NAME"
  "objectDomain":"Procedure"
}
```

Tables, views, and columns:

Copy code

```
[
  {
    "Columns": [
      {
        "columnName": "column1_name"
      },
      {
        "columnName": "column2_name"
      }
    ],
    "objectDomain":"VIEW",
    "objectName": "5F3297829072D2E23B852D7787825FF762E74EF3.PUBLIC.VIEW_1"
  },
  {
    "Columns": [
      {
        "columnName": "column3_name"
      },
      {
        "columnName": "column4_name"
      }
    ],
    "objectDomain":"TABLE",
    "objectName": "D85A2CE1531C6C1E077FA701713047305BDF5A83.PUBLIC.TABLE1"
  }
]
```

### LISTING\_OBJECTS\_ACCESSED array

The LISTING\_OBJECTS\_ACCESSED column was removed from this view by the 2024\_08 behavior change bundle. It contained the same
data as the SHARE\_OBJECTS\_ACCESSED column. Use [SHARE\_OBJECTS\_ACCESSED array](#label-share-objects-accessed-array) instead. For more information, see
[LISTING\_ACCESS\_HISTORY view (DATA\_SHARING\_USAGE): Deprecate LISTING\_OBJECTS\_ACCESSED column](/release-notes/bcr-bundles/2024_08/bcr-1758).

## Examples

This section contains the following example SQL queries for the LISTING\_ACCESS\_HISTORY view:

- [Aggregate view of access over time](#label-aggregate-access-over-time)
- [Aggregate view of access over time by consumer](#label-aggregate-access-by-consumer)
- [Access count by column](#label-access-count-by-column)
- [Table joins](#label-table-joins)
- [Table joins by consumer](#label-table-joins-by-consumer)
- [Range of filter values by consumer](#label-filter-value-range)
- [Columns used in GROUP BY clauses](#label-group-by-columns)
- [Unload queries by consumer](#label-query-types-by-consumer)

### Aggregate view of access over time

An aggregate view of which functions, stored procedures, tables, views, and columns have been accessed (over a certain period) and the total number of times.

Copy code

```
select
  lah.exchange_name,
  lah.listing_global_name,
  lah.share_name,
  los.value:"objectName"::string as object_name,
  coalesce(los.value:"objectDomain"::string, los.value:"objectDomain"::string) as object_type,
  count(distinct lah.query_token) as n_queries,
  count(distinct lah.consumer_account_locator) as n_distinct_consumer_accounts
from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
join lateral flatten(input=>lah.share_objects_accessed) as los
where true
  and query_date between '2022-03-01' and '2022-04-30'
group by 1,2,3,4,5
order by 1,2,3,4,5;
```

### Aggregate view of access over time by consumer

This example is similar to [Aggregate view of access over time](#label-aggregate-access-over-time), broken down by consumer.

Copy code

```
select
  lah.exchange_name,
  lah.listing_global_name,
  lah.share_name,
  los.value:"objectName"::string as object_name,
  coalesce(los.value:"objectDomain"::string, los.value:"objectDomain"::string) as object_type,
  consumer_account_locator,
  count(distinct lah.query_token) as n_queries
from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
join lateral flatten(input=>lah.share_objects_accessed) as los
where true
  and query_date between '2022-03-01' and '2022-04-30'
group by 1,2,3,4,5,6
order by 1,2,3,4,5,6;
```

### Access count by column

For a given object (table, view), how many times each column was accessed.

Copy code

```
select
  los.value:"objectDomain"::string as object_type,
  los.value:"objectName"::string as object_name,
  cols.value:"columnName"::string as column_name,
  count(distinct lah.query_token) as n_queries,
  count(distinct lah.consumer_account_locator) as n_distinct_consumer_accounts
from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
join lateral flatten(input=>lah.share_objects_accessed) as los
join lateral flatten(input=>los.value, path=>'columns') as cols
where true
  and los.value:"objectDomain"::string in ('Table', 'View')
  and query_date between '2022-03-01' and '2022-04-30'
  and los.value:"objectName"::string = 'DATABASE_NAME.SCHEMA_NAME.TABLE_NAME'
  and lah.consumer_account_locator = 'CONSUMER_ACCOUNT_LOCATOR'
group by 1,2,3;
```

### Table joins

A view of which combination of tables are being joined together.

Copy code

```
with
accesses as (
  select
    lah.query_token,
    array_agg(distinct los.value:"objectName"::string) as object_names
  from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
  join lateral flatten(input=>lah.share_objects_accessed) as los
  where true
    and los.value:"objectDomain"::string in ('Table', 'View')
    and query_date between '2022-03-01' and '2022-04-30'
  group by 1
)
select
  object_names,
  sum(1) as n_queries
from accesses
group by 1
```

### Table joins by consumer

A view of which tables are being joined together (pairs) broken down by consumer.

Copy code

```
with
accesses as (
  select distinct
    los.value:"objectDomain"::string as object_type,
    los.value:"objectName"::string as object_name,
    lah.query_token,
    lah.consumer_account_locator
  from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
  join lateral flatten(input=>lah.share_objects_accessed) as los
  where true
    and los.value:"objectDomain"::string in ('Table', 'View')
    and query_date between '2022-03-01' and '2022-04-30'
)
select
  a1.object_name as object_name_1,
  a2.object_name as object_name_2,
  a1.consumer_account_locator as consumer_account_locator,
  count(distinct a1.query_token) as n_queries
from accesses as a1
join accesses as a2
  on a1.query_token = a2.query_token
  and a1.object_name < a2.object_name
group by 1,2,3;
```

### Range of filter values by consumer

A view of the earliest and latest date literals in consumer filters on date and timestamp columns, broken down by consumer.

Copy code

```
select
  lah.consumer_account_organization,
  lah.consumer_account_name,
  sos.value:"objectName"::string as object_name,
  filters.value:"columnName"::string as column_name,
  min(filters.value:"columnValue"::date) as earliest_filter_value,
  max(filters.value:"columnValue"::date) as latest_filter_value,
  count(distinct lah.query_token) as n_queries
from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
join lateral flatten(input=>lah.share_objects_accessed) as sos
join lateral flatten(input=>sos.value, path=>'filterObjects') as filters
where true
  and lah.query_date >= dateadd('day', -7, current_date())
  and filters.value:"columnValue"::date is not null
group by 1,2,3,4
order by 1,2,3,4;
```

### Columns used in GROUP BY clauses

A view of how often consumers group by each column.

Copy code

```
select
  sos.value:"objectName"::string as object_name,
  gb.value:"columnName"::string as column_name,
  count(distinct lah.query_token) as n_queries,
  count(distinct lah.consumer_account_locator) as n_distinct_consumer_accounts
from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
join lateral flatten(input=>lah.share_objects_accessed) as sos
join lateral flatten(input=>sos.value, path=>'groupByObjects') as gb
where true
  and lah.query_date >= dateadd('day', -7, current_date())
group by 1,2
order by 3 desc;
```

To do the same for columns passed to aggregate functions, flatten `aggregateObjects` instead of `groupByObjects`.

### Unload queries by consumer

To count the queries in the last seven days that unloaded data from your listing, broken down by consumer and unload type, run the following statement:

Copy code

```
select
  lah.consumer_account_locator,
  lah.consumer_account_name,
  lah.query_type,
  count(distinct lah.query_token) as n_queries
from SNOWFLAKE.DATA_SHARING_USAGE.LISTING_ACCESS_HISTORY as lah
where lah.query_date >= dateadd('day', -7, current_date())
  and lah.query_type in ('UNLOAD', 'PARTITIONED_UNLOAD')
group by 1,2,3
order by 4 desc;
```

To count other query types, change the values in the `query_type` filter.
