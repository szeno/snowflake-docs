# DATABASES view

This Information Schema view displays a row for each database defined in your account.

Note

This view uses Snowflake terminology of “database” whereas all the other Information Schema views use the standard INFORMATION\_SCHEMA terminology of “catalog”. The two terms have the same meaning.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| DATABASE\_NAME | VARCHAR | Name of the database. |
| DATABASE\_OWNER | VARCHAR | Name of the role that owns the database. |
| IS\_TRANSIENT | VARCHAR | Whether this is a transient database. |
| COMMENT | VARCHAR | Comment for this database. |
| CREATED | TIMESTAMP\_LTZ | Creation time of the database. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| RETENTION\_TIME | NUMBER | Number of days that historical data is retained for Time Travel. |
| TYPE | VARCHAR | Specifies the type of database. Valid values are:     - APPLICATION : a Snowflake Native App.   - APPLICATION\_PACKAGE : an application package.   - STANDARD: a normal database.   - IMPORTED DATABASE: a database created from a share.   - PERSONAL DATABASE: a personal database, linked to its owner. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- The view only displays objects for which the current role for the session has been granted access privileges. The view does not honor the MANAGE GRANTS privilege and consequently may show less
  information compared to a SHOW command when both are executed by a user who holds the MANAGE GRANTS privilege.
- This view contains all of the databases in the account (regardless of the database’s INFORMATION\_SCHEMA used to query the view).
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.
