# DESCRIBE GATEWAY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Describes the properties of a [gateway](/developer-guide/snowpark-container-services/gateway).

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE GATEWAY](/sql-reference/sql/create-gateway) , [ALTER GATEWAY](/sql-reference/sql/alter-gateway), [DROP GATEWAY](/sql-reference/sql/drop-gateway) , [SHOW GATEWAYS](/sql-reference/sql/show-gateways)

## Syntax

Copy code

```
DESC[RIBE] GATEWAY <name>
```

## Parameters

`name`
:   Specifies the identifier for the gateway to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command output provides gateway properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | Gateway name. |
| `ingress_url` | Gateway ingress URL. |
| `privatelink_ingress_url` | PrivateLink ingress URL. |
| `database_name` | Database in which the gateway is created. |
| `schema_name` | Schema in which the gateway is created. |
| `owner` | Role that owns the gateway. |
| `owner_role_type` | The type of role that owns the object, either ROLE or DATABASE\_ROLE. |
| `spec` | Gateway specification in YAML format. For a traffic split gateway, the spec includes `type: traffic_split`, `split_type`, and `targets`. For a shadow traffic gateway, the spec includes `type: shadow_traffic`, `primary`, and `shadow`. This column is only shown if the role executing the command has USAGE, MODIFY, or OWNERSHIP privilege on the gateway. |
| `created_on` | Timestamp when the gateway was created. |
| `updated_on` | Timestamp when the gateway was last updated. |
| `comment` | Gateway related comment. |

Expand

Show lessSee more

Note

If the role used has USAGE, MODIFY, or OWNERSHIP privilege on the gateway, the `spec` column will be shown.
If not, the other columns will be shown, but not the `spec` column.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE, MODIFY, or OWNERSHIP | Gateway | Any of these privileges allows describing the gateway. Only roles with these privileges can view the spec. |
| USAGE | Database | Required on the database containing the gateway. |
| USAGE | Schema | Required on the schema containing the gateway. |

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

The following example describes the gateway named `split_gateway`:

Copy code

```
DESCRIBE GATEWAY split_gateway;
```
