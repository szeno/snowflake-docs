# ALTER FUNCTION (Snowpark Container Services)

Modifies the properties of an existing [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function).

To make any other changes to a service function, you must drop the function (using [DROP FUNCTION (Snowpark Container Services)](/sql-reference/sql/drop-function-spcs)) and then recreate it.

See also:
:   [Service functions](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function), [CREATE FUNCTION](/sql-reference/sql/create-function-spcs), [DESC FUNCTION](/sql-reference/sql/desc-function-spcs), [DROP FUNCTION](/sql-reference/sql/drop-function-spcs)

## Syntax

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  RENAME TO <new_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  SET CONTEXT_HEADERS = ( <context_function_1> [ , <context_function_2> ...] )

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  SET MAX_BATCH_ROWS = <integer>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  SET MAX_BATCH_RETRIES = <integer>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  SET ON_BATCH_FAILURE = { ABORT | RETURN_NULL }

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  SET BATCH_TIMEOUT_SECS = <integer>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  SET COMMENT = '<string_literal>'

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  SET SERVICE = '<service_name>' ENDPOINT = '<endpoint_name>'

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] )
  UNSET { CONTEXT_HEADERS | MAX_BATCH_ROWS | MAX_BATCH_RETRIES | ON_BATCH_FAILURE | BATCH_TIMEOUT_SECS | COMMENT }
```

## Parameters

`name`
:   Specifies the identifier for the service function to alter. The identifier can contain the schema name and database name, as well as the function name.
    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in
    double quotes are also case sensitive.

`arg_data_type [ , ... ]`
:   Specifies the arguments/input data types for the service function.

    If the function accepts arguments, then the ALTER command must specify the argument types because functions support
    name overloading (that is, two functions in the same schema can have the same name), and the argument types are used to
    identify the function.

`RENAME TO new_name`
:   Specifies the new identifier for the service function; the combination of the identifier and existing argument data types must be unique for the schema.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    When specifying the new name for the service function, do not specify argument data types or parentheses; specify only the new name.

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Specifies the properties to set for the function:

    `COMMENT = 'string_literal'`
    :   Specifies a comment for the function, which is displayed in the DESCRIPTION column in the [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions)
        output.

    `SERVICE = '<service_name>' ENDPOINT = '<endpoint_name>'`
    :   Specifies the service name and the endpoint name as defined in the service specification.

    `CONTEXT_HEADERS = ( context_function_1 [ , context_function_2 ... ] )`
    :   It allows binding Snowflake context function results to HTTP headers.

        Each value must be the name of a context function. Don’t include quote marks around the names.

        More details about this parameter are in [CREATE FUNCTION (Snowpark Container Services)](/sql-reference/sql/create-function-spcs).

    `MAX_BATCH_ROWS = integer`
    :   Specifies the [batch size](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-working-with-services-batch-size-concurrency) when sending data to a service to increase concurrency

    `MAX_BATCH_RETRIES = integer`
    :   Specifies the number of times you want Snowflake to retry a failed batch.

    `ON_BATCH_FAILURE = { ABORT | RETURN_NULL }`
    :   Specifies the behavior of the function after Snowflake reaches the maximum number of retries processing the batch.

        - `ABORT`: Service function aborts execution. Any remaining batches of rows are not processed.
        - `RETURN_NULL`: Service function returns a NULL for each row in the failed batch and continues processing the remaining batches. If you choose this option, note the following caveats:
          - If these batches depend on each other and one batch fails, this could lead to unexpected results.
          - If your service can return a NULL as a valid response, then it’s not possible to differentiate NULL returned by Snowflake due to batch failure and NULL returned by your service.

    `BATCH_TIMEOUT_SECS = integer`
    :   Specifies the maximum duration for processing a single batch of rows, including retries (and polling for async function requests), after which Snowflake should terminate the batch request.

        Acceptable Values: greater than 0 and less than or equal to 604800 seconds (7 days).

`UNSET ...`
:   Specifies the properties to unset for the function, which resets them to the defaults. Note that you can’t unset the service endpoint.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Function |  |
| USAGE | Service endpoint | Usage on a service endpoint is granted to service roles defined in the service specification. You then grant the service role to the role altering the service function. This privilege is required if altering a service endpoint. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename a service function:

Copy code

```
ALTER FUNCTION my_echo_udf(VARCHAR) RENAME TO my_echo_udf_temp;
```

Set a comment for a service function:

Copy code

```
ALTER FUNCTION my_echo_udf(VARCHAR) SET COMMENT = 'some comment';
```

Set the maximum number of rows per batch for a service function:

Copy code

```
ALTER FUNCTION my_echo_udf(number) SET MAX_BATCH_ROWS = 100;
```

Set the CURRENT\_USER context header for a service function:

Copy code

```
ALTER FUNCTION my_echo_udf(VARCHAR) SET CONTEXT_HEADER = (CURRENT_USER);
```

Unset MAX\_BATCH\_ROWS for a service function:

Copy code

```
ALTER FUNCTION my_echo_udf(VARCHAR) UNSET MAX_BATCH_ROWS;
```
