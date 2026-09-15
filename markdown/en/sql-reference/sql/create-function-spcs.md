# CREATE FUNCTION (Snowpark Container Services)

Creates a [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function).

This command supports the following variants:

- [CREATE OR ALTER FUNCTION (Snowpark Container Services)](#label-create-or-alter-function-spcs-syntax): Creates a service function if it doesn’t exist or alters an existing service function.

See also:
:   [Service functions](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function), [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function),
    [DESC FUNCTION](/sql-reference/sql/desc-function-spcs), [DROP FUNCTION](/sql-reference/sql/drop-function-spcs), [ALTER FUNCTION](/sql-reference/sql/alter-function-spcs)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] FUNCTION <name> ( [ <arg_name> <arg_data_type> ] [ , ... ] )
  RETURNS <result_data_type>
  [ [ NOT ] NULL ]
  [ { CALLED ON NULL INPUT | { RETURNS NULL ON NULL INPUT | STRICT } } ]
  [ { VOLATILE | IMMUTABLE } ]
  SERVICE = <service_name>
  ENDPOINT = <endpoint_name>
  [ COMMENT = '<string_literal>' ]
  [ CONTEXT_HEADERS = ( <context_function_1> [ , <context_function_2> ...] ) ]
  [ MAX_BATCH_ROWS = <integer> ]
  [ MAX_BATCH_RETRIES = <integer> ]
  [ ON_BATCH_FAILURE = { ABORT | RETURN_NULL } ]
  [ BATCH_TIMEOUT_SECS = <integer> ]
  AS '<http_path_to_request_handler>'
```

## Variant syntax

### CREATE OR ALTER FUNCTION (Snowpark Container Services)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new service function if it doesn’t already exist, or transforms an existing service function into the service function
defined in the statement. A CREATE OR ALTER FUNCTION (Snowpark Container Services) statement follows the syntax rules of a CREATE
FUNCTION (Snowpark Container Services) statement and has the same limitations as an [ALTER FUNCTION (Snowpark Container Services)](/sql-reference/sql/alter-function-spcs)
statement.

Supported function alterations include changes to the following:

- CONTEXT\_HEADERS
- SERVICE
- ENDPOINT
- MAX\_BATCH\_ROWS
- MAX\_BATCH\_RETRIES
- ON\_BATCH\_FAILURE
- BATCH\_TIMEOUT\_SECS

For more information, see [CREATE OR ALTER FUNCTION (Snowpark Container Services) usage notes](#label-create-or-alter-function-spcs-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE [ OR ALTER ] FUNCTION ...
```

## Required parameters

