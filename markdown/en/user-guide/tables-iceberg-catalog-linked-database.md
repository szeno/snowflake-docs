# Use a catalog-linked database for Apache Iceberg™ tables

With a catalog-linked database, you can access multiple remote Iceberg tables
from Snowflake without creating individual [externally managed tables](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration).

A catalog-linked database is a Snowflake database connected to an external Iceberg REST catalog.
Snowflake automatically syncs with the external catalog to detect namespaces and Iceberg tables,
and registers the remote tables to the catalog-linked database. Catalog-linked databases also support creating and dropping schemas or Iceberg tables.

## Billing for catalog-linked databases

Snowflake bills your account for the following usage:

- Automatic table discovery, create schema, drop schema, and drop table. Snowflake will bill your account for this usage under the
  CREDITS\_USED\_CLOUD\_SERVICES usage type. Usage for
  cloud services is charged only if the daily consumption of cloud services exceeds 10% of the daily usage of virtual warehouses. For more
  information, see [Understanding billing for cloud services usage](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage).
- Create table. Snowflake will bill your account for this usage under the CREDITS\_USED\_COMPUTE usage type through auto refresh.
  The cost for this usage is described in Table 5 of the [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) on the Snowflake website.
  Refer to the Snowflake-managed compute column for the Automated Refresh and Data Registration row.
