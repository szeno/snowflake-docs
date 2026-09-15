# Executing SQL statements

The [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql) command lets you execute ad-hoc SQL queries or files containing SQL queries using the following options:

- To execute an ad-hoc query, use the `-q` command-line option. For example:

  Copy code

  ```
  snow sql -q "SELECT * FROM FOO;"
  ```
- To execute a file containing a SQL query, use the `-f` command-line option to specify the path to the file. For example:

  Copy code

  ```
  snow sql -f my_query.sql
  ```

The `snow sql` command can also execute multiple statements; in that case, multiple result sets are returned. For example, running:

Copy code

```
snow sql -q "select 'a', 'b'; select 'c', 'd';"
```

results in the following output:

```
select 'a', 'b';
+-----------+
| 'A' | 'B' |
|-----+-----|
| a   | b   |
+-----------+

select 'c', 'd';
+-----------+
| 'C' | 'D' |
|-----+-----|
| c   | d   |
+-----------+
```

You can also execute [scripting blocks](/developer-guide/snowflake-scripting/running-examples) in Snowflake CLI with a caveat relating to the `$$` delimiter.

For example:

Copy code

```
EXECUTE IMMEDIATE $$
-- Snowflake Scripting code
DECLARE
  radius_of_circle FLOAT;
  area_of_circle FLOAT;
BEGIN
  radius_of_circle := 3;
  area_of_circle := pi() * radius_of_circle * radius_of_circle;
  RETURN area_of_circle;
END;
$$
;
```

Some operating systems interpret `$$` as a process ID (PID) instead of recognizing it as a scripting block delimiter. To address this limitation, you can use the following alternatives:

> - If you still want to specify the scripting block on the command line, you can escape the `$$` delimiters, as in `\$\$`.
> - You can also put the scripting block with the default `$$` delimiters into a separate file and call it with the `snow sql -f <filename>` command.

For more information, see the [snow sql](/developer-guide/snowflake-cli/command-reference/sql-commands/sql) command.

## Using variables for SQL templates

In certain situations, you might want to change your SQL queries based on the context. The `snow sql` command supports client-side variable substitution that lets you use variables in the command that are resolved locally before submitting the query. Variables in the SQL string take the form `<% variable_name %>`, and the `-D` (or `--variable`) option specifies the value of the variable.

> Note
>
> You can currently use the SnowSQL `&variable_name` and `<% variable_name %>` syntax for templates. However, Snowflake recommends using the `<% variable_name %>` syntax.

For example, to specify a database using a client-side variable, you can enter a command similar to the following:

Copy code

```
snow sql -q "select * from <% database %>.logs" -D "database=dev"
```

When executed, the command substitutes the value `dev` in the `<% database %>` variable to create the `dev.logs` table reference and then sends the `select * from dev.logs` SQL query to Snowflake for processing.

You can also specify multiple variable inputs, as shown:

Copy code

```
snow sql \
-q "grant usage on database <% database %> to <% role %>" \
-D "database=dev" \
-D "role=eng_rl"
```

This example generates the following SQL query:

Copy code

```
grant usage on database dev to eng_rl
```

The `--enable-templating` option lets you specify which templating syntaxes are resolved in a SQL query. Snowflake CLI supports the following syntaxes:

- `STANDARD`: Support the standard Snowflake CLI variable syntax (`<% variable_name %>`). Enabled by default.
- `LEGACY`: Support the SnowSQL variable syntax (`&{ variable_name }` or `&variable_name`). Enabled by default.
- `JINJA`: Support the Jinja variable syntax (`{{ variable_name }}`). Disabled by default.
- `ALL`: Allow all supported syntaxes. Disabled by default.
- `NONE`: Do not support templating. Disabled by default.

The following examples illustrate different ways to support templating:

- Disable templating, so that neither of the query variables is resolved:

  Copy code

  ```
  snow sql --enable-templating NONE -q "select '<% not_resolved %> &not_resolved'"
  ```
- Allow JINJA and STANDARD templating, while disallowing LEGACY templating:

  Copy code

  ```
  snow sql --enable-templating JINJA --enable-templating STANDARD -q "select '<% resolved %> {{ resolved }} &not_resolved'"
  ```
