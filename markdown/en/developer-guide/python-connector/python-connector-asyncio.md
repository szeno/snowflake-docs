# Using asynchronous I/O with the Python Connector

The `snowflake.connector.aio` module is the asyncio interface for the Snowflake Connector for Python. It is part of the connector package, and it exposes the same PEP 249 `Connection` and `Cursor` objects as [Using the Python Connector](/developer-guide/python-connector/python-connector-example). Methods that talk to Snowflake are coroutines, so you `await` them from an asyncio event loop.

Use this module when your application already runs on an event loop. For scripts and libraries that call the connector from ordinary functions, use the synchronous `snowflake.connector` module.

Asynchronous I/O is separate from [asynchronous queries](/developer-guide/python-connector/python-connector-example#label-python-connector-querying-data-asynchronous). An asynchronous query returns before Snowflake finishes the statement. You can submit one from either module.

## Open a connection

`snowflake.connector.aio.connect()` accepts the same connection parameters as [Connecting to Snowflake with the Python Connector](/developer-guide/python-connector/python-connector-connect). Those parameters are defined by `snowflake.connector.ConnectionConfig`.

`async with` opens the session when you enter the block and closes it when you leave:

> Copy code
>
> ```
> async with snowflake.connector.aio.connect() as conn:
>     ...
> ```

## Run a query

`cursor()` returns a cursor immediately. It isn’t a coroutine. `execute()`, `executemany()`, `fetchone()`, `fetchmany()`, and `fetchall()` are coroutines.

> Copy code
>
> ```
> async with conn.cursor() as cur:
>     await cur.execute(
>         "SELECT col1, col2 FROM testtable WHERE col1 > %s",
>         (100,),
>     )
>     async for col1, col2 in cur:
>         print(f"{col1}, {col2}")
> ```

`async for` reads rows until the result set is exhausted. `async with` closes the cursor when the block ends. `Cursor.close()` isn’t a coroutine.

Pass `DictCursor` to receive each row as a dictionary:

> Copy code
>
> ```
> from snowflake.connector.aio import DictCursor
>
> async with conn.cursor(DictCursor) as cur:
>     await cur.execute("SELECT col1, col2 FROM testtable")
>     print(await cur.fetchone())
> ```

Pass bound values as `parameters`. `execute()` doesn’t accept `params` as another name for that argument.

## Run queries concurrently

To overlap work on one connection, give each task its own cursor.

> Copy code
>
> ```
> async def fetch_rows(conn, sql):
>     async with conn.cursor() as cur:
>         await cur.execute(sql)
>         return await cur.fetchall()
>
> async with snowflake.connector.aio.connect() as conn:
>     results = await asyncio.gather(
>         fetch_rows(conn, "SELECT 1"),
>         fetch_rows(conn, "SELECT 2"),
>     )
> ```

## Submit an asynchronous query

`execute_async()` submits a statement and returns before Snowflake finishes it. On this module, status checks and result retrieval are coroutines too. For the query lifecycle, see [Performing an asynchronous query](/developer-guide/python-connector/python-connector-example#label-python-connector-querying-data-asynchronous).

> Copy code
>
> ```
> async with conn.cursor() as cur:
>     result = await cur.execute_async("SELECT COUNT(*) FROM testtable")
>     query_id = result["queryId"]
>     status = await conn.get_query_status_throw_if_error(query_id)
>     while conn.is_still_running(status):
>         await asyncio.sleep(1)
>         status = await conn.get_query_status_throw_if_error(query_id)
>     await cur.get_results_from_sfqid(query_id)
>     print(await cur.fetchall())
> ```

`is_still_running()` is an ordinary method. `get_query_status()` and `get_query_status_throw_if_error()` are coroutines.

## Use pandas

Install the `pandas` extra as described in [Using Pandas with the Python Connector](/developer-guide/python-connector/python-connector-pandas). Fetch methods and `write_pandas()` are coroutines, and they require an asyncio connection.

> Copy code
>
> ```
> from snowflake.connector.aio import write_pandas
>
> async with conn.cursor() as cur:
>     await cur.execute("SELECT * FROM testtable")
>     dataframe = await cur.fetch_pandas_all()
>
> success, nchunks, nrows, copy_results = await write_pandas(
>     conn,
>     dataframe,
>     "testtable_copy",
>     auto_create_table=True,
> )
> ```

`fetch_pandas_batches()` and `fetch_arrow_batches()` return async iterators:

> Copy code
>
> ```
> async with conn.cursor() as cur:
>     await cur.execute("SELECT * FROM testtable")
>     async for batch in cur.fetch_pandas_batches():
>         my_dataframe_processing_function(batch)
> ```

`snowflake.connector.aio` doesn’t provide `pd_writer()` or `make_pd_writer()`. `DataFrame.to_sql()` calls its writer synchronously and can’t await a coroutine. For `to_sql()`, use [Using Pandas with the Python Connector](/developer-guide/python-connector/python-connector-pandas).
