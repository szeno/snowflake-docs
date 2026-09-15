# Monitor object tags

You can monitor tags and how they’ve been implemented using Snowsight or SQL.

## Monitor tags with Snowsight

Use the following information about the **Tags & policies** area in Snowsight. To monitor tags using SQL instead, see [Monitor tags with SQL](#label-object-tagging-monitor-sql).

You can use the Snowsight **Governance & security** » **Tags & policies** area to monitor and report on the usage of
policies and tags with tables, views, and columns. There are two different interfaces: **Dashboard** and **Tagged Objects**.

When using the **Dashboard** and the **Tagged Objects** interface, note the following details.

- The **Dashboard** and **Tagged Objects** interfaces require a running warehouse.
- Snowsight updates the **Dashboard** every 12 hours.
- The **Tagged Objects** information latency can be up to two hours and returns up to 1000 objects.

# Accessing the Governance area in Snowsight

To access the **Tags & policies** area, your Snowflake account must be [Enterprise Edition or higher](/user-guide/intro-editions).
Additionally, you must do either of the following:

- Use the ACCOUNTADMIN role.
- Use an account role that is directly granted the GOVERNANCE\_VIEWER and OBJECT\_VIEWER database roles.

  You must use an account role with these database role grants. Currently, Snowsight does not evaluate role hierarchies
  and user-defined database roles that have access to tables, views, data access policies, and tags.

  To determine if your account role is granted these two database roles, use a [SHOW GRANTS](/sql-reference/sql/show-grants) command:

  > Copy code
  >
  > ```
  > SHOW GRANTS LIKE '%VIEWER%' TO ROLE data_engineer;
  > ```
  >
  > ```
  > |-------------------------------+-----------+---------------+-----------------------------+------------+-----------------+--------------+------------|
  > | created_on                    | privilege | granted_on    | name                        | granted_to | grantee_name    | grant_option | granted_by |
  > |-------------------------------+-----------+---------------+-----------------------------+------------+-----------------+--------------+------------|
  > | 2024-01-24 17:12:26.984 +0000 | USAGE     | DATABASE_ROLE | SNOWFLAKE.GOVERNANCE_VIEWER | ROLE       | DATA_ENGINEER   | false        |            |
  > | 2024-01-24 17:12:47.967 +0000 | USAGE     | DATABASE_ROLE | SNOWFLAKE.OBJECT_VIEWER     | ROLE       | DATA_ENGINEER   | false        |            |
  > |-------------------------------+-----------+---------------+-----------------------------+------------+-----------------+--------------+------------|
  > ```

  If your account role is not granted either or both of these database roles, use the [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role) command
  and run the SHOW GRANTS command again to confirm the grants:

  > Copy code
  >
  > ```
  > USE ROLE ACCOUNTADMIN;
  > GRANT DATABASE ROLE SNOWFLAKE.GOVERNANCE_VIEWER TO ROLE data_engineer;
  > GRANT DATABASE ROLE SNOWFLAKE.OBJECT_VIEWER TO ROLE data_engineer;
  > SHOW GRANTS LIKE '%VIEWER%' TO ROLE data_engineer;
  > ```

  For details about these database roles, see [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).

## Dashboard

As a data administrator, you can use the **Dashboard** interface to monitor tag and policy usage in the following ways.

- Coverage: specifies the count and percentage based on whether a table, view, or column has a policy or tag.
- Prevalence: lists and counts the most frequently used policies and tags.

The coverage and prevalence provide a snapshot as to how well the data is protected and tagged.

When you select a count number, percentage, policy name, or tag name, the **Tagged Objects** interface opens. The **Tagged Objects**
interface updates the filters automatically based on your selection in the **Dashboard**.

The monitoring information is an alternative or complement to running complex and query-intensive operations on multiple Account
Usage views.

These views might include, but are not limited to, the [COLUMNS](/sql-reference/account-usage/columns),
[POLICY\_REFERENCES](/sql-reference/account-usage/policy_references), [TABLES](/sql-reference/account-usage/tables),
[TAG\_REFERENCES](/sql-reference/account-usage/tag_references), and [VIEWS](/sql-reference/account-usage/views) views.

## Tagged Objects

As a data administrator, you can use this table to associate the coverage and prevalence in the **Dashboard** to a list of specific
tables, view, or columns quickly. You can also filter the table results manually as follows.

- Choose **Tables** or **Columns**.
- For tags, you can filter with tags, without tags, or by a specific tag.
- For policies, you can filter with policies, without policies, or by a specific policy.

When you select a row in the table, the **Table Details** or **Columns** tab in **Catalog** » **Database Explorer** opens. You can edit
the tag and policy assignments as needed.

## Monitor tags with SQL

You can monitor tags with SQL by using two different Account Usage views, two Information Schema table functions, an Account Usage table
function, and a system function.

It can be helpful to think of two general approaches to determine how to monitor tag usage.

- [Discover Tags](#discover-tags)
- [Identify Assignments](#identify-assignments)

### Discover tags

Snowflake supports the following options to list tags and to identify the string value for a given tag key.

- Identify tags in your account:

  Use the [TAGS](/sql-reference/account-usage/tags) view in the Account Usage schema of the shared SNOWFLAKE database. This view
  can be thought of as a *catalog* for all tags in your Snowflake account that provides information on current and deleted tags. For
  example:

  Copy code

  ```
  SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TAGS
    ORDER BY tag_name;
  ```
- Identify a value for a given tag:

  Use the [SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) system function to return the tag value assigned to the specified tag, and
  the Snowflake object or column.

  Copy code

  ```
  SELECT SYSTEM$GET_TAG('cost_center', 'my_table', 'table');
  ```

### Identify assignments

Snowflake supports different options to identify tag assignments, depending on whether the query needs to target the account or a
specific database, and whether you want to track tag inheritance.

- Account-level query with lineage:

  Use the Account Usage table function [TAG\_REFERENCES\_WITH\_LINEAGE](/sql-reference/functions/tag_references_with_lineage) to determine all of the objects that
  have a given tag key and tag value, including objects that inherited tags:

  Copy code

  ```
  SELECT *
    FROM TABLE(
   SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES_WITH_LINEAGE(
     'my_db.my_schema.cost_center'
   )
    );
  ```
- Account-level query without lineage:

  Use the Account Usage [TAG\_REFERENCES](/sql-reference/account-usage/tag_references) view to determine all of the objects that
  have a given tag key and tag value, but does not include objects that inherited the tag:

  Copy code

  ```
  SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TAG_REFERENCES
    ORDER BY tag_name, domain, object_id;
  ```
- Database-level query, with lineage:

  Every Snowflake database includes an [Snowflake Information Schema](/sql-reference/info-schema). Use the Information Schema table function
  [TAG\_REFERENCES](/sql-reference/functions/tag_references) to determine all of the objects that have a given tag, including objects that inherited the
  tag, in a given database:

  Copy code

  ```
  SELECT *
    FROM TABLE(
   my_db.INFORMATION_SCHEMA.TAG_REFERENCES(
     'my_table',
     'table'
   )
    );
  ```
- Database-level query for all of the tags on every column in a table or view, with lineage:

  Use the Information Schema table function [TAG\_REFERENCES\_ALL\_COLUMNS](/sql-reference/functions/tag_references_all_columns) to obtain all of the tags that
  are set on every column in a given table or view.

  Note that the domain `TABLE` must be used for all objects that contain columns, even if the object name is a view
  (that is, view, materialized view).

  Copy code

  ```
  SELECT *
    FROM TABLE(
   INFORMATION_SCHEMA.TAG_REFERENCES_ALL_COLUMNS(
     'my_table',
     'table'
   )
    );
  ```
