Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# DATABASES view

This Account Usage view displays a row for each database defined in your account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database. |
| DATABASE\_NAME | VARCHAR | Name of the database. |
| DATABASE\_OWNER | VARCHAR | Name of the role that owns the database. |
| IS\_TRANSIENT | VARCHAR | Whether the database is transient. |
| COMMENT | VARCHAR | Comment for the database. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the database was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| DELETED | TIMESTAMP\_LTZ | Date and time when the database was dropped. |
| RETENTION\_TIME | NUMBER | Number of days that historical data is retained for Time Travel. |
| RESOURCE\_GROUP | VARCHAR | For internal use. |
| TYPE | VARCHAR | Specifies the type of database. Valid values are:     - APPLICATION: a Snowflake Native App.   - APPLICATION\_PACKAGE: an application package.   - STANDARD: a normal database.   - IMPORTED DATABASE: a database created from a share.   - PERSONAL DATABASE: a personal database linked to its owner. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| OBJECT\_VISIBILITY | OBJECT | `OBJECT_VISIBILITY`  [Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open  Available to all accounts.  This property controls the [discoverability of the objects](/user-guide/ui-snowsight/object-visibility-universal-search) in the account, enabling users without explicit access privileges to find objects and request access. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 180 minutes (3 hours).

- The view displays all of the databases in an account.
- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command executed by a user who holds the MANAGE GRANTS privilege.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
