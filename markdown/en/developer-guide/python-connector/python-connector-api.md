# Python Connector API

The Snowflake Connector for Python implements the Python Database API v2.0 specification
(PEP-249). This topic covers the standard
API and the Snowflake-specific extensions.

For more information, see the [PEP-249](https://www.python.org/dev/peps/pep-0249/) documentation.

## Module: `snowflake.connector`

The main module is `snowflake.connector`, which creates a `Connection` object and provides
`Error` classes.

### Constants

apilevel
:   String constant stating the supported API level. The connector supports API
    `"2.0"`.

threadsafety
:   Integer constant stating the level of thread safety the interface supports. The
    Snowflake Connector for Python supports level `2`, which states that threads can share
    the module and connections.

paramstyle
:   String constant stating the type of parameter marker formatting expected
    by the interface. The connector supports the `"pyformat"` type by default, which applies to
    Python extended format codes (e.g. `...WHERE name=%s` or `...WHERE name=%(name)s`).
    `Connection.connect` can override `paramstyle` to change the bind variable formats to
    `"qmark"` or `"numeric"`, where the variables are `?` or `:N`, respectively.

    For example:

    Copy code

    ```
    format: .execute("... WHERE my_column = %s", (value,))
    pyformat: .execute("... WHERE my_column = %(name)s", {"name": value})
    qmark: .execute("... WHERE my_column = ?", (value,))
    numeric: .execute("... WHERE my_column = :1", (value,))
    ```

    Note

    The binding variable occurs on the client side if `paramstyle` is `"pyformat"` or
    `"format"`, and on the server side if `"qmark"` or `"numeric"`. Currently,
    there is no significant difference between those options in terms of performance or features
    because the connector doesn’t support compiling SQL text followed by
    multiple executions. Instead, the `"qmark"` and `"numeric"` options align with the query text
    compatibility of other drivers (i.e. JDBC, ODBC, Go Snowflake Driver), which support server
    side bindings with the variable format `?` or `:N`.

### Functions

connect(parameters…)
:   Purpose:
    :   Constructor for creating a connection to the database. Returns a `Connection` object.

        By default, autocommit mode is enabled (i.e. if the connection is closed, all changes are committed). If you need a
        transaction, use the [BEGIN](/sql-reference/sql/begin) command to start the transaction, and [COMMIT](/sql-reference/sql/commit)
        or [ROLLBACK](/sql-reference/sql/rollback) to commit or roll back any changes.

    Parameters:
    :   The valid input parameters are:

        | Parameter | Required | Description |
        | --- | --- | --- |
        | `account` | Yes | Your account identifier. The account identifier does not include the `snowflakecomputing.com` suffix.     For details and examples, see [Usage Notes](#label-account-format-info) (in this topic). |
        | `user` | Yes | Login name for the user. |
        | `password` | Yes | Password for the user. |
        | `application` |  | Name that identifies the application making the connection. |
        | `region` |  | \*Deprecated\* This description of the parameter is for backwards compatibility only.. |
        | `host` |  | Host name. |
        | `port` |  | Port number (`443` by default). |
        | `database` |  | Name of the default database to use. After login, you can use [USE DATABASE](/sql-reference/sql/use-database) to change the database. |
        | `schema` |  | Name of the default schema to use for the database. After login, you can use [USE SCHEMA](/sql-reference/sql/use-schema) to change the schema. |
        | `role` |  | Name of the default role to use. After login, you can use [USE ROLE](/sql-reference/sql/use-role) to change the role. |
        | `warehouse` |  | Name of the default warehouse to use. After login, you can use [USE WAREHOUSE](/sql-reference/sql/use-warehouse) to change the warehouse.. |
        | `passcode_in_password` |  | `False` by default. Set this to `True` if the MFA (Multi-Factor Authentication) passcode is embedded in the login password. |
        | `passcode` |  | The passcode provided by Duo when using MFA (Multi-Factor Authentication) for login. |
        | `private_key` |  | The private key used for authentication. For more information, see [Using key-pair authentication and key-pair rotation](/developer-guide/python-connector/python-connector-connect#label-python-key-pair-authn-rotation). |
        | `private_key_file` |  | Specifies the path to the private key file for the specified user. See [Using key-pair authentication and key-pair rotation](/developer-guide/python-connector/python-connector-connect#label-python-key-pair-authn-rotation). |
        | `private_key_file_pwd` |  | Specifies the passphrase to decrypt the private key file for the specified user. See [Using key-pair authentication and key-pair rotation](/developer-guide/python-connector/python-connector-connect#label-python-key-pair-authn-rotation). |
        | `autocommit` |  | `None` by default, which honors the Snowflake parameter [AUTOCOMMIT](/sql-reference/parameters). Set to `True` or `False` to enable or disable autocommit mode in the session, respectively. |
        | `client_fetch_use_mp` |  | When set to `True`, it enables multi-processed fetching, which for many cases should reduce the fetching time. Default: `False`. |
        | `client_prefetch_threads` |  | Number of threads used to download the results sets (`4` by default). Increasing the value improves fetch performance but requires more memory. |
        | `client_session_keep_alive` |  | To keep the session active indefinitely (even if there is no activity from the user), set this to `True`. When setting this to `True`, call the `close` method to terminate the thread properly; otherwise, the process might hang. The default value depends on the version of the connector that you are using:   - **Version 2.4.6 and later:** `None` by default.   When the value is `None`, the [CLIENT\_SESSION\_KEEP\_ALIVE](/sql-reference/parameters#label-client-session-keep-alive) session parameter takes precedence.     To override the session parameter, pass in `True` or `False` for this argument. - **Version 2.4.5 and earlier:** `False` by default.   When the value is `False` (either by specifying the value explicitly or by omitting the argument), the [CLIENT\_SESSION\_KEEP\_ALIVE](/sql-reference/parameters#label-client-session-keep-alive) session parameter takes precedence.   Passing `client_session_keep_alive=False` to the `connect` method does not override the value `TRUE` in the `CLIENT_SESSION_KEEP_ALIVE` session parameter. |
        | `login_timeout` |  | Timeout in seconds for login. By default, 60 seconds. The login request gives up after the timeout length if the HTTP response is “success”. |
        | `network_timeout` |  | Timeout in seconds for all other operations. By default, none/infinite. A general request gives up after the timeout length if the HTTP response is not “success”. |
        | `ocsp_response_cache_filename` |  | URI for the OCSP response cache file. By default, the OCSP response cache file is created in the cache directory:   - Linux: `~/.cache/snowflake/ocsp_response_cache` - macOS: `~/Library/Caches/Snowflake/ocsp_response_cache` - Windows: `%USERPROFILE%AppDataLocalSnowflakeCachesocsp_response_cache`   To locate the file in a different directory, specify the path and file name in the URI (e.g. `file:///tmp/my_ocsp_response_cache.txt`).. |
        | `authenticator` |  | Authenticator for Snowflake:   - `snowflake` (default) to use the internal Snowflake authenticator. - `externalbrowser` to authenticate using your web browser and Okta, AD FS, or any other SAML 2.0-compliant identity provider (IdP) that has been defined for your account.   You can enable the `SNOWFLAKE_AUTH_FORCE_SERVER` environment variable to force re-authentication through the browser even if a valid SSO session exists. For more information, see [Using connection caching to minimize the number of prompts for authentication — \*Optional\*](/user-guide/admin-security-fed-auth-use#label-browser-based-sso-connection-caching).   - `https://<okta_account_name>.okta.com` (i.e. the URL endpoint for your Okta account) to authenticate through native Okta. - `oauth` to authenticate using OAuth. You must also specify the `token` parameter and set its value to the OAuth access token. - `username_password_mfa` to authenticate with MFA token caching. For more details, see [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching). - `OAUTH_AUTHORIZATION_CODE` to use the OAuth 2.0 Authorization Code flow. - `OAUTH_CLIENT_CREDENTIALS` to use the OAuth 2.0 Client Credentials flow. - `WORKLOAD_IDENTITY` to authenticate with the [workload identity federation (WIF)](/user-guide/workload-identity-federation) authenticator.   If the value is not `snowflake`, the user and password parameters must be your login credentials for the IdP. |
        | `validate_default_parameters` |  | `False` by default. If `True`, then:   - Raise an exception if the specified database, schema, or warehouse doesn’t exist. - Print a warning to stderr if an invalid argument name or an argument value of the wrong data type is passed. |
        | `paramstyle` |  | `pyformat` by default for client side binding. Specify `qmark` or `numeric` to change bind variable formats for server side binding. |
        | `timezone` |  | `None` by default, which honors the Snowflake parameter [TIMEZONE](/sql-reference/parameters). Set to a valid time zone (e.g. `America/Los_Angeles`) to set the session time zone. |
        | `arrow_number_to_decimal` |  | `False` by default, which means that [NUMBER](/sql-reference/data-types-numeric#label-data-type-number) column values are returned as double-precision floating point numbers (`float64`).     Set this to `True` to return DECIMAL column values as decimal numbers (`decimal.Decimal`) when calling the `fetch_pandas_all()` and `fetch_pandas_batches()` methods.     This parameter was introduced in version 2.4.3 of the Snowflake Connector for Python. |
        | `socket_timeout` |  | Timeout in seconds for socket-level read and connect requests. For more information, see [Managing connection timeouts](/developer-guide/python-connector/python-connector-connect#label-python-manage-timeouts). |
        | `backoff_policy` |  | Name of the generator function that defines how long to wait between retries. For more information, see [Managing connection backoff policies for retries](/developer-guide/python-connector/python-connector-connect#label-python-manage-retries). |
        | `enable_connection_diag` |  | Whether to generate a connectivity diagnostic report. Default is `False`. |
        | `connection_diag_log_path` |  | Absolute path for the location of the diagnostic report. Used only if `enable_connection_diag` is `True`. Default is the default temp directory for your operating system, such as `/tmp` for Linux or Mac. |
        | `connection_diag_allowlist_path` |  | Absolute path to a JSON file containing the output of `SYSTEM$ALLOWLIST()` or `SYSTEM$ALLOWLIST_PRIVATELINK()`. Required only if the user defined in the connection does not have permission to run the system allowlist functions or if connecting to the account URL fails. |
        | `iobound_tpe_limit` |  | Size of the preprocess\_tpe and postprocess threadpool executors (TPEs). By default, the value is the lesser of the number of files and the number of CPU cores. |
        | `unsafe_file_write` |  | Specifies which file permissions to assign to files downloaded from a stage using a GET command. `False` (default) sets the file permissions to `600`, which means only the owner can access the files. `True` sets the permissions to `644`, which gives the owner read and write permissions and read-only permissions to everyone else. For more information, see [Downloading data](/developer-guide/python-connector/python-connector-example#label-python-connector-downloading-data). |
        | `oauth_client_id` |  | Value of `client id` provided by the Identity Provider for Snowflake integration (Snowflake security integration metadata). |
        | `oauth_client_secret` |  | Value of the `client secret` provided by the Identity Provider for Snowflake integration (Snowflake security integration metadata). |
        | `oauth_authorization_url` |  | Identity Provider endpoint supplying the authorization code to the driver. When using Snowflake as an Identity Provider ,this value is derived from the `server` or `account` parameters. |
        | `oauth_token_request_url` |  | Identity Provider endpoint supplying the access tokens to the driver. When using Snowflake as an Identity Provider ,this value is derived from the `server` or `account` parameters. |
        | `oauth_scope` |  | Scope requested in the Identity Provider authorization request. By default, it is derived from the role. When multiple scopes are required, the value should be a space-separated list of multiple scopes. |
        | `oauth_redirect_uri` |  | URI to use for authorization code redirection (Snowflake security integration metadata). Default: `http://127.0.0.1:{randomAvailablePort}`. |
        | `oauth_disable_pkce` |  | Disables Proof Key for Code Exchange (PKCE), a security enhancement that ensures that even if malicious attackers intercept an Authorization Code, they won’t be able to change it to a valid access token. |
        | `oauth_enable_refresh_token` |  | Enables a silent re-authentication when the actual access token becomes outdated, providing it’s supported by the Authorization Server and `client_store_temporary_credential` is set to `True`. |
        | `oauth_enable_single_use_refresh_tokens` |  | Whether to opt-in to single-use refresh token semantics. |
        | `oauth_credentials_in_body` |  | Whether or not credentials should be sent in the body for OAuth authentication. Default is `False`. |
        | `oauth_socket_uri` |  | URI to use for the OAuth socket connection. Default: `http://127.0.0.1:{randomAvailablePort}`. |
        | `client_store_temporary_credential` |  | Whether or not to allow clients to cache SSO credentials on the client side. For this setting to take effect, caching must be enabled on the server. For more information, see [Using connection caching to minimize the number of prompts for authentication — \*Optional\*](/user-guide/admin-security-fed-auth-use#label-browser-based-sso-connection-caching). Default is `False`. |
        | `client_request_mfa_token` |  | Whether or not to allow clients to cache MFA credentials on the client side For this setting to take effect, caching must be enabled on the server. For more information, see [Using MFA token caching to minimize the number of prompts during authentication — \*optional\*](/user-guide/security-mfa#label-mfa-token-caching). Default is `False`. |
        | `workload_identity_provider` |  | Platform of the workload identity provider. Possible values include: `AWS`, `AZURE`, `GCP`, and `OIDC`. |
        | `workload_identity_impersonation_path` |  | An array of strings that provide an identity chain to use when connecting to Snowflake. Array elements are either a full service account address or a service account’s unique ID.  Impersonation works by following each array entry in order to obtain a token that allows authorization of the next service account. Each account in the identity chain needs permissions to impersonate the next account only. The final account in the list obtains your Snowflake connection token and is used to connect to Snowflake.  Account impersonation is supported only for Google Cloud and AWS workloads. |
        | `unsafe_skip_file_permissions_check` |  | Whether to skip permissions checks on file access. Default is `False`. |
        | `cert_revocation_check_mode` |  | Certificate revocation check mode. For accepted values, see [CertRevocationCheckMode](#label-python-crl-validation-options). |
        | `allow_certificates_without_crl_url` |  | Whether to allow certificates without certificate revocation list distribution points. Default is `False`. |
        | `crl_connection_timeout_ms` |  | The connection timeout for certificate revocation list downloads, in milliseconds. Default is `3000`. |
        | `crl_read_timeout_ms` |  | The read timeout for certificate revocation list downloads, in milliseconds. Default is `3000`. |
        | `crl_cache_validity_hours` |  | How long the certificate revocation list cache is valid, in hours. Default is `24`. |
        | `enable_crl_cache` |  | Whether or not to enable certificate revocation list caching. Default is `True`. |
        | `enable_crl_file_cache` |  | Whether to cache certificate revocation list to disk. Applies only when `enable_crl_cache` is `True`. Default is `True`. |
        | `crl_cache_dir` |  | The directory to store the certificate revocation list cache in. Applies only when `enable_crl_file_cache` is `True`. |
        | `crl_cache_removal_delay_days` |  | The amount of time to keep expired certificate revocation list files on disk, in days. Default is `7`. |
        | `crl_cache_cleanup_interval_hours` |  | How often to clean the certificate revocation list cache, in hours. Default is `1`. |
        | `crl_cache_start_cleanup` |  | Whether to run certificate revocation list cleanup activities in the background. Default is `False`. |
        | `ocsp_root_certs_dict_lock_timeout` |  | Timeout for acquiring the lock on the OCSP root certs dictionary, in seconds. A value of `-1` disables timeouts. Default is `-1`. |
        | `no_proxy` |  | Comma-separated list of hostnames that should bypass the proxy. You can use an asterisk (`*`) in the hostnames. For more information, see [Using a proxy server](/developer-guide/python-connector/python-connector-connect#label-python-using-a-proxy-server). |

        Expand

        Show lessSee more

### Attributes

Error, Warning, …
:   All exception classes defined by the Python database API standard. The Snowflake
    Connector for Python provides the attributes `msg`, `errno`, `sqlstate`,
    `sfqid` and `raw_msg`.

### Usage notes for the `account` parameter (for the `connect` method)

For the required `account` parameter, specify your [account identifier](/user-guide/gen-conn-config).

Note that the account identifier does not include the `snowflakecomputing.com` domain name. Snowflake automatically
appends this when creating the connection.

The following example uses the [account name as an identifier](/user-guide/admin-account-identifier#label-account-name-using) for the account `myaccount` in
the organization `myorganization`.

Copy code

```
ctx = snowflake.connector.connect(
    user='<user_name>',
    password='<password>',
    account='myorganization-myaccount',
    ... )
```

The following example uses the [account locator](/user-guide/admin-account-identifier#label-account-locator) `xy12345` as the account identifier:

Copy code

```
ctx = snowflake.connector.connect(
    user='<user_name>',
    password='<password>',
    account='xy12345',
    ... )
```

Note that this example uses an account in the AWS US West (Oregon) region. If the account is in a different region or if the
account uses a different cloud provider, you need to
[specify additional segments after the account locator](/user-guide/admin-account-identifier#label-account-locator).

## Object: `Connection`

A `Connection` object holds the connection and session information to keep the database connection active. If it is closed or the session expires, any subsequent operations will fail.

### Methods

autocommit(True|False)
:   Purpose:
    :   Enables or disables autocommit mode. By default, autocommit is enabled (`True`).

close()
:   Purpose:
    :   Closes the connection. If a transaction is still open when the connection is closed, the
        changes are rolled back.

        Closing the connection explicitly removes the active session from the server; otherwise, the active session continues until it is eventually purged from the server, limiting the number of concurrent queries.

        For example:

        Copy code

        ```
        # context manager ensures the connection is closed
        with snowflake.connector.connect(...) as con:
            con.cursor().execute(...)

        # try & finally to ensure the connection is closed.
        con = snowflake.connector.connect(...)
        try:
            con.cursor().execute(...)
        finally:
            con.close()
        ```

commit()
:   Purpose:
    :   If autocommit is disabled, commits the current transaction. If autocommit is enabled, this
        method is ignored.

rollback()
:   Purpose:
    :   If autocommit is disabled, rolls back the current transaction. If autocommit is enabled,
        this method is ignored.

cursor()
:   Purpose:
    :   Constructor for creating a `Cursor` object. The return values from
        `fetch*()` calls will be a single sequence or list of sequences.

cursor(snowflake.connector.DictCursor)
:   Purpose:
    :   Constructor for creating a `DictCursor` object. The return values from
        `fetch*()` calls will be a single dict or list of dict objects. This
        is useful for fetching values by column name from the results.

execute\_string(sql\_text, remove\_comments=False, return\_cursors=True)
:   Purpose:
    :   Execute one or more SQL statements passed as strings. If `remove_comments` is set to `True`,
        comments are removed from the query. If `return_cursors` is set to `True`, this
        method returns a sequence of `Cursor` objects in the order of execution.

    Example:
    :   This example shows executing multiple commands in a single string and then using the sequence of
        cursors that is returned:

        Copy code

        ```
        cursor_list = connection1.execute_string(
            "SELECT * FROM testtable WHERE col1 LIKE 'T%';"
            "SELECT * FROM testtable WHERE col2 LIKE 'A%';"
            )

        for cursor in cursor_list:
           for row in cursor:
              print(row[0], row[1])
        ```

    Note

    Methods such as `execute_string()` that allow multiple SQL statements in a single
    string are vulnerable to SQL injection attacks. Avoid using string concatenation,
    or functions such as Python’s `format()` function, to dynamically compose a SQL statement
    by combining SQL with data from users unless you have validated the user data. The example
    below demonstrates the problem:

    Copy code

    ```
    # "Binding" data via the format() function (UNSAFE EXAMPLE)
    value1_from_user = "'ok3'); DELETE FROM testtable WHERE col1 = 'ok1'; select pi("
    sql_cmd = "insert into testtable(col1) values('ok1'); "                  \
              "insert into testtable(col1) values('ok2'); "                  \
              "insert into testtable(col1) values({col1});".format(col1=value1_from_user)
    # Show what SQL Injection can do to a composed statement.
    print(sql_cmd)

    connection1.execute_string(sql_cmd)
    ```

    The dynamically-composed statement looks like the following (newlines have
    been added for readability):

    Copy code

    ```
    insert into testtable(col1) values('ok1');
    insert into testtable(col1) values('ok2');
    insert into testtable(col1) values('ok3');
    DELETE FROM testtable WHERE col1 = 'ok1';
    select pi();
    ```

    If you are combining SQL statements with strings entered by untrusted users,
    then it is safer to bind data to a statement than to compose a string.
    The `execute_string()` method doesn’t take binding parameters, so to bind parameters
    use `Cursor.execute()` or `Cursor.executemany()`.

execute\_stream(sql\_stream, remove\_comments=False)
:   Purpose:
    :   Execute one or more SQL statements passed as a stream object. If `remove_comments` is set to `True`,
        comments are removed from the query. This generator yields each `Cursor` object as SQL statements run.

        If `sql_stream` ends with comment lines, you must set `remove_comments` to `True`, similar to the following:

        Copy code

        ```
        sql_script = """
        -- This is first comment line;
        select 1;
        select 2;
        -- This is comment in middle;
        -- With some extra comment lines;
        select 3;
        -- This is the end with last line comment;
        """
        sql_stream = StringIO(sql_script)
        with con.cursor() as cur:
                for result_cursor in con.execute_stream(sql_stream,remove_comments=True):
                    for result in result_cursor:
                        print(f"Result: {result}")
        ```

get\_query\_status(query\_id)
:   Purpose:
    :   Returns the status of a query.

    Parameters:
    :   `query_id`

        > The ID of the query. See [Retrieving the Snowflake query ID](/developer-guide/python-connector/python-connector-example#label-python-connector-retrieve-query-id).

    Returns:
    :   Returns the `QueryStatus` object that represents the status of the query.

    Example:
    :   See [Checking the status of a query](/developer-guide/python-connector/python-connector-example#label-python-connector-check-query-status).

get\_query\_status\_throw\_if\_error(query\_id)
:   Purpose:
    :   Returns the status of a query. If the query results in an error, this method raises a `ProgrammingError` (as the
        `execute()` method would).

    Parameters:
    :   `query_id`

        > The ID of the query. See [Retrieving the Snowflake query ID](/developer-guide/python-connector/python-connector-example#label-python-connector-retrieve-query-id).

    Returns:
    :   Returns the `QueryStatus` object that represents the status of the query.

    Example:
    :   See [Checking the status of a query](/developer-guide/python-connector/python-connector-example#label-python-connector-check-query-status).

is\_valid()
:   Purpose:
    :   Returns `True` if the connection is stable enough to receive queries.

is\_still\_running(query\_status)
:   Purpose:
    :   Returns `True` if the query status indicates that the query has not yet completed or is still in process.

    Parameters:
    :   `query_status`

        > The `QueryStatus` object that represents the status of the query. To get this object for a query, see
        > [Checking the status of a query](/developer-guide/python-connector/python-connector-example#label-python-connector-check-query-status).

    Example:
    :   See [Checking the status of a query](/developer-guide/python-connector/python-connector-example#label-python-connector-check-query-status).

is\_an\_error(query\_status)
:   Purpose:
    :   Returns `True` if the query status indicates that the query resulted in an error.

    Parameters:
    :   `query_status`

        > The `QueryStatus` object that represents the status of the query. To get this object for a query, see
        > [Checking the status of a query](/developer-guide/python-connector/python-connector-example#label-python-connector-check-query-status).

    Example:
    :   See [Checking the status of a query](/developer-guide/python-connector/python-connector-example#label-python-connector-check-query-status).

### Attributes

expired
:   Tracks whether the connection’s master token has expired.

messages
:   The list object including sequences (exception class, exception value) for all
    messages received from the underlying database for this connection.

    The list is cleared automatically by any method call.

errorhandler
:   Read/Write attribute that references an error handler to call in case an
    error condition is met.

    The handler must be a Python callable that accepts the following arguments:

    > `errorhandler(connection, cursor, errorclass, errorvalue)`

Error, Warning, …
:   All exception classes defined by the Python database API standard.

## Object: `Cursor`

A `Cursor` object represents a database cursor for execute and fetch operations.
Each cursor has its own attributes, `description` and `rowcount`, such that
cursors are isolated.

### Methods

close()
:   Purpose:
    :   Closes the cursor object.

describe(command [, parameters][, timeout][, file\_stream])
:   Purpose:
    :   Returns metadata about the result set without executing a database command. This returns the same metadata that is
        available in the `description` attribute after executing a query.

        This method was introduced in version 2.4.6 of the Snowflake Connector for Python.

    Parameters:
    :   See the parameters for the `execute()` method.

    Returns:
    :   Returns a list of [ResultMetadata](#label-python-connector-resultmetadata-object) objects that describe the columns
        in the result set.

    Example:
    :   See [Retrieving column metadata](/developer-guide/python-connector/python-connector-example#label-python-connector-column-metadata).

execute(command [, parameters][, timeout][, file\_stream])
:   Purpose:
    :   Prepares and executes a database command.

    Parameters:
    :   `command`

        > A string containing the SQL statement to execute.

        `parameters`

        > (Optional) If you used parameters for [binding data](/developer-guide/python-connector/python-connector-example#label-python-connector-binding-data) in the SQL
        > statement, set this to the list or dictionary of variables that should be bound to those parameters.
        >
        > For more information about mapping the Python data types for the variables to the SQL data types of the corresponding
        > columns, see [Data type mappings for and bindings](#label-python-connector-data-type-mappings).

        `timeout`

        > (Optional) Number of seconds to wait for the query to complete. If the query has not completed after this time has
        > passed, the query should be aborted.

        `file_stream`

        > (Optional) When executing a PUT command, you can use this parameter to upload an in-memory file-like object (e.g. the
        > I/O object returned from the Python `open()` function), rather than a file on the filesystem. Set this
        > parameter to that I/O object.
        >
        > When specifying the URI for the data file in the PUT command:
        >
        > - You can use any directory path. The directory path that you specify in the URI is ignored.
        > - For the filename, specify the name of the file that should be created on the stage.
        >
        > For example, to upload a file from a file stream to a file named:
        >
        > Copy code
        >
        > ```
        > @mystage/myfile.csv
        > ```
        >
        > use the following call:
        >
        > Copy code
        >
        > ```
        > cursor.execute(
        >     "PUT file://this_directory_path/is_ignored/myfile.csv @mystage",
        >     file_stream=<io_object>)
        > ```

    Returns:
    :   Returns the reference of a `Cursor` object.

executemany(command, seq\_of\_parameters)
:   Purpose:
    :   Prepares a database command and executes it against all parameter sequences
        found in `seq_of_parameters`. You can use this method to
        [perform a batch insert operation](/developer-guide/python-connector/python-connector-example#label-python-connector-binding-batch-inserts).

    Parameters:
    :   `command`

        > The command is a string containing the code to execute.
        > The string should contain one or more placeholders (such as
        > question marks) for [Binding data](/developer-guide/python-connector/python-connector-example#label-python-connector-binding-data).
        >
        > For example:
        >
        > Copy code
        >
        > ```
        > "insert into testy (v1, v2) values (?, ?)"
        > ```

        `seq_of_parameters`

        > This should be a sequence (list or tuple) of lists or tuples. See the example code below for example
        > sequences.

    Returns:
    :   Returns the reference of a `Cursor` object.

    Example:
    :   Copy code

        ```
        # This example uses qmark (question mark) binding, so
        # you must configure the connector to use this binding style.
        from snowflake import connector
        connector.paramstyle='qmark'

        stmt1 = "create table testy (V1 varchar, V2 varchar)"
        cs.execute(stmt1)

        # A list of lists
        sequence_of_parameters1 = [ ['Smith', 'Ann'], ['Jones', 'Ed'] ]
        # A tuple of tuples
        sequence_of_parameters2 = ( ('Cho', 'Kim'), ('Cooper', 'Pat') )

        stmt2 = "insert into testy (v1, v2) values (?, ?)"
        cs.executemany(stmt2, sequence_of_parameters1)
        cs.executemany(stmt2, sequence_of_parameters2)
        ```

    Internally, multiple `execute` methods are called and the result set from the
    last `execute` call will remain.

    Note

    The `executemany` method can only be used to execute a single parameterized SQL statement
    and pass multiple bind values to it.

    Executing multiple SQL statements separated by a semicolon in one `execute` call is not supported.
    Instead, issue a separate `execute` call for each statement.

execute\_async(…)
:   Purpose:
    :   Prepares and submits a database command for asynchronous execution.
        See [Performing an asynchronous query](/developer-guide/python-connector/python-connector-example#label-python-connector-querying-data-asynchronous).

    Parameters:
    :   This method uses the same parameters as the `execute()` method.

    Returns:
    :   Returns the reference of a `Cursor` object.

    Example:
    :   See [Examples of asynchronous queries](/developer-guide/python-connector/python-connector-example#label-python-connector-asynchronous-query-examples).

fetch\_arrow\_all()
:   Purpose:
    :   This method fetches all the rows in a cursor and loads them into a PyArrow table.

    Parameters:
    :   `force_microsecond_precision`

        > When `True`, all timestamp columns are converted to microsecond precision, ensuring consistent schema across all batches. This feature is useful when your data contains timestamps outside the nanosecond range (1677-2262), such as ’9999-12-31’ or ’0001-01-01’. When `False` (default), precision is determined per-batch based on the data, which might cause pyarrow schema mismatch errors when combining batches. Note that enabling this truncates sub-microsecond precision (scale 7-9).

    Returns:
    :   Returns a PyArrow table containing all the rows from the result set.

        If there are no rows, this returns None.

    Example:
    :   See [Distributing workloads that fetch results with the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-distributed-fetch).

fetch\_arrow\_batches()
:   Purpose:
    :   This method fetches a subset of the rows in a cursor and delivers them to a PyArrow table.

    Parameters:
    :   `force_microsecond_precision`

        > When `True`, all timestamp columns are converted to microsecond precision, ensuring consistent schema across all batches. This feature is useful when your data contains timestamps outside the nanosecond range (1677-2262), such as ’9999-12-31’ or ’0001-01-01’. When `False` (default), precision is determined per-batch based on the data, which might cause pyarrow schema mismatch errors when combining batches. Note that enabling this truncates sub-microsecond precision (scale 7-9).

    Returns:
    :   Returns a PyArrow table containing a subset of the rows from the result set.

        Returns None if there are no more rows to fetch.

    Example:
    :   See [Distributing workloads that fetch results with the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-distributed-fetch).

get\_result\_batches()
:   Purpose:
    :   Returns a list of [ResultBatch](#label-python-connector-resultbatch-object) objects that you can use to fetch a
        subset of rows from the result set.

    Parameters:
    :   None.

    Returns:
    :   Returns a list of [ResultBatch](#label-python-connector-resultbatch-object) objects or `None` if the query has
        not finished executing.

    Example:
    :   See [Distributing workloads that fetch results with the Snowflake Connector for Python](/developer-guide/python-connector/python-connector-distributed-fetch).

get\_results\_from\_sfqid(query\_id)
:   Purpose:
    :   Retrieves the results of an asynchronous query or a previously submitted synchronous query.

    Parameters:
    :   `query_id`

        > The ID of the query. See [Retrieving the Snowflake query ID](/developer-guide/python-connector/python-connector-example#label-python-connector-retrieve-query-id).

    Example:
    :   See [Using the query ID to retrieve the results of a query](/developer-guide/python-connector/python-connector-example#label-python-connector-retrieve-results).

fetchone()
:   Purpose:
    :   Fetches the next row of a query result set and returns a single sequence/dict or
        `None` when no more data is available.

fetchmany([size=cursor.arraysize])
:   Purpose:
    :   Fetches the next rows of a query result set and returns a list of
        sequences/dict. An empty sequence is returned when no more rows are available.

fetchall()
:   Purpose:
    :   Fetches all or remaining rows of a query result set and returns a list of
        sequences/dict.

fetch\_pandas\_all()
:   Purpose:
    :   This method fetches all the rows in a cursor and loads them into a pandas DataFrame.

    Parameters:
    :   `force_microsecond_precision`

        > When `True`, all timestamp columns are converted to microsecond precision, ensuring consistent schema across all batches. This feature is useful when your data contains timestamps outside the nanosecond range (1677-2262), such as ’9999-12-31’ or ’0001-01-01’. When `False` (default), precision is determined per-batch based on the data, which might cause pyarrow schema mismatch errors when combining batches. Note that enabling this truncates sub-microsecond precision (scale 7-9).

    Returns:
    :   Returns a DataFrame containing all the rows from the result set.

        For more information about pandas data frames, see the [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) documentation .

        If there are no rows, this returns `None`.

    Usage Notes:
    :   - This method is not a complete replacement for the `read_sql()` method of pandas; this method is to provide
          a fast way to retrieve data from a SELECT query and store the data in a pandas DataFrame.
        - Currently, this method works only for SELECT statements.

    Examples:
    :   Copy code

        ```
        ctx = snowflake.connector.connect(
                  host=host,
                  user=user,
                  password=password,
                  account=account,
                  warehouse=warehouse,
                  database=database,
                  schema=schema,
                  protocol='https',
                  port=port)

        # Create a cursor object.
        cur = ctx.cursor()

        # Execute a statement that will generate a result set.
        sql = "select * from t"
        cur.execute(sql)

        # Fetch the result set from the cursor and deliver it as the pandas DataFrame.
        df = cur.fetch_pandas_all()

        # ...
        ```

fetch\_pandas\_batches()
:   Purpose:
    :   This method fetches a subset of the rows in a cursor and delivers them to a pandas DataFrame.

    Parameters:
    :   `force_microsecond_precision`

        > When `True`, all timestamp columns are converted to microsecond precision, ensuring consistent schema across all batches. This feature is useful when your data contains timestamps outside the nanosecond range (1677-2262), such as ’9999-12-31’ or ’0001-01-01’. When `False` (default), precision is determined per-batch based on the data, which might cause pyarrow schema mismatch errors when combining batches. Note that enabling this truncates sub-microsecond precision (scale 7-9).

    Returns:
    :   Returns a DataFrame containing a subset of the rows from the result set.

        For more information about pandas data frames, see the [pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) documentation.

        Returns `None` if there are no more rows to fetch.

    Usage Notes:
    :   - Depending upon the number of rows in the result set, as well as the number of rows specified in the method
          call, the method might need to be called more than once, or it might return all rows in a single batch if
          they all fit.
        - This method is not a complete replacement for the `read_sql()` method of pandas; this method is to provide
          a fast way to retrieve data from a SELECT query and store the data in a pandas DataFrame.
        - Currently, this method works only for SELECT statements.

    Examples:
    :   Copy code

        ```
        ctx = snowflake.connector.connect(
                  host=host,
                  user=user,
                  password=password,
                  account=account,
                  warehouse=warehouse,
                  database=database,
                  schema=schema,
                  protocol='https',
                  port=port)

        # Create a cursor object.
        cur = ctx.cursor()

        # Execute a statement that will generate a result set.
        sql = "select * from t"
        cur.execute(sql)

        # Fetch the result set from the cursor and deliver it as the pandas DataFrame.
        for df in cur.fetch_pandas_batches():
            my_dataframe_processing_function(df)

        # ...
        ```

**iter**()
:   Returns self to make cursors compatible with the iteration protocol.

### Attributes

description
:   Read-only attribute that returns metadata about the columns in the result set.

    This attribute is set after you call the `execute()` method to execute the query. (In version 2.4.6 or later, you can
    retrieve this metadata without executing the query by calling the `describe()` method.)

    This attribute is set to one of the following:

    - **Versions 2.4.5 and earlier:** This attribute is set to a list of tuples.
    - **Versions 2.4.6 and later:** This attribute is set to a list of
      [ResultMetadata](#label-python-connector-resultmetadata-object) objects.

    Each tuple or `ResultMetadata` object contains the metadata that describes a column in the result set. You can access
    the metadata by index or, in versions 2.4.6 and later, by `ResultMetadata` object attribute:

    | Index of Value | ResultMetadata Attribute | Description |
    | --- | --- | --- |
    | `0` | `name` | Column name. |
    | `1` | `type_code` | Internal [type code](#label-python-connector-type-codes). |
    | `2` | `display_size` | (Not used. Same as internal\_size.) |
    | `3` | `internal_size` | Internal data size. |
    | `4` | `precision` | Precision of numeric data. |
    | `5` | `scale` | Scale for numeric data. |
    | `6` | `is_nullable` | `True` if NULL values allowed for the column or `False`. |

    Expand

    Show lessSee more

    For examples of getting this attribute, see [Retrieving column metadata](/developer-guide/python-connector/python-connector-example#label-python-connector-column-metadata).

rowcount
:   Read-only attribute that returns the number of rows in the last `execute` produced.
    The value is `-1` or `None` if no `execute` is executed.

sfqid
:   Read-only attribute that returns the Snowflake query ID in the last `execute` or `execute_async` executed.

arraysize
:   Read/write attribute that specifies the number of rows to fetch at a time with `fetchmany()`.
    It defaults to `1` meaning to fetch a single row at a time.

connection
:   Read-only attribute that returns a reference to the `Connection` object on which the cursor
    was created.

messages
:   List object that includes the sequences (exception class, exception value) for all messages
    which it received from the underlying database for the cursor.

    The list is cleared automatically by any method call except for `fetch*()` calls.

errorhandler
:   Read/write attribute that references an error handler to call in case an error condition is
    met.

    The handler must be a Python callable that accepts the following arguments:

    > `errorhandler(connection, cursor, errorclass, errorvalue)`

stats
:   Provides detailed row-level statistics for DML operations, particularly useful for CTAS (CREATE TABLE AS SELECT) statements where DML statistics were previously unavailable.

    Returns a `QueryResultStats` `NamedTuple` with four fields:

    - `num_rows_inserted` : Number of rows inserted (`int` | `None`)
    - `num_rows_deleted` : Number of rows deleted (`int` | `None`)
    - `num_rows_updated` : Number of rows updated (`int` | `None`)
    - `num_dml_duplicates` : Number of duplicate rows in DML statement (`int` | `None`)

    If no DML stats are available, returns a `QueryResultStats` instance with all fields set to `None`, including the following situations:

    - DML operations where no rows were affected (such as a DELETE … clause with a WHERE condition returning `FALSE` for all entries)
    - Non-DML type of SQL statements (such as DDL and DQL)
    - Multi-statements
    - Async queries (`execute_async)`
    - Result retrieval with QueryID (`get_results_from_sfqid`)

    Note that the `stats` property does not return `None` in these cases; it always returns a `QueryResultStats` instance with all fields set to `None`.

### Type codes

In the `Cursor` object, the `description` attribute and the `describe()` method provide a list of tuples
(or, in versions 2.4.6 and later, [ResultMetadata](#label-python-connector-resultmetadata-object) objects) that describe the
columns in the result set.

In a tuple, the value at the index `1` (the `type_code` attribute In the `ResultMetadata` object) represents the
column data type. The Snowflake Connector for Python uses the following map to get the string representation, based on the type
code:

| type\_code | String Representation | Data Type |
| --- | --- | --- |
| 0 | FIXED | NUMBER/INT |
| 1 | REAL | REAL |
| 2 | TEXT | VARCHAR/STRING |
| 3 | DATE | DATE |
| 4 | TIMESTAMP | TIMESTAMP |
| 5 | VARIANT | VARIANT |
| 6 | TIMESTAMP\_LTZ | TIMESTAMP\_LTZ |
| 7 | TIMESTAMP\_TZ | TIMESTAMP\_TZ |
| 8 | TIMESTAMP\_NTZ | TIMESTAMP\_TZ |
| 9 | OBJECT | OBJECT |
| 10 | ARRAY | ARRAY |
| 11 | BINARY | BINARY |
| 12 | TIME | TIME |
| 13 | BOOLEAN | BOOLEAN |
| 14 | GEOGRAPHY | GEOGRAPHY |
| 15 | GEOMETRY | GEOMETRY |
| 16 | VECTOR | VECTOR |

Expand

Show lessSee more

### Data type mappings for `qmark` and `numeric` bindings

If `paramstyle` is either `"qmark"` or `"numeric"`, the following default mappings from
Python to Snowflake data type are used:

| Python Data Type | Data Type in Snowflake |
| --- | --- |
| `int` | NUMBER(38, 0) |
| `long` | NUMBER(38, 0) |
| `decimal` | NUMBER(38, <scale>) |
| `float` | REAL |
| `str` | TEXT |
| `unicode` | TEXT |
| `bytes` | BINARY |
| `bytearray` | BINARY |
| `bool` | BOOLEAN |
| `date` | DATE |
| `time` | TIME |
| `timedelta` | TIME |
| `datetime` | TIMESTAMP\_NTZ |
| `struct_time` | TIMESTAMP\_NTZ |

Expand

Show lessSee more

If you need to map to another Snowflake type (e.g. `datetime` to `TIMESTAMP_LTZ`), specify the
Snowflake data type in a tuple consisting of the Snowflake data type followed by the value. See
[Binding datetime with TIMESTAMP](/developer-guide/python-connector/python-connector-example#label-python-connector-binding-timestmamp-qmark) for examples.

## Object: `Exception`

PEP-249 defines the exceptions that the
Snowflake Connector for Python can raise in case of errors or warnings. The application must
handle them properly and decide to continue or stop running the code.

For more information, see the [PEP-249](https://www.python.org/dev/peps/pep-0249/) documentation.

### Methods

No methods are available for `Exception` objects.

### Attributes

errno
:   Snowflake DB error code.

msg
:   Error message including error code, SQL State code and query ID.

raw\_msg
:   Error message. No error code, SQL State code or query ID is included.

sqlstate
:   ANSI-compliant SQL State code

sfqid
:   Snowflake query ID.

## Object `ResultBatch`

A `ResultBatch` object encapsulates a function that retrieves a subset of rows in a result set. To
[distribute the work of fetching results across multiple workers or nodes](/developer-guide/python-connector/python-connector-distributed-fetch), you can call
`get_result_batches()` method in the [Cursor](#label-python-connector-cursor-object) object to retrieve a list of
`ResultBatch` objects and distribute these objects to different workers or nodes for processing.

### Attributes

#### rowcount

Read-only attribute that returns the number of rows in the result batch.

#### compressed\_size

Read-only attribute that returns the size of the data (when compressed) in the result batch.

#### uncompressed\_size

Read-only attribute that returns the size of the data (uncompressed) in the result batch.

### Methods

to\_arrow()
:   Purpose:
    :   This method returns a PyArrow table containing the rows in the `ResultBatch` object.

    Parameters:
    :   None.

    Returns:
    :   Returns a PyArrow table containing the rows from the `ResultBatch` object.

        If there are no rows, this returns None.

to\_pandas()
:   Purpose:
    :   This method returns a pandas DataFrame containing the rows in the `ResultBatch` object.

    Parameters:
    :   None.

    Returns:
    :   Returns a pandas DataFrame containing the rows from the `ResultBatch` object.

        If there are no rows, this returns an empty pandas DataFrame.

## Object: `ResultMetadata`

A `ResultMetadata` object represents metadata about a column in the result set.
A list of these objects is returned by the `description` attribute and `describe` method of the `Cursor`
object.

This object was introduced in version 2.4.6 of the Snowflake Connector for Python.

### Methods

None.

### Attributes

name
:   Name of the column

type\_code
:   Internal [type code](#label-python-connector-type-codes).

display\_size
:   Not used. Same as internal\_size.

internal\_size
:   Internal data size.

precision
:   Precision of numeric data.

scale
:   Scale for numeric data.

is\_nullable
:   `True` if NULL values allowed for the column or `False`.

## Module: `snowflake.connector.constants`

The `snowflake.connector.constants` module defines constants used in the API.

### Enums

QueryStatus
:   Represents the status of an asynchronous query. This enum has the following constants:

    | Enum Constant | Description |
    | --- | --- |
    | RUNNING | The query is still running. |
    | ABORTING | The query is in the process of being aborted on the server side. |
    | SUCCESS | The query finished successfully. |
    | FAILED\_WITH\_ERROR | The query finished unsuccessfully. |
    | QUEUED | The query is queued for execution (i.e. has not yet started running), typically because it is waiting for resources. |
    | DISCONNECTED | The session’s connection is broken. The query’s state will change to “FAILED\_WITH\_ERROR” soon. |
    | RESUMING\_WAREHOUSE | The warehouse is starting up and the query is not yet running. |
    | BLOCKED | The statement is waiting on a lock held by another statement. |
    | NO\_DATA | Data about the statement is not yet available, typically because the statement has not yet started executing. |

    Expand

    Show lessSee more

CertRevocationCheckMode
:   How to treat certificate revocation lists (CRLs) attached to a certificate. This enum has the following constants:

    | Enum Constant | Description |
    | --- | --- |
    | DISABLED | No revocation check is done. |
    | ADVISORY | Only a revoked certificate can invalidate the chain. Errors related to the CRL don’t revoke a certificate. |
    | ENABLED | Each certificate must have at least one valid CRL. Errors in connection, parsing, or validation of all associated CRLs revokes a certificate. |

    Expand

    Show lessSee more

## Module: `snowflake.connector.pandas_tools`

The `snowflake.connector.pandas_tools` module provides functions for
working with the pandas data analysis library.

For more information, see the [pandas data analysis library](https://pandas.pydata.org/) documentation.

### Functions

write\_pandas(parameters…)
:   Purpose:
    :   Writes a pandas DataFrame to a table in a Snowflake database.

        To write the data to the table, the function saves the data to Parquet files, uses the [PUT](/sql-reference/sql/put) command to upload these files to a temporary stage, and uses the [COPY INTO <table>](/sql-reference/sql/copy-into-table) command to copy the data from the files to the table. You can use some of the function parameters to control how the `PUT` and `COPY INTO <table>` statements are executed.

    Parameters:
    :   The valid input parameters are:

        | Parameter | Required | Description |
        | --- | --- | --- |
        | `conn` | Yes | `Connection` object that holds the connection to the Snowflake database. |
        | `df` | Yes | `pandas.DataFrame` object containing the data to be copied into the table. |
        | `table_name` | Yes | Name of the table where the data should be copied. |
        | `database` |  | Name of the database containing the table. By default, the function writes to the database that is currently in use in the session. Note: If you specify this parameter, you must also specify the `schema` parameter. |
        | `schema` |  | Name of the schema containing the table. By default, the function writes to the table in the schema that is currently in use in the session. |
        | `bulk_upload_chunks` |  | Setting this parameter to `True` changes the behavior of the `write_pandas` function to first write all the data chunks to the local disk and then perform the wildcard upload of the chunks folder to the stage. When set to `False` (default), the chunks are saved, uploaded, and deleted one by one. |
        | `chunk_size` |  | Number of elements to insert at a time. By default, the function inserts all elements at once in one chunk. |
        | `compression` |  | The compression algorithm to use for the Parquet files. You can specify either `"gzip"` for better compression or `"snappy"` for faster compression. By default, the function uses `"gzip"`. |
        | `on_error` |  | Specifies how errors should be handled. Set this to one of the string values documented in the `ON_ERROR` [copy option](/sql-reference/sql/copy-into-table#label-copy-into-table-copyoptions). By default, the function uses `"ABORT_STATEMENT"`. |
        | `parallel` |  | Number of threads to use when uploading the Parquet files to the temporary stage. For the default number of threads used and guidelines on choosing the number of threads, see [the parallel parameter of the PUT command](/sql-reference/sql/put#label-put-parameter-parallel). |
        | `quote_identifiers` |  | If `False`, prevents the connector from [putting double quotes around identifiers](/sql-reference/identifiers-syntax) before sending the identifiers to the server. By default, the connector puts double quotes around identifiers. |

        Expand

        Show lessSee more

    Returns:
    :   Returns a tuple of `(success, num_chunks, num_rows, output)` where:

        - `success` is `True` if the function successfully wrote the data to the table.
        - `num_chunks` is the number of chunks of data that the function copied.
        - `num_rows` is the number of rows that the function inserted.
        - `output` is the output of the `COPY INTO <table>` command.

    Example:
    :   The following example writes the data from a pandas DataFrame to the table named ‘customers’.

        Copy code

        ```
        import pandas
        from snowflake.connector.pandas_tools import write_pandas

        # Create the connection to the Snowflake database.
        cnx = snowflake.connector.connect(...)

        # Create a DataFrame containing data about customers
        df = pandas.DataFrame([('Mark', 10), ('Luke', 20)], columns=['name', 'balance'])

        # Write the data from the DataFrame to the table named "customers".
        success, nchunks, nrows, _ = write_pandas(cnx, df, 'customers')
        ```

pd\_writer(parameters…)
:   Purpose:
    :   `pd_writer` is an
        insertion method for inserting data into
        a Snowflake database.

        When calling `pandas.DataFrame.to_sql`,
        pass in `method=pd_writer` to specify that you want to use `pd_writer` as the method for inserting data.
        (You do not need to call `pd_writer` from your own code. The `to_sql` method calls `pd_writer` and
        supplies the input parameters needed.)

        For more information see:

        - [insertion method](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql-method) documentation.
        - [pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html) documentation.

        Note

        Please note that when column names in the pandas `DataFrame` contain only lowercase letters, you must enclose
        the column names in double quotes; otherwise the connector raises a `ProgrammingError`.

        The `snowflake-sqlalchemy` library does not quote lowercase column names when creating a table,
        while `pd_writer` quotes column names by default. The issue arises because the COPY INTO
        command expects column names to be quoted.

        Future improvements will be made in the `snowflake-sqlalchemy` library.

        For example:

        Copy code

        ```
        import pandas as pd
        from snowflake.connector.pandas_tools import pd_writer

        sf_connector_version_df = pd.DataFrame([('snowflake-connector-python', '1.0')], columns=['NAME', 'NEWEST_VERSION'])

        # Specify that the to_sql method should use the pd_writer function
        # to write the data from the DataFrame to the table named "driver_versions"
        # in the Snowflake database.
        sf_connector_version_df.to_sql('driver_versions', engine, index=False, method=pd_writer)

        # When the column names consist of only lower case letters, quote the column names
        sf_connector_version_df = pd.DataFrame([('snowflake-connector-python', '1.0')], columns=['"name"', '"newest_version"'])
        sf_connector_version_df.to_sql('driver_versions', engine, index=False, method=pd_writer)
        ```

        The `pd_writer` function uses the `write_pandas()` function to write the data in the DataFrame to the
        Snowflake database.

    Parameters:
    :   The valid input parameters are:

        | Parameter | Required | Description |
        | --- | --- | --- |
        | `table` | Yes | `pandas.io.sql.SQLTable` object for the table. |
        | `conn` | Yes | `sqlalchemy.engine.Engine` or `sqlalchemy.engine.Connection` object used to connect to the Snowflake database. |
        | `keys` | Yes | Names of the table columns for the data to be inserted. |
        | `data_iter` | Yes | Iterator for the rows containing the data to be inserted. |

        Expand

        Show lessSee more

    Example:
    :   The following example passes `method=pd_writer` to the `pandas.DataFrame.to_sql` method, which in turn calls
        the `pd_writer` function to write the data in the pandas DataFrame to a Snowflake database.

        Copy code

        ```
        import pandas
        from snowflake.connector.pandas_tools import pd_writer

        # Create a DataFrame containing data about customers
        df = pandas.DataFrame([('Mark', 10), ('Luke', 20)], columns=['name', 'balance'])

        # Specify that the to_sql method should use the pd_writer function
        # to write the data from the DataFrame to the table named "customers"
        # in the Snowflake database.
        df.to_sql('customers', engine, index=False, method=pd_writer)
        ```

## Date and timestamp support

Snowflake supports multiple DATE and TIMESTAMP data types, and the Snowflake Connector
allows binding native `datetime` and `date` objects for update and fetch operations.

### Fetching data

When fetching date and time data, the Snowflake data types are converted into Python data types:

| Snowflake Data Types | Python Data Type | Behavior |
| --- | --- | --- |
| TIMESTAMP\_TZ | [datetime](https://docs.python.org/2/library/datetime.html#datetime.datetime) with [tzinfo](https://docs.python.org/2/library/datetime.html#tzinfo-objects) | Fetches data, including the time zone offset, and translates it into a `datetime` with `tzinfo` object. |
| TIMESTAMP\_LTZ, TIMESTAMP | [datetime](https://docs.python.org/2/library/datetime.html#datetime.datetime) with [tzinfo](https://docs.python.org/2/library/datetime.html#tzinfo-objects) | Fetches data, translates it into a `datetime` object, and attaches `tzinfo` based on the [TIMESTAMP\_TYPE\_MAPPING](/sql-reference/parameters#label-timestamp-type-mapping) session parameter. |
| TIMESTAMP\_NTZ | [datetime](https://docs.python.org/2/library/datetime.html#datetime.datetime) | Fetches data and translates it into a `datetime` object. No time zone information is attached to the object. |
| DATE | [date](https://docs.python.org/2/library/datetime.html#datetime.date) | Fetches data and translates it into a `date` object. No time zone information is attached to the object. |

Expand

Show lessSee more

Note

`tzinfo` is a UTC offset-based time zone object and not IANA time zone
names. The time zone names might not match, but equivalent offset-based
time zone objects are considered identical.

### Updating data

When updating date and time data, the Python data types are converted to Snowflake data types:

| Python Data Type | Snowflake Data Types | Behavior |
| --- | --- | --- |
| datetime | TIMESTAMP\_TZ, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, DATE | Converts a datetime object into a string in the format of `YYYY-MM-DD HH24:MI:SS.FF TZH:TZM` and updates it. If no time zone offset is provided, the string will be in the format of `YYYY-MM-DD HH24:MI:SS.FF`. The user is responsible for setting the `tzinfo` for the `datetime` object. |
| struct\_time | TIMESTAMP\_TZ, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, DATE | Converts a struct\_time object into a string in the format of `YYYY-MM-DD HH24:MI:SS.FF TZH:TZM` and updates it. The time zone information is retrieved from `time.timezone`, which includes the time zone offset from UTC. The user is responsible for setting the TZ environment variable for `time.timezone`. |
| date | TIMESTAMP\_TZ, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, DATE | Converts a date object into a string in the format of `YYYY-MM-DD`. No time zone is considered. |
| time | TIMESTAMP\_TZ, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, DATE | Converts a time object into a string in the format of `HH24:MI:SS.FF`. No time zone is considered. |
| timedelta | TIMESTAMP\_TZ, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, DATE | Converts a timedelta object into a string in the format of `HH24:MI:SS.FF`. No time zone is considered. |

Expand

Show lessSee more
