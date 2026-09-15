# snow sql

Executes a Snowflake query. Use either query, filename, or input option. Query to execute can be specified using query option, filename option (all queries from file will be executed), or via stdin by piping output from another command. For example `cat my.sql | snow sql -i`. The command supports variable substitution that happens on the client side.

## Syntax

Copy code

```
snow sql
  --query <query>
  --filename <files>
  --stdin
  --variable <data_override>
  --retain-comments
  --single-transaction / --no-single-transaction
  --enable-templating <enabled_templating>
  --local-only
  --no-prompt-exit-repl
  --project <project_definition>
  --env <env_overrides>
  --connection <connection>
  --host <host>
  --port <port>
  --account <account>
  --user <user>
  --password <password>
  --authenticator <authenticator>
  --workload-identity-provider <workload_identity_provider>
  --private-key-file <private_key_file>
  --token <token>
  --token-file-path <token_file_path>
  --database <database>
  --schema <schema>
  --role <role>
  --warehouse <warehouse>
  --temporary-connection
  --mfa-passcode <mfa_passcode>
  --enable-diag
  --diag-log-path <diag_log_path>
  --diag-allowlist-path <diag_allowlist_path>
  --oauth-client-id <oauth_client_id>
  --oauth-client-secret <oauth_client_secret>
  --oauth-authorization-url <oauth_authorization_url>
  --oauth-token-request-url <oauth_token_request_url>
  --oauth-redirect-uri <oauth_redirect_uri>
  --oauth-scope <oauth_scope>
  --oauth-disable-pkce
  --oauth-enable-refresh-tokens
  --oauth-enable-single-use-refresh-tokens
  --client-store-temporary-credential
  --format <format>
  --verbose
  --debug
  --silent
  --enhanced-exit-codes
  --decimal-precision <decimal_precision>
```

## Arguments

None

## Options

`--query, -q TEXT`
:   Query to execute.

`--filename, -f FILE`
:   File to execute. Default: [].

`--stdin, -i`
:   Read the query from standard input. Use it when piping input to this command. Default: False.

`--variable, -D TEXT`
:   String in format of key=value. If provided the SQL content will be treated as template and rendered using provided data.

`--retain-comments`
:   Retains comments in queries passed to Snowflake. Default: False.

`--single-transaction / --no-single-transaction`
:   Connects with autocommit disabled. Wraps BEGIN/COMMIT around statements to execute them as a single transaction, ensuring all commands complete successfully or no change is applied. Default: False.

`--enable-templating [LEGACY%STANDARD%JINJA%ALL%NONE]`
:   Syntax used to resolve variables before passing queries to Snowflake. Default: [<\_EnabledTemplating.LEGACY: ‘LEGACY’>, <\_EnabledTemplating.STANDARD: ‘STANDARD’>].

`--local-only`
:   Restrict !source and !load to local files. When set, !source/!load directives that reference http:// or https:// URLs are rejected instead of being fetched. Use this flag in environments where SQL inputs should not trigger outbound network requests, or when running SQL files whose content should be reviewed locally before execution. [env var: SNOWFLAKE\_CLI\_SQL\_LOCAL\_ONLY | config: cli.sql\_local\_only].

`--no-prompt-exit-repl`
:   Do not prompt before exiting the REPL.

`-p, --project TEXT`
:   Path where the Snowflake project is stored. Defaults to the current working directory.

`--env TEXT`
:   String in the format key=value. Overrides variables from the env section used for templates. Default: [].

`--connection, -c, --environment TEXT`
:   Name of the connection, as defined in your *config.toml* file. Default: *default*.

`--host TEXT`
:   Host address for the connection. Overrides the value specified for the connection.

`--port INTEGER`
:   Port for the connection. Overrides the value specified for the connection.

`--account, --accountname TEXT`
:   Name assigned to your Snowflake account. Overrides the value specified for the connection.

`--user, --username TEXT`
:   Username to connect to Snowflake. Overrides the value specified for the connection.

`--password TEXT`
:   Snowflake password. Overrides the value specified for the connection.

`--authenticator TEXT`
:   Snowflake authenticator. Overrides the value specified for the connection.

`--workload-identity-provider TEXT`
:   Workload identity provider (AWS, AZURE, GCP, OIDC). Overrides the value specified for the connection.

`--private-key-file, --private-key-path TEXT`
:   Snowflake private key file path. Overrides the value specified for the connection.

`--token TEXT`
:   OAuth token to use when connecting to Snowflake.

`--token-file-path TEXT`
:   Path to file with an OAuth token to use when connecting to Snowflake.

`--database, --dbname TEXT`
:   Database to use. Overrides the value specified for the connection.

`--schema, --schemaname TEXT`
:   Database schema to use. Overrides the value specified for the connection.

