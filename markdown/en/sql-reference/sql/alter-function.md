# ALTER FUNCTION

Modifies the properties of an existing user-defined or external function.

To make any other changes to a UDF, you must drop the function (using [DROP FUNCTION](/sql-reference/sql/drop-function)) and then recreate it.

See also:
:   [Writing external functions](/sql-reference/external-functions), [User-defined functions overview](/developer-guide/udf/udf-overview), [CREATE FUNCTION](/sql-reference/sql/create-function) , [DROP FUNCTION](/sql-reference/sql/drop-function) ,
    [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions) , [DESCRIBE FUNCTION](/sql-reference/sql/desc-function), [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function) ,
    [DESCRIBE FUNCTION](/sql-reference/sql/desc-function) , [DROP FUNCTION](/sql-reference/sql/drop-function) , [SHOW EXTERNAL FUNCTIONS](/sql-reference/sql/show-external-functions)

## Syntax

### User-defined and external functions

The syntax for ALTER FUNCTION varies depending on which language you’re using as the UDF handler.

#### Java handler

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) RENAME TO <new_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET SECURE

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET { SECURE | LOG_LEVEL | TRACE_LEVEL | COMMENT }

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET
  [ LOG_LEVEL = '<log_level>' ]
  [ TRACE_LEVEL = '<trace_level>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , <integration_name> ... ] ) ]
  [ SECRETS = ( '<secret_variable_name>' = <secret_name> [ , '<secret_variable_name>' = <secret_name> ... ] ) ]
  [ COMMENT = '<string_literal>' ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET TAG <tag_name> [ , <tag_name> ... ]
```

#### JavaScript handler

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) RENAME TO <new_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET SECURE

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET { SECURE | LOG_LEVEL | TRACE_LEVEL | COMMENT }

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET
  [ LOG_LEVEL = '<log_level>' ]
  [ TRACE_LEVEL = '<trace_level>' ]
  [ COMMENT = '<string_literal>' ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET TAG <tag_name> [ , <tag_name> ... ]
```

#### Python handler

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) RENAME TO <new_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET SECURE

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET { SECURE | LOG_LEVEL | TRACE_LEVEL | COMMENT }

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET
  [ LOG_LEVEL = '<log_level>' ]
  [ TRACE_LEVEL = '<trace_level>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , <integration_name> ... ] ) ]
  [ SECRETS = ( '<secret_variable_name>' = <secret_name> [ , '<secret_variable_name>' = <secret_name> ... ] ) ]
  [ COMMENT = '<string_literal>' ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET TAG <tag_name> [ , <tag_name> ... ]
```

#### Scala handler

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) RENAME TO <new_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET SECURE

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET { SECURE | LOG_LEVEL | TRACE_LEVEL | COMMENT }

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET
  [ LOG_LEVEL = '<log_level>' ]
  [ TRACE_LEVEL = '<trace_level>' ]
  [ EXTERNAL_ACCESS_INTEGRATIONS = ( <integration_name> [ , <integration_name> ... ] ) ]
  [ SECRETS = ( '<secret_variable_name>' = <secret_name> [ , '<secret_variable_name>' = <secret_name> ... ] ) ]
  [ COMMENT = '<string_literal>' ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET TAG <tag_name> [ , <tag_name> ... ]
```

#### SQL handler

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) RENAME TO <new_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET SECURE

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET { SECURE | LOG_LEVEL | TRACE_LEVEL | COMMENT }

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET
  [ LOG_LEVEL = '<log_level>' ]
  [ TRACE_LEVEL = '<trace_level>' ]
  [ COMMENT = '<string_literal>' ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET DCM PROJECT
```

### External functions

#### Any language handler

Copy code

```
ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET API_INTEGRATION = <api_integration_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET HEADERS = ( [ '<header_1>' = '<value>' [ , '<header_2>' = '<value>' ... ] ] )

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET CONTEXT_HEADERS = ( [ <context_function_1> [ , <context_function_2> ...] ] )

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET MAX_BATCH_ROWS = <integer>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET COMPRESSION = <compression_type>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) SET { REQUEST_TRANSLATOR | RESPONSE_TRANSLATOR } = <udf_name>

ALTER FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> , ... ] ) UNSET
              { COMMENT | HEADERS | CONTEXT_HEADERS | MAX_BATCH_ROWS | COMPRESSION | SECURE | REQUEST_TRANSLATOR | RESPONSE_TRANSLATOR }
