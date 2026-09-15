# USE ROLE

Specifies the active/current primary role for the session. The currently active primary role sets the context that determines whether the
current user has the necessary privileges to execute [CREATE <object>](/sql-reference/sql/create) statements or perform any other SQL action.

Authorization to perform any SQL action other than creating objects can be provided by secondary roles.

For more information, see [Overview of Access Control](/user-guide/security-access-control-overview).

See also:
:   [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) , [CREATE ROLE](/sql-reference/sql/create-role) , [ALTER ROLE](/sql-reference/sql/alter-role) , [DROP ROLE](/sql-reference/sql/drop-role) , [SHOW ROLES](/sql-reference/sql/show-roles)

## Syntax

Copy code

```
USE ROLE <name>
```

## Parameters

`name`
:   Specifies the identifier for the role to use for the session. If the identifier contains spaces or special characters, the entire string
    must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- To use a role, the role must have been granted to the user.
- Only a single primary role can be active at a time in a user session.

  [Secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) enable you to perform SQL actions using
  the combined privileges of the other roles granted to you.

## Examples

Copy code

```
USE ROLE myrole;
```