`name`
:   Specifies the identifier (`name`) and any input arguments for the function.

    - The identifier does not need to be unique for the schema in which the function is created because functions are
      [identified and resolved by the combination of the name and argument types](/developer-guide/udf-stored-procedure-naming-conventions#label-procedure-function-name-overloading).
    - The identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
      identifier string is enclosed in double quotes (for example, “My object”). Identifiers enclosed in double quotes are also
      case-sensitive. See [Identifier requirements](/sql-reference/identifiers-syntax).

`( [ arg_name arg_data_type ] [ , ... ] )`
:   Specifies the arguments/inputs for the service function. These should correspond to the arguments that the
    service expects.

    If there are no arguments, then include the parentheses without any argument name(s) and data type(s).

`RETURNS result_data_type`
:   Specifies the data type of the result returned by the function.

`SERVICE = service_name`
:   Specifies the name of the Snowpark Container Services service.

`ENDPOINT = endpoint_name`
:   Specifies the name of the endpoint as defined in the service specification.

`AS http_path_to_request_handler`
:   Specifies the HTTP path to the service code that is executed when the function is called.

## Optional parameters

`[ [ NOT ] NULL ]`
:   Specifies whether the function can return NULL values or must return only non-null values. The default is NULL (that is, the function can
    return NULL).

`CALLED ON NULL INPUT` or `{ RETURNS NULL ON NULL INPUT | STRICT }`
:   Specifies the behavior of the function when called with null inputs. In contrast to system-defined functions, which always return null when any
    input is null, functions can handle null inputs, returning non-null values even when an input is null:

    - `CALLED ON NULL INPUT` will always call the function with null inputs. It’s up to the function to handle such values appropriately.
    - `RETURNS NULL ON NULL INPUT` (or its synonym `STRICT`) will not call the function if any input is null. Instead, a null value
      will always be returned for that row. Note that the function might still return null for non-null inputs.

    Default: `CALLED ON NULL INPUT`

`{ VOLATILE | IMMUTABLE }`
:   Specifies the behavior of the function when returning results:

    > - `VOLATILE`: function might return different values for different rows, even for the same input (for example, due to non-determinism and
    >   statefulness).
    > - `IMMUTABLE`: function assumes that the function, when called with the same inputs, will always return the same result. This guarantee
    >   is not checked. Specifying `IMMUTABLE` for a function that returns different values for the same input will result in undefined
    >   behavior.

    Default: `VOLATILE`

`MAX_BATCH_ROWS = integer`
:   Specifies the [batch size](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-working-with-services-batch-size-concurrency) when sending data to a service to increase concurrency.

`MAX_BATCH_RETRIES = integer`
:   Specifies the number of times you want Snowflake to retry a failed batch.

    Default: 3

`ON_BATCH_FAILURE = { ABORT | RETURN_NULL }`
:   Specifies the behavior of the function after Snowflake reaches the maximum number of retries processing the batch.

    - `ABORT`: Service function aborts execution. Any remaining batches of rows are not processed.
    - `RETURN_NULL`: Service function returns a NULL for each row in the failed batch and continues processing the remaining batches. If you choose this option, note the following caveats:
      - If these batches depend on each other and one batch fails, this could lead to unexpected results.
      - If your service can return a NULL as a valid response, then it is not possible to differentiate NULL returned by Snowflake due to batch failure and NULL returned by your service.

    Default: `ABORT`

`BATCH_TIMEOUT_SECS = integer`
:   Specifies the maximum duration for processing a single batch of rows, including retries (and polling for async function requests), after which Snowflake should terminate the batch request.

    Acceptable values: greater than 0 and less than or equal to 604800 seconds (7 days).

    Default: 3600 seconds (1 hour)

`COMMENT = 'string_literal'`
:   Specifies a comment for the function, which is displayed in the DESCRIPTION column in the [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions)
    output.

    Default: `user-defined function`

`CONTEXT_HEADERS = ( context_function_1 [ , context_function_2 ...] )`
:   This binds Snowflake context function results to HTTP headers.
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

    Snowflake prepends `sf-context` to the header before it’s written to the HTTP request.

    Example:

    Copy code

    ```
    CONTEXT_HEADERS = (current_timestamp)
    ```

    In this example, Snowflake writes the header `sf-context-current-timestamp` into the HTTP request.

    Context functions can generate characters that are illegal in HTTP header values, including (but not limited to) the following:

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

    For example, suppose that the context function CURRENT\_STATEMENT() returns the following:

    Copy code

    ```
    select
      /*ÄÎßë¬±©®*/
      my_service_function(1);
    ```

    The value sent in `sf-context-current-statement` is the following:

    Copy code

    ```
    select /* */ my_service_function(1);
    ```

    To ensure that your service code can access the original result (with illegal characters) from the context function
    even if illegal characters have been replaced, Snowflake also sends a binary context header that contains the
    context function result encoded in [base64](/sql-reference/binary-input-output#label-base64-format).

    In the example above, the value sent in the base64-encoded header is the result of the following call:

    Copy code

    ```
    base64_encode('select\n/*ÄÎßë¬±©®*/\nmy_service_function(1)')
    ```

    The remote service is responsible for decoding the base64 value if needed.

    Each such base64 header is named according to the following convention:

    Copy code

    ```
    sf-context-<context-function>-base64
    ```

    In the example above, the name of the header would be the following:

    Copy code

    ```
    sf-context-current-statement-base64
    ```

    If no context headers are sent, then no base64 context headers are sent.

    If the rows sent to a service function are split across multiple batches, then all batches contain the same
    context headers and the same binary context headers.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE FUNCTION | Schema |  |
| USAGE | Service Endpoint | Usage on a service endpoint is granted to service roles defined in the service specification. You then grant the service role to the role creating the service function. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## General usage notes

- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## CREATE OR ALTER FUNCTION (Snowpark Container Services) usage notes

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The following alterations are not supported:

- RETURNS
- Volatility (VOLATILE/IMMUTABLE)
- Null handling (CALLED ON NULL INPUT / RETURNS NULL ON NULL)

## Examples

### Create a simple service function

In [Tutorial-1](/developer-guide/snowpark-container-services/tutorials/tutorial-1), you create the following service function:

Copy code

```
CREATE FUNCTION my_echo_udf (InputText VARCHAR)
  RETURNS VARCHAR
  SERVICE=echo_service
  ENDPOINT=echoendpoint
  AS '/echo';
```

This function connects with the specific ENDPOINT of the specified SERVICE. When you invoke this function, Snowflake sends a
request to the `/echo` path inside the service container.

Note the following:

- The `my_echo_udf` function takes a string as input and returns a string.
- The SERVICE property identifies the service (`echo_service`), and the ENDPOINT property identifies the user-friendly
  endpoint name (`echoendpoint`).
- The `AS '/echo'` specifies the path for the service. In `echo_service.py` (see service code), the `@app.post` decorator associates this
  path with the `echo` function.

### Alter a service function using the CREATE OR ALTER FUNCTION (Snowpark Container Services) command

Alter a function `my_echo_udf` to set the maximum number of batch rows to 100, and add a context header and endpoint:

Copy code

```
CREATE OR ALTER FUNCTION my_echo_udf (InputText VARCHAR)
  RETURNS VARCHAR
  SERVICE = echo_service
  ENDPOINT = reverse_echoendpoint
  CONTEXT_HEADERS = (current_account)
  MAX_BATCH_ROWS = 100
  AS '/echo';
```
