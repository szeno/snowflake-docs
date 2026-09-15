# DESCRIBE NOTIFICATION INTEGRATION

Describes the properties of a notification integration.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration) , [ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration) , [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations) ,
    [DROP INTEGRATION](/sql-reference/sql/drop-integration)

## Syntax

Copy code

```
{ DESC | DESCRIBE } NOTIFICATION INTEGRATION <name>
```

## Parameters

`name`
:   Specifies the identifier for the notification integration to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `property` | The name of the property (see [Properties of notification integrations](/sql-reference/sql/desc-notification-integration#label-desc-notification-integration-properties)). |
| `property_type` | The data type of the property (for example, `Boolean` or `String`). |
| `property_value` | The value assigned to the property. |
| `property_default` | The default value of the property. |

Expand

Show lessSee more

The `property` column can include the following properties of the notification integration:

**Properties of notification integrations**

| Property | Description |
| --- | --- |
| `ENABLED` | Specifies whether or not the notification integration is enabled. |
| `DIRECTION` | Specifies whether the notification integration supports sending notifications (`OUTBOUND`) or receiving notifications (`INBOUND`). |
| `COMMENT` | Specifies the comment for the notification integration. |
| Additional properties specific to the notification integration type. | These are the properties that you set when creating or altering the notification integration.  For more information about these properties, see the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration) or [ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration) command for the specific type. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE | Integration |  |
| OWNERSHIP | Integration | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

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

Describe the properties of a notification integration named `my_notify_int`:

Copy code

```
DESC INTEGRATION my_notify_int;
```