`--role, --rolename TEXT`
:   Role to use. Overrides the value specified for the connection.

`--warehouse TEXT`
:   Warehouse to use. Overrides the value specified for the connection.

`--temporary-connection, -x`
:   Uses a connection defined with command-line parameters, instead of one defined in config. Default: False.

`--mfa-passcode TEXT`
:   Token to use for multi-factor authentication (MFA).

`--enable-diag`
:   Whether to generate a connection diagnostic report. Default: False.

`--diag-log-path TEXT`
:   Path for the generated report. Defaults to system temporary directory. Default: <system\_temporary\_directory>.

`--diag-allowlist-path TEXT`
:   Path to a JSON file that contains allowlist parameters.

`--oauth-client-id TEXT`
:   Value of client id provided by the Identity Provider for Snowflake integration.

`--oauth-client-secret TEXT`
:   Value of the client secret provided by the Identity Provider for Snowflake integration.

`--oauth-authorization-url TEXT`
:   Identity Provider endpoint supplying the authorization code to the driver.

`--oauth-token-request-url TEXT`
:   Identity Provider endpoint supplying the access tokens to the driver.

`--oauth-redirect-uri TEXT`
:   URI to use for authorization code redirection.

`--oauth-scope TEXT`
:   Scope requested in the Identity Provider authorization request.

`--oauth-disable-pkce`
:   Disables Proof Key for Code Exchange (PKCE). Default: *False*.

`--oauth-enable-refresh-tokens`
:   Enables a silent re-authentication when the current access token becomes outdated. Default: *False*.

`--oauth-enable-single-use-refresh-tokens`
:   Whether to opt-in to single-use refresh token semantics. Default: *False*.

`--client-store-temporary-credential`
:   Store the temporary credential.

`--format [TABLE|JSON|JSON_EXT|CSV]`
:   Specifies the output format. Default: TABLE.

`--verbose, -v`
:   Displays log entries for log levels *info* and higher. Default: False.

`--debug`
:   Displays log entries for log levels *debug* and higher; debug logs contain additional information. Default: False.

`--silent`
:   Turns off intermediate output to console. Default: False.

`--enhanced-exit-codes`
:   Differentiate exit error codes based on failure type. Default: False.

`--decimal-precision INTEGER`
:   Number of decimal places to display for decimal values. Uses Python’s default precision if not specified. [env var: SNOWFLAKE\_DECIMAL\_PRECISION].

`--help`
:   Displays the help text for this command.

## Usage notes

You can specify the SQL query to execute using one of the following options:

- Specify the query string using the `--query` option.
- Use the `--filename` option to execute one or more files containing a SQL query or queries. When you specify multiple files, all files are executed sequentially on a single connection. For example:

  - `snow sql -f myfile.sql`
  - `snow sql -f file1.sql -f file2.sql -f file3.sql`
- Specify the query as `stdin` and pipe it to the `snow sql` command, such as `cat my.sql | snow sql`.
- If your query contains special characters, such as the dollar sign in [SYSTEM functions](/sql-reference/functions-system), that you do not want the shell to interpret, you can do either of the following:

  - Enclose the query in single quotes instead of double quotes, as in:

    `snow sql -q 'SELECT SYSTEM$CLIENT_VERSION_INFO()'`
  - Escape the special character, as in:

    `snow sql -q "SELECT SYSTEM\$CLIENT_VERSION_INFO()"`
- Use variables for templating SQL queries with a combination of a `<% variable_name %>` placeholder in your SQL queries and a `-D` command-line option, in the form:

  Copy code

  ```
  snow sql -q "select * from my-database order by <% column_name %>" -D "column_name=Country"
  ```

  Note

  You can currently use the SnowSQL `&variable_name` and `<% variable_name %>` syntax for templates. However, Snowflake recommends using the `<% variable_name %>` syntax.
- Specify a scripting block in queries. For example:

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

  Note

  When specifying the scripting block directly on the Snowflake CLI command line, the `$$` delimiters might not work for some shells because they interpret that delimiter as something else. For example, the bash and zsh shells interpret it as the process ID (PID). To address this limitation, you can use the following alternatives:

  - If you still want to specify the scripting block on the command line, you can escape the `$$` delimiters, as in `\$\$`.
  - You can also put the scripting block with the default `$$` delimiters into a separate file and call it with the `snow sql -f filename` command.

### Formatting JSON output

The `--format` option provides two ways to display JSON:

- `JSON`: Returns JSON as quoted strings, similar to the following:

  Copy code

  ```
  snow sql --format json -q "SELECT PARSE_JSON('{\"name\": \"Alice\", \"age\": 30}') as json_col"
  ```

  ```
  [
    {
     "JSON_COL": "{\"name\": \"Alice\", \"age\": 30}"
    }
  ]
  ```
