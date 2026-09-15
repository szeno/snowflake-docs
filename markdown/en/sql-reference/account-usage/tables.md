Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# TABLES view

This Account Usage view displays a row for each table and view in the account.

See also:
:   [COLUMNS view](/sql-reference/account-usage/columns) , [VIEWS view](/sql-reference/account-usage/views), [TABLES view](/sql-reference/info-schema/tables) (Information Schema)

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| TABLE\_ID | NUMBER | Internal, Snowflake-generated identifier for the table. |
| TABLE\_NAME | VARCHAR | Name of the table. |
| TABLE\_SCHEMA\_ID | NUMBER | Internal, Snowflake-generated identifier of the schema for the table. |
| TABLE\_SCHEMA | VARCHAR | Schema that the table belongs to. |
| TABLE\_CATALOG\_ID | NUMBER | Internal, Snowflake-generated identifier of the database for the table. |
| TABLE\_CATALOG | VARCHAR | Database that the table belongs to. |
| TABLE\_OWNER | VARCHAR | Name of the role that owns the table. |
| TABLE\_TYPE | VARCHAR | Indicates the table type. Valid values are `BASE TABLE`, `TEMPORARY TABLE`, `EXTERNAL TABLE`, `EVENT TABLE`, `VIEW`, or `MATERIALIZED VIEW`. |
| IS\_TRANSIENT | VARCHAR | Indicates whether the table is transient. |
| CLUSTERING\_KEY | VARCHAR | Column(s) and/or expression(s) that comprise the clustering key for the table. |
| ROW\_COUNT | NUMBER | Number of rows in the table. |
| BYTES | NUMBER | Number of bytes accessed by a scan of the table. |
| RETENTION\_TIME | NUMBER | Number of days that historical data is retained for Time Travel. |
| SELF\_REFERENCING\_COLUMN\_NAME | VARCHAR | Not applicable for Snowflake. |
| REFERENCE\_GENERATION | VARCHAR | Not applicable for Snowflake. |
| USER\_DEFINED\_TYPE\_CATALOG | VARCHAR | Not applicable for Snowflake. |
| USER\_DEFINED\_TYPE\_SCHEMA | VARCHAR | Not applicable for Snowflake. |
| USER\_DEFINED\_TYPE\_NAME | VARCHAR | Not applicable for Snowflake. |
| IS\_INSERTABLE\_INTO | VARCHAR | Not applicable for Snowflake. |
| IS\_TYPED | VARCHAR | Not applicable for Snowflake. |
| COMMIT\_ACTION | VARCHAR | Not applicable for Snowflake. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the table was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time the object was last altered by a DML, DDL, or background metadata operation. See [Usage Notes](#usage-notes). |
| LAST\_DDL | TIMESTAMP\_LTZ | Timestamp of the last DDL operation performed on the table or view.  All supported table/view DDL operations update this field:   - { CREATE | ALTER | DROP | UNDROP } TABLE - { CREATE | ALTER | DROP } VIEW   All ALTER TABLE operations update this field, including setting or unsetting a table parameter (for example, COMMENT, DATA\_RETENTION\_TIME, etc.) and changes to table columns (ADD / MODIFY / RENAME / DROP).  For more information, see the [Usage Notes](#usage-notes). |
| LAST\_DDL\_BY | VARCHAR | The current username for the user who executed the last DDL operation. If the user has been dropped, shows `DROPPED_USER(<id>)`.  For dropped users, you can join the `<id>` with the USER\_ID column in the USERS view of the ACCOUNT\_USAGE or ORGANIZATION\_USAGE schema. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the table was dropped. |
| AUTO\_CLUSTERING\_ON | VARCHAR | Status of Automatic Clustering for a table. For details, see [Viewing the Automatic Clustering status for a table](/user-guide/tables-auto-reclustering#label-viewing-auto-clustering). |
| COMMENT | VARCHAR | Comment for the table. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| INSTANCE\_ID | NUMBER | Internal/system-generated identifier for the instance which the object belongs to. |
| IS\_ICEBERG | VARCHAR | Indicates whether the table is an [Iceberg table](/user-guide/tables-iceberg). Valid values are `YES` or `NO`. |
| IS\_DYNAMIC | VARCHAR | Indicates whether the table is a [dynamic table](/user-guide/dynamic-tables/overview). Valid values are `YES` or `NO`. |
| IS\_HYBRID | VARCHAR | Indicates whether the table is a [hybrid table](/user-guide/tables-hybrid). Valid values are `YES` or `NO`. |
| ARCHIVE\_STORAGE\_COOL\_ROW\_COUNT | NUMBER | The number of rows that are in the COOL storage tier. |
| ARCHIVE\_STORAGE\_COOL\_BYTES | NUMBER | The number of bytes accessed by retrieving data from the COOL storage tier. |
| ARCHIVE\_STORAGE\_COLD\_ROW\_COUNT | NUMBER | The number of rows that are in the COLD storage tier. |
| ARCHIVE\_STORAGE\_COLD\_BYTES | NUMBER | The number of bytes accessed by retrieving data from the COLD storage tier. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 90 minutes.
- Note

  With [BCR-2127](/release-notes/bcr-bundles/2025_07/bcr-2127),
  this view includes new columns for storage lifecycle policies.
  To view storage lifecycle policy columns, you must enable the 2025\_07 behavior change bundle
  in your account.

  To [enable this bundle in your account](/release-notes/bcr-bundles/managing-behavior-change-releases#label-manage-bcr-enable-bundle),
  execute the following statement:

  Copy code

  ```
  SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2025_07');
  ```

- The view does not recognize the MANAGE GRANTS privilege and consequently may show less information compared to a SHOW command executed by a user who holds the MANAGE GRANTS privilege.
- Querying the `SUM(BYTES)` for a table does not represent the total storage usage, because the amount does not include Time Travel and Fail-safe usage.
- Using the value in the LAST\_ALTERED column for Time Travel is \_not\_ recommended and can return unexpected results for the following
  reaons:

  - Time Travel can only be used to query historical data modified by a [DML operation](/user-guide/data-time-travel#label-time-travel-querying).
  - The LAST\_ALTERED column inludes both DML and DDL operations (see the next usage note).
  - For DML operations, the value in the LAST\_ALTERED column is the timestamp at the beginning of the statement execution rather than
    the time of the commit of the transaction containing this statement.
- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

  For views and tables, use the LAST\_DDL column for the last modification time for an object.
- The value in the LAST\_DDL column is updated as follows:

  > - When a table or view is created, the LAST\_DDL timestamp is the same as the CREATED timestamp.
  > - When a table or view is dropped, the LAST\_DDL timestamp is the same as the DELETED timestamp.
  > - Last DDL data is not available for operations that occurred before the columns were
  >   [added](/release-notes/bcr-bundles/2023_01/bcr-891). The new DDL fields contain `null` until a DDL operation is executed.
  > - For replicated databases, the LAST\_DDL and LAST\_DDL\_BY fields are only updated for objects in the primary database. After failover, the
  >   LAST\_DDL and LAST\_DDL\_BY fields are updated for DDL operations for the tables and views in the newly promoted primary database. These
  >   fields will remain unchanged for objects in the now secondary database.
  > - For objects in secondary databases that are newly created during a refresh operation, these fields are `null`.
- The LAST\_ALTERED column does not necessarily indicate the last refreshed time for external tables.
  To retrieve the last refreshed time for an auto-refreshed external table, you can use the
  [SYSTEM$EXTERNAL\_TABLE\_PIPE\_STATUS](/sql-reference/functions/system_external_table_pipe_status) function, which returns
  information such as the timestamp of the last file Snowflake has registered.

## Examples

Retrieve the total size (in bytes) of all active tables in all schemas in your account:

Copy code

```
SELECT table_schema, SUM(bytes)
  FROM SNOWFLAKE.ACCOUNT_USAGE.TABLES
  WHERE deleted IS NULL
  GROUP BY table_schema;
```
