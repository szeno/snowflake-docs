Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# GRANTS\_TO\_USERS view

This Account Usage view can be used to query the roles that have been granted to a user.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CREATED\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the role is granted. |
| DELETED\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the role is revoked. |
| ROLE | VARCHAR | Identifier for the role granted to the user. |
| GRANTED\_TO | VARCHAR | For this view, the value is `USER`. |
| GRANTEE\_NAME | VARCHAR | Name of the user to whom the privilege is granted. |
| GRANTED\_BY | VARCHAR | Identifier for the role that granted the privilege. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The GRANTS\_TO\_USERS view **does not** include grants of privileges and non-account roles to users. For that information, see the
  [GRANTS\_TO\_ROLES view](/sql-reference/organization-usage/grants_to_roles).
- This view records current grants and historical grants, including grants that were revoked and granted again. When a single grant occurs
  and as long as it remains active (that is, not revoked):

  - The view includes one row for the grant of the same role to the same user.
  - A regrant of the same role to the same user is not recorded as a new row. Instead, the DELETED\_ON column remains NULL while the grant
    is active.
- When a grant is revoked from the user, the DELETED\_ON column for the grant is updated from NULL to the timestamp when the grant was
  revoked.
- After revoking the role from the user, a grant of the same role to the same user is recorded in a new row. In this new row, the
  DELETED\_ON column value is NULL because the grant is now active.
