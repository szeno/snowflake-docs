# ALTER TABLE (event tables)

Modifies the properties, columns, or constraints for an existing [event table](/developer-guide/logging-tracing/event-table-setting-up).

See also:
:   [CREATE EVENT TABLE](/sql-reference/sql/create-event-table) , [DROP TABLE](/sql-reference/sql/drop-table) , [SHOW EVENT TABLES](/sql-reference/sql/show-event-tables) , [DESCRIBE EVENT TABLE](/sql-reference/sql/desc-event-table)

## Syntax

Copy code

```
ALTER TABLE [ IF EXISTS ] <name> RENAME TO <new_table_name>

ALTER TABLE [ IF EXISTS ] <name> clusteringAction

ALTER TABLE [ IF EXISTS ] <name> dataGovnPolicyTagAction

ALTER TABLE [ IF EXISTS ] <name> searchOptimizationAction

ALTER TABLE [ IF EXISTS ] <name> SET
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ CHANGE_TRACKING = { TRUE | FALSE  } ]
  [ CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ] ]
  [ COMMENT = '<string_literal>' ]

ALTER TABLE [ IF EXISTS ] <name> UNSET {
                                       DATA_RETENTION_TIME_IN_DAYS         |
                                       MAX_DATA_EXTENSION_TIME_IN_DAYS     |
                                       CHANGE_TRACKING                     |
                                       CONTACT <purpose>                   |
                                       COMMENT                             |
                                       }
```

Where:

