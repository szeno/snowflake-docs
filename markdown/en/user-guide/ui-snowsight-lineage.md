# Data Lineage

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Snowflake tracks how data flows from source to target objects, for example from a table to a view, and lets you see
where the data in an object came from or where it goes. This information is called *data lineage*, and it helps you
understand the relationships between your Snowflake objects.

Data lineage captures two types of relationship:

- Data movement, such as when data is copied or materialized from one object to another. For example, CREATE TABLE AS
  SELECT (CTAS), INSERT, or MERGE operations on tables result in data movement.
- Object dependencies, when an object references a base object but does not materialize or copy data, such as when a
  view references a table.

Snowflake data lineage provides these benefits:

- Provides impact analysis by understanding the relationship between different objects.
- Enhances monitoring and troubleshooting by viewing data movement lineage and object dependencies.
- Facilitates compliance by tracking the flow of sensitive data.
- Helps you work with tags and masking policies on columns to protect sensitive data.
- Enhances trust in the data by understanding the source and target objects and columns.
- Allows administration for viewing lineage to be delegated. For more information, see [Access control for lineage information](#label-lineage-privileges).

## About upstream and downstream relationships

Data lineage helps you understand the relationships of an object in terms of source and target objects. In lineage terminology, the source
object is “upstream” of the target object, and the target object is “downstream” of the source object. Snowsight reveals objects
incrementally, one step at a time upstream or downstream from your selection.

For example, in this SQL statement:

Copy code

```
CREATE TABLE table2 AS SELECT col1 FROM table1;
```

`table2` is the target table, and is downstream of the source table, `table1`. Column `col1`, which originates
in table `table1`, is included in table `table2`; this is also a downstream lineage relationship.

If you view the details of table `table1` in Snowsight, the **Lineage** tab displays an arrow pointing from `table1` to
`table2` to indicate the downstream lineage relationship. If you instead start at table `table2`, an arrow points from
`table2` upstream to `table1`.

## Get started

To start using data lineage in Snowsight, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) with the [necessary privileges](#label-lineage-privileges).
2. In the navigation menu, select **Catalog** » **Database Explorer**, and then select a [supported object](#label-ui-lineage-supported-objects) such as a table or
   view.
3. Select the **Lineage** tab.

Basic actions on the **Lineage** tab include the following:

> ![Example screenshot of data lineage in Snowsight](/static/images/governance/data-lineage.png)

- **A.** Select an object to show additional details about it, including columns and tags on those columns.
- **B.** Select **+/-** to show or hide objects that are further upstream or downstream.
- **C.** Select the arrow that connects two objects to show information about how the downstream object was created (for
  example, the SQL statement that created an object). Your access control privileges determine what information appears.
- **D.** Opens a new lineage diagram that focuses on the lineage of the selected object.

To learn about using the **Lineage** tab to perform other actions, see the following:

- [Lineage node grouping](#label-ui-lineage-grouping)
- [Column lineage](#label-ui-lineage-columns)
- [Work with tags](#label-ui-lineage-tags)
- [Identify masking policies](#label-ui-lineage-masking-policy)

## Lineage node grouping

Lineage graphs are automatically organized into collapsible node groups:

- **Snowflake objects** are grouped hierarchically by database, then by schema.
- **External objects** are grouped by vendor.
- **Objects you don’t have access to** are placed in a separate group that is collapsed by default.

Each group displays the number of nodes it contains, and large groups are paginated. If a node is hidden due to its group being collapsed or paginated, corresponding edges will connect to the group header.

## Column lineage

You can use Snowsight to trace the relationship between columns in a source object and columns in a target object. For a given
column, you can determine all upstream and downstream columns that share lineage with the column.

To determine the lineage of a column:

1. [Open the Lineage tab](#label-lineage-get-started) and select the object that contains the column you are interested in tracing. A side panel opens.
2. Hover over the column name in the side panel, and select **View Lineage**.
3. Select **Upstream Lineage** or **Downstream Lineage** to list the columns in upstream or downstream objects.

   You can use the **Distance** column to determine how far away a column is in the lineage. For example, if the downstream distance is 1,
   then the column is in an object that was created directly from the current object. If the downstream distance is 2, then the column
   exists in an object that was created from an object that was created from the current object.

## Work with tags

The **Lineage** tab provides an integrated governance experience that lets you view the lineage of columns, identify columns that should
have tags, and apply new tags all in the same workflow.

Whether you can see and apply tags depends on the access control privileges of the role you are using to view the **Lineage** tab. For
information about the privileges required to work with tags, see [Summary of DDL commands, operations, and privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).

### Find tags on an object and its columns

1. [Open the Lineage tab](#label-lineage-get-started) and select the object you’re interested in. A side panel opens.
2. To view the tags on the object itself, look under the **Details** section of the side panel.
3. To view the tags on a column of the object, find the column in the **Columns** section. If there is a tag, a tag symbol appears next to
   the column name. Hover over the symbol to see the tag name and value.

### Identify and remedy missing tags or incorrect tag values

If there’s a tag on one column, there’s a good chance the same tag should be applied to upstream columns and downstream columns that share
lineage with the column. Similarly, the value of a tag on upstream columns and downstream columns often needs to be the same.

The data lineage workflow identifies tags that are missing from upstream and downstream columns and tags that have a different value. It
then helps you apply the missing tags or change the tag value on those columns.

1. [Open the Lineage tab](#label-lineage-get-started) and select the object that contains the column you’re interested in tracing. A side panel opens.
2. Hover over the column name in the side panel, and select **View Lineage**.
3. In the **View Column Lineage** dialog, select **Downstream Lineage** or **Upstream Lineage**.

   If there are missing tags or mismatched tag values on the downstream or upstream column, a banner appears. You can use the color coding
   in the **Tags** column to identify what is wrong with the tag:

   - If a tag has a dashed border, the column does not have the tag applied.
   - If a tag has a yellow border, the value of the tag doesn’t match.
4. To remedy these missing or mismatched tags, do the following:

   1. Select **Review and Apply**.
   2. After confirming you’d like to accept the proposed changes, select **Apply**.

## Identify masking policies

1. [Open the Lineage tab](#label-lineage-get-started), and select the object you are interested in. A side panel opens.
2. To view the masking policy on a column of the object, find the column in the **Columns** section. If the column is protected by a
   masking policy, a symbol appears next to the column name. Hover over the symbol to see the masking policy name and details.

   If there’s a problem with the masking policy, for example there are multiple masking policies assigned to the same column,
   **Policy Error** appears instead of the mask symbol. If you hover over **Policy Error**, an explanation of the error appears. For
   additional help identifying why the error might have occurred, see [Tag and policy discovery](/user-guide/tag-based-masking-policies#label-tag-based-masking-discovery) and
   [Troubleshoot tag-based masking policies](/user-guide/tag-based-masking-policies#label-tab-based-masking-troubleshoot).

## Lineage created by a stored procedure or task

A stored procedure or task can result in lineage between an upstream object and a downstream object. You can select the arrow that connects
the objects to obtain more information about the stored procedure or task. You must have privileges to access the stored procedure or task
to view this information.

If the downstream object was created by a stored procedure, the **Stored Procedures** section contains the following
information:

- **Direct** — Displays the name of the stored procedure that, when executed, resulted in the downstream object.
- **Root** — If the direct stored procedure is nested within other stored procedures, this field displays the name of the stored
  procedure that is at the top of the hierarchy of nested procedures.

To view additional information about a stored procedure, select the **Go to procedure** icon next to its name.

Keep in mind the following:

- If you [call a stored procedure anonymously](/sql-reference/sql/call-with), details about the stored procedure do not appear in the
  lineage.
- Details about stored procedures and tasks are not backfilled. Lineage that occurred before the introduction of support for stored
  procedures and tasks doesn’t include details about the stored procedure or task.

## Retrieve lineage programmatically

You can use the [GET\_LINEAGE (SNOWFLAKE.CORE)](/sql-reference/functions/get_lineage-snowflake-core) function to retrieve lineage information programmatically. This
function returns a subset of the information provided by the **Lineage** tab in Snowsight.

## Supported operations for data lineage

The following operations create upstream and downstream relationships between a source object and a target object:

- [COPY INTO](/sql-reference/sql/copy-into-table)
- [CREATE TABLE … AS SELECT](/sql-reference/sql/create-table#label-ctas-syntax) (CTAS)
- [CREATE TABLE … CLONE](/sql-reference/sql/create-table#label-create-table-clone-syntax)
- [CREATE VIEW](/sql-reference/sql/create-view)
- [CREATE MATERIALIZED VIEW](/sql-reference/sql/create-materialized-view)
- [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view)
- [INSERT … SELECT …](/sql-reference/sql/insert)
- [MERGE](/sql-reference/sql/merge)
- [UPDATE](/sql-reference/sql/update), for example:

  Copy code

  ```
  UPDATE mydb.schema1.table1 FROM mydb.schema2.table2 SET table1.col1 = table2.col1;
  ```

## Supported objects

Data lineage supports data movement and dependency between [table-like objects](/guides-overview-db). A
“table-like” object is any object that can be queried like a table, including tables (nothing is more table-like than a
table). Table-like objects include:

- Tables
- Dynamic tables
- External tables
- Iceberg tables
- Views
- Materialized views
- Semantic views

Stages can also participate in data lineage relationships, as can the following machine learning objects.

- [Datasets](/developer-guide/snowflake-ml/dataset)
- [Feature Views](/developer-guide/snowflake-ml/feature-store/feature-views) (which are actually dynamic tables or views inside Snowflake)
- [Models](/developer-guide/snowflake-ml/model-registry/overview)

Column lineage is supported between columns in any two table-like objects. You can, for example, select a column in a table
to view downstream column lineage, which shows the other table-like objects where that column appears.

Note

Column lineage is not currently supported for semantic views.

Additionally, you can see tag and masking policy associations if you are using a role that has privileges for managing
tags and masking policies.

### Lineage for objects from external data sources

Snowflake can track data lineage for sources and destinations outside of Snowflake. This provides visibility into how data flows from
external ETL tools and databases into your Snowflake objects, creating a comprehensive view of your entire data pipeline.

For more information, see [External lineage](/user-guide/external-lineage).

### ML Lineage

[ML Lineage](/developer-guide/snowflake-ml/ml-lineage) specifically supports machine learning relationships, which
focus on how data is used and transformed in machine learning workflows, rather than on simpler movement or dependency
relationships. Relationships between the following types of objects are supported:

- [Datasets](/developer-guide/snowflake-ml/dataset)
- [Feature Views](/developer-guide/snowflake-ml/feature-store/feature-views) (which is actually a dynamic table or a view inside Snowflake)
- [Models](/developer-guide/snowflake-ml/model-registry/overview)

### Lineage for Cortex Agents

Data lineage tracks the objects that a [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents) can reach through the tools
declared in its specification, so you can see which data reaches an agent. The agent appears as a downstream consumer
of those objects:

- A [semantic view](/sql-reference/sql/create-semantic-view) that a Cortex Analyst tool references is upstream of the
  agent.
- A [Cortex Search service](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview) that a Cortex Search
  tool references is upstream of the agent.

Because a semantic view is itself downstream of the tables it references, lineage shows the whole path from a table,
through the semantic view, to the agent.

Snowflake records these relationships when you run [CREATE AGENT](/sql-reference/sql/create-agent) or
[ALTER AGENT … COMMIT VERSION](/sql-reference/sql/alter-agent), and reconciles them with the agent’s active version
each time you commit a new version. If you remove a tool from the specification, the corresponding relationship is
removed the next time you commit a version.

## Access control for lineage information

A role with the following privileges can access the **Lineage** tab and view an object’s upstream and downstream lineage objects and
dependencies:

- VIEW LINEAGE on the account.
- Any privilege on the objects for which you want to evaluate the lineage, such as SELECT on a table. If you want to let users view the
  lineage of an object without being able to access its data, you can grant the REFERENCES privilege on the object.
- USAGE on the database and schema that contains the object.

The VIEW LINEAGE privilege controls whether a user can view data lineage for their objects. By default, the PUBLIC role has this privilege,
which means everyone has the ability to view lineage. To narrow who can view lineage, you can revoke the VIEW LINEAGE privilege from the
PUBLIC role and grant it to custom roles instead.

You can configure a role to view the full lineage of all objects, even if the role doesn’t have privileges on the objects, database, or schema.
Simply grant the role the RESOLVE ALL privilege on the account, for example, `GRANT RESOLVE ALL ON ACCOUNT TO ROLE lineage_role;`. The
role still requires the VIEW LINEAGE privilege.

If a user does not have privileges on an upstream or downstream object in the lineage graph, the object appears gray with a
message stating that they have insufficient privileges to view the object. The gray object does not imply a terminal node in the lineage
graph; it merely indicates that the user cannot view lineage any further upstream or downstream from that point because they don’t have the
privileges to retrieve that object’s lineage. This behavior also applies to objects and columns protected by other access policies.

A user must have privileges to access the [QUERY\_HISTORY view](/sql-reference/account-usage/query_history) to see the SQL statement that resulted in the
target object.

## Lineage history and retention

Lineage was introduced to Snowflake in November 2024. Lineage information is available as follows:

- Lineage for an object dependency (for example, a view based on a table) that occurred before this date *is* available.
- Lineage for data movement (for example, using a CTAS statement to create a table from another table) that occurred before this date
  *is not* available.

Historical information is retained as follows:

- Column lineage is retained for one year.
- Object lineage is retained for one year.

## Limitations and considerations

- Lineage is not available for the following kinds of objects:

  - Objects in a shared database.
  - Objects in the shared SNOWFLAKE database.
  - Objects in the INFORMATION\_SCHEMA of a database.
  - Semantic views created before early February 2026.
- Dynamic tables appear in the lineage graph for other objects, but the **Lineage** tab does not appear for dynamic tables
  themselves.
- Deleted tables are not shown in the lineage graph, but renamed tables are shown.
- Temporary tables are not shown in the lineage graph.
- Lineage does not include a table that was used for filtering or joining when data did not move from the table to the downstream object. In
  the following example, table `t2` is not considered part of the lineage of table `target_table`:

  Copy code

  ```
  CREATE TABLE target_table AS
    SELECT t1.c1, t1.c2
   FROM t1, t2
   WHERE t1.c3 = t2.c3;
  ```
- Lineage cannot track the movement of data that results from separate, disjointed queries. For example, the following set of queries does
  not result in lineage from table `sourceTable1` to table `target_table`.

  Copy code

  ```
  SET read_output1 = (SELECT c1 FROM sourceTable1);

  INSERT INTO target_table(c1) VALUES ($read_output1);
  ```

  This limitation applies to anything that caused the data movement, including stored procedures.
- You cannot use the [GET\_LINEAGE (SNOWFLAKE.CORE)](/sql-reference/functions/get_lineage-snowflake-core) function to obtain lineage information related to a stored
  procedure.
- Lineage for Cortex Agents has the following limitations:

  - Relationships are recorded when you create an agent or commit a version. An agent whose most recent version was
    committed before agent lineage was introduced doesn’t appear in lineage until you commit a new version.
  - A Cortex Analyst tool that uses a semantic model file on a stage, rather than a semantic view object, doesn’t
    produce a lineage relationship.
  - A tool reference that can’t be resolved, because the object doesn’t exist or because the role committing the
    version can’t access it, is skipped.
  - Agent lineage is tracked at the object level. Column lineage isn’t available for agents.
  - An agent is a leaf in the lineage graph. No objects currently appear downstream of an agent.
  - Agent lineage is recorded only in the account that owns the agent. A shared or replicated agent doesn’t have
    lineage in other accounts.
  - Agent relationships don’t appear in [OBJECT\_DEPENDENCIES view](/sql-reference/account-usage/object_dependencies).