- `JSON_EXT`: Returns JSON as JSON objects, similar to the following:

  Copy code

  ```
  snow sql --format JSON_EXT -q "SELECT PARSE_JSON('{\"name\": \"Alice\", \"age\": 30}') as json_col"
  ```

  ```
  [
    {
   "JSON_COL": {
   "name": "Alice",
   "age": 30
    }
  ]
  ```

### Enhanced error codes

The `--enhanced-exit-codes` option provides information that helps identify whether problems result from query execution or from invalid command options. With this option, the `snow sql` command provides the following return codes:

- `0`: Successful execution
- `2`: Command parameter issues
- `5`: Query execution issues
- `1`: Other types of issues

After the command executes, you can use the `echo $?` shell command to see the return code.

In this example, the command contains both a query parameter (`-q 'select 1'`) and a query file parameter (`-f my.query`), which is an invalid parameter combination:

Copy code

```
snow sql --enhanced-exit-codes -q 'select 1' -f my.query

echo $?
```

```
2
```

The following examples show the effect of the `--enhanced-exit-codes` option when the command contains an invalid query (slect is misspelled):

- With the `--enhanced-exit-codes` option, the command returns a `5` exit code to indicate a query error:

  Copy code

  ```
  snow sql --enhanced-exit-codes -q 'slect 1'

  echo $?
  ```

  ```
  5
  ```
- Without the `--enhanced-exit-codes` option, the command returns a `1` exit code to indicate a generic (other) error:

  Copy code

  ```
  snow sql --enhanced-exit-codes -q 'slect 1'

  echo $?
  ```

  ```
  1
  ```

Alternatively, you can set the `SNOWFLAKE_ENHANCED_EXIT_CODES` environment variable to `1` to send the enhanced return codes for all `snow sql` commands.

### Interactive mode

The `snow sql` command supports an interactive mode that lets you enter SQL commands one at a time. Interactive mode provides the following features:

- Syntax highlighting

  ![Interactive mode syntax highlighting](/static/images/screens/snowcli/interactive-sql-syntax-highlight.png)
- Code completion while typing

  ![Interactive mode code completion](/static/images/screens/snowcli/interactive-sql-code-completion.png)
- Searchable history

  To search your command history, press `CTRL-R`:

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
  │ Welcome to Snowflake-CLI REPL                                                   │
  │ Type 'exit' or 'quit' to leave                                                  │
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

### Multiple commands in a single transaction

The `--single-transaction` option lets you enter multiple SQL commands to execute as an all-or-nothing set of commands.
By executing commands in a single transaction, you can ensure that all of the commands complete successfully before committing any of the changes.
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
  snow sql -q "insert into my_tbl values (123); insert into my_tbl values (124); select BAD;" --single-transaction
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

## Examples

- The following example uses the SQL [SYSTEM$CLIENT\_VERSION\_INFO](/sql-reference/functions/system_client_version_info) system function to return version information about the clients and drivers.

  Copy code

  ```
  snow sql --query 'SELECT SYSTEM$CLIENT_VERSION_INFO();'
  ```

  ```
  select current_version();
  +-------------------+
  | CURRENT_VERSION() |
  |-------------------|
  | 8.25.1            |
  +-------------------+
  ```
- The following example shows how you can specify a database using a client-side variable:

  Copy code

  ```
  snow sql -q "select * from <% database %>.logs" -D "database=dev"
  ```

  When executed, the command substitutes the value `dev` in the `<% database %>` variable to create the `dev.logs` identifier and then sends the `select * from dev.logs` SQL query to Snowflake for processing.

  Note

  You can currently use the SnowSQL `&variable_name` and `<% variable_name %>` syntax for templates. However, Snowflake recommends using the `<% variable_name %>` syntax.
- This example shows how to pass in environment variables using the `--env` option:

  Copy code

  ```
  snow sql -q "select '<% ctx.env.test %>'" --env test=value_from_cli
  ```
- By default, Snowflake CLI removes comments in SQL query from the output. The following example uses the `--retain-comments` option to include the comments in the query results.

  Assume the `example.sql` file contains the following statements and comment:

  Copy code

  ```
  select 'column1';
  -- My comment
  select 'column2';
  ```

  When you execute the following command, `-- My comment` appears in the query results.

  Copy code

  ```
  snow sql -f example.sql --retain-comments
  ```

  Copy code

  ```
  select 'column1';
  +-----------+
  | 'COLUMN1' |
  |-----------|
  | ABC       |
  +-----------+

  -- My comment
  select 'column2';
  +-----------+
  | 'COLUMN2' |
  |-----------|
  | 123       |
  +-----------+
  ```