> Copy code
>
> ```
> clusteringAction ::=
>   {
>      CLUSTER BY ( <expr> [ , <expr> , ... ] )
>    | { SUSPEND | RESUME } RECLUSTER
>    | DROP CLUSTERING KEY
>   }
> ```
>
> Copy code
>
> ```
> dataGovnPolicyTagAction ::=
>   {
>       SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]
>     | UNSET TAG <tag_name> [ , <tag_name> ... ]
>   }
>   |
>   {
>       ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ROW ACCESS POLICY <policy_name>
>     | DROP ROW ACCESS POLICY <policy_name> ,
>         ADD ROW ACCESS POLICY <policy_name> ON ( <col_name> [ , ... ] )
>     | DROP ALL ROW ACCESS POLICIES
>   }
> ```
>
> Copy code
>
> ```
> searchOptimizationAction ::=
>   {
>      ADD SEARCH OPTIMIZATION [
>        ON <search_method_with_target> [ , <search_method_with_target> ... ]
>      ]
>
>    | DROP SEARCH OPTIMIZATION [
>        ON { <search_method_with_target> | <column_name> | <expression_id> }
>           [ , ... ]
>      ]
>
>   }
> ```
>
> For details, see [Search optimization actions ()](#label-alter-table-searchoptimizationaction-event-table).

## Parameters

`name`
:   Identifier for the event table to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in double
    quotes. Identifiers enclosed in double quotes are also case-sensitive.

`RENAME TO new_table_name`
:   Renames the specified event table with a new identifier that is not currently used by any other event tables in the schema.

    Note

    Not supported on the default event table, SNOWFLAKE.TELEMETRY.EVENTS.

    For more details about event table identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object (table, column, etc.) is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Specifies one or more properties/parameters to set for the event table (separated by blank spaces, commas, or new lines):

    `DATA_RETENTION_TIME_IN_DAYS = integer`
    :   Object-level parameter that modifies the retention period for the event table for Time Travel. For more details, see
        [Understanding & using Time Travel](/user-guide/data-time-travel) and [Working with Temporary and Transient Tables](/user-guide/tables-temp-transient).

        For a detailed description of this parameter, as well as more information about object parameters, see [Parameters](/sql-reference/parameters).

        Values:

        > - Standard Edition: `0` or `1`
        > - Enterprise Edition:
        >   - `0` to `90` for permanent event tables
        >   - `0` or `1` for temporary and transient event tables

        Note

        A value of `0` effectively disables Time Travel for the event table.

    `MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
    :   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for the event table to
        prevent streams on the event table from becoming stale.

        For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

    `CHANGE_TRACKING = { TRUE | FALSE }`
    :   Specifies to enable or disable change tracking on the event table.

        - `TRUE` enables change tracking on the event table. This option adds a pair of hidden columns to the source event table and begins storing
          change tracking metadata in the columns. These columns consume a small amount of storage.

          The change tracking metadata can be queried using the [CHANGES](/sql-reference/constructs/changes) clause for [SELECT](/sql-reference/sql/select)
          statements, or by creating and querying one or more streams on the event table.
        - `FALSE` disables change tracking on the event table. The pair of hidden columns is dropped from the event table.

    `CONTACT purpose = contact [ , purpose = contact ... ]`
    :   Associate the existing object with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

        You cannot set the CONTACT property with other properties in the same statement.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the event table.

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the event table, which resets them back to their defaults:

    - `DATA_RETENTION_TIME_IN_DAYS`
    - `MAX_DATA_EXTENSION_TIME_IN_DAYS`
    - `CHANGE_TRACKING`
    - `CONTACT purpose`
    - `COMMENT`

    You cannot unset the CONTACT property with other properties in the same statement.

## Data Governance policy and tag actions (`dataGovnPolicyTagAction`)

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`policy_name`
:   Identifier for the policy; must be unique for your schema.

The following clauses apply to all table kinds that support row access policies, such as but not limited to tables, views, and event tables.
To simplify, the clauses just refer to “table.”

> `ADD ROW ACCESS POLICY policy_name ON (col_name [ , ... ])`
> :   Adds a row access policy to the table.
>
>     At least one column name must be specified. Additional columns can be specified with a comma separating each column name. Use this
>     expression to add a row access policy to both an event table and an external table.
>
> `DROP ROW ACCESS POLICY policy_name`
> :   Drops a row access policy from the table.
>
>     Use this clause to drop the policy from the table.
>
> `DROP ROW ACCESS POLICY policy_name, ADD ROW ACCESS POLICY policy_name ON ( col_name [ , ... ] )`
> :   Drops the row access policy that is set on the table and adds a row access policy to the same table in a single SQL statement.
>
> `DROP ALL ROW ACCESS POLICIES`
> :   Drops all [row access policy](/user-guide/security-row-using) associations from the table.
>
>     This expression is helpful when a row access policy is dropped from a schema before dropping the policy from an event table. Use this expression to drop row access policy associations from the table.
>
>     Suppose that a row access policy applied to the table when the backup was created, and the policy was later dropped. After you
>     restore the table from a [backup](/user-guide/backups), you can’t query it until you run an ALTER TABLE command with the
>     DROP ALL ROW ACCESS POLICIES clause.
>
> `SET AGGREGATION POLICY policy_name`
> :   `[ ENTITY KEY (col_name [ , ... ]) ] [ FORCE ]`
>     :   Assigns an [aggregation policy](/user-guide/aggregation-policies) to the table.
>
>         Use the optional ENTITY KEY parameter to define which columns uniquely identity an entity within the table. For more information, see
>         [Implementing entity-level privacy with aggregation policies](/user-guide/aggregation-policies-entity-privacy).
>
>         Use the optional FORCE parameter to atomically replace an existing aggregation policy with the new aggregation policy.
>
> `UNSET AGGREGATION POLICY`
> :   Detaches an aggregation policy from the table.
>
> `SET JOIN POLICY policy_name`
> :   `[ FORCE ]`
>     :   Assigns a [join policy](/user-guide/join-policies) to the table.
>
>         Use the optional FORCE parameter to atomically replace an existing join policy with the new join policy.
>
> `UNSET JOIN POLICY`
> :   Detaches a join policy from the table.

## Clustering actions (`clusteringAction`)

`CLUSTER BY ( expr [ , expr , ... ] )`
:   Specifies (or modifies) one or more event table columns or column expressions as the clustering key for the event table. These are the
    columns/expressions for which clustering is maintained by Automatic Clustering.

    Important

    Clustering keys are not intended or recommended for all event tables; they typically benefit very large (i.e. multi-terabyte) event tables.

    Before you specify a clustering key for an event table, please see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

`SUSPEND | RESUME RECLUSTER`
:   Enables or disables [Automatic Clustering](/user-guide/tables-auto-reclustering) for the event table.

`DROP CLUSTERING KEY`
:   Drops the clustering key for the event table.

For more information about clustering keys and reclustering, see [Understanding Snowflake Table Structures](/user-guide/tables-micro-partitions).

## Search optimization actions (`searchOptimizationAction`)

`ADD SEARCH OPTIMIZATION`
:   Adds [search optimization](/user-guide/search-optimization-service) for the entire event table or, if you specify the optional
    ON clause, for specific columns.

    Note:

    - Search optimization can be expensive to maintain, especially if the data in the event table changes frequently.
      For more information, see [Search optimization cost estimation and management](/user-guide/search-optimization/cost-estimation#label-search-optimization-maintenance-billing).
    - If you try to add search optimization on a materialized view, Snowflake returns an error message.

[Preview Feature](/release-notes/preview-features) — Open

The ON clause is part of a preview feature that is available to all accounts that are Enterprise Edition (or higher).

`ON search_method_with_target [, search_method_with_target ... ]`
:   Specifies that you want to configure search optimization for specific columns or VARIANT fields (rather than the entire event table).

    For `search_method_with_target`, use an expression with the following syntax:

    Copy code

    ```
    <search_method>(<target> [, ...])
    ```

    Where:

    - `search_method` specifies one of the following methods that optimizes queries for a particular type of predicate:

      | Search Method | Description |
      | --- | --- |
      | `EQUALITY` | Equality and IN predicates. |
      | `SUBSTRING` | Predicates that match substrings and regular expressions (e.g. [[ NOT ] LIKE](/sql-reference/functions/like), [[ NOT ] ILIKE](/sql-reference/functions/ilike), [[ NOT ] RLIKE](/sql-reference/functions/rlike), [REGEXP\_LIKE](/sql-reference/functions/regexp_like), etc.) |
      | `GEO` | Predicates that use GEOGRAPHY types. |

      Expand

      Show lessSee more
    - `target` specifies the column, VARIANT field, or an asterisk (\*).

      Depending on the value of `search_method`, you can specify a column or VARIANT field of one of the following types:

      | Search Method | Supported Targets |
      | --- | --- |
      | `EQUALITY` | Columns of numerical, string, binary, and VARIANT data types, including paths to fields in VARIANTs.  To specify a VARIANT field, use a colon-delimited path to the field (e.g. `my_column:my_field_name:my_nested_field_name`), or use [dot or bracket notation](/user-guide/querying-semistructured#label-traversing-semistructured-data) (e.g. `my_column:my_field_name.my_nested_field_name` or `my_column['my_field_name']['my_nested_field_name']`).  When you specify a VARIANT field, the configuration applies to all nested fields under that field. For example, suppose that you specify `ON EQUALITY(src:a.b)`:  - This configuration can improve queries `on src:a.b` and on any nested fields (e.g. `src:a.b.c`, `src:a.b.c.d`,   etc.). - This configuration does not affect queries that do not use the `src:a.b` prefix (e.g. `src:a`, `src:z`, etc.). |
      | `SUBSTRING` | Columns of string data types. |
      | `GEO` | Columns of the GEOGRAPHY data type. |

      Expand

      Show lessSee more

      To specify all applicable columns in the event table as targets, use an asterisk (`*`).

      Note that you cannot specify both an asterisk and specific column names for a given search method. However, you can
      specify an asterisk in different search methods.

      For example, you can specify the following expressions:

      Copy code

      ```
      -- Allowed
      ON SUBSTRING(*)
      ON EQUALITY(*), SUBSTRING(*), GEO(*)
      ```

      You cannot specify the following expressions:

      Copy code

      ```
      -- Not allowed
      ON EQUALITY(*, c1)
      ON EQUALITY(c1, *)
      ON EQUALITY(v1:path, *)
      ON EQUALITY(c1), EQUALITY(*)
      ```

    To specify more than one search method on a target, use a comma to separate each subsequent method and target:

    Copy code

    ```
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1), EQUALITY(c2, c3);
    ```

    If you run the ALTER TABLE … ADD SEARCH OPTIMIZATION ON … command multiple times on the same event table, each subsequent command
    adds to the existing configuration for the event table. For example, suppose that you run the following commands:

    Copy code

    ```
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2);
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c3, c4);
    ```

    This adds equality predicates for the columns c1, c2, c3, and c4 to the configuration for the event table. This is equivalent to
    running the command:

    Copy code

    ```
    ALTER TABLE t1 ADD SEARCH OPTIMIZATION ON EQUALITY(c1, c2, c3, c4);
    ```

    For examples, see [Enabling search optimization for specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-adding).

`DROP SEARCH OPTIMIZATION`
:   Removes [search optimization](/user-guide/search-optimization-service) for the entire event table or, if you specify the
    optional ON clause, from specific columns.

    Note:

    - If an event table has the search optimization property, then dropping the event table and undropping it preserves the
      search optimization property.
    - Removing the search optimization property from an event table and then adding it back incurs the same cost as adding it the first
      time.

[Preview Feature](/release-notes/preview-features) — Open

The ON clause is part of a preview feature that is available to all accounts that are Enterprise Edition (or higher).

`ON search_method_with_target | column_name | expression_id [, ... ]`
:   Specifies that you want to drop the search optimization configuration for specific columns or VARIANT fields (rather than
    dropping search optimization for the entire event table).

    To identify the column configuration to drop, specify one of the following:

    - For `search_method_with_target`, specify a method for optimizing queries for one or more specific targets, which can
      be columns or VARIANT fields. Use the
      [syntax described earlier](/sql-reference/sql/alter-table#label-alter-table-searchoptimizationaction-search-method-target).
    - For `column_name`, specify the name of the column configured for search optimization. Specifying the column name drops
      all expressions for that column, including expressions that use VARIANT fields in the column.
    - For `expression_id`, specify the ID for an expression listed in the output of the
      [DESCRIBE SEARCH OPTIMIZATION](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-displaying) command.

    To specify more than one of these, use a comma between items.

    You can specify any combination of search methods with targets, column names, and expression IDs.

    For examples, see [Dropping search optimization for specific columns](/user-guide/search-optimization/enabling#label-search-optimization-service-configuration-dropping).

## Usage notes

- Changes to an event table are not automatically propagated to views created on that event table.
- To alter an event table, you must be using a role that has ownership privilege on the event table.
- To add clustering to an event table, you must also have USAGE or OWNERSHIP privileges on the schema and database that
  contain the event table.

- For row access policies:
  - Snowflake supports adding and dropping row access policies in a single SQL statement.

    For example, to replace a row access policy that is already set on a table with a different policy, drop the row access policy first
    and then add the new row access policy.
  - For a given resource (i.e. table or view), to `ADD` or `DROP` a row access policy you must have either the
    [APPLY ROW ACCESS POLICY](/user-guide/security-row-intro#label-security-row-privileges) privilege on the schema, or the
    [OWNERSHIP](/user-guide/security-row-intro#label-security-row-privileges) privilege on the resource and the APPLY privilege on the row access policy resource.
  - A table or view can only be protected by one row access policy at a time. Adding a policy fails if the policy body refers to a table or
    view column that is protected by a row access policy or the column protected by a masking policy.

    Similarly, adding a masking policy to a table column fails if the masking policy body refers to a table that is protected by a row
    access policy or another masking policy.
  - Row access policies cannot be applied to system views or table functions.
  - Similar to other [DROP <object>](/sql-reference/sql/drop) operations, Snowflake returns an error if attempting to drop a row access policy from a
    resource that does not have a row access policy added to it.
  - If an object has both a row access policy and one or more masking policies, the row access policy is evaluated first.

- If you create a foreign key, the columns in the REFERENCES clause must be listed in the same order as they were
  listed for the primary key. For example:

  Copy code

  ```
  CREATE TABLE parent ... CONSTRAINT primary_key_1 PRIMARY KEY (c_1, c_2) ...
  CREATE TABLE child  ... CONSTRAINT foreign_key_1 FOREIGN KEY (...) REFERENCES parent (c_1, c_2) ...
  ```

  In both cases, the order of the columns is `c_1, c_2`. If the order of the columns in the foreign key had been different
  (for example, `c_2, c_1`), the attempt to create the foreign key would have failed.

- You can use data metric functions with event tables by executing an [ALTER TABLE](/sql-reference/sql/alter-table) command. For more information, see
  [Use SQL to set up data metric functions](/user-guide/data-quality-working).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- ALTER TABLE … CHANGE\_TRACKING = TRUE

  - When an event table is altered to enable change tracking, the event table is locked for the duration of the operation.
    Locks can cause latency with some associated DDL/DML operations.
    For more information, refer to [Resource locking](/sql-reference/transactions#label-txn-locking).

## Examples

Rename event table `t1` to `a1`:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE t1(a1 number);
>
> SHOW TABLES LIKE 't1';
>
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+
>            created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes | owner  | retention_time |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+
>  Tue, 17 Mar 2015 16:52:33 -0700 | T1   | TESTDB        | MY_SCHEMA   | TABLE |         |            | 0    | 0     | PUBLIC | 1              |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+
>
> ALTER TABLE t1 RENAME TO tt1;
>
> SHOW TABLES LIKE 'tt1';
>
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+
>            created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes | owner  | retention_time |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+
>  Tue, 17 Mar 2015 16:52:33 -0700 | TT1  | TESTDB        | MY_SCHEMA   | TABLE |         |            | 0    | 0     | PUBLIC | 1              |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------+----------------+
> ```

