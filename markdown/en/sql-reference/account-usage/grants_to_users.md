Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# GRANTS\_TO\_USERS view

This Account Usage view can be used to query the roles that have been granted to a user.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| CREATED\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the role is granted. |
| DELETED\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the role is revoked. |
| EXPIRES\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when a temporary role grant expires. `NULL` for permanent grants. |
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
  - Granting the same role to the same user again, from the same grantor, doesn’t add a row unless the statement changes the grant’s
    expiration. In that case, the DELETED\_ON column of the existing row is set, and a new row records the grant with its new EXPIRES\_ON
    and CREATED\_ON values.
- When a grant is revoked from the user, the DELETED\_ON column for the grant is updated from NULL to the timestamp when the grant was
  revoked.
- After revoking the role from the user, a grant of the same role to the same user is recorded in a new row. In this new row, the
  DELETED\_ON column value is NULL because the grant is now active.
- When a [temporary grant](/sql-reference/sql/grant-role#label-grant-role-temporary-grants) expires, its row keeps a NULL DELETED\_ON
  value until Snowflake removes the grant. DELETED\_ON then shows when the grant was removed, which is later than EXPIRES\_ON. To list
  grants that are currently active, filter on both columns. For example, in the ACCOUNT\_USAGE schema:

  Copy code

  ```
  SELECT role, grantee_name, granted_by, expires_on
    FROM SNOWFLAKE.ACCOUNT_USAGE.GRANTS_TO_USERS
    WHERE deleted_on IS NULL
      AND (expires_on IS NULL OR expires_on > CURRENT_TIMESTAMP());
  ```