- Enable all syntaxes, so the SQL query resolves all three syntaxes:

  Copy code

  ```
  snow sql --enable-templating ALL -q "select '<% resolved %> {{ resolved }}'"
  snow sql --enable-templating ALL -q "select '&resolved {{ resolved }}'"
  ```

Note

JINJA variables, if enabled, are resolved after STANDARD and LEGACY variables.

## Storing variables in the `snowflake.yml` project definition file

Specifying variables as `snow sql` command-line options might not always be practical, or perhaps you might not want to specify sensitive values on the command line. In such cases, you can define variables and values in the `snowflake.yml` project definition file. Then you can just specify the variable names in the form `<% ctx.env.<variable_name> %>` instead of using the `-D "<variable> = <value>"` option.

Using the example from the previous section, you could store the database and role variables in the `snowflake.yml` file and change the query to:

Copy code

```
snow sql -q "grant usage on database <% ctx.env.database %> to <% ctx.env.role %>"
```

In this example, the `snow sql` command looks for the variable definitions in the project definition file and extracts the values without making them visible on the command line.
The `snowflake.yml` file should be located either in the current working directory or in the location specified with the `-p` option.

For more information about storing these values in the project definition file, see [Use variables in SQL](/developer-guide/snowflake-cli/project-definitions/use-sql-variables).

## Executing SQL queries asynchronously

