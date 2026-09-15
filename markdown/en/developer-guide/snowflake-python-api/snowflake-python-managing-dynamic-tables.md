# Managing Snowflake dynamic tables with Python

You can use Python to manage Snowflake dynamic tables, which are a new table type for continuous processing pipelines. Dynamic tables
materialize the results of a specified query. For an overview of this feature, see [Dynamic tables](/user-guide/dynamic-tables/overview).

The Snowflake Python APIs represents dynamic tables with two separate types:

- `DynamicTable`: Exposes a dynamic table’s properties such as its name, target lag, warehouse, and query statement.
- `DynamicTableResource`: Exposes methods you can use to fetch a corresponding `DynamicTable` object, suspend and resume the
  dynamic table, and drop the dynamic table.

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Creating a dynamic table

To create a dynamic table, first create a `DynamicTable` object, and then create a `DynamicTableCollection` object from the API
`Root` object. Using `DynamicTableCollection.create`, add the new dynamic table to Snowflake.

Code in the following example creates a `DynamicTable` object that represents a dynamic table named `my_dynamic_table` in the
`my_db` database and the `my_schema` schema, with the minimum required options specified:

Copy code

```
from snowflake.core.dynamic_table import DynamicTable, DownstreamLag

my_dt = DynamicTable(
  name='my_dynamic_table',
  target_lag=DownstreamLag(),
  warehouse='my_wh',
  query='SELECT * FROM t',
)
dynamic_tables = root.databases['my_db'].schemas['my_schema'].dynamic_tables
dynamic_tables.create(my_dt)
```

The code creates a `DynamicTableCollection` variable `dynamic_tables` and uses `DynamicTableCollection.create` to create
a new dynamic table in Snowflake.

Code in the following example creates a `DynamicTable` object that represents a dynamic table named `my_dynamic_table2` in the
`my_db` database and the `my_schema` schema with all currently possible options specified:

Copy code

```
from snowflake.core.dynamic_table import DynamicTable, UserDefinedLag

root.databases['my_db'].schemas['my_schema'].dynamic_tables.create(
  DynamicTable(
      name='my_dynamic_table2',
      kind='PERMANENT',
      target_lag=UserDefinedLag(seconds=60),
      warehouse='my_wh',
      query='SELECT * FROM t',
      refresh_mode='FULL',
      initialize='ON_SCHEDULE',
      cluster_by=['id > 1'],
      comment='test table',
      data_retention_time_in_days=7,
      max_data_extension_time_in_days=7,
  )
)
```

### Cloning a dynamic table

Code in the following example creates a new dynamic table named `my_dynamic_table2` with the same column definitions and all existing
data from the source dynamic table `my_dynamic_table` in the `my_db` database and the `my_schema` schema:

> Note
>
> This clone operation uses the `DynamicTableClone` object, which includes the optional `target_lag` and `warehouse`
> parameters, and currently does not support other parameters.

Copy code

```
from snowflake.core.dynamic_table import DynamicTableClone

root.databases['my_db'].schemas['my_schema'].dynamic_tables.create(
  DynamicTableClone(
      name='my_dynamic_table2',
      warehouse='my_wh2',
  ),
  clone_table='my_dynamic_table',
)
```

For more information about this functionality, see [CREATE DYNAMIC TABLE … CLONE](/sql-reference/sql/create-dynamic-table#label-create-dt-clone-syntax).

## Getting dynamic table details

You can get information about a dynamic table by calling the `DynamicTableResource.fetch` method, which returns a
`DynamicTable` object.

Code in the following example gets information about a dynamic table named `my_dynamic_table` in the `my_db` database and the
`my_schema` schema:

Copy code

```
dynamic_table = root.databases['my_db'].schemas['my_schema'].dynamic_tables['my_dynamic_table']
dt_details = dynamic_table.fetch()
print(dt_details.to_dict())
```

## Listing dynamic tables

You can list dynamic tables using the `DynamicTableCollection.iter` method, which returns a `PagedIter` iterator of
`DynamicTable` objects.

Code in the following example lists dynamic tables whose name starts with the text `my` in the `my_db` database and the `my_schema`
schema, and then prints the name of each:

Copy code

```
from snowflake.core.dynamic_table import DynamicTableCollection

dt_list = root.databases['my_db'].schemas['my_schema'].dynamic_tables.iter(like='my%')
for dt_obj in dt_list:
  print(dt_obj.name)
```

## Swapping dynamic table names

You can swap the name of a dynamic table with another dynamic table in a single transaction using the `DynamicTableResource.swap_with`
method. For more information, see the SWAP WITH parameter description in [ALTER DYNAMIC TABLE](/sql-reference/sql/alter-dynamic-table#label-alter-dynamic-table-swap).

Code in the following example swaps `my_dynamic_table` with `other_dynamic_table` in the same database and schema:

Copy code

```
my_table_res = root.databases['my_db'].schemas['my_schema'].tables['my_dynamic_table']
my_table_res.swap_with('other_dynamic_table')
```

## Performing dynamic table operations

You can perform common dynamic table operations—such as refreshing, suspending, and resuming a dynamic table—with a
`DynamicTableResource` object.

For more information about these dynamic table operations, see [Table, view, sequence, and user-defined type commands](/sql-reference/commands-table) in the SQL command reference.

To demonstrate some operations you can do with a dynamic table resource, code in the following example does the following:

1. Gets the `my_dynamic_table` dynamic table resource object in the `my_db` database and the `my_schema` schema.
2. Refreshes the dynamic table.
3. Suspends the dynamic table.
4. Resumes the dynamic table.
5. Drops the dynamic table.
6. Restores the most recent version of the dropped dynamic table.

Copy code

```
my_dynamic_table_res = root.databases["my_db"].schemas["my_schema"].dynamic_tables["my_dynamic_table"]

my_dynamic_table_res.refresh()
my_dynamic_table_res.suspend()
my_dynamic_table_res.resume()
my_dynamic_table_res.drop()
my_dynamic_table_res.undrop()
```