- Creating a table when you query it before Snowflake has registered it. That work runs on the
  virtual warehouse that runs your statement, and Snowflake bills it as normal warehouse usage. For more information, see
  [On-demand table creation](#label-catalog-linked-db-on-demand-creation).

Snowflake won’t bill you for any cloud services that you use during table creation.

Note

To view the credit usage for your catalog-linked databases, use the [CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY view](/sql-reference/account-usage/catalog_linked_database_usage_history).

## Workflow to configure access to your external catalog and table storage

The following steps cover how to create a catalog-linked database, check the sync status between
Snowflake and your catalog, and create or query a table in the database.

1. [Configure access to your external catalog and table storage](#label-catalog-linked-db-access)
2. [Create a catalog-linked database](#label-catalog-linked-db-create)
3. [Check the catalog sync status](#label-catalog-linked-db-check-sync)
4. [Query a table in your catalog-linked database](#label-catalog-linked-db-query) or [Write to your remote catalog](#label-catalog-linked-db-write)

Note

- If your external data is in Unity Catalog, see [Tutorial: Set up bidirectional access to Apache Iceberg™ tables in Databricks Unity Catalog](/user-guide/tutorials/tables-iceberg-set-up-bidirectional-access-to-unity-catalog) to get started with catalog-linked databases.
- If your external data is in AWS Glue, see [Build Data Lakes using Apache Iceberg with Snowflake and AWS Glue](https://www.snowflake.com/en/developers/guides/data-lake-using-apache-iceberg-with-snowflake-and-aws-glue/).

## Configure access to your external catalog and table storage

Before you create a catalog-linked database, you need to configure access to
your external catalog and table storage. To configure this access, you configure a catalog integration with vended credentials. With this
option, your remote Iceberg catalog must support credential vending.

For instructions, see [Use catalog-vended credentials for Apache Iceberg™ tables](/user-guide/tables-iceberg-configure-catalog-integration-vended-credentials).

Note

If your remote Iceberg catalog doesn’t support credential vending, you must also configure an [external volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) to configure access to table storage.
For instructions, see
[configure an external volume for your cloud storage provider](/user-guide/tables-iceberg-configure-external-volume).
You still need a catalog integration for your external catalog. If you don’t use vended credentials, see
[configure an Apache Iceberg™ REST catalog integration for your remote Iceberg catalog](/user-guide/tables-iceberg-configure-catalog-integration-rest).

## Create a catalog-linked database

Create a catalog-linked database with the [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked) command:

The following example creates a catalog-linked database that uses vended credentials. The sync interval is 30 seconds, which is the default.
The sync interval tells Snowflake how often to poll your remote catalog.

Copy code

```
CREATE DATABASE my_linked_db
  LINKED_CATALOG = (
    CATALOG = 'my_catalog_int'
  );
```

Note

To create a catalog-linked database that uses an external volume, see [CREATE DATABASE (catalog-linked)](/sql-reference/sql/create-database-catalog-linked), including
the [example](/sql-reference/sql/create-database-catalog-linked#label-create-catalog-linked-database-examples).

Your catalog-linked database includes a link icon.

![A catalog-linked database with a link icon](/static/images/tables-iceberg-catalog-linked-database.png)

## Check the configuration of a catalog-linked database

After you create a catalog-linked database, use the [SYSTEM$GET\_CATALOG\_LINKED\_DATABASE\_CONFIG](/sql-reference/functions/system_get_catalog_linked_database_config) function to
check the configuration for the database.

Copy code

```
SELECT SYSTEM$GET_CATALOG_LINKED_DATABASE_CONFIG('my_linked_db');
```

## Check the catalog sync status

To check whether Snowflake has successfully linked your remote catalog to your database, use the [SYSTEM$CATALOG\_LINK\_STATUS](/sql-reference/functions/system_catalog_link_status)
function.

The function also provides information to help you identify tables in the remote catalog that fail to sync.

Copy code

```
SELECT SYSTEM$CATALOG_LINK_STATUS('my_linked_db');
```

### Identify tables that were created but couldn’t be initialized

To identify tables in the remote catalog that synced successfully but fail to refresh automatically, run the [SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables)
command, and then refer to the `auto_refresh_status` column in the output. These tables
have an `executionState` of `ICEBERG_TABLE_NOT_INITIALIZED` in the output.

For example, Snowflake might successfully discover and create a table in your remote catalog to your catalog-linked database, but this
table has a corrupted data file in your remote catalog. As a result, Snowflake can’t automatically refresh the table until you resolve
the error.

Automated refresh is turned off for these kinds of tables, so querying the table in Snowflake returns an error that says the
table was never initialized. To query the table, you must fix the error, and then [turn on automated refresh for the table](/user-guide/tables-iceberg-auto-refresh#label-tables-iceberg-auto-refresh-update).

## Query a table in your catalog-linked database

After you create a catalog-linked database, Snowflake starts the table discovery process and
automatically polls your linked catalog using the value of the SYNC\_INTERVAL\_SECONDS parameter (with a default interval of 30 seconds) to check for changes.

In the database, allowed namespaces from the remote catalog appear as schemas, and Iceberg tables appear under their respective schemas.

You can query the remote tables by using a SELECT statement.

Note

For the requirements for identifying objects in a catalog-linked database, see [Requirements for identifier resolution in a catalog-linked database](#label-catalog-linked-identifier-requirements).

For more information about object identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

For example:

Copy code

```
USE DATABASE my_linked_db;

SELECT * FROM my_namespace.my_iceberg_table
  LIMIT 20;
```

If the table exists in your remote catalog but Snowflake hasn’t registered it yet, that statement
creates the table instead of failing. For more information, see [On-demand table creation](#label-catalog-linked-db-on-demand-creation).

## On-demand table creation

Snowflake discovers new tables from your remote catalog automatically, on a regular sync interval.
On-demand table creation lets you skip that wait: if you reference a table that exists in your
remote catalog but isn’t registered in your catalog-linked database yet, Snowflake creates it as
part of running your statement instead of returning an error.

Normally, a table becomes available in a catalog-linked database only after Snowflake’s automatic
discovery process syncs with your remote catalog. If you add a table to the remote catalog and then
immediately query it from Snowflake by name, the query can fail because Snowflake hasn’t
discovered the table yet.

With on-demand table creation, referencing a not-yet-registered table by name triggers Snowflake to
create it during that statement, provided the table exists in the remote catalog. This can also
create the schema if the schema itself isn’t registered yet. You don’t need to wait for the next
discovery cycle.

### Reference a table before it’s registered

If you run a statement against a table that exists in your remote catalog but isn’t yet registered
in your catalog-linked database, Snowflake creates the table (and its schema, if that’s also
missing) and then completes your statement against it. That first statement might take longer than
later ones, because Snowflake creates the table as part of running it.

Copy code

```
USE DATABASE my_linked_db;

SELECT * FROM my_namespace.new_iceberg_table
  LIMIT 20;
```

On-demand table creation applies to the following statements:

- `SELECT`, including tables referenced in common table expressions (CTEs), subqueries, and views.
- The `SELECT` part of `CREATE TABLE ... AS SELECT` and `CREATE VIEW ... AS SELECT`.
- DML statements such as `INSERT`, `UPDATE`, `DELETE`, and `MERGE`, whether the statement reads from
  or writes to the table. For `INSERT ... SELECT` and `MERGE`, this applies to both the target table and
  the source table.
- `DESCRIBE TABLE`.

On-demand table creation doesn’t apply to other statements, such as `CREATE` (for the table being
created), `DROP`, `ALTER` (including `ALTER ICEBERG TABLE ... REFRESH`), `GRANT`, `REVOKE`, and
`COMMENT`. Until Snowflake registers a table, the table doesn’t appear in the output of
[SHOW ICEBERG TABLES](/sql-reference/sql/show-iceberg-tables) or in [INFORMATION\_SCHEMA](/sql-reference/info-schema) and
[ACCOUNT\_USAGE](/sql-reference/account-usage) views.

If the table doesn’t exist in your remote catalog either, the statement returns a standard
object-does-not-exist error, the same as it would for any missing table. The same is true if
Snowflake would need to create the schema and the schema’s namespace is excluded by the database’s
ALLOWED\_NAMESPACES or BLOCKED\_NAMESPACES list.

Snowflake runs this creation on the virtual warehouse that runs your statement, and bills it as
normal warehouse usage. The `CREATE ICEBERG TABLE` statement that Snowflake runs to create the table
appears in your query history even though you didn’t run it yourself.

If Snowflake can’t create the table, the statement returns an error similar to the following:

```
SQL Execution Error: Create of table 'my_iceberg_table' in the catalog-linked database failed: reason
```

## Write to your remote catalog

You can use Snowflake to create namespaces and Iceberg tables in your linked catalog. For more information, see the
following topics:

- [Write support for externally managed Apache Iceberg™ tables](/user-guide/tables-iceberg-externally-managed-writes)
- [Use CREATE SCHEMA to create namespaces in your external catalog](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-externally-managed-writes-create-schema)
- [Create an Iceberg table in a catalog-linked database](/user-guide/tables-iceberg-externally-managed-writes#label-tables-iceberg-external-writes-create-table-cld)

## Requirements for identifier resolution in a catalog-linked database

The requirement for resolving an identifier depends on the following:

- The value that you specified for the CATALOG\_CASE\_SENSITIVITY parameter when you
  [created your catalog-linked database](/sql-reference/sql/create-database-catalog-linked)
- Whether your external Iceberg catalog uses case-sensitive or case-insensitive identifiers.

Note

- These identifier resolution rules apply only to identifiers within the catalog-linked database. Identifiers
  outside the catalog-linked database follow standard Snowflake
  [identifier resolution rules](/sql-reference/identifiers-syntax).
- These requirements apply to all SQL statements, including queries and DDL commands such as CREATE and ALTER.
- If your catalog uses CASE\_INSENSITIVE mode (the default for catalogs like AWS Glue and Unity Catalog), you don’t need to
  double-quote identifiers for any commands. For DDL, Snowflake normalizes object names to lowercase on the remote catalog
  except when you use double-quoted mixed-case identifiers with QUOTED\_IDENTIFIERS\_IGNORE\_CASE set to FALSE (the default).
  See the CASE\_INSENSITIVE row in the table for details.
- If your catalog uses CASE\_SENSITIVE mode and normalizes to lowercase, you must use lowercase letters and surround
  the schema, table, and column names in double quotes when creating or altering objects.

The following table shows the requirement for each scenario:

| CATALOG\_CASE\_SENSITIVITY value | External Iceberg catalog uses | Requirement |
| --- | --- | --- |
| CASE\_SENSITIVE | Case sensitive identifiers | Snowflake matches identifiers exactly as they appear, including case. Snowflake automatically converts unquoted identifiers to uppercase, but quoted identifiers must match exactly the case in your external catalog.  The following example shows a valid query for creating a table:  Copy code  ``` CREATE TABLE "Table1" (id INT, name STRING); ```  Snowflake creates the table in the external catalog as `Table1`, which preserves the capitalization you used. Note that you can also create a lowercase `table1` table, if needed.  The following example shows a valid query for selecting the `Table1` table:  Copy code  ``` SELECT * FROM "Table1"; ```  In the previous example, the double quotes are required for matching the capitalization exactly.  The following example shows an invalid query, unless a `TABLE1` table exists:  Copy code  ``` SELECT * FROM table1; ```  In the previous example, the query is invalid if `TABLE1` doesn’t exist because the identifier isn’t surrounded with double quotes. As a result, Snowflake converts the identifier to uppercase.  The following example shows an invalid query for the case when an all uppercase `TABLE1` doesn’t exist:  Copy code  ``` SELECT * FROM TABLE1; ``` |
| CASE\_SENSITIVE | Case insensitive identifiers | If the external Iceberg catalog is actually case insensitive, and normalizes to lowercase, you must surround identifiers in double quotes.  The following example shows valid queries:  Copy code  ``` SELECT * from "s1"; SELECT * from "lowercasetablename"; ``` |
| CASE\_INSENSITIVE | Case insensitive identifiers | If your case-insensitive catalog has a lowercase `table1` table, all of the following queries are valid:  Copy code  ``` SELECT * from table1; SELECT * from TABLE1; SELECT * from Table1; SELECT * from "table1"; ```  You don’t need to use double quotes when creating or altering objects. The DDL examples that follow show how Snowflake normalizes object names to lowercase on the remote catalog; the **Quoted identifiers** and **QUOTED\_IDENTIFIERS\_IGNORE\_CASE parameter** subsections describe when double quotes preserve mixed case. For example:  Copy code  ``` CREATE SCHEMA My_Schema; ```  Snowflake creates the schema as `my_schema` on the remote catalog. You can then refer to it using any casing:  Copy code  ``` CREATE ICEBERG TABLE My_Schema.My_Table (Col1 INT, Col2 STRING); ```  Snowflake creates the table as `my_table` with columns `col1` and `col2` (all lowercase) on the remote catalog.  Copy code  ``` ALTER ICEBERG TABLE my_table ADD COLUMN New_Col STRING; ```  Snowflake adds the column as `new_col` (lowercase) on the remote catalog.  Copy code  ``` ALTER ICEBERG TABLE my_table RENAME COLUMN col2 TO Aux_Column; ```  Snowflake renames the column to `aux_column` (lowercase) on the remote catalog.  **Quoted identifiers**: When [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case) is FALSE (the default), double-quoted identifiers preserve the exact casing you specify. For example, `CREATE SCHEMA "MySchema"` creates a schema named `MySchema` (mixed case) on the remote catalog. You must then use the same quoted form to reference it.  **QUOTED\_IDENTIFIERS\_IGNORE\_CASE parameter**: When [QUOTED\_IDENTIFIERS\_IGNORE\_CASE](/sql-reference/parameters#label-quoted-identifiers-ignore-case) is TRUE in a catalog-linked database with CASE\_INSENSITIVE, Snowflake resolves identifiers in a case-insensitive manner whether they are double-quoted or unquoted. For DDL, Snowflake still normalizes object names to lowercase on the remote catalog, consistent with the unquoted DDL examples in this section. |
| CASE\_INSENSITIVE | Case sensitive identifiers | If the external Iceberg catalog is actually case sensitive, Snowflake treats unquoted identifiers as case-insensitive and automatically converts unquoted identifiers to uppercase. When you create or query objects, Snowflake matches identifiers regardless of case, as long as they are unquoted.  Using this pattern is discouraged because Snowflake can’t resolve two different identifiers that differ in casing. This pattern only works when no two identifiers are different in casing only.  Consider the case where the remote catalog has a `Table1` table. All of the following queries are valid for querying that table.  Copy code  ``` SELECT * from table1; SELECT * from TABLE1; SELECT * from Table1; SELECT * from "Table1"; ```  Quoted identifiers preserve case and match exactly. However, in CASE\_INSENSITIVE mode, unquoted and quoted forms are both supported. |

Expand

Show lessSee more

## Considerations for using a catalog-linked database for Iceberg tables

Consider the following items when you use a catalog-linked database:

- Supported only when you use a catalog integration for Iceberg REST (for example, Snowflake Open Catalog).
- To limit automatic table discovery to a specific set of namespaces, use the ALLOWED\_NAMESPACES parameter. You can also use the
  BLOCKED\_NAMESPACES parameter to block a set of namespaces.
- Snowflake doesn’t sync remote catalog access control for users or roles.
- You can create schemas, externally managed Iceberg tables, or database roles in a catalog-linked database. Creating other Snowflake objects
  isn’t currently supported.
- When you create a catalog-linked database, you can’t specify the default Iceberg version or merge-on-read behavior to use for
  Iceberg tables.

  However, you can modify these properties for an existing database by using the [ALTER DATABASE (catalog-linked)](/sql-reference/sql/alter-database-catalog-linked)
  command to set the following parameters:

  - ICEBERG\_VERSION\_DEFAULT
  - ICEBERG\_MERGE\_ON\_READ\_BEHAVIOR
- For Iceberg tables in a catalog-linked database:

  - Snowflake bidirectionally syncs table and column descriptions between the remote catalog and Snowflake. Sync can
    update a description to a new value, but never replaces a non-empty description with an empty one. Other remote catalog
    table properties, such as retention policies or buffers, aren’t copied, and altering table properties isn’t currently
    supported.
  - [Automated refresh](/user-guide/tables-iceberg-auto-refresh) is enabled by default. If the `table-uuid` of an external table
    and the catalog-linked database table don’t match, refresh fails and Snowflake drops the table from the catalog-linked database; Snowflake doesn’t change the remote table.
  - If you drop a table from the remote catalog, Snowflake drops the table from the catalog-linked database.
    This action is asynchronous, so you might not see the change in the remote catalog right away.
  - If you rename a table in the remote catalog, Snowflake drops the existing table from the catalog-linked database and creates a table with the new name.
  - Masking policies and tags are supported. Other Snowflake-specific features, including replication and cloning, aren’t supported.
  - The character that you choose for the NAMESPACE\_FLATTEN\_DELIMITER parameter can’t appear in your remote namespaces. During the auto discovery process,
    Snowflake skips any namespace that contains the delimiter, and doesn’t create a corresponding schema in your catalog-linked database.
  - If you specify anything other than `_`, `$`, or numbers for the NAMESPACE\_FLATTEN\_DELIMITER parameter,
    you must put the schema name in quotes when you query the table.
  - To check whether a namespace is nested under another namespace, use the [SHOW SCHEMAS](/sql-reference/sql/show-schemas) command
    and check the `is_nested` column in the output.
  - For databases linked to AWS Glue, you must use lowercase letters and surround the schema, table, and column names in double quotes.
    This is also required for other Iceberg REST catalogs that only support lowercase identifiers.

    The following example shows a valid query:

    Copy code

    ```
    CREATE SCHEMA "s1";
    ```

    The following statements aren’t valid, because they use uppercase letters or omit the double quotes:

    Copy code

    ```
    CREATE SCHEMA s1;
    CREATE SCHEMA "Schema1";
    ```
  - Using UNDROP ICEBERG TABLE isn’t supported.
  - Sharing:

    - [Sharing with a listing](/collaboration/use-auto-fulfillment-with-open-table-formats) is supported for catalog-linked databases that use Apache Iceberg™ REST catalog integrations.
    - Direct sharing is supported
- For writing to tables in a catalog-linked database:

  - Creating and writing to tables in nested namespaces is supported only when your catalog integration uses a catalog that
    supports nested namespaces. For other REST catalogs, creating and writing to tables in nested namespaces isn’t supported.
  - Don’t use a period (`.`) in a namespace name unless period is the value you set for NAMESPACE\_FLATTEN\_DELIMITER and
    NAMESPACE\_MODE is set to FLATTEN\_NESTED\_NAMESPACE. Otherwise, the namespace won’t be created.
  - Position [row-level deletes](https://iceberg.apache.org/spec/#row-level-deletes) are supported for tables stored
    on Amazon S3, Azure, or Google Cloud. Row-level deletes with equality delete files aren’t supported. For more information about row-level deletes,
    see [Use row-level deletes](/user-guide/tables-iceberg-manage#label-tables-iceberg-row-level-deletes). To turn off position deletes, which enable
    running the Data Manipulation Language (DML) operations in copy-on-write mode, set the `ICEBERG_MERGE_ON_READ_BEHAVIOR` parameter to `'DISABLED'` at the table, schema, or
    database level.
