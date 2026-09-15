# DESCRIBE FUNCTION (Snowpark Container Services)

Describes the specified [service function](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function), including the signature (arguments), return value, language, and body (path to the Snowpark Container Services service).

See also:
:   [Service functions](/developer-guide/snowpark-container-services/working-with-services#label-snowpark-containers-service-communicating-service-function), [CREATE FUNCTION](/sql-reference/sql/create-function-spcs), [ALTER FUNCTION](/sql-reference/sql/alter-function-spcs), [DROP FUNCTION](/sql-reference/sql/drop-function-spcs)

## Syntax

Copy code

```
{ DESC | DESCRIBE } FUNCTION [ IF EXISTS ] <name> ( [ <arg_data_type> ] [ , ... ] )
```

## Required parameters

`name`
:   Specifies the identifier for the service function to describe. If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case sensitive.

`( [ arg_name arg_data_type ] [ , ... ] )`
:   Specifies the arguments/inputs for the service function. These should correspond to the arguments that the
    service expects.

    If there are no arguments, then include the parentheses without any argument name(s) and data type(s).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Service function |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

In [Tutorial-1](/developer-guide/snowpark-container-services/tutorials/tutorial-1), you create a service function (my\_echo\_udf). The following DESC FUNCTION command returns the service function description:

Copy code

```
DESC FUNCTION my_echo_udf(VARCHAR);
```

Example output:

```
+--------------------+----------------------+
| property           | value                |
|--------------------+----------------------|
| signature          | (INPUTTEXT VARCHAR)  |
| returns            | VARCHAR              |
| language           | NULL                 |
| null handling      | CALLED ON NULL INPUT |
| volatility         | VOLATILE             |
| body               | /echo                |
| headers            | null                 |
| context_headers    | null                 |
| max_batch_rows     | not set              |
| service            | ECHO_SERVICE         |
| service_endpoint   | echoendpoint         |
| max_batch_retries  | 3                    |
| on_batch_failure   | ABORT                |
| batch_timeout_secs | not set              |
+--------------------+----------------------+
```