```

## Parameters

### User-defined and external functions

`name`
:   Specifies the identifier for the UDF to alter. The identifier can contain the schema name and database name, as well as the function name.
    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in
    double quotes are also case-sensitive.

`arg_data_type [ , ... ]`
:   Specifies the arguments/input data types for the external function.

    If the function accepts arguments, then the ALTER command must specify the argument types because functions support
    name overloading (i.e. two functions in the same schema can have the same name), and the argument types are used to
    identify the function.

`SET ...`
:   Specifies the properties to set for the function:

    `SECURE`
    :   Specifies whether a function is secure. For more details, see [Protecting Sensitive Information with Secure UDFs and Stored Procedures](/developer-guide/secure-udf-procedure).

    `LOG_LEVEL = 'log_level'`
    :   Specifies the severity level of messages that should be ingested and made available in the active event table. Messages at
        the specified level (and at more severe levels) are ingested.

        For more information about levels, see [LOG\_LEVEL](/sql-reference/parameters#label-log-level). For information about setting log level, see
        [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

    `TRACE_LEVEL = 'trace_level'`
    :   Controls how trace events are ingested into the event table.

        For information about levels, see [TRACE\_LEVEL](/sql-reference/parameters#label-trace-level). For information about setting trace level, see
        [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).

    `EXTERNAL_ACCESS_INTEGRATIONS = ( integration_name [ , ... ] )`
    :   The names of [external access integrations](/sql-reference/sql/create-external-access-integration) needed in order for this
        function’s handler code to access external networks.

        An external access integration contains [network rules](/sql-reference/sql/create-network-rule) and
        [secrets](/sql-reference/sql/create-secret) that specify the external locations and credentials (if any) needed for handler code
        to make requests of an external network, such as an external REST API.

        For more information, refer to [External network access overview](/developer-guide/external-network-access/external-network-access-overview).

    `SECRETS = ( 'secret_variable_name' = secret_name [ , ... ] )`
    :   Assigns the names of secrets to variables so that you can use the variables to reference the secrets when retrieving information from
        secrets in handler code.

        This parameter’s value is a list of assignment expressions with the following parts:

        - `secret_name` as the name of a secret specified in an
          [external access integration’s](/sql-reference/sql/create-external-access-integration) ALLOWED\_AUTHENTICATION\_SECRETS parameter
          value. That external access integration’s name must, in turn, be specified as a value of this CREATE FUNCTION call’s
          EXTERNAL\_ACCESS\_INTEGRATIONS parameter.

          You will receive an error if you specify a SECRETS value whose secret isn’t also included in an integration specified by the
          EXTERNAL\_ACCESS\_INTEGRATIONS parameter.
        - `'secret_variable_name'` as the variable that will be used in handler code when retrieving information from the secret.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the function. The value you specify is displayed in the `DESCRIPTION`
        column in the [SHOW FUNCTIONS](/sql-reference/sql/show-functions) and [SHOW USER FUNCTIONS](/sql-reference/sql/show-user-functions) output.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies the properties to unset for the function, which resets them to the defaults.

`UNSET DCM PROJECT`

> Detaches the function from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the function and the DCM project without dropping the function. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

### User-defined functions

`RENAME TO new_name`
:   Specifies the new identifier for the UDF; the combination of the identifier and existing argument data types must be unique for the schema.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    When specifying the new name for the UDF, do not specify argument data types or parentheses; specify only the new name.

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

### External functions

`RENAME TO new_name`
:   Specifies the new identifier for the function.

    The identifier does not need to be unique for the schema in which the function is created because functions are
    identified and resolved by their name and argument types. However, the signature (name and parameter data types)
    must be unique within the schema.

    The `name` must follow the rules for Snowflake [identifiers](/sql-reference/identifiers).
    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note

    When specifying the new name for the external function, do not specify argument data types or parentheses;
    the function will continue using the same arguments as before.

`api_integration_name`
:   This is the name of the API integration object that should be used to authenticate the call to the proxy service.

    More details about this parameter are in [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

`HEADERS = ( 'header_1' = 'value' [ , 'header_2' = 'value' ... ] )`
:   This clause allows users to attach key-value metadata that is sent with every request.

    The value must be a constant string, not an expression.

    More details about this parameter are in [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

`CONTEXT_HEADERS = ( [ context_function_1 [ , context_function_2 ... ] ] )`
:   This is similar to HEADERS, but instead of allowing only constant strings, it allows binding Snowflake
    context function results to HTTP headers.

    Each value must be the name of a context function. The names should not be quoted.

    More details about this parameter are in [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

`COMPRESSION = compression_type`
:   If this clause is specified, the JSON payload is compressed using the specified format when sent from Snowflake to
    the proxy service, and when sent back from the proxy service to Snowflake.

    For more details about valid values of `compression_type`, see [CREATE EXTERNAL FUNCTION](/sql-reference/sql/create-external-function).

`{ REQUEST_TRANSLATOR | RESPONSE_TRANSLATOR } = udf_name`
:   Add a request translator or a response translator if the external function does not already have one or replace an existing request translator
    or response translator by specifying the name of a previously-created JavaScript UDF.
    For more information, see [Using request and response translators with data for a remote service](/sql-reference/external-functions-translators).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Function | Enables calling a UDF or external function. |
| APPLY | Tag | Enables setting a tag on the UDF or external function. |

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

### User-defined functions

- If using a UDF in a [masking policy](/sql-reference/sql/create-masking-policy), ensure the data type of the column, UDF, and masking policy match. For
  more information, see [User-defined functions in a masking policy](/user-guide/security-column-intro#label-security-column-intro-udf-policy).

### External functions

- There is no UNSET command for API\_INTEGRATION. You can change the API\_INTEGRATION, but you cannot unset it. For more, see
  [ALTER API INTEGRATION](/sql-reference/sql/alter-api-integration).

## Examples

Rename the function `function1` to `function2`:

Copy code

```
ALTER FUNCTION IF EXISTS function1(number) RENAME TO function2;
```

Convert a regular function `function2` to a secure function:

Copy code

```
ALTER FUNCTION function2(number) SET SECURE;
```

### External functions

Change the API Integration for an external function:

Copy code

```
ALTER FUNCTION function4(number) SET API_INTEGRATION = api_integration_2;
```

Set the maximum number of rows per batch for an external function:

Copy code

```
ALTER FUNCTION function5(number) SET MAX_BATCH_ROWS = 100;
```
