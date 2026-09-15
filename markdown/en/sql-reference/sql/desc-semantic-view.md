# DESCRIBE SEMANTIC VIEW

Describes the properties of the logical tables, dimensions, facts, and metrics that make up a
[semantic view](/user-guide/views-semantic/overview).

See also:
:   [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view), [ALTER SEMANTIC VIEW](/sql-reference/sql/alter-semantic-view), [DROP SEMANTIC VIEW](/sql-reference/sql/drop-semantic-view), [SHOW SEMANTIC VIEWS](/sql-reference/sql/show-semantic-views), [SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions), [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric), [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts), [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics)

## Syntax

Copy code

```
{ DESCRIBE | DESC } SEMANTIC VIEW <name>
```

## Parameters

`name`
:   Specifies the identifier for the semantic view to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The command output provides the properties and metadata about the logical tables, relationships, facts, dimensions, metrics, and
the semantic view itself.

Each row in the view represents a property of:

- A logical table
- A relationship
- A fact
- A dimension
- A metric
- A verified query
- Custom instructions
- The semantic view itself

The following is an example of the output of the command:

```
+--------------+------------------------------+---------------+--------------------------+----------------------------------------+
| object_kind  | object_name                  | parent_entity | property                 | property_value                         |
|--------------+------------------------------+---------------+--------------------------+----------------------------------------|
| NULL         | NULL                         | NULL          | COMMENT                  | Comment about the semantic view        |
| TABLE        | CUSTOMERS                    | NULL          | BASE_TABLE_DATABASE_NAME | SNOWFLAKE_SAMPLE_DATA                  |
| ...          | ...                          | ...           | ...                      | ...                                    |
| DIMENSION    | CUSTOMER_NAME                | CUSTOMERS     | TABLE                    | CUSTOMERS                              |
| ...          | ...                          | ...           | ...                      | ...                                    |
| RELATIONSHIP | LINE_ITEM_TO_ORDERS          | LINE_ITEMS    | TABLE                    | LINE_ITEMS                             |
| ...          | ...                          | ...           | ...                      | ...                                    |
| FACT         | DISCOUNTED_PRICE             | LINE_ITEMS    | TABLE                    | LINE_ITEMS                             |
| ...          | ...                          | ...           | ...                      | ...                                    |
| METRIC       | AVERAGE_LINE_ITEMS_PER_ORDER | ORDERS        | TABLE                    | ORDERS                                 |
| ...          | ...                          | ...           | ...                      | ...                                    |
+--------------+------------------------------+---------------+--------------------------+----------------------------------------+
```

As shown above, each row represents a property of a logical table, dimension, relationship, metric, or fact. For example:

- The first row is the value of the `comment` property of the semantic view itself.
- The second row is the value of the `base_table_database_name` property of the logical table named `customers`.

The view includes the following columns:

| Column | Description |
| --- | --- |
| `object_kind` | Type of the object that has the property for this row. The value can be one of the following:   - `TABLE` (the logical tables for the view) - `RELATIONSHIP` - `DIMENSION` - `FACT` - `METRIC` - `DERIVED_METRIC` (for [derived metrics](/user-guide/views-semantic/sql#label-semantic-views-create-derived-metrics)) - `CUSTOM_INSTRUCTIONS` (for [custom instructions](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions)) - `AI_VERIFIED_QUERY` (for [verified queries](/user-guide/views-semantic/sql#label-semantic-views-verified-queries)) - `NULL` (properties that apply to the semantic view itself, such as a comment) |
| `object_name` | Name of the dimension, fact, metric, logical table, relationship, or verified query that has the property for this row.  For rows that represent properties of the semantic view itself and rows that represent custom instructions, the value in this column is NULL. |
| `parent_entity` | Name of the parent entity of the dimension, fact, metric, or relationship.  The value of this column is NULL for rows that represent:   - The semantic view itself. - Properties of logical tables. - Properties of [derived metrics](/user-guide/views-semantic/sql#label-semantic-views-create-derived-metrics). - Properties of [custom instructions](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions). - Properties of [verified queries](/user-guide/views-semantic/sql#label-semantic-views-verified-queries). |
| `property` | Name of the property of the logical table, constraint, relationship, dimension, fact, metric, custom instruction, or semantic view.  The value in this column depends on the type of the object (`object_kind`).  See the following sections for details about the properties and their possible values, based on the value in the `object_kind` column:   - For `TABLE`, see [Properties for logical tables](#label-desc-semantic-view-properties-tables). - For `CONSTRAINT`, see [Properties for constraints](#label-desc-semantic-view-properties-constraints). - For `RELATIONSHIP`, see [Properties for relationships](#label-desc-semantic-view-properties-relationships). - For `FACT`, `DIMENSION`, and `METRIC`, see [Properties for facts, dimensions, and metrics](#label-desc-semantic-view-properties-semantic-expressions). - For `CUSTOM_INSTRUCTIONS`, see [Properties for custom instructions](#label-desc-semantic-view-properties-custom-instructions). - For `AI_VERIFIED_QUERY`, see [Properties for verified queries](#label-desc-semantic-view-properties-verified-queries). - For `NULL`, see [Properties for semantic views](#label-desc-semantic-view-properties). |
| `property_value` | Value of the property of the logical table, relationship, dimension, fact, metric, custom instruction, or semantic view. |

Expand

Show lessSee more

### Properties for logical tables

If the `object_kind` column contains `TABLE`, the `property` column can contain the following values:

| Property name | Description |
| --- | --- |
| `BASE_TABLE_DATABASE_NAME` | Name of the database containing the logical table. Not present if the logical table is defined as a [SQL query](/user-guide/views-semantic/inline-view). |
| `BASE_TABLE_SCHEMA_NAME` | Name of the schema containing the logical table. Not present if the logical table is defined as a SQL query. |
| `BASE_TABLE_NAME` | Name of the logical table. Not present if the logical table is defined as a SQL query. |
| `DEFINITION` | The SQL query that defines the logical table. Present only if the logical table is defined as a [SQL query](/user-guide/views-semantic/inline-view) rather than a physical table. |
| `SYNONYMS` | [Array](/sql-reference/data-types-semistructured#label-data-type-array) of VARCHAR values, representing the synonyms for the logical table. |
| `PRIMARY_KEY` | [Array](/sql-reference/data-types-semistructured#label-data-type-array) of VARCHAR values, specifying the names of the columns that make up the primary key for the logical table. |

Expand

Show lessSee more

### Properties for constraints

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

If the `object_kind` column contains `CONSTRAINT`, the row represents a constraint that is used for a
[range join](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins). The `property` column can contain the following values:

| Property name | Description |
| --- | --- |
| `CONSTRAINT_TYPE` | The value is `DISTINCT_RANGE`. |
| `START_COLUMN` | The name of the column that represents the start of the range. |
| `END_COLUMN` | The name of the column that represents the end of the range. |

Expand

Show lessSee more

### Properties for relationships

If the `object_kind` column contains `RELATIONSHIP`, the `property` column can contain the following values:

| Property name | Description |
| --- | --- |
| `TABLE` | Name of one of the logical tables in the relationship. |
| `FOREIGN_KEY` | Name of the column in that logical table used in the relationship. |
| `REF_TABLE` | Name of the other logical table in the relationship. |
| `REF_KEY` | One of the following values:  - For relationships that represent [range joins](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins), an array that contains   JSON-formatted strings for objects with the following keys:    - The `start_column` key specifies the name of the column that represents the start of the range.   - The `end_column` key specifies the name of the column that represents the end of the range.   - The `type` key is `RANGE`. - For relationships that represent [ASOF joins](/user-guide/views-semantic/sql#label-semantic-views-create-relationships-asof), an array that contains the   following elements:    - The name of the column in the first table.   - A JSON object with the following fields:     - `column`: Name of the column in the second table.     - `type`: `ASOF`.   - For other types of relationships, the name of the column in the other logical table in the relationship. |

Expand

Show lessSee more

### Properties for facts, dimensions, and metrics

If the `object_kind` column contains `FACT`, `DIMENSION`, or `METRIC`, the `property` column can contain the
following values:

| Property name | Description |
| --- | --- |
| `TABLE` | Name of the logical table used to define the dimension, fact, or metric. |
| `EXPRESSION` | The SQL expression for the dimension, fact, or metric. |
| `DATA_TYPE` | The SQL data type of the evaluated SQL expression. |
| `ACCESS_MODIFIER` | `PRIVATE` for [private facts and metrics](/user-guide/views-semantic/sql#label-semantic-views-private). `PUBLIC` for everything else. |

Expand

Show lessSee more

Note

For [derived metrics](/user-guide/views-semantic/sql#label-semantic-views-create-derived-metrics), the `TABLE` property is not present.

In addition, if the row represents a
[dimension that uses a Cortex Search Service](/user-guide/views-semantic/sql#label-semantic-views-create-cortex-search-service-dimension), the `property`
column can contain the following values:

| Property name | Description |
| --- | --- |
| `CORTEX_SEARCH_SERVICE_COLUMN_NAME` | The name of the column that the Cortex Search Service allows you to search on. |
| `CORTEX_SEARCH_SERVICE_DATABASE_NAME` | The name of the database that contains the Cortex Search Service. |
| `CORTEX_SEARCH_SERVICE_SCHEMA_NAME` | The name of the schema that contains the Cortex Search Service. |
| `CORTEX_SEARCH_SERVICE_NAME` | The name of the Cortex Search Service. |

Expand

Show lessSee more

### Properties for custom instructions

If the `object_kind` column contains `CUSTOM_INSTRUCTIONS`, the row represents a property of a
[custom instruction](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions). The `property` column can contain the following values:

| Property name | Description |
| --- | --- |
| `AI_QUESTION_CATEGORIZATION` | [Custom instructions for Cortex Analyst](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions) that explain how to classify questions. |
| `AI_SQL_GENERATION` | Custom instructions for Cortex Analyst that explain how to generate the SQL statement. |

Expand

Show lessSee more

### Properties for verified queries

If the `object_kind` column contains `AI_VERIFIED_QUERY`, the row represents a property of a
[verified query](/user-guide/views-semantic/sql#label-semantic-views-verified-queries). The `property` column can contain the following values:

| Property name | Description |
| --- | --- |
| `QUESTION` | The question that should produce the expected query. |
| `VERIFIED_AT` | The timestamp (in seconds after the Unix epoch) when the query was verified. |
| `ONBOARDING_QUESTION` | If TRUE, the question is an [onboarding question](/user-guide/snowflake-cortex/cortex-analyst/suggested-questions-feature) (a question that is suggested to users interacting with an app powered by Cortex Analyst). |
| `VERIFIED_BY` | The purpose and name of the [contact](/user-guide/contacts-using) who verified that the query answers the question. |
| `SQL` | The SQL statement for the query that answers the question. |

Expand

Show lessSee more

### Properties for semantic views

If the `object_kind` column is NULL, the `property` column can contain the following values:

| Property name | Description |
| --- | --- |
| `COMMENT` | Comment about the semantic view. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| Any | Semantic view |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

The following example describes the semantic view named `tpch_rev_analysis`:

Copy code

```
DESC SEMANTIC VIEW tpch_rev_analysis;
```

```
+--------------+------------------------------+---------------+--------------------------+----------------------------------------+
| object_kind  | object_name                  | parent_entity | property                 | property_value                         |
|--------------+------------------------------+---------------+--------------------------+----------------------------------------|
| NULL         | NULL                         | NULL          | COMMENT                  | Comment about the semantic view        |
| TABLE        | CUSTOMERS                    | NULL          | BASE_TABLE_DATABASE_NAME | SNOWFLAKE_SAMPLE_DATA                  |
| TABLE        | CUSTOMERS                    | NULL          | BASE_TABLE_SCHEMA_NAME   | TPCH_SF1                               |
| TABLE        | CUSTOMERS                    | NULL          | BASE_TABLE_NAME          | CUSTOMER                               |
| TABLE        | CUSTOMERS                    | NULL          | PRIMARY_KEY              | ["C_CUSTKEY"]                          |
| TABLE        | CUSTOMERS                    | NULL          | COMMENT                  | Main table for customer data           |
| DIMENSION    | CUSTOMER_NAME                | CUSTOMERS     | TABLE                    | CUSTOMERS                              |
| DIMENSION    | CUSTOMER_NAME                | CUSTOMERS     | EXPRESSION               | customers.c_name                       |
| DIMENSION    | CUSTOMER_NAME                | CUSTOMERS     | DATA_TYPE                | VARCHAR(25)                            |
| DIMENSION    | CUSTOMER_NAME                | CUSTOMERS     | SYNONYMS                 | ["customer name"]                      |
| DIMENSION    | CUSTOMER_NAME                | CUSTOMERS     | COMMENT                  | Name of the customer                   |
| TABLE        | LINE_ITEMS                   | NULL          | BASE_TABLE_DATABASE_NAME | SNOWFLAKE_SAMPLE_DATA                  |
| TABLE        | LINE_ITEMS                   | NULL          | BASE_TABLE_SCHEMA_NAME   | TPCH_SF1                               |
| TABLE        | LINE_ITEMS                   | NULL          | BASE_TABLE_NAME          | LINEITEM                               |
| TABLE        | LINE_ITEMS                   | NULL          | PRIMARY_KEY              | ["L_ORDERKEY","L_LINENUMBER"]          |
| TABLE        | LINE_ITEMS                   | NULL          | COMMENT                  | Line items in orders                   |
| RELATIONSHIP | LINE_ITEM_TO_ORDERS          | LINE_ITEMS    | TABLE                    | LINE_ITEMS                             |
| RELATIONSHIP | LINE_ITEM_TO_ORDERS          | LINE_ITEMS    | REF_TABLE                | ORDERS                                 |
| RELATIONSHIP | LINE_ITEM_TO_ORDERS          | LINE_ITEMS    | FOREIGN_KEY              | ["L_ORDERKEY"]                         |
| RELATIONSHIP | LINE_ITEM_TO_ORDERS          | LINE_ITEMS    | REF_KEY                  | ["O_ORDERKEY"]                         |
| FACT         | DISCOUNTED_PRICE             | LINE_ITEMS    | TABLE                    | LINE_ITEMS                             |
| FACT         | DISCOUNTED_PRICE             | LINE_ITEMS    | EXPRESSION               | l_extendedprice * (1 - l_discount)     |
| FACT         | DISCOUNTED_PRICE             | LINE_ITEMS    | DATA_TYPE                | NUMBER(25,4)                           |
| FACT         | DISCOUNTED_PRICE             | LINE_ITEMS    | COMMENT                  | Extended price after discount          |
| FACT         | LINE_ITEM_ID                 | LINE_ITEMS    | TABLE                    | LINE_ITEMS                             |
| FACT         | LINE_ITEM_ID                 | LINE_ITEMS    | EXPRESSION               | CONCAT(l_orderkey, '-', l_linenumber)  |
| FACT         | LINE_ITEM_ID                 | LINE_ITEMS    | DATA_TYPE                | VARCHAR(134217728)                     |
| TABLE        | ORDERS                       | NULL          | BASE_TABLE_DATABASE_NAME | SNOWFLAKE_SAMPLE_DATA                  |
| TABLE        | ORDERS                       | NULL          | BASE_TABLE_SCHEMA_NAME   | TPCH_SF1                               |
| TABLE        | ORDERS                       | NULL          | BASE_TABLE_NAME          | ORDERS                                 |
| TABLE        | ORDERS                       | NULL          | SYNONYMS                 | ["sales orders"]                       |
| TABLE        | ORDERS                       | NULL          | PRIMARY_KEY              | ["O_ORDERKEY"]                         |
| TABLE        | ORDERS                       | NULL          | COMMENT                  | All orders table for the sales domain  |
| RELATIONSHIP | ORDERS_TO_CUSTOMERS          | ORDERS        | TABLE                    | ORDERS                                 |
| RELATIONSHIP | ORDERS_TO_CUSTOMERS          | ORDERS        | REF_TABLE                | CUSTOMERS                              |
| RELATIONSHIP | ORDERS_TO_CUSTOMERS          | ORDERS        | FOREIGN_KEY              | ["O_CUSTKEY"]                          |
| RELATIONSHIP | ORDERS_TO_CUSTOMERS          | ORDERS        | REF_KEY                  | ["C_CUSTKEY"]                          |
| METRIC       | AVERAGE_LINE_ITEMS_PER_ORDER | ORDERS        | TABLE                    | ORDERS                                 |
| METRIC       | AVERAGE_LINE_ITEMS_PER_ORDER | ORDERS        | EXPRESSION               | AVG(orders.count_line_items)           |
| METRIC       | AVERAGE_LINE_ITEMS_PER_ORDER | ORDERS        | DATA_TYPE                | NUMBER(36,6)                           |
| METRIC       | AVERAGE_LINE_ITEMS_PER_ORDER | ORDERS        | COMMENT                  | Average number of line items per order |
| FACT         | COUNT_LINE_ITEMS             | ORDERS        | TABLE                    | ORDERS                                 |
| FACT         | COUNT_LINE_ITEMS             | ORDERS        | EXPRESSION               | COUNT(line_items.line_item_id)         |
| FACT         | COUNT_LINE_ITEMS             | ORDERS        | DATA_TYPE                | NUMBER(18,0)                           |
| METRIC       | ORDER_AVERAGE_VALUE          | ORDERS        | TABLE                    | ORDERS                                 |
| METRIC       | ORDER_AVERAGE_VALUE          | ORDERS        | EXPRESSION               | AVG(orders.o_totalprice)               |
| METRIC       | ORDER_AVERAGE_VALUE          | ORDERS        | DATA_TYPE                | NUMBER(30,8)                           |
| METRIC       | ORDER_AVERAGE_VALUE          | ORDERS        | COMMENT                  | Average order value across all orders  |
| DIMENSION    | ORDER_DATE                   | ORDERS        | TABLE                    | ORDERS                                 |
| DIMENSION    | ORDER_DATE                   | ORDERS        | EXPRESSION               | o_orderdate                            |
| DIMENSION    | ORDER_DATE                   | ORDERS        | DATA_TYPE                | DATE                                   |
| DIMENSION    | ORDER_DATE                   | ORDERS        | COMMENT                  | Date when the order was placed         |
| DIMENSION    | ORDER_YEAR                   | ORDERS        | TABLE                    | ORDERS                                 |
| DIMENSION    | ORDER_YEAR                   | ORDERS        | EXPRESSION               | YEAR(o_orderdate)                      |
| DIMENSION    | ORDER_YEAR                   | ORDERS        | DATA_TYPE                | NUMBER(4,0)                            |
| DIMENSION    | ORDER_YEAR                   | ORDERS        | COMMENT                  | Year when the order was placed         |
+--------------+------------------------------+---------------+--------------------------+----------------------------------------+
```
