# CREATE EXTERNAL FUNCTION

Creates a new [external function](/sql-reference/external-functions).

This command supports the following variants:

- [CREATE OR ALTER EXTERNAL FUNCTION](#label-create-or-alter-external-function-syntax): Creates an external function if it doesn’t exist or alters an existing external function.

See also:
:   [ALTER FUNCTION](/sql-reference/sql/alter-function), [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions),
    [DROP FUNCTION](/sql-reference/sql/drop-function), [DESCRIBE FUNCTION](/sql-reference/sql/desc-function),
    [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] [ SECURE ] EXTERNAL FUNCTION <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS <result_data_type>
  [ [ NOT ] NULL ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  [ COMMENT = '<string_literal>' ]
  API_INTEGRATION = <api_integration_name>
  [ HEADERS = ( '<header_1>' = '<value_1>' [ , '<header_2>' = '<value_2>' ... ] ) ]
  [ CONTEXT_HEADERS = ( <context_function_1> [ , <context_function_2> ...] ) ]
  [ MAX_BATCH_ROWS = <integer> ]
  [ COMPRESSION = <compression_type> ]
  [ REQUEST_TRANSLATOR = <request_translator_udf_name> ]
  [ RESPONSE_TRANSLATOR = <response_translator_udf_name> ]
  AS '<url_of_proxy_and_resource>';
```

## Variant syntax

### CREATE OR ALTER EXTERNAL FUNCTION

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new external function if it doesn’t already exist, or transforms an existing external function into the
function defined in the statement. A CREATE OR ALTER EXTERNAL FUNCTION statement follows the syntax rules of a
CREATE EXTERNAL FUNCTION statement and has the same limitations as an [ALTER FUNCTION](/sql-reference/sql/alter-function)
statement.

Supported function alterations include changes to the following:

- API\_INTEGRATION
- COMMENT
- COMPRESSION
- CONTEXT\_HEADERS
- HEADERS
- MAX\_BATCH\_ROWS
- RESPONSE\_TRANSLATOR
- REQUEST\_TRANSLATOR
- SECURE

For more information, see [CREATE OR ALTER EXTERNAL FUNCTION usage notes](#label-create-or-alter-external-function-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE [ OR ALTER ] EXTERNAL FUNCTION ...
```

## Required parameters

`name`:
:   Specifies the identifier for the function.

    The identifier can contain the schema name and database name, as well as the function name.

    The identifier does not need to be unique for the schema in which the function is created because functions are
    identified and resolved by their name and argument types. However, the signature (name and argument data types)
    must be unique within the schema.

    The `name` must follow the rules for Snowflake [identifiers](/sql-reference/identifiers).
    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Setting `name` the same as the remote service name can make the relationship more clear.
    However, this is not required.

`( [ arg_name arg_data_type ] [ , ... ] )`
:   Specifies the arguments/inputs for the external function. These should correspond to the arguments that the remote
    service expects.

    If there are no arguments, then include the parentheses without any argument name(s) and data type(s).

`RETURNS result_data_type`
:   Specifies the data type returned by the function.

`API_INTEGRATION = api_integration_name`
:   This is the name of the API integration object that should be used to authenticate the call to the proxy service.

`AS 'url_of_proxy_and_resource'`
:   This is the invocation URL of the proxy service (e.g. API Gateway or API Management service) and resource through
    which Snowflake calls the remote service.

## Optional parameters

`SECURE`
:   Specifies that the function is secure. If a function is secure, the URL, the HTTP headers, and the context headers
    are hidden from all users who are not owners of the function.

`[ [ NOT ] NULL ]`
:   This clause indicates whether the function can return NULL values or must return only NON-NULL values.
    If `NOT NULL` is specified, the function must return only non-NULL values. If `NULL` is specified, the
    function can return NULL values.

    Default: The default is NULL (i.e. the function can return NULL values).

`CALLED ON NULL INPUT` or `{ RETURNS NULL ON NULL INPUT | STRICT }`
:   Specifies the behavior of the function when called with null inputs. In contrast to system-defined functions,
    which always return null when any input is null, external functions can handle null inputs,
    returning non-null values even when an input is null:

    > - `CALLED ON NULL INPUT` will always call the function with null inputs. It is up to the function to
    >   handle such values appropriately.
    > - `RETURNS NULL ON NULL INPUT` (or its synonym `STRICT`) will not call the function if any input
    >   is null. Instead, a null value will always be returned for that row. Note that the function might
    >   still return null for non-null inputs.

    Default: `CALLED ON NULL INPUT`

`{ VOLATILE | IMMUTABLE }`
:   Specifies the behavior of the function when returning results:

    > - `VOLATILE`: The function can return different values for different rows, even for the same input (e.g.
    >   due to non-determinism and statefulness).
    > - `IMMUTABLE`: The function always returns the same result when called with the same input.
    >   Snowflake does not check or guarantee this; the remote service must be designed to behave this way.
    >   Specifying `IMMUTABLE` for a function that actually returns different values for the same input will
    >   result in undefined behavior.

    Default: `VOLATILE`

    Snowflake recommends that you set this explicitly rather than accept the default. Setting this
    explicitly reduces the chance of error, and tells users how the function behaves.
    (The [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions) command shows whether a function is volatile or immutable.)

    For important additional information about VOLATILE vs. IMMUTABLE external functions, see
    [Categorize your function as volatile or immutable](/sql-reference/external-functions-best-practices#label-external-functions-volatile-vs-immutable).

`COMMENT = 'string_literal'`
:   Specifies a comment for the function, which is displayed in the DESCRIPTION column in the
    [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions) output.

    Default: `user-defined function`

`HEADERS = ( 'header_1' = 'value_1' [ , 'header_2' = 'value_2' ... ] )`
:   This clause allows users to specify key-value metadata that is sent with every request.
    The creator of the external function decides what goes into the headers, and the caller does not have any control
    over it. Snowflake prepends all of the specified header names with the prefix “sf-custom-”, and sends them as HTTP
    headers.

    The value must be a constant string, not an expression.

    Here’s an example:

    Copy code

    ```
    HEADERS = (
        'volume-measure' = 'liters',
        'distance-measure' = 'kilometers'
    )
    ```

    This causes Snowflake to add two HTTP headers to every HTTPS request:
    `sf-custom-volume-measure` and `sf-custom-distance-measure`, with their corresponding values.

    The rules for header names are different from the rules for Snowflake database identifiers. Header names can be
    composed of most visible standard ASCII characters (decimal 32 - 126) except the following:

    - the space character
    - `(`
    - `)`
    - `,`
    - `/`
    - `:`
    - `;`
    - `<`
    - `>`
    - `=`
    - `"`
    - `?`
    - `@`
    - `[`
    - `]`
    - `\`
    - `{`
    - `}`
    - `_`

    Note specifically that the underscore character is not allowed in header names.

    The header name and value are delimited by single quotes, so any single quotes inside the header name or value
    must be escaped with the backslash character.

    If the backslash character is used as a literal character inside a header value, it must be escaped.

    In header values, both spaces and tabs are allowed, but header values should not contain more than one whitespace
    character in a row. This restriction applies to combinations of whitespace characters (e.g. a space followed by a
    tab) as well as individual whitespace characters (e.g. two spaces in a row).

    If the function author marks the function as secure (with `CREATE SECURE EXTERNAL FUNCTION...`), then the
    headers, the context headers, the binary context headers, and the URL are not visible to function users.

    The sum of the sizes of the header names and header values for an external function must be less than or equal
    to 8 KB.

`CONTEXT_HEADERS = ( context_function_1 [ , context_function_2 ...] )`
:   This is similar to HEADERS, but instead of using constant strings, it binds Snowflake context function results to HTTP headers.
    (For more information about Snowflake context functions, see: [Context functions](/sql-reference/functions-context).)

    Not all context functions are supported in context headers. The following are supported:

    - CURRENT\_ACCOUNT()
    - CURRENT\_CLIENT()
    - CURRENT\_DATABASE()
    - CURRENT\_DATE()
    - CURRENT\_IP\_ADDRESS()
    - CURRENT\_REGION()
    - CURRENT\_ROLE()
    - CURRENT\_SCHEMA()
    - CURRENT\_SCHEMAS()
    - CURRENT\_SESSION()
    - CURRENT\_STATEMENT()
    - CURRENT\_TIME()
    - CURRENT\_TIMESTAMP()
    - CURRENT\_TRANSACTION()
    - CURRENT\_USER()
    - CURRENT\_VERSION()
    - CURRENT\_WAREHOUSE()
    - LAST\_QUERY\_ID()
    - LAST\_TRANSACTION()
    - LOCALTIME()
    - LOCALTIMESTAMP()

    When function names are listed in the CONTEXT\_HEADERS clause, the function names should not be quoted.

    Snowflake prepends `sf-context` to the header before it is written to the HTTP request.

    Example:

    Copy code

    ```
    CONTEXT_HEADERS = (current_timestamp)
    ```

    In this example, Snowflake writes the header `sf-context-current-timestamp` into the HTTP request.

    The characters allowed in context header names and values are the same as the characters allowed in
    [custom header names and values](/sql-reference/sql/create-external-function#label-external-function-headers-valid-characters).

    Context functions can generate characters that are illegal in HTTP header values, including (but not limited to):

    - newline
    - `Ä`
    - `Î`
    - `ß`
    - `ë`
    - `¬`
    - `±`
    - `©`
    - `®`

    Snowflake replaces each sequence of one or more illegal characters with one space character. (The replacement
    is per sequence, not per character.)

    For example, suppose that the context function CURRENT\_STATEMENT() returns:

    Copy code

    ```
    select
      /*ÄÎßë¬±©®*/
      my_external_function(1);
    ```

    The value sent in `sf-context-current-statement` is:

    Copy code

    ```
    select /* */ my_external_function(1);
    ```

    To ensure that remote services can access the original result (with illegal characters) from the context function
    even if illegal characters have been replaced, Snowflake also sends a binary context header that contains the
    context function result encoded in [base64](/sql-reference/binary-input-output#label-base64-format).

    In the example above, the value sent in the base64 header is the result of calling:

    Copy code

    ```
    base64_encode('select\n/ÄÎßë¬±©®/\nmy_external_function(1)')
    ```

    The remote service is responsible for decoding the base64 value if needed.

    Each such base64 header is named according to the following convention:

    Copy code

    ```
    sf-context-<context-function>-base64
    ```

    In the example above, the name of the header would be

    Copy code

    ```
    sf-context-current-statement-base64
    ```

    If no context headers are sent, then no base64 context headers are sent.

    If the rows sent to an external function are split across multiple batches, then all batches contain the same
    context headers and the same binary context headers.

`MAX_BATCH_ROWS = integer`
:   This specifies the maximum number of rows in each batch sent to the proxy service.

    The purpose of this parameter is to limit batch sizes for remote services that have memory constraints or other
    limitations. This parameter is not a performance tuning parameter. This parameter specifies a maximum
    size, not a recommended size.

    If you do not specify MAX\_BATCH\_ROWS, Snowflake estimates the optimal batch size and uses that.

    Snowflake recommends leaving this parameter unset unless the remote service requires a limit.

`COMPRESSION = compression_type`
:   If this clause is specified, the JSON payload is compressed when sent from Snowflake to the proxy service, and when
    sent back from the proxy service to Snowflake.

    Valid values are:

    - `NONE`.
    - `GZIP`.
    - `DEFLATE`.
    - `AUTO`.
      - On AWS, `AUTO` is equivalent to `GZIP`.
      - On Azure, `AUTO` is equivalent to `NONE`.
      - On GCP, `AUTO` is equivalent to `NONE`.

    The Amazon API Gateway automatically compresses/decompresses requests. For more information about
    Amazon API Gateway compression and decompression, see:
    <https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-gzip-compression-decompression.html>

    For information about compression and decompression for other cloud platform proxy services, see the documentation
    for those cloud platforms.

    Default: The default is `AUTO`.

`REQUEST_TRANSLATOR = request_translator_udf_name`
:   This specifies the name of the request translator function. For more information, see [Using request and response translators with data for a remote service](/sql-reference/external-functions-translators).

`RESPONSE_TRANSLATOR = response_translator_udf_name`
:   This specifies the name of the response translator function. For more information, see [Using request and response translators with data for a remote service](/sql-reference/external-functions-translators).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FUNCTION | Schema | Operating on functions also requires the USAGE privilege on the parent database and schema. |
| Either OWNERSHIP or USAGE | API integration | Required to create external functions that reference an API integration. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

- When compression is used, Snowflake sets the HTTP headers “Content-Encoding” and “Accept-Encoding”.
- The argument type(s) and the return type cannot be GEOGRAPHY.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## CREATE OR ALTER EXTERNAL FUNCTION usage notes

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

- Alterations to the function definition and its return type are not supported.

## Examples

### Create an external function through an Amazon API Gateway proxy service

The following example shows a CREATE EXTERNAL FUNCTION statement that is called through an Amazon API Gateway
proxy service:

Copy code

```
CREATE OR REPLACE EXTERNAL FUNCTION local_echo(string_col VARCHAR)
  RETURNS VARIANT
  API_INTEGRATION = demonstration_external_api_integration_01
  AS 'https://xyz.execute-api.us-west-2.amazonaws.com/prod/remote_echo';
```

In this example:

- `local_echo` is the name called from a SQL statement (for example, you can execute
  `SELECT local_echo(varchar_column) ...;`).
- `string_col VARCHAR` contains the name and data type of the input parameter(s). An external function can have 0 or more
  input parameters.
- `VARIANT` is the data type of the value returned by the external function.
- The name `demonstration_external_api_integration_01` is the name of the API integration created earlier in a
  [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) statement.
- The URL `https://xyz.execute-api.us-west-2.amazonaws.com/prod/remote_echo` is the string that identifies the proxy service and
  resource. An HTTP POST command is sent to this URL.

### Alter an external function using the CREATE OR ALTER EXTERNAL FUNCTION command

Alter the external function `local_echo` created above to set the maximum number of batch rows to 100, compression
to GZIP, and add headers and a context header:

Copy code

```
CREATE OR ALTER SECURE EXTERNAL FUNCTION local_echo(string_col VARCHAR)
  RETURNS VARIANT
  API_INTEGRATION = demonstration_external_api_integration_01
  HEADERS = ('header_variable1'='header_value', 'header_variable2'='header_value2')
  CONTEXT_HEADERS = (current_account)
  MAX_BATCH_ROWS = 100
  COMPRESSION = "GZIP"
  AS 'https://xyz.execute-api.us-west-2.amazonaws.com/prod/remote_echo';
```
