# Executing statements

Statements can be executed by calling the `connection.execute()` method. The `execute()` method accepts an `options`
object that can be used to specify the SQL text and a `complete` callback.
The `complete` callback is invoked when a statement has finished executing and the result is ready to be consumed:

> Copy code
>
> ```
> const statement = connection.execute({
>   sqlText: 'CREATE DATABASE testdb',
>   complete: function (err, stmt, rows) {
>     if (err) {
>       console.error(`Failed to execute statement due to the following error: ${err.message}`);
>     } else {
>       console.log(`Successfully executed statement: ${stmt.getSqlText()}`);
>     }
>   }
> });
> ```

Note

The maximum payload size of a single request is 128 MB.

## Execute queries asynchronously

The Snowflake Node.js Driver supports asynchronous queries (that is, queries that return control to the user before the query completes). You can start a query, then use polling to determine when the query has completed. After the query completes, you can read the result set.

You enable asynchronous queries by including `asyncExec: true` in the `connection.execute` method.

The following example shows how to execute queries asynchronously using a `Promise`.

Copy code

```
let queryId;

// 1. Execute query with asyncExec set to true
await new Promise((resolve) => {
  connection.execute({
    sqlText: "CALL SYSTEM$WAIT(3, 'SECONDS')",
    asyncExec: true,
    complete: async function (err, stmt, rows) {
      queryId = stmt.getQueryId(); // Get the query ID
      resolve();
    }
  });
});

// 2. Get results using the query ID
const statement = await connection.getResultsFromQueryId({ queryId: queryId });
await new Promise((resolve, reject) => {
  const stream = statement.streamRows();
  stream.on('error', err => {
    reject(err);
  });
  stream.on('data', row => {
    console.log(row);
  });
  stream.on('end', () => {
    resolve();
  });
});
```

You can also use callbacks to monitor asynchronous queries, as shown in the following example.

1. Enable asynchronous queries by including `asyncExec: true` in the `connection.execute` method.

   Copy code

   ```
   // 1. Execute query with asyncExec set to true
   connection.execute({
     sqlText: "CALL SYSTEM$WAIT(3, 'SECONDS')",
     asyncExec: true,
     complete: async function (err, stmt, rows) {
    const queryId = stmt.getQueryId();

    // 2. Get results using the query ID
    connection.getResultsFromQueryId({
      queryId: queryId,
      complete: async function (err, _stmt, rows) {
        console.log(rows);
      }
    });
     }
   });
   ```
2. Check on the status of the query, which was submitted to be executed asynchronously.

   Copy code

   ```
   let queryId;

   // 1. Execute query with asyncExec set to true
   await new Promise((resolve, reject) => {
     const statement = connection.execute({
    sqlText: "CALL SYSTEM$WAIT(3, 'SECONDS')",
    asyncExec: true,
    complete: async function (err, stmt, rows) {
      queryId = statement.getQueryId();
      resolve();
    }
     });
   });

   // 2. Check query status until it's finished executing
   const seconds = 2;
   let status = await connection.getQueryStatus(queryId);
   while (connection.isStillRunning(status)) {
     console.log(`Query status is ${status}, timeout for ${seconds} seconds`);

     await new Promise((resolve) => {
    setTimeout(() => resolve(), 1000 * seconds);
     });

     status = await connection.getQueryStatus(queryId);
   }

   console.log(`Query has finished executing, status is ${status}`);
   ```

## Execute a batch of SQL statements (multi-statement support)

With version 1.6.18 and later of the Node.js connector, you can send
a batch of SQL statements separated by semicolons to be executed in a single request.

Note

- Executing multiple statements in a single query requires that a valid warehouse is available in a session.
- By default, Snowflake returns an error for queries issued with multiple statements to protect against SQL injection attacks.
  Executing multiple statements in a single query increases the risk of SQL injection. Snowflake recommends using it sparingly.
  You can reduce the risk by using the `MULTI_STATEMENT_COUNT` parameter to specify the number of statements to be executed, which makes it more difficult to inject a statement by appending to it.

