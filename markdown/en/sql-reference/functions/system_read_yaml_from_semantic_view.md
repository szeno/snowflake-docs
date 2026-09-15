Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW

Returns the
[specification of a semantic model (in YAML format)](/user-guide/views-semantic/sql)
for a [semantic view](/user-guide/views-semantic/overview).

See also:
:   [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml) ,
    [SYSTEM$READ\_OSI\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_osi_yaml_from_semantic_view)

## Syntax

Copy code

```
SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW( '<semantic_view_name>' )
```

## Arguments

`'semantic_view_name'`
:   Name of the semantic view.

    If the semantic view is in a different schema or database than the current schema or database, specify the
    [partial or fully qualified name](/sql-reference/name-resolution) (for example, `my_schema.my_semantic_view` or
    `my_db.my_schema.my_semantic_view`).

## Returns

Returns a VARCHAR value containing the
[specification for the semantic model in YAML format](/user-guide/views-semantic/sql).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
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

If the name of the database, schema, or view is a [double-quoted identifier](/sql-reference/identifiers-syntax#label-delimited-identifier) (for example, if
the name contains spaces), you must include double quotes around the name. For example:

Copy code

```
SELECT SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW(
  '"my database"."my schema"."my semantic view"'
);
```

## Examples

The following example returns the YAML specification for the semantic view named `tpch_analysis` in the database `my_db` and
schema `my_schema`:

Copy code

```
SELECT SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW(
  'my_db.my_schema.tpch_rev_analysis'
);
```

```
+-------------------------------------------------------------+
| READ_YAML_FROM_SEMANTIC_VIEW                                |
|-------------------------------------------------------------|
| name: TPCH_REV_ANALYSIS                                     |
| description: Semantic view for revenue analysis             |
| tables:                                                     |
|   - name: CUSTOMERS                                         |
|     description: Main table for customer data               |
|     base_table:                                             |
|       database: SNOWFLAKE_SAMPLE_DATA                       |
|       schema: TPCH_SF1                                      |
|       table: CUSTOMER                                       |
|     primary_key:                                            |
|       columns:                                              |
|         - C_CUSTKEY                                         |
|     dimensions:                                             |
|       - name: CUSTOMER_NAME                                 |
|         synonyms:                                           |
|           - customer name                                   |
|         description: Name of the customer                   |
|         expr: customers.c_name                              |
|         data_type: VARCHAR(25)                              |
|       - name: C_CUSTKEY                                     |
|         expr: C_CUSTKEY                                     |
|         data_type: VARCHAR(134217728)                       |
|   - name: LINE_ITEMS                                        |
|     description: Line items in orders                       |
|     base_table:                                             |
|       database: SNOWFLAKE_SAMPLE_DATA                       |
|       schema: TPCH_SF1                                      |
|       table: LINEITEM                                       |
|     primary_key:                                            |
|       columns:                                              |
|         - L_ORDERKEY                                        |
|         - L_LINENUMBER                                      |
|     dimensions:                                             |
|       - name: L_ORDERKEY                                    |
|         expr: L_ORDERKEY                                    |
|         data_type: VARCHAR(134217728)                       |
|       - name: L_LINENUMBER                                  |
|         expr: L_LINENUMBER                                  |
|         data_type: VARCHAR(134217728)                       |
|     facts:                                                  |
|       - name: DISCOUNTED_PRICE                              |
|         description: Extended price after discount          |
|         expr: l_extendedprice * (1 - l_discount)            |
|         data_type: "NUMBER(25,4)"                           |
|       - name: LINE_ITEM_ID                                  |
|         expr: "CONCAT(l_orderkey, '-', l_linenumber)"       |
|         data_type: VARCHAR(134217728)                       |
|   - name: ORDERS                                            |
|     synonyms:                                               |
|       - sales orders                                        |
|     description: All orders table for the sales domain      |
|     base_table:                                             |
|       database: SNOWFLAKE_SAMPLE_DATA                       |
|       schema: TPCH_SF1                                      |
|       table: ORDERS                                         |
|     primary_key:                                            |
|       columns:                                              |
|         - O_ORDERKEY                                        |
|     dimensions:                                             |
|       - name: ORDER_DATE                                    |
|         description: Date when the order was placed         |
|         expr: o_orderdate                                   |
|         data_type: DATE                                     |
|       - name: ORDER_YEAR                                    |
|         description: Year when the order was placed         |
|         expr: YEAR(o_orderdate)                             |
|         data_type: "NUMBER(4,0)"                            |
|       - name: O_ORDERKEY                                    |
|         expr: O_ORDERKEY                                    |
|         data_type: VARCHAR(134217728)                       |
|       - name: O_CUSTKEY                                     |
|         expr: O_CUSTKEY                                     |
|         data_type: VARCHAR(134217728)                       |
|     facts:                                                  |
|       - name: COUNT_LINE_ITEMS                              |
|         expr: COUNT(line_items.line_item_id)                |
|         data_type: "NUMBER(18,0)"                           |
|     metrics:                                                |
|       - name: AVERAGE_LINE_ITEMS_PER_ORDER                  |
|         description: Average number of line items per order |
|         expr: AVG(orders.count_line_items)                  |
|       - name: ORDER_AVERAGE_VALUE                           |
|         description: Average order value across all orders  |
|         expr: AVG(orders.o_totalprice)                      |
| relationships:                                              |
|   - name: LINE_ITEM_TO_ORDERS                               |
|     left_table: LINE_ITEMS                                  |
|     right_table: ORDERS                                     |
|     relationship_columns:                                   |
|       - left_column: L_ORDERKEY                             |
|         right_column: O_ORDERKEY                            |
|   - name: ORDERS_TO_CUSTOMERS                               |
|     left_table: ORDERS                                      |
|     right_table: CUSTOMERS                                  |
|     relationship_columns:                                   |
|       - left_column: O_CUSTKEY                              |
|         right_column: C_CUSTKEY                             |
|                                                             |
+-------------------------------------------------------------+
```
