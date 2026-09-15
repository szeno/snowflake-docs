Categories:
:   [Context functions](/sql-reference/functions-context) (Session Object)

# CURRENT\_SECONDARY\_ROLES

Returns the [secondary roles](/user-guide/security-access-control-overview#label-access-control-role-enforcement) in use for the current session.

To activate a different set of secondary roles for the session, execute the [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles) command.

## Syntax

Copy code

```
CURRENT_SECONDARY_ROLES()
```

## Arguments

None.

## Returns

Returns a string (VARCHAR) that is a JSON-encoded object containing the following name/value pairs:

`roles`
:   Contains a list of the activated secondary roles. This list includes only those roles that are directly granted to the user; roles lower
    in the hierarchy of these roles are not listed.

`value`
:   Contains a list of the requested secondary roles, either those requested with the current user’s `DEFAULT_SECONDARY_ROLES` property or
    with the USE SECONDARY ROLES command.

## Usage notes

Granting access on a secure UDF or secure view that contains CURRENT\_SECONDARY\_ROLES to a share is allowed. When the
secure UDF or secure view is accessed from the data-sharing consumer account, CURRENT\_SECONDARY\_ROLES always returns a
NULL value.

## Examples

The current user has `DEFAULT_SECONDARY_ROLES=('ALL')`. Custom roles `role1`, `role2`, and `role3` are granted
to the current user and are active as secondary roles:

Copy code

```
SELECT CURRENT_SECONDARY_ROLES();
```

```
+------------------------------------------------------+
|           CURRENT_SECONDARY_ROLES()                  |
+------------------------------------------------------+
| {"roles":"ROLE1,ROLE2,ROLE3","value":"ALL"}          |
+------------------------------------------------------+
```
