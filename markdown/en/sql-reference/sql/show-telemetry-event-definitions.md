# SHOW TELEMETRY EVENT DEFINITIONS

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Lists the [event definitions](/developer-guide/native-apps/event-definition) for the specified app.

## Syntax

Copy code

```
SHOW TELEMETRY EVENT DEFINITIONS IN APPLICATION <name>
```

## Parameters

`name`
:   Specifies the identifier for the app. If the identifier contains
    spaces, special characters, or mixed-case characters, the entire string must be enclosed
    in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Output

Shows information about the event definitions for an app.

| Column | Description |
| --- | --- |
| `name` | The name of the event definition. Event definition names begin with the `SNOWFLAKE$` prefix. |
| `type` | The type of event definition. See [Configure event definitions for an app](/developer-guide/native-apps/event-definition) for more information. |
| `sharing` | Specifies if the event definition is `MANDATORY` or `OPTIONAL`. |
| `status` | Specifies if the event definition is enabled in the consumer account. |

Expand

Show lessSee more

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

## Example

Copy code

```
SHOW TELEMETRY EVENT DEFINITIONS IN APPLICATION hello_snowflake;
```

```
+--------------------------+----------------+---------------+--------------+
|   name                   |   type         |   sharing     |   status     |
+--------------------------+----------------+---------------+--------------+
|   SNOWFLAKE$DEBUG_LOGS   |   DEBUG_LOGS   |   OPTIONAL    |   ENABLED    |
|   SNOWFLAKE$TRACES       |   TRACES       |   MANDATORY   |   ENABLED    |
+--------------------------+----------------+---------------+--------------+
```
