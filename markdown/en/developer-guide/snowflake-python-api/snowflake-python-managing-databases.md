# Managing Snowflake databases, schemas, tables, and views with Python

You can use Python to manage Snowflake databases, schemas, tables, and views. For more information about managing and working with data in
Snowflake, see [Databases, Tables and Views - Overview](/guides-overview-db).

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

## Managing databases

You can manage databases in Snowflake. The Snowflake Python APIs represents databases with two separate types:

- `Database`: Exposes a database’s properties, such as its name.
- `DatabaseResource`: Exposes methods you can use to fetch a corresponding `Database` object and to drop the database.

**Topics**

- [Creating a database](#label-snowflake-python-create-db)
- [Getting database details](#label-snowflake-python-fetch-db-details)
- [Listing databases](#label-snowflake-python-list-dbs)
- [Dropping or restoring a database](#label-snowflake-python-drop-db)

### Creating a database

You can create a database by calling the `DatabaseCollection.create` method and passing a `Database` object that represents the
database you want to create. To create a database, first create a `Database` object that specifies the database name.

Code in the following example creates a `Database` object representing a database named `my_db` and then creates the
database by passing the `Database` object to the `DatabaseCollection.create` method:

Copy code

```
from snowflake.core.database import Database

my_db = Database(name="my_db")
root.databases.create(my_db)
```

### Getting database details

You can get information about a database by calling the `DatabaseResource.fetch` method, which returns a `Database`
object.

Code in the following example gets information about a database named `my_db`:

Copy code

```
my_db = root.databases["my_db"].fetch()
print(my_db.to_dict())
```

### Listing databases

You can list databases using the `iter` method, which returns a `PagedIter` iterator.

Code in the following example lists databases whose name begins with `my`:

Copy code

```
databases = root.databases.iter(like="my%")
for database in databases:
  print(database.name)
```

### Dropping or restoring a database

You can drop a database using the `DatabaseResource.drop` method or restore a database using the `DatabaseResource.undrop`
method.

To demonstrate these operations, code in the following example drops and then restores the most recent version of the `my_db` database:

Copy code

```
my_db_res = root.databases["my_db"]
my_db_res.drop()
my_db_res.undrop()
```

## Managing schemas

You can manage schemas in Snowflake. A schema is a database-level object. When you create or reference a schema, you do so in the context
of its database.

The Snowflake Python APIs represents schemas with two separate types:

- `Schema`: Exposes a schema’s properties, such as its name.
- `SchemaResource`: Exposes methods you can use to fetch a corresponding `Schema` object and to drop the schema.

**Topics**

- [Creating a schema](#label-snowflake-python-create-schema)
- [Getting schema details](#label-snowflake-python-fetch-schema-details)
- [Listing schemas](#label-snowflake-python-list-schemas)
- [Dropping or restoring a schema](#label-snowflake-python-drop-schema)

### Creating a schema

To create a schema, first create a `Schema` object that specifies the schema name.

Code in the following example creates a `Schema` object representing a schema named `my_schema`:

Copy code

```
from snowflake.core.schema import Schema

my_schema = Schema(name="my_schema")
root.databases["my_db"].schemas.create(my_schema)
```

The code then creates the schema in the `my_db` database by passing the `Schema` object to the `SchemaCollection.create`
method.

### Getting schema details

You can get information about a schema by calling the `SchemaResource.fetch` method, which returns a `Schema` object.

Code in the following example gets a `Schema` object that represents the `my_schema` schema:

Copy code

```
my_schema = root.databases["my_db"].schemas["my_schema"].fetch()
print(my_schema.to_dict())
```

### Listing schemas

You can list the schemas in a specified database using the `iter` method. The method returns a `PagedIter` iterator of
`Schema` objects.

Code in the following example lists schema names in the `my_db` database:

Copy code

```
schema_list = root.databases["my_db"].schemas.iter()
for schema_obj in schema_list:
  print(schema_obj.name)
```

### Dropping or restoring a schema

You can drop a schema using the `SchemaResource.drop` method or restore a schema using the `SchemaResource.undrop` method.

To demonstrate these operations, code in the following example drops and then restores the most recent version of the `my_schema` schema:

Copy code

```
my_schema_res = root.databases["my_db"].schemas["my_schema"]
my_schema_res.drop()
my_schema_res.undrop()
```

## Managing standard tables

You can manage standard tables in Snowflake. A table is a schema-level object. When you create or reference a table, you do so in the
context of its schema.

The Snowflake Python APIs represents tables with two separate types:

- `Table`: Exposes a table’s properties, such as its name and columns.
- `TableResource`: Exposes methods you can use to fetch a corresponding `Table` object, update the properties of the table, and
  drop the table.

**Topics**

- [Creating a table](#label-snowflake-python-create-table)
- [Getting table details](#label-snowflake-python-fetch-table-details)
- [Creating or altering a table](#label-snowflake-python-alter-table)
- [Listing tables](#label-snowflake-python-list-tables)
- [Swapping table names](#label-snowflake-python-swap-tables)
- [Performing table operations](#label-snowflake-python-perform-table-operations)

### Creating a table

To create a table, first create a `Table` object that specifies the table name, column names, and column data types.

Code in the following example creates a `Table` object representing a table named `my_table` with the specified columns:

Copy code

```
from snowflake.core.table import Table, TableColumn

my_table = Table(
  name="my_table",
  columns=[TableColumn(name="c1", datatype="int", nullable=False),
           TableColumn(name="c2", datatype="string")]
)
root.databases["my_db"].schemas["my_schema"].tables.create(my_table)
```

The code then creates the table in the `my_db` database and `my_schema` schema by passing the `Table` object to the
`TableCollection.create` method.

### Getting table details

You can get information about a table by calling the `TableResource.fetch` method, which returns a `Table` object.

Code in the following example gets information about a table named `my_table`:

Copy code

```
my_table = root.databases["my_db"].schemas["my_schema"].tables["my_table"].fetch()
print(my_table.to_dict())
```

### Creating or altering a table

You can set properties of a `Table` object and pass it to the `TableResource.create_or_alter` method to create a table if it
doesn’t exist, or alter it according to the table definition if it does exist. The behavior of `create_or_alter` is intended to be
idempotent, which means that the resulting table object will be the same regardless of whether the table exists before you call the method.

Note

The `create_or_alter` method uses default values for any [Table](https://docs.snowflake.com/en/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.table.Table)
properties that you don’t explicitly define. For example, if you don’t set `data_retention_time_in_days`, its value defaults to
`None` even if the table previously existed with a different value.

Code in the following example appends a new column named `c3` of datatype `int` to the `my_table` table, and then alters the
table in Snowflake:

Copy code

```
from snowflake.core.table import PrimaryKey, TableColumn

my_table = root.databases["my_db"].schemas["my_schema"].tables["my_table"].fetch()
my_table.columns.append(TableColumn(name="c3", datatype="int", nullable=False, constraints=[PrimaryKey()]))

my_table_res = root.databases["my_db"].schemas["my_schema"].tables["my_table"]
my_table_res.create_or_alter(my_table)
```

### Listing tables

You can list the tables in a specified schema using the `iter` method, which returns a `PagedIter` iterator of
`Table` objects.

Code in the following example lists tables whose name begins with `my`:

Copy code

```
tables = root.databases["my_db"].schemas["my_schema"].tables.iter(like="my%")
for table_obj in tables:
  print(table_obj.name)
```

### Swapping table names

You can swap (exchange) the name of a table with another table in a single transaction using the `TableResource.swap_with` method.
For more information, see the SWAP WITH parameter description in [ALTER TABLE](/sql-reference/sql/alter-table).

Code in the following example swaps `my_table` with `other_table` in the same database and schema:

Copy code

```
my_table_res = root.databases["my_db"].schemas["my_schema"].tables["my_table"]
my_table_res.swap_with("other_table")
```

Code in the following example swaps `my_table` (in the `my_db` database and `my_schema` schema) with `other_table` (in the
`other_db` database and `other_schema` schema):

Copy code

```
my_table_res = root.databases["my_db"].schemas["my_schema"].tables["my_table"]
my_table_res.swap_with(to_swap_table_name="other_table", target_database="other_db", target_schema="other_schema")
```

### Performing table operations

You can perform common table operations—such as managing [reclustering](/user-guide/tables-auto-reclustering) for a table and
dropping or restoring a table—with a `TableResource` object.

For more information about these table operations, see [Table, view, sequence, and user-defined type commands](/sql-reference/commands-table) in the SQL command reference.

To demonstrate some operations you can do with a table resource, code in the following example does the following:

1. Gets the `my_table` table resource object in the `my_db` database and the `my_schema` schema.
2. Suspends reclustering for the table.
3. Resumes reclustering for the table.
4. Drops the table.
5. Restores the most recent version of the dropped table.

Copy code

```
my_table_res = root.databases["my_db"].schemas["my_schema"].tables["my_table"]

my_table_res.suspend_recluster()
my_table_res.resume_recluster()
my_table_res.drop()
my_table_res.undrop()
```

## Managing event tables

You can manage Snowflake event tables, which are a special kind of database table with a predefined set of columns where Snowflake can
collect telemetry data. For more information, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).

The Snowflake Python APIs represents event tables with two separate types:

- `EventTable`: Exposes an event table’s properties such as its name, data retention time, max data extension time, and change
  tracking option.
- `EventTableResource`: Exposes methods you can use to fetch a corresponding `EventTable` object, rename the event table, and
  drop the event table.

**Topics**

- [Creating an event table](#label-snowflake-python-create-event-table)
- [Getting event table details](#label-snowflake-python-fetch-event-table-details)
- [Listing event tables](#label-snowflake-python-list-event-tables)
- [Performing event table operations](#label-snowflake-python-perform-event-table-operations)

### Creating an event table

To create an event table, first create a `EventTable` object, and then create a `EventTableCollection` object from the API
`Root` object. Using `EventTableCollection.create`, add the new event table to Snowflake.

Code in the following example creates a `EventTable` object that represents an event table named `my_event_table` with the
specified parameters:

Copy code

```
from snowflake.core.event_table import EventTable

event_table = EventTable(
  name="my_event_table",
  data_retention_time_in_days = 3,
  max_data_extension_time_in_days = 5,
  change_tracking = True,
  default_ddl_collation = 'EN-CI',
  comment = 'CREATE EVENT TABLE'
)

event_tables = root.databases["my_db"].schemas["my_schema"].event_tables
event_tables.create(my_event_table)
```

The code creates a `EventTableCollection` variable `event_tables` and uses `EventTableCollection.create` to create a new
event table in Snowflake.

### Getting event table details

You can get information about an event table by calling the `EventTableResource.fetch` method, which returns a `EventTable`
object.

Code in the following example gets information about an event table named `my_event_table`:

Copy code

```
my_event_table = root.databases["my_db"].schemas["my_schema"].event_tables["my_event_table"].fetch()
print(my_event_table.to_dict())
```

### Listing event tables

You can list event tables using the `EventTableCollection.iter` method, which returns a `PagedIter` iterator of
`EventTable` objects.

Code in the following example lists event tables whose name starts with `my` in the `my_db` database and `my_schema` schema, and
prints the name of each:

Copy code

```
from snowflake.core.event_table import EventTableCollection

event_tables: EventTableCollection = root.databases["my_db"].schemas["my_schema"].event_tables
event_table_iter = event_tables.iter(like="my%")  # returns a PagedIter[EventTable]
for event_table_obj in event_table_iter:
  print(event_table_obj.name)
```

Code in the following example also lists event tables whose name begins with `my`, but it uses the `starts_with` parameter instead
of `like`. This example also sets the optional parameter `show_limit=10` to limit the number of results to `10`:

Copy code

```
event_tables: EventTableCollection = root.databases["my_db"].schemas["my_schema"].event_tables
event_table_iter = event_tables.iter(starts_with="my", show_limit=10)
for event_table_obj in event_table_iter:
  print(event_table_obj.name)
```

### Performing event table operations

You can perform common event table operations—such as renaming an event table and dropping an event table—with a
`EventTableResource` object.

Note

Only the RENAME functionality of [ALTER TABLE (event tables)](/sql-reference/sql/alter-table-event-table) is currently supported.

RENAME is not supported on the default event table, SNOWFLAKE.TELEMETRY.EVENTS.

To demonstrate operations you can do with an event table resource, code in the following example does the following:

1. Gets the `my_event_table` event table resource object in the `my_db` database and the `my_schema` schema.
2. Renames the event table.
3. Drops the event table.

Copy code

```
my_event_table_res = root.databases["my_db"].schemas["my_schema"].event_tables["my_event_table"]

my_event_table_res.rename("my_other_event_table")
my_event_table_res.drop()
```

## Managing views

You can manage views in Snowflake. A view is a schema-level object and allows the result of a query to be accessed as if it were a table.
When you create or reference a view, you do so in the context of its schema.

Note

[ALTER VIEW](/sql-reference/sql/alter-view) is currently not supported.

The Snowflake Python APIs represents views with two separate types:

- `View`: Exposes a view’s properties, such as its name, columns, and SQL query statement.
- `ViewResource`: Exposes methods you can use to fetch a corresponding `View` object and to drop the view.

**Topics**

- [Creating a view](#label-snowflake-python-create-view)
- [Getting view details](#label-snowflake-python-fetch-view-details)
- [Listing views](#label-snowflake-python-list-views)
- [Dropping a view](#label-snowflake-python-drop-view)

### Creating a view

To create a view, first create a `View` object that specifies the view name, columns, and SQL query statement.

Code in the following example creates a `View` object representing a view named `my_view` with the specified columns and SQL
query:

Copy code

```
from snowflake.core.view import View, ViewColumn

my_view = View(
  name="my_view",
  columns=[
      ViewColumn(name="c1"), ViewColumn(name="c2"), ViewColumn(name="c3"),
  ],
  query="SELECT * FROM my_table",
)

root.databases["my_db"].schemas["my_schema"].views.create(my_view)
```

The code then creates the view in the `my_db` database and `my_schema` schema by passing the `View` object to the
`ViewCollection.create` method.

### Getting view details

You can get information about a view by calling the `ViewResource.fetch` method, which returns a `View` object.

Code in the following example gets a `View` object that represents the `my_view` view:

Copy code

```
my_view = root.databases["my_db"].schemas["my_schema"].views["my_view"].fetch()
print(my_view.to_dict())
```

### Listing views

You can list the views in a specified database using the `iter` method. The method returns a `PagedIter` iterator of
`View` objects.

Code in the following example lists views whose name begins with `my` in the `my_db` database and `my_schema` schema:

Copy code

```
view_list = root.databases["my_db"].schemas["my_schema"].views.iter(like="my%")
for view_obj in view_list:
  print(view_obj.name)
```

Code in the following example also lists views whose name begins with `my`, but it uses the `starts_with` parameter instead of
`like`. This example also sets the optional parameter `show_limit=10` to limit the number of results to `10`:

Copy code

```
view_list = root.databases["my_db"].schemas["my_schema"].views.iter(starts_with="my", show_limit=10)
for view_obj in view_list:
  print(view_obj.name)
```

### Dropping a view

You can drop a view using the `ViewResource.drop` method.

Code in the following example drops the `my_view` view:

Copy code

```
my_view_res = root.databases["my_db"].schemas["my_schema"].views["my_view"]
my_view_res.drop()
```
