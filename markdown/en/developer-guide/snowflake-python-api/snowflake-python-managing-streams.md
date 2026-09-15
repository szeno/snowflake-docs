# Managing Snowflake streams with Python

You can use Python to manage Snowflake streams, which are objects that record data manipulation language (DML) changes made to tables,
including inserts, updates, and deletes, as well as metadata about each change. For more information, see [Introduction to streams](/user-guide/streams-intro).

Note

[ALTER STREAM](/sql-reference/sql/alter-stream) is currently not supported.

The Snowflake Python APIs represents streams with two separate types:

- `Stream`: Exposes a stream’s properties such as its name, target lag, warehouse, and query statement.
- `StreamResource`: Exposes methods you can use to fetch a corresponding `Stream` object, suspend and resume the stream, and
  drop the stream.

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

## Creating a stream

To create a stream, first create a `Stream` object, and then create a `StreamCollection` object from the API `Root`
object. Using `StreamCollection.create`, add the new stream to Snowflake.

You can create a stream on the following object types:

- Standard tables
- Views
- Directory tables

### On a source table

Code in the following example creates a `Stream` object that represents a stream named `my_stream_on_table` on the source table
`my_table` in the `my_db` database and the `my_schema` schema, with the specified stream properties:

Note

The `StreamSourceTable` type only supports standard tables. Other types of tables—such as dynamic tables, event tables, external
tables, and Iceberg tables—are currently not supported.

Copy code

```
from snowflake.core.stream import PointOfTimeOffset, Stream, StreamSourceTable

stream_on_table = Stream(
  "my_stream_on_table",
  StreamSourceTable(
      point_of_time = PointOfTimeOffset(reference="before", offset="1"),
      name = 'my_table',
      append_only = True,
      show_initial_rows = False,
  ),
  comment = 'create stream on table'
)

streams = root.databases['my_db'].schemas['my_schema'].streams
streams.create(stream_on_table)
```

The code creates a `StreamCollection` variable `streams` and uses `StreamCollection.create` to create a new stream in
Snowflake.

### On a source view

Code in the following example creates a `Stream` object that represents a stream named `my_stream_on_view` on the source view
`my_view` in the `my_db` database and the `my_schema` schema, with the specified stream properties:

Copy code

```
from snowflake.core.stream import PointOfTimeOffset, Stream, StreamSourceView

stream_on_view = Stream(
  "my_stream_on_view",
  StreamSourceView(
      point_of_time = PointOfTimeOffset(reference="before", offset="1"),
      name = 'my_view',
  ),
  comment = 'create stream on view'
)

streams = root.databases['my_db'].schemas['my_schema'].streams
streams.create(stream_on_view)
```

### On a source directory table

Code in the following example creates a `Stream` object that represents a stream named `my_stream_on_directory_table` on the source
directory table `my_directory_table` in the `my_db` database and the `my_schema` schema, with the specified stream properties:

Copy code

```
from snowflake.core.stream import PointOfTimeOffset, Stream, StreamSourceStage

stream_on_directory_table = Stream(
  "my_stream_on_directory_table",
  StreamSourceStage(
      point_of_time = PointOfTimeOffset(reference="before", offset="1"),
      name = 'my_directory_table',
  ),
  comment = 'create stream on directory table'
)

streams = root.databases['my_db'].schemas['my_schema'].streams
streams.create(stream_on_directory_table)
```

### Cloning a stream

Code in the following example creates a new stream named `my_stream` with the same definition as the source stream `my_other_stream` in
the `my_db` database and the `my_schema` schema:

Copy code

```
from snowflake.core.stream import Stream

streams = root.databases['my_db'].schemas['my_schema'].streams
streams.create("my_stream", clone_stream="my_other_stream")
```

## Getting stream details

You can get information about a stream by calling the `StreamResource.fetch` method, which returns a `Stream` object.

Code in the following example gets information about a stream named `my_stream` in the `my_db` database and the `my_schema` schema:

Copy code

```
stream = root.databases['my_db'].schemas['my_schema'].streams['my_stream']
stream_details = stream.fetch()
print(stream_details.to_dict())
```

## Listing streams

You can list streams using the `StreamCollection.iter` method, which returns a `PagedIter` iterator of `Stream` objects.

Code in the following example lists streams whose name starts with `my` in the `my_db` database and the `my_schema` schema, and then
prints the name of each:

Copy code

```
stream_list = root.databases['my_db'].schemas['my_schema'].streams.iter(like='my%')
for stream_obj in stream_list:
  print(stream_obj.name)
```

Code in the following example also lists streams whose name begins with `my`, but it uses the `starts_with` parameter instead of
`like`. This example also sets the optional parameter `show_limit=10` to limit the number of results to `10`:

Copy code

```
stream_list = root.databases['my_db'].schemas['my_schema'].streams.iter(starts_with="my", show_limit=10)
for stream_obj in stream_list:
  print(stream_obj.name)
```

## Dropping a stream

You can drop a stream with a `StreamResource` object.

Code in the following example gets the `my_stream` stream resource object and then drops the stream.

Copy code

```
my_stream_res = root.streams["my_stream"]
my_stream_res.drop()
```