Change the order of the clustering key for an event table:

> Copy code
>
> ```
> CREATE OR REPLACE TABLE T1 (id NUMBER, date TIMESTAMP_NTZ, name STRING) CLUSTER BY (id, date);
>
> SHOW TABLES LIKE 'T1';
>
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
>            created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes |    owner     | retention_time |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
>  Tue, 21 Jun 2016 15:42:12 -0700 | T1   | TESTDB        | TESTSCHEMA  | TABLE |         | (ID,DATE)  | 0    | 0     | ACCOUNTADMIN | 1              |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
>
> -- Change the order of the clustering key
> ALTER TABLE t1 CLUSTER BY (date, id);
>
> SHOW TABLES LIKE 'T1';
>
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
>            created_on            | name | database_name | schema_name | kind  | comment | cluster_by | rows | bytes |    owner     | retention_time |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
>  Tue, 21 Jun 2016 15:42:12 -0700 | T1   | TESTDB        | TESTSCHEMA  | TABLE |         | (DATE,ID)  | 0    | 0     | ACCOUNTADMIN | 1              |
> ---------------------------------+------+---------------+-------------+-------+---------+------------+------+-------+--------------+----------------+
> ```

The following example adds a row access policy on an event table while specifying a single column. After setting the policy, you can verify by checking
the [information schema](/user-guide/security-row-intro#label-security-row-policy-refs).

> Copy code
>
> ```
> ALTER TABLE t1
>   ADD ROW ACCESS POLICY rap_t1 ON (empl_id);
> ```

The following example adds a row access policy while specifying two columns in a single event table.

> Copy code
>
> ```
> ALTER TABLE t1
>   ADD ROW ACCESS POLICY rap_test2 ON (cost, item);
> ```

The following example drops a row access policy from an event table. Verify the policies were dropped by querying the
[information schema](/user-guide/security-row-intro#label-security-row-policy-refs).

> Copy code
>
> ```
> ALTER TABLE t1
>   DROP ROW ACCESS POLICY rap_v1;
> ```

The following example shows how to combine adding and dropping row access policies in a single SQL statement for a table. Verify the
results by checking the [information schema](/user-guide/security-row-intro#label-security-row-policy-refs).

> Copy code
>
> ```
> alter table t1
>   drop row access policy rap_t1_version_1,
>   add row access policy rap_t1_version_2 on (empl_id);
> ```
