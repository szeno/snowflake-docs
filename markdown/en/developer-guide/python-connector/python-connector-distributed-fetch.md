# Distributing workloads that fetch results with the Snowflake Connector for Python

If you are using a distributed environment to parallelize workloads, you can use the Snowflake Connector for Python to distribute
the work of fetching and processing results.

## Introduction

After you use the `Cursor` object to execute a query, you can distribute the work of fetching the results by using
result batches. A *result batch* encapsulates a function that retrieves a subset of the results. You can assign different workers
to use different result batches to fetch and process results in parallel.

## Retrieving the list of result batches

After executing a query, you can retrieve the results in one of the following formats:

- [ResultBatch](/developer-guide/python-connector/python-connector-api#label-python-connector-resultbatch-object) objects.

  To do this, call the `get_result_batches()` method in the [Cursor](/developer-guide/python-connector/python-connector-api#label-python-connector-cursor-object) object.
  This returns a list of `ResultBatch` objects that you can assign to different workers for processing. For example:

  Copy code

  ```
  with connect(...) as conn:
   with conn.cursor() as cur:
       # Execute a query.
       cur.execute('select seq4() as n from table(generator(rowcount => 100000));')

       # Get the list of result batches
       result_batch_list = cur.get_result_batches()

       # Get the number of result batches in the list.
       num_result_batches = len(result_batch_list)

       # Split the list of result batches into two
       # to distribute the work of fetching results
       # between two workers.
       result_batch_list_1 = result_batch_list[:: 2]
       result_batch_list_2 = result_batch_list[1 :: 2]
  ```
- PyArrow tables.

  For more information, see [PyArrow tables](https://arrow.apache.org/docs/python/data.html#tables).

  You can use the following methods to retrieve the result batches as PyArrow tables:

  - `fetch_arrow_all()`: Call this method to return a PyArrow table containing all of the results.
  - `fetch_arrow_batches()`: Call this method to return an iterator that you can use to return a PyArrow table for each
    result batch.

  For example:

  Copy code

  ```
  with connect(...) as conn:
   with conn.cursor() as cur:
       # Execute a query.
       cur.execute('select seq4() as n from table(generator(rowcount => 100000));')

       # Return a PyArrow table containing all of the results.
       table = cur.fetch_arrow_all()

       # Iterate over a list of PyArrow tables for result batches.
       for table_for_batch in cur.fetch_arrow_batches():
         my_pyarrow_table_processing_function(table_for_batch)
  ```
- [pandas DataFrame](/developer-guide/python-connector/python-connector-pandas) objects.

  If you have
  [installed the pandas-compatible version of the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-pandas#label-python-connector-pandas-install),
  you can use the following methods to retrieve the result batches as pandas DataFrame objects:

  - `fetch_pandas_all()`: Call this method to return a pandas DataFrame containing all of the results.
  - `fetch_pandas_batches()`: Call this method to return an iterator that you can use to return a pandas DataFrame for each
    result batch.

  For example:

  Copy code

  ```
  with connect(...) as conn:
   with conn.cursor() as cur:
       # Execute a query.
       cur.execute('select seq4() as n from table(generator(rowcount => 100000));')

       # Return a pandas DataFrame containing all of the results.
       table = cur.fetch_pandas_all()

       # Iterate over a list of pandas DataFrames for result batches.
       for dataframe_for_batch in cur.fetch_pandas_batches():
         my_dataframe_processing_function(dataframe_for_batch)
  ```

## Serializing result batches

To move the result batches to other workers or nodes, you can serialize and deserialize the result batches. For example:

Copy code

```
import pickle

# Serialize a result batch from the first list.
pickled_batch = pickle.dumps(result_batch_list_1[1])

# At this point, you can move the serialized data to
# another worker/node.
...

# Deserialize the result batch for processing.
unpickled_batch = pickle.loads(pickled_batch)
```

## Working with result batches

The next sections explain how to work with [ResultBatch](/developer-guide/python-connector/python-connector-api#label-python-connector-resultbatch-object) objects:

- [Iterating over rows in a result batch](#label-python-connector-result-batch-iterate)
- [Materializing the rows in a result batch](#label-python-connector-result-batch-materialize)
- [Getting the number of rows and size of a result batch](#label-python-connector-result-batch-size-count)
- [Converting an arrow result batch to a PyArrow table or pandas DataFrame](#label-python-connector-result-batch-convert)

### Iterating over rows in a result batch

With a `ResultBatch` object, you can iterate over the rows that are part of that batch. For example:

Copy code

```
# Iterate over the list of result batches.
for batch in result_batch_list_1:
    # Iterate over the subset of rows in a result batch.
    for row in batch:
        print(row)
```

When you create an iterator of a `ResultBatch` object, the object fetches and converts the subset of rows for that batch.

### Materializing the rows in a result batch

To materialize the subset of rows in a result batch by passing that `ResultBatch` object to the `list()` function. For
example:

Copy code

```
# Materialize the subset of results for the first result batch
# in the list.
first_result_batch = result_batch_list_1[1]
first_result_batch_data = list(first_result_batch)
```

### Getting the number of rows and size of a result batch

If you need to determine the number of rows in a result batch and the size of the data, you can use
[rowcount](/developer-guide/python-connector/python-connector-api#label-python-connector-resultbatch-rowcount),
[compressed\_size](/developer-guide/python-connector/python-connector-api#label-python-connector-resultbatch-compressed-size),
and [uncompressed\_size](/developer-guide/python-connector/python-connector-api#label-python-connector-resultbatch-uncompressed-size) attributes of the `ResultBatch` object.
For example:

Copy code

```
# Get the number of rows in a result batch.
num_rows = first_result_batch.rowcount

# Get the size of the data in a result batch.
compressed_size = first_result_batch.compressed_size
uncompressed_size = first_result_batch.uncompressed_size
```

Note that these attributes are available before you iterate over the result batch. You don’t need to fetch the subset of rows for
the batch in order to get the values of these attributes.

### Converting an arrow result batch to a PyArrow table or pandas DataFrame

To convert an `ArrowResultBatch` to a PyArrow table or a pandas DataFrame, use the following methods:

- `to_pandas()`: Call this method to return a pandas DataFrame containing the rows in a `ArrowResultBatch`, if you have
  [installed the pandas-compatible version of the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-pandas#label-python-connector-pandas-install).
- `to_arrow()`: Call this method to return a PyArrow table containing the rows in a `ResultBatch`.

For example:

Copy code

```
with conn_cnx as con:
  with con.cursor() as cur:
    cur.execute("select col1 from table")
    batches = cur.get_result_batches()

    # Get the row from the ResultBatch as a pandas DataFrame.
    dataframe = batches[0].to_pandas()

    # Get the row from the ResultBatch as a PyArrow table.
    table = batches[0].to_arrow()
```
