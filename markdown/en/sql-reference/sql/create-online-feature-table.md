# CREATE ONLINE FEATURE TABLE

Creates a new online feature table in the current/specified schema or replaces an existing table.

See also:
:   [ALTER ONLINE FEATURE TABLE](/sql-reference/sql/alter-online-feature-table) , [DESCRIBE ONLINE FEATURE TABLE](/sql-reference/sql/desc-online-feature-table), [DROP ONLINE FEATURE TABLE](/sql-reference/sql/drop-online-feature-table) , [SHOW ONLINE FEATURE TABLES](/sql-reference/sql/show-online-feature-tables)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] ONLINE FEATURE TABLE <name>
  PRIMARY KEY ( <col_name> [ , <col_name> , ... ] )
  TARGET_LAG = '<num> { seconds | minutes | hours | days }'
  WAREHOUSE = <warehouse_name>
  [ REFRESH_MODE = { AUTO | FULL | INCREMENTAL } ]
  [ TIMESTAMP_COLUMN = <col_name> ]
  [ [ WITH ] COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
FROM <source>
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the online feature table; must be unique for the schema in which the table is created.

`PRIMARY KEY ( col_name [ , col_name , ... ] )`
:   Specifies the required primary key constraint of the table. Primary key serves as a unique identifier of every row in the table and serves as a lookup key in the fast SELECT queries.

`TARGET_LAG = 'num { seconds | minutes | hours | days }'`
:   Specifies the maximum amount of time that the online feature table’s content should lag behind updates to the source.

    Must be between 10 seconds and 8 days, inclusive.

`WAREHOUSE = warehouse_name`
:   Specifies the name of the warehouse that provides the compute resources for refreshing the online feature table.

    You must use a role that has the USAGE privilege on this warehouse in order to create the online feature table.

`FROM source`
:   Specifies the data source of the online feature table. Must be either a view or a dynamic table.

## Optional parameters

`REFRESH_MODE = \{ AUTO | FULL | INCREMENTAL \}`
:   Specifies the refresh mode for the online feature table.

    Note

    This property cannot be altered after you create the online feature table. To modify the property, recreate the online feature table.

    `AUTO`
    :   When refresh mode is AUTO, the system attempts to apply an incremental refresh by default. However, when incremental refresh isn’t supported or expected to perform well, the online feature table automatically selects full refresh instead.

        To determine the best mode for your use case, experiment with refresh modes and automatic recommendations. For consistent behavior across Snowflake releases, explicitly set the refresh mode on all online feature tables.

        To verify the refresh mode for your online feature tables, view online feature table refresh mode using SHOW ONLINE FEATURE TABLES command.

    `FULL`
    :   Enforces a full refresh of the online feature table, even if the online feature table can be incrementally refreshed.

    `INCREMENTAL`
    :   Enforces an incremental refresh of the online feature table. If the query that underlies the online feature table can’t perform an incremental refresh, online feature table creation fails and displays an error message.

    Default: AUTO

`TIMESTAMP_COLUMN = col_name`
:   Specifies the column in the source treated as the timestamp column.

    Default: No value

`COMMENT = 'string_literal'`
:   Specifies a comment for the online feature table.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the tag name and the tag string value. The maximum number of characters for the tag value is 256.

    Default: No value

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE ONLINE FEATURE TABLE | Schema | Role that has the CREATE ONLINE FEATURE TABLE privilege on the schema. |
| USAGE | Warehouse | Required on the warehouse specified in the WAREHOUSE parameter |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

Attention

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example creates an online feature table named `my_online_feature_table` with a primary key on the `ID` column:

Copy code

```
CREATE ONLINE FEATURE TABLE my_online_feature_table
  PRIMARY KEY (ID)
  TIMESTAMP_COLUMN = 'TS'
  TARGET_LAG = '30 seconds'
  WAREHOUSE = MY_WAREHOUSE
FROM MY_SOURCE_DYNAMIC_TABLE;
```

In this example, `ID` and `TS` refer to the respective columns in the existing dynamic table `MY_SOURCE_DYNAMIC_TABLE`.
