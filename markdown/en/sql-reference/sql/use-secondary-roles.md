# USE SECONDARY ROLES

Specifies the active/current secondary roles for the session. The currently-active secondary roles set the context that determines whether
the current user has the necessary privileges to perform SQL actions.

Note that authorization to execute [CREATE <object>](/sql-reference/sql/create) statements to create objects is provided by the primary role.

For more information, see [secondary role enforcement](/user-guide/security-access-control-overview#label-access-control-role-enforcement).

See also:
:   [USE ROLE](/sql-reference/sql/use-role)

## Syntax

Copy code

```
USE SECONDARY ROLES {
      ALL
    | NONE
    | <role_name> [ , <role_name> ... ]
  }
```

## Parameters

`ALL`
:   All roles that have been granted to the user in addition to the current active primary role.

    Note that the set of roles is reevaluated when each SQL statement executes. If additional roles are granted to the user, and that user
    executes a new SQL statement, the newly granted roles are active secondary roles for the new SQL statement. The same logic applies to
    roles that are revoked from a user.

`NONE`
:   Disables secondary roles. The authorization for all SQL actions is provided via the primary role.

`role_name [ , role_name ... ]`
:   Activates the specified roles as secondary roles. The secondary roles can be user-defined account roles or system roles. Specify the role
    name as it is stored in Snowflake.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Usage notes

- When specifying individual role names:

  - Each named role must have been granted to the current user. The command immediately
    validates each specified role; if any role has not been granted, the command fails with
    an error.
  - The command records the desired set of secondary roles for the session. The roles
    activated for each subsequent SQL statement might be a subset of the desired set,
    for example, if a session policy restricts certain secondary roles.
- When `ALL` is specified, the command doesn’t validate role grants up front. Instead, the
  active secondary roles are determined dynamically when each SQL statement executes. This
  means newly granted roles are activated automatically, and revoked roles are no longer
  active, without needing to reissue the command.
- If a session policy restricts which secondary roles can be activated, the command still
  succeeds but might return an informational message indicating that the activated secondary
  roles will be limited by the policy.

## Examples

Copy code

```
USE SECONDARY ROLES ALL;
```

Copy code

```
USE SECONDARY ROLES test_role_1, test_role_2;
```