Snowflake CLI lets you execute one or more SQL queries asynchronously. Instead of waiting for a result, the `snow sql` command schedules the queries at Snowflake and returns a query ID. After a query finishes, you can get the result using the [!result](#label-snowcli-sql-query-result-cmd) query command or the SQL [RESULT\_SCAN](/sql-reference/functions/result_scan) command.

To execute a SQL query asynchronously, end the query with `;>` instead of `;`, as shown:

Copy code

```
snow sql -q 'select "My async query" ;>'
```

The following example executes a single query asynchronously:

Copy code

```
snow sql -q "select 'This is async query';>"
```

```
select 'This is async query'
+--------------------------------------+
| scheduled query ID                   |
|--------------------------------------|
| 01bc3011-080f-f2d7-0001-c1be14bae7c2 |
+--------------------------------------+
```

You can then use the returned query ID in the [!result](#label-snowcli-sql-query-result-cmd) query command to display the query result:

Copy code

```
snow sql -q '!result 01bc3011-080f-f2d7-0001-c1be14bae7c2'
```

```
+-----------------------+
| 'THIS IS ASYNC QUERY' |
|-----------------------|
| This is async query   |
+-----------------------+
```

You can also execute multiple queries in the query string, both asynchronously and synchronously, as shown:

Copy code

```
snow sql -q "select 'This is async query';> select 'Not an async query'; select 'Another async query';>"
```

```
select 'This is async query'
+--------------------------------------+
| scheduled query ID                   |
|--------------------------------------|
| 01bc3b8c-0109-2e81-0000-0f2d0e5a4a32 |
+--------------------------------------+

select 'Not an async query';
+----------------------+
| 'NOT AN ASYNC QUERY' |
|----------------------|
| Not an async query   |
+----------------------+

select 'Another async query'
+--------------------------------------+
| scheduled query ID                   |
|--------------------------------------|
| 01bc3b8c-0109-2e81-0000-0f2d0e5a4a36 |
+--------------------------------------+
```

## Working with SQL query commands

Snowflake CLI provides the following commands that you can use inside your SQL queries:

- [!source](#label-snowcli-sql-query-source-cmd), which executes SQL in local files or URLs.
- [!queries](#label-snowcli-sql-query-queries-cmd), which lists all SQL queries.
- [!result](#label-snowcli-sql-query-result-cmd), which displays the result of a SQL query.
- [!abort](#label-snowcli-sql-query-abort-cmd), which aborts an active SQL query.
- [!edit](#label-snowcli-sql-query-edit-cmd), which opens an external editor to modify and execute SQL commands.

Tip

If you enclose your SQL query in double quotes (`""`) instead of single quotes (`''`), you might
need to escape the exclamation point (`!`) based on which shell you use.

### Execute SQL in local files or URLs

You can use the `!source` query command in your SQL query to execute SQL in local files or a URL-based file. For example, the following command executes all SQL commands in a local file named `my_sql_code.sql`:

Copy code

```
snow sql -q '!source my_sql_code.sql'
```

You can also nest `!source` commands in the SQL files, such as:

Copy code

```
select emp_id FROM employees;
!source code_file_2.sql
```

In this example, the command executes the SELECT query and then executes the SQL commands in the `code_file_2.sql` file.

To execute multiple SQL files using `!source`, place each directive on a separate line in a wrapper file. For example, create a file named `run_all.sql` with the following contents:

Copy code

```
!source script1.sql
!source script2.sql
!source script3.sql
```

Then execute the wrapper file:

Copy code

```
snow sql -f run_all.sql
```

All three files are executed sequentially on a single connection. Alternatively, you can use multiple `-f` options to achieve the same result without a wrapper file, such as `snow sql -f script1.sql -f script2.sql -f script3.sql`.

Before executing `!source` queries, Snowflake CLI does the following:

- Evaluates variable substitutions and templates.
- Reads the contents of all nested files to ensure that no recursion occurs.

Caution

`snow sql` can execute SQL from remote URLs. Only execute SQL from sources you trust.

When the variables and templates are resolved and no recursion is detected, the command sends the code to Snowflake for execution.

Note

If you use double quotes (`""`) instead of single quotes (`''`) around a `!source` query, you might need to escape the `!` (`\!`) depending on which shell you use.

The following examples illustrate different ways you can execute source files.

- Execute code in a local file.

  This example assumes you have a simple query in a local SQL file.

  Copy code

  ```
  cat code_to_execute.sql
  ```

  ```
  select 73;
  ```

  To execute the code in the file, enter the following command:

  Copy code

  ```
  snow sql -q '!source code_to_execute.sql'
  ```

  ```
  select 73;
  +----+
  | 73 |
  |----|
  | 73 |
  +----+
  ```
- Execute code in a URL-based file.

  This example assumes you have the same simple query in a SQL file at a URL.

  To execute the code in the file, enter the following command:

  Copy code

  ```
  snow sql -q '!source https://trusted-host/trusted-content.sql'
  ```

  ```
  select 73;
  +----+
  | 73 |
  |----|
  | 73 |
  +----+
  ```
- Execute code that uses variable substitution and templating.

  This example assumes you have a query in a local SQL file that uses a template variable.

  Copy code

  ```
  cat code_with_variable.sql
  ```

  ```
  select '<% ctx.env.Message %>';
  ```

  To execute the code in the file, enter the following command that defines the variable value:

  Copy code

  ```
  snow sql -q '!source code_&value.sql;' -D value=with_variable --env Message='Welcome !'
  ```

  ```
  select 'Welcome !';
  +-------------+
  | 'WELCOME !' |
  |-------------|
  | Welcome !   |
  +-------------+
  ```

Note

The `!source` command supports the legacy `!load` alias.

### List all SQL queries

The `!queries` query command lists all queries for an account. By default, the command lists the 25 most recent queries executed in the current session.

For example, the following `!queries` query command returns the three most recent queries for a specific user:

> Copy code
>
> ```
> snow sql -q '!queries user=user1 amount=3'
> ```
>
> ```
> +-------------------------------------------------------------------------------------------------------------------------------------+
> | QUERY ID                             | SQL TEXT                                                           | STATUS    | DURATION_MS |
> |--------------------------------------+--------------------------------------------------------------------+-----------+-------------|
> | 01bc3040-080f-f4f9-0001-c1be14bb603a | select current_version();                                          | SUCCEEDED | 3858        |
> | 01bc303d-080f-f4e9-0001-c1be14bb1812 | SELECT SYSTEM$CANCEL_QUERY('01bc3011-080f-f2d7-0001-c1be14bae7c2') | SUCCEEDED | 564         |
> | 01bc3011-080f-f2d7-0001-c1be14bae7c2 | select 'This is async query'                                       | SUCCEEDED | 931         |
> +-------------------------------------------------------------------------------------------------------------------------------------+
> ```

You can use the following filters to narrow the list of returned queries:

| Filter | Default | Description |
| --- | --- | --- |
| amount (integer) | 25 | Number of recent queries to return (default: 25). |
| session (boolean) | N/A | If provided, return only queries executed in the current session. |
| warehouse (string) | None | Return queries executed only on the specified warehouse. |
| user (string) | None | Return queries executed only by the specified user. |
| duration (milliseconds) | 0 | Return only queries that took at least the specified number of milliseconds. |
| start\_date (string) | None | Return only queries executed after the specified date. Date is expected to be provided in ISO format (for example `2025-01-01T09:00:00`). |
| end\_date (string) | None | Return only queries executed before the specified date. Date is expected to be provided in ISO format (for example `2025-01-01T09:00:00`). |
| start (integer) | None | Return only queries executed after the specified Unix timestamp (in milliseconds). |
| end (integer) | None | Return only queries executed before the specified Unix timestamp (in milliseconds). |
| status (enum) | None | Return only queries in one of the following statuses:   - RUNNING - SUCCEEDED - FAILED - BLOCKED - QUEUED - ABORTED |
| type | None | Return only queries of one of the following types:   - SELECT - INSERT - UPDATE - DELETE - MERGE - MULTI\_TABLE\_INSERT - COPY - COMMIT - ROLLBACK - BEGIN\_TRANSACTION - SHOW - GRANT - CREATE - ALTER |

Expand

Show lessSee more

The following examples return queries using different filters:

- Return the 25 most recent queries executed in the current session:

  Copy code

  ```
  snow sql -q 'select 42; select 15; !queries session'
  ```
- Return the 20 most recent queries executed in the account:

  Copy code

  ```
  snow sql -q '!queries amount=20'
  ```
- Return the 20 most recent queries executed in the account that took longer than 200 milliseconds to run:

  Copy code

  ```
  snow sql -q '!queries amount=20 duration=200'
  ```
- Return the 25 most recent queries executed in the specified warehouse:

  Copy code

  ```
  snow sql -q '!queries warehouse=mywh'
  ```

### Return a completed SQL query result

The `!result` query command returns the result of a completed query, given its query ID. You can obtain the query ID in the following ways:

- Check the [Query History page](/user-guide/ui-snowsight-activity) in Snowsight.
- Run the `!queries` SQL query command.
- Use the ID returned by an [asynchronous query](#label-snowcli-sql-async).

Copy code

```
snow sql -q '!result 01bc3011-080f-f2d7-0001-c1be14bae7c2'
```

```
+-----------------------+
| 'THIS IS ASYNC QUERY' |
|-----------------------|
| This is async query   |
+-----------------------+
```

### Abort an active SQL query

The `!abort` query command aborts an active query, given its query ID. You can obtain the query ID in the following ways:

- Check the [Query History page](/user-guide/ui-snowsight-activity) in Snowsight.
- Run the `!queries` SQL query command.
- Use the ID returned by an [asynchronous query](#label-snowcli-sql-async).

Copy code

```
snow sql -q '!abort 01bc3011-080f-f2d7-0001-c1be14bae7c2'
```

```
+-------------------------------------------------------------+
| SYSTEM$CANCEL_QUERY('01BC3011-080F-F2D7-0001-C1BE14BAE7C2') |
|-------------------------------------------------------------|
| Identified SQL statement is not currently executing.        |
+-------------------------------------------------------------+
```

### Open an external editor to modify and execute SQL commands

The `!edit` query command opens an external editor where you can modify SQL commands to execute when you exit the editor. The editor is specified in the `EDITOR` environment variable or, if the environment variable is not set, the default system editor is used.

To enter commands in an external editor, follow these steps:

1. If not already defined in your shell, set the `EDITOR` environment variable to your preferred text editor.
2. Enter the `snow sql` command:

   Copy code

   ```
   snow sql
   ```
3. At the `>` prompt, enter the `!edit` command:

   Copy code

   ```
   > !edit
   ```

   The command opens the specified text editor.
4. Enter your SQL commands in the editor, as shown:

   Copy code

   ```
   SELECT current_user() ;
   ```
5. Save the file and exit the editor.

   The commands you entered are displayed, as shown:

   ```
   ✓ Edited SQL loaded into prompt. Modify as needed or press Enter to execute.
   > select current_user();
   ```
6. To execute the commands, press `ENTER`.

   The command output is displayed, as shown:

   ```
   +----------------+
   | CURRENT_USER() |
   |----------------|
   | USER1          |
   +----------------+
   ```

## Entering multiple commands in a single transaction

The `--single-transaction` option lets you enter multiple SQL commands to execute as an all-or-nothing set of commands.
By executing commands in a single transaction, you can ensure that all of the commands are completed successfully before committing any of the changes.
If any of the commands fail, none of the changes from the successful commands persist.

The following examples show successful and unsuccessful transactions:

- Successful command execution

  Copy code

  ```
  snow sql -q "insert into my_tbl values (123); insert into my_tbl values (124);" --single-transaction
  ```

  ```
  BEGIN;
  +----------------------------------+
  | status                           |
  |----------------------------------|
  | Statement executed successfully. |
  +----------------------------------+

  insert into my_tbl values (123);
  +-------------------------+
  | number of rows inserted |
  |-------------------------|
  | 1                       |
  +-------------------------+

  insert into my_tbl values (124);
  +-------------------------+
  | number of rows inserted |
  |-------------------------|
  | 1                       |
  +-------------------------+

  COMMIT
  +----------------------------------+
  | status                           |
  |----------------------------------|
  | Statement executed successfully. |
  +----------------------------------+
  ```

  You can then verify that the commands were committed to the database:

  Copy code

  ```
  snow sql -q "select count(*) from my_tbl"
  ```

  ```
  select count(*) from my_tbl
  +----------+
  | COUNT(*) |
  |----------|
  | 2        |
  +----------+
  ```
- Unsuccessful single transaction

  Copy code

  ```
  snow sql -c patcli -q "insert into my_tbl values (123); insert into my_tbl values (124); select BAD;" --single-transaction
  ```

  ```
  BEGIN;
  +----------------------------------+
  | status                           |
  |----------------------------------|
  | Statement executed successfully. |
  +----------------------------------+

  insert into my_tbl values (123);
  +-------------------------+
  | number of rows inserted |
  |-------------------------|
  | 1                       |
  +-------------------------+

  insert into my_tbl values (124);
  +-------------------------+
  | number of rows inserted |
  |-------------------------|
  | 1                       |
  +-------------------------+

  select BAD;
  ╭─ Error ───────────────────────────────────────────────────────────────────────────────╮
  │ 000904 (42000): 01bc3b84-0810-0247-0001-c1be14ee11ce: SQL compilation error: error    │
  │ line 1 at position 7                                                                  │
  │ invalid identifier 'BAD'                                                              │
  ╰───────────────────────────────────────────────────────────────────────────────────────╯
  ```

> You can then verify that the commands were not committed to the database:
>
> > Copy code
> >
> > ```
> > snow sql -q "select count(*) from my_tbl"
> > ```
> >
> > ```
> > select count(*) from my_tbl
> > +----------+
> > | COUNT(*) |
> > |----------|
> > | 0        |
> > +----------+
> > ```

## Entering SQL commands in interactive mode

The `snow sql` command supports an interactive mode that lets you enter SQL commands one at a time. Interactive mode provides the following features:

- Syntax highlighting

  ![Interactive mode syntax highlighting](/static/images/screens/snowcli/interactive-sql-syntax-highlight.png)
- Code completion while typing

  ![Interactive mode code completion](/static/images/screens/snowcli/interactive-sql-code-completion.png)
- Searchable history

  Pressing `CTRL-R` lets you search your command history:

  ![Interactive mode searchable history](/static/images/screens/snowcli/interactive-sql-history.png)
- Multi-line input

  Pressing `ENTER` on a line that does not end with a semicolon (`;`) moves the cursor to the next line for more commands until a statement ends with a semicolon.

  ![Interactive mode multi-line input](/static/images/screens/snowcli/interactive-sql-multiline.png)

To use interactive mode, enter the `snow sql` command followed by `ENTER`, as shown:

Copy code

```
snow sql
```

The command opens a sub-shell with a `>` prompt where you can enter SQL commands interactively:

```
$ snow sql
  ╭───────────────────────────────────────────────────────────────────────────────────╮
  │ Welcome to Snowflake-CLI REPL                                                     │
  │ Type 'exit' or 'quit' to leave                                                    │
  ╰───────────────────────────────────────────────────────────────────────────────────╯
  >
```

You can then enter SQL commands, as shown:

Copy code

```
> create table my_table (c1 int);
```

```
+-------------------------------------+
| status                              |
|-------------------------------------|
| Table MY_TABLE successfully created.|
+-------------------------------------+
```

Note

You must end each SQL statement with a semicolon (`;`).

To exit interactive mode, enter `exit`, `quit`, or `CTRL-D`.
