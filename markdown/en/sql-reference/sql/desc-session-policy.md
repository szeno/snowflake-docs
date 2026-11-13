# DESCRIBE SESSION POLICY

Describes the details about a session policy.

DESCRIBE can be abbreviated to DESC.

See also:
:   [Session Policy DDL Reference](/user-guide/session-policies-managing#label-session-policy-ddl-reference)

## Syntax

Copy code

```
{ DESCRIBE | DESC } SESSION POLICY <name>
```

## Parameters

`name`
:   Identifier for the session policy; must be unique for your account.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY SESSION POLICY | Account |  |
| OWNERSHIP | Session policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on session policy DDL and privileges, see [Managing session policies](/user-guide/session-policies-managing).

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

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

The command returns one row per property of the session policy, with the following columns:

| Column | Description |
| --- | --- |
| `property` | The name of the property. |
| `value` | The value of the property for this session policy. |
| `default` | The default value of the property. |
| `description` | A description of the property. |

Expand

Show lessSee more

The `property` column contains the following values:

- `CREATED_ON`
- `NAME`
- `OWNER`
- `OWNER_ROLE_TYPE`
- `COMMENT`
- `SESSION_IDLE_TIMEOUT_MINS`
- `SESSION_UI_IDLE_TIMEOUT_MINS`
- `SESSION_MAX_LIFESPAN_MINS`
- `SESSION_UI_MAX_LIFESPAN_MINS`
- `ALLOWED_SECONDARY_ROLES`
- `BLOCKED_SECONDARY_ROLES`
- `AGENT_RESTRICTED_SESSION_SCOPE`

For the meaning and valid values of each setting, see [CREATE SESSION POLICY](/sql-reference/sql/create-session-policy). For details about
`AGENT_RESTRICTED_SESSION_SCOPE`, see [Restricted Session Scope for agents](/user-guide/restricted-session-scope).

## Example

Copy code

```
DESC SESSION POLICY session_policy_prod_1;
```

```
+--------------------------------+--------------------------------------------------+---------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| property                       | value                                            | default | description                                                                                                                                          |
|--------------------------------+--------------------------------------------------+---------+------------------------------------------------------------------------------------------------------------------------------------------------------|
| CREATED_ON                     | 2026-01-19 15:30:06.006 Z                        | null    | Timestamp when the session policy was created.                                                                                                       |
| NAME                           | session_policy_prod_1                            | null    | Name of the session policy.                                                                                                                          |
| OWNER                          | PUBLIC                                           | null    | Owner role of the session policy.                                                                                                                    |
| OWNER_ROLE_TYPE                | ROLE                                             | null    | Owner role type of the session policy.                                                                                                               |
| COMMENT                        | session policy for use in the prod_1 environment | null    | user comment associated to an object in the dictionary                                                                                               |
| SESSION_IDLE_TIMEOUT_MINS      | 60                                               | 240     | Number of minutes of idle time in a non-UI session (e.g. driver session) before the user must reauthenticate.                                        |
| SESSION_UI_IDLE_TIMEOUT_MINS   | 30                                               | 1080    | Number of minutes of idle time in a UI session before the user must reauthenticate.                                                                  |
| SESSION_MAX_LIFESPAN_MINS      | 0                                                | 0       | Maximum lifespan in minutes for a non-UI session (e.g. driver session) before the user must reauthenticate. 0 means no maximum lifespan enforcement. |
| SESSION_UI_MAX_LIFESPAN_MINS   | 0                                                | 0       | Maximum lifespan in minutes for a UI session before the user must reauthenticate. 0 means no maximum lifespan enforcement.                           |
| ALLOWED_SECONDARY_ROLES        | []                                               | null    | List of secondary roles allowed to be activated in a user session.                                                                                   |
| BLOCKED_SECONDARY_ROLES        | null                                             | null    | List of secondary roles blocked from activation in a user session.                                                                                   |
| AGENT_RESTRICTED_SESSION_SCOPE | null                                             | null    | Name of a Restricted Session Scope applied to sessions attributed to an agent identity.                                                              |
+--------------------------------+--------------------------------------------------+---------+------------------------------------------------------------------------------------------------------------------------------------------------------+
```