For more information about these types of attacks, see [SQL injection](https://en.wikipedia.org/wiki/SQL_injection).

You can execute multiple statements as a batch in the same way you execute queries with single statements, except that the query string
contains multiple statements separated by semicolons. Note that multiple statements execute sequentially, not in parallel.
The `MULTI_STATEMENT_COUNT` parameter specifies the exact number of statements the batch contains.

For example, if you set `MULTI_STATEMENT_COUNT=3`, a batch statement must include precisely three
statements. If you submit a batch statement with any other number of statements, the Node.js driver rejects the request. You can set
`MULTI_STATEMENT_COUNT=0` to allow batch queries to contain any number of statements. However, be aware that using this value
reduces the protection against SQL injection attacks.

You can set this parameter at the session level using the following command, or you can set the value
separately each time you submit a query.

Copy code

```
ALTER SESSION SET multi_statement_count = <n>
```

By setting the value the session level, you do not need to set it when you execute each time you execute a batch statement.
The following example sets the number of statements at the session level to three and then executes three SQL statements:

> Copy code
>
> ```
> const statement = connection.execute({
>   sqlText: 'ALTER SESSION SET multi_statement_count=0',
>   complete: function (err, stmt, rows) {
>     if (err) {
>       console.error(`Failed to execute statement due to the following error: ${err.message}`);
>     } else {
>       testMulti();
>     }
>   }
> });
>
> function testMulti() {
>   console.log('select bind execute.');
>   const selectStatement = connection.execute({
>     sqlText: 'create or replace table test(n int); insert into test values(1), (2); select * from test order by n',
>     complete: function (err, stmt, rows) {
>       if (err) {
>         console.error(`Failed to execute statement due to the following error: ${err.message}`);
>       } else {
>         console.log('==== complete');
>         console.log(`==== sqlText=${stmt.getSqlText()}`);
>         if (stmt.hasNext()) {
>           stmt.NextResult();
>         } else {
>           // do something else, for example close the connection
>         }
>       }
>     }
>   });
> }
> ```

You can also set the number of statements in a batch each time you execute a multi-statement query by setting
`MULTI_STATEMENT_COUNT` as a parameter for the `connection.execute` function. The following example sets the number of
statements to three for the batch and includes three SQL statements in the batch query:

> Copy code
>
> ```
> // connection needs to be already set up
> connection.connect((err, conn) => {
>   if (err) {
>     console.error(`Unable to connect: ${err.message}`);
>   } else {
>     console.log(`Successfully connected to Snowflake, connection id ${conn.getId()}`);
>     testMulti();
>   }
> });
>
> function testMulti() {
>   console.log('execute multi-statement query');
>   connection.execute({
>     sqlText: 'create or replace table test(n int); insert into test values(1), (2); select * from test order by n',
>     parameters: { MULTI_STATEMENT_COUNT: 3 },
>     complete: function (err, stmt, rows) {
>       if (err) {
>         console.error(`Failed to execute statement: ${err.message}`);
>       } else {
>         console.log('==== complete');
>         console.log(`==== sqlText=${stmt.getSqlText()}`);
>         if (rows) {
>           const stream = stmt.streamRows();
>           console.log(`====QueryId=${stmt.getQueryId()}`);
>
>           stream.on('data', row => {
>             console.log(row);
>           });
>           stream.on('end', () => {
>             console.log('done');
>           });
>         }
>
>         if ('hasNext' in stmt && stmt.hasNext()) {
>           stmt.NextResult();
>         } else {
>           connection.destroy(err1 => {
>             if (err1) {
>               console.error(`Unable to disconnect: ${err1.message}`);
>             } else {
>               console.log(`Disconnected connection with id: ${connection.getId()}`);
>             }
>           });
>         }
>       }
>     }
>   });
> }
> ```

## Binding statement parameters

Occasionally, you might want to [bind](/sql-reference/bind-variables) data in a statement with a placeholder.
Executing statements in this manner is useful because it helps prevent SQL injection attacks. Consider the
following statement:

> Copy code
>
> ```
> connection.execute({
>   sqlText: 'SELECT c1 FROM (SELECT 1 AS c1 UNION ALL SELECT 2 AS c1) WHERE c1 = 1;'
> });
> ```

You can achieve the same result using the following bindings:

> Copy code
>
> ```
> connection.execute({
>   sqlText: 'SELECT c1 FROM (SELECT :1 AS c1 UNION ALL SELECT :2 AS c1) WHERE c1 = :1;',
>   binds: [1, 2]
> });
> ```

The `?` syntax for bindings is also supported:

> Copy code
>
> ```
> connection.execute({
>   sqlText: 'SELECT c1 FROM (SELECT ? AS c1 UNION ALL SELECT ? AS c1) WHERE c1 = ?;',
>   binds: [1, 2, 1]
> });
> ```

Note

There is an upper limit to the size of data that you can bind, or that you can combine in a batch.
For details, see [Limits on Query Text Size](/user-guide/query-size-limits).

## Binding an array for bulk insertions

Binding an array of data is supported for bulk INSERT operation. Pass an array of arrays as follows:

> Copy code
>
> ```
> connection.execute({
>   sqlText: 'INSERT INTO t(c1, c2, c3) values(?, ?, ?)',
>   binds: [[1, 'string1', 2.0], [2, 'string2', 4.0], [3, 'string3', 6.0]]
> });
> ```

Note

Binding a large array will impact performance and might be rejected if the size of data is too large to be handled by the server.

You can also bind arrays of `VARIANT` data. To illustrate, assume you create a table with a column of `VARIANT` data, as follows:

Copy code

```
create or replace table test(id int, foo variant);
```

You could then execute the following script:

Copy code

```
// standard stuff like defining connection, etc
const statement = connection.execute({
  // table columns are id: int, foo: variant
  sqlText: 'insert into test_db.public.test select value:id, value:foo from table(flatten(parse_json(?)))',
  binds: [JSON.stringify([
    { id: 1, foo: [{ a: '1', b: '2' }] },
    { id: 2, foo: [{ c: '3', d: '4' }] }
  ])],
  complete: function (err, stmt, rows) {
    if (err) {
      console.error(`Failed to execute statement due to the following error: ${err.message}`);
    } else {
      console.log(`[queryID ${statement.getStatementId()}, requestId ${statement.getRequestId()}] Number of rows produced: ${rows.length}`);
      // rest of the code
    }
  }
});
```

## Canceling statements

A statement can be canceled by calling the `statement.cancel()` method:

> Copy code
>
> ```
> statement.cancel((err, stmt) => {
>   if (err) {
>     console.error(`Unable to abort statement due to the following error: ${err.message}`);
>   } else {
>     console.log('Successfully aborted statement');
>   }
> });
> ```

## Resubmitting requests

If you are unsure whether Snowflake successfully executed an SQL statement, perhaps due to a network error or timeout,
you can resubmit the same statement using its request ID. For example, suppose you submit an INSERT command to add data but
did not receive an acknowledgement in a timely
manner, so you don’t know what happened with the command. In this scenario, you don’t just want to execute the same
command as a new command
because it could result in executing the command twice, producing data duplication.

By including the request ID in the SQL statement,
you can avoid the potential for data duplication. Resubmitting the request with the request ID from the
initial request ensures that the resubmitted command executes only if the initial request failed. For more information, refer to
[Resubmitting a request to execute SQL statements](/developer-guide/sql-api/submitting-requests#label-sql-api-generating-request-id).

Note

To resubmit a query using a request ID, you must use the same connection that generated the request ID. If you want to
retrieve the result of query from a different connection, refer to [RESULT\_SCAN](/sql-reference/functions/result_scan).

The following code samples demonstrate how you can save and use a request ID to resubmit a statement. When you execute a statement,
you can use the `getRequestId()` function to retrieve the ID of the submitted request. You can then use that ID to execute the same
statement at a later time. The following example executes an INSERT statement and saves its request ID in the `requestId` variable.

> Copy code
>
> ```
> let requestId;
> connection.execute({
>   sqlText: 'INSERT INTO testTable VALUES (1);',
>   complete: function (err, stmt, rows) {
>     const stream = stmt.streamRows();
>     requestId = stmt.getRequestId(); // Retrieves the request ID
>     stream.on('data', row => {
>       console.log(row);
>     });
>     stream.on('end', () => {
>       console.log('done');
>     });
>   }
> });
> ```

If you do not receive an acknowledgement that the command executed successfully, you can resubmit the request using the saved
request ID as shown below.

> Copy code
>
> ```
> connection.execute({
>   sqlText: 'INSERT INTO testTable VALUES (1);',  // optional
>   requestId: requestId,  // Uses the request ID from before
>   complete: function (err, stmt, rows) {
>     const stream = stmt.streamRows();
>     stream.on('data', row => {
>       console.log(row);
>     });
>     stream.on('end', () => {
>       console.log('done');
>     });
>   }
> });
> ```

If you choose to resubmit a request with a `requestId` and `sqlText`, be aware of the following interactions:

- If the `requestId` already exists, meaning it matches a previous request, the command ignores the `sqlText` query and resubmits
  the query from the original command.
- If the `requestId` does not exist, meaning it does not match a previous request, the command executes the `sqlText` query.
