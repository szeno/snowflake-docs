# SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML

Creates a [semantic view](/user-guide/views-semantic/overview) from a
[semantic model specification in YAML format](/user-guide/views-semantic/sql), or verifies
that you can use a semantic model specification to create a semantic view.

The stored procedure uses the name from the YAML specification for the name of the semantic view.

If a semantic view with the same name already exists, the stored procedure attempts to replace that semantic view and copy the
grants from that semantic view. This has the same effect as running
[CREATE OR REPLACE SEMANTIC VIEW … COPY GRANTS](/sql-reference/sql/create-semantic-view).

You can pass `TRUE` for the `create_or_alter` argument to use
[CREATE OR ALTER SEMANTIC VIEW](/sql-reference/sql/create-or-alter) semantics instead, which preserves existing
[materializations](/user-guide/views-semantic/materializations) when possible.

See also:
:   [SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_yaml_from_semantic_view),
    [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_OSI\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_osi_yaml),
    [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view)

## Syntax

Copy code

```
SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML(
  '<fully_qualified_schema_name>' ,
  '<yaml_specification>'
  [ , <verify_only> ]
  [ , <create_or_alter> ]
)
```

## Arguments

**Required:**

`'fully_qualified_schema_name'`
:   [Fully qualified name](/sql-reference/name-resolution) of the schema where you want to create the semantic view.

    You must qualify the schema name with the database name (for example, `my_db.my_schema`). Otherwise, an error occurs.

`'yaml_specification'`
:   [Semantic model specification in YAML format](/user-guide/views-semantic/sql).

    If the specification contains quotes, backslashes, or newlines, you can use a
    [dollar-quoted string constant](/sql-reference/data-types-text#label-dollar-quoted-string-constants) for this argument.

**Optional:**

`verify_only`
:   If TRUE, verifies that you can use the semantic model specified by `'yaml_specification'` to create a semantic view.

    You can specify this to verify that you can create a semantic view from the model before you attempt to create the semantic
    view.

    Default: FALSE

`create_or_alter`
:   If TRUE, uses [CREATE OR ALTER SEMANTIC VIEW](/sql-reference/sql/create-or-alter) semantics instead of
    CREATE OR REPLACE when a semantic view with the same name already exists. This preserves existing
    [materializations](/user-guide/views-semantic/materializations) that aren’t affected by the changes.

    Default: FALSE

## Returns

Returns a VARCHAR value containing the status of the operation to create the semantic view or verify that the semantic view can
be created.

If the stored procedure fails to create the semantic view or verify that the semantic view can be created, the stored procedure
throws an exception.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SEMANTIC VIEW | Schema | Required to create a new semantic view. |
| SELECT | Table, view | Required on any tables and/or views used in the semantic view definition. |
| OWNERSHIP | Existing semantic view with the same name. | If a semantic view with the same name already exists, the stored procedure attempts to replace that semantic view. To replace an existing semantic view, you must use a role that has been granted the OWNERSHIP privilege.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

If the name of the database or schema is a [double-quoted identifier](/sql-reference/identifiers-syntax#label-delimited-identifier) (for example, if the name
contains spaces), you must include double quotes around the name. For example:

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML(
  '"my database"."my schema"',
  ...
);
```

## Examples

The following example verifies that you can use a given semantic model specification in YAML to create a semantic view named
`tpch_analysis` in the database `my_db` and schema `my_schema`:

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML(
  'my_db.my_schema',
  $$
  name: TPCH_REV_ANALYSIS
  description: Semantic view for revenue analysis
  tables:
    - name: CUSTOMERS
      description: Main table for customer data
      base_table:
        database: SNOWFLAKE_SAMPLE_DATA
        schema: TPCH_SF1
        table: CUSTOMER
      primary_key:
        columns:
          - C_CUSTKEY
      dimensions:
        - name: CUSTOMER_NAME
          synonyms:
            - customer name
          description: Name of the customer
          expr: customers.c_name
          data_type: VARCHAR(25)
        - name: C_CUSTKEY
          expr: C_CUSTKEY
          data_type: VARCHAR(134217728)
      metrics:
        - name: CUSTOMER_COUNT
          description: Count of number of customers
          expr: COUNT(c_custkey)
    - name: LINE_ITEMS
      description: Line items in orders
      base_table:
        database: SNOWFLAKE_SAMPLE_DATA
        schema: TPCH_SF1
        table: LINEITEM
      primary_key:
        columns:
          - L_ORDERKEY
          - L_LINENUMBER
      dimensions:
        - name: L_ORDERKEY
          expr: L_ORDERKEY
          data_type: VARCHAR(134217728)
        - name: L_LINENUMBER
          expr: L_LINENUMBER
          data_type: VARCHAR(134217728)
      facts:
        - name: DISCOUNTED_PRICE
          description: Extended price after discount
          expr: l_extendedprice * (1 - l_discount)
          data_type: "NUMBER(25,4)"
        - name: LINE_ITEM_ID
          expr: "CONCAT(l_orderkey, '-', l_linenumber)"
          data_type: VARCHAR(134217728)
    - name: ORDERS
      synonyms:
        - sales orders
      description: All orders table for the sales domain
      base_table:
        database: SNOWFLAKE_SAMPLE_DATA
        schema: TPCH_SF1
        table: ORDERS
      primary_key:
        columns:
          - O_ORDERKEY
      dimensions:
        - name: ORDER_DATE
          description: Date when the order was placed
          expr: o_orderdate
          data_type: DATE
        - name: ORDER_YEAR
          description: Year when the order was placed
          expr: YEAR(o_orderdate)
          data_type: "NUMBER(4,0)"
        - name: O_ORDERKEY
          expr: O_ORDERKEY
          data_type: VARCHAR(134217728)
        - name: O_CUSTKEY
          expr: O_CUSTKEY
          data_type: VARCHAR(134217728)
      facts:
        - name: COUNT_LINE_ITEMS
          expr: COUNT(line_items.line_item_id)
          data_type: "NUMBER(18,0)"
      metrics:
        - name: AVERAGE_LINE_ITEMS_PER_ORDER
          description: Average number of line items per order
          expr: AVG(orders.count_line_items)
        - name: ORDER_AVERAGE_VALUE
          description: Average order value across all orders
          expr: AVG(orders.o_totalprice)
  relationships:
    - name: LINE_ITEM_TO_ORDERS
      left_table: LINE_ITEMS
      right_table: ORDERS
      relationship_columns:
        - left_column: L_ORDERKEY
          right_column: O_ORDERKEY
      relationship_type: many_to_one
    - name: ORDERS_TO_CUSTOMERS
      left_table: ORDERS
      right_table: CUSTOMERS
      relationship_columns:
        - left_column: O_CUSTKEY
          right_column: C_CUSTKEY
      relationship_type: many_to_one
  $$,
TRUE);
```

If the specification is valid, the stored procedure returns the following message:

```
+----------------------------------------------------------------------------------+
| SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML                                            |
|----------------------------------------------------------------------------------|
| YAML file is valid for creating a semantic view. No object has been created yet. |
+----------------------------------------------------------------------------------+
```

If the YAML syntax is invalid, the stored procedure throw an exception. For example, if a colon is missing:

Copy code

```
relationships
  - name: LINE_ITEM_TO_ORDERS
```

the stored procedure throws an exception, indicating that the YAML syntax is invalid:

```
392400 (22023): Uncaught exception of type 'EXPRESSION_ERROR' on line 3 at position 23 :
  Invalid semantic model YAML: while scanning a simple key
   in 'reader', line 90, column 3:
        relationships
        ^
  could not find expected ':'
   in 'reader', line 91, column 11:
          - name: LINE_ITEM_TO_ORDERS
                ^
```

If the specification refers to a physical table that does not exist, the stored procedure throws an exception:

Copy code

```
base_table:
  database: SNOWFLAKE_SAMPLE_DATA
  schema: TPCH_SF1
  table: NONEXISTENT
```

```
002003 (42S02): Uncaught exception of type 'EXPRESSION_ERROR' on line 3 at position 23 :
  SQL compilation error:
  Table 'SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.NONEXISTENT' does not exist or not authorized.
```

Similarly, if the specification refers to a primary key column that does not exist, the stored procedure throws an exception:

Copy code

```
primary_key:
  columns:
    - NONEXISTENT
```

```
000904 (42000): Uncaught exception of type 'EXPRESSION_ERROR' on line 3 at position 23 :
  SQL compilation error: error line 0 at position -1
  invalid identifier 'NONEXISTENT'
```

The following example creates a semantic view named `tpch_analysis` in the database `my_db` and schema `my_schema`:

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML(
  'my_db.my_schema',
  $$
  name: TPCH_REV_ANALYSIS
  description: Semantic view for revenue analysis
  tables:
    - name: CUSTOMERS
      description: Main table for customer data
      base_table:
        database: SNOWFLAKE_SAMPLE_DATA
        schema: TPCH_SF1
        table: CUSTOMER
      primary_key:
        columns:
          - C_CUSTKEY
      dimensions:
        - name: CUSTOMER_NAME
          synonyms:
            - customer name
          description: Name of the customer
          expr: customers.c_name
          data_type: VARCHAR(25)
        - name: C_CUSTKEY
          expr: C_CUSTKEY
          data_type: VARCHAR(134217728)
      metrics:
        - name: CUSTOMER_COUNT
          description: Count of number of customers
          expr: COUNT(c_custkey)
    - name: LINE_ITEMS
      description: Line items in orders
      base_table:
        database: SNOWFLAKE_SAMPLE_DATA
        schema: TPCH_SF1
        table: LINEITEM
      primary_key:
        columns:
          - L_ORDERKEY
          - L_LINENUMBER
      dimensions:
        - name: L_ORDERKEY
          expr: L_ORDERKEY
          data_type: VARCHAR(134217728)
        - name: L_LINENUMBER
          expr: L_LINENUMBER
          data_type: VARCHAR(134217728)
      facts:
        - name: DISCOUNTED_PRICE
          description: Extended price after discount
          expr: l_extendedprice * (1 - l_discount)
          data_type: "NUMBER(25,4)"
        - name: LINE_ITEM_ID
          expr: "CONCAT(l_orderkey, '-', l_linenumber)"
          data_type: VARCHAR(134217728)
    - name: ORDERS
      synonyms:
        - sales orders
      description: All orders table for the sales domain
      base_table:
        database: SNOWFLAKE_SAMPLE_DATA
        schema: TPCH_SF1
        table: ORDERS
      primary_key:
        columns:
          - O_ORDERKEY
      dimensions:
        - name: ORDER_DATE
          description: Date when the order was placed
          expr: o_orderdate
          data_type: DATE
        - name: ORDER_YEAR
          description: Year when the order was placed
          expr: YEAR(o_orderdate)
          data_type: "NUMBER(4,0)"
        - name: O_ORDERKEY
          expr: O_ORDERKEY
          data_type: VARCHAR(134217728)
        - name: O_CUSTKEY
          expr: O_CUSTKEY
          data_type: VARCHAR(134217728)
      facts:
        - name: COUNT_LINE_ITEMS
          expr: COUNT(line_items.line_item_id)
          data_type: "NUMBER(18,0)"
      metrics:
        - name: AVERAGE_LINE_ITEMS_PER_ORDER
          description: Average number of line items per order
          expr: AVG(orders.count_line_items)
        - name: ORDER_AVERAGE_VALUE
          description: Average order value across all orders
          expr: AVG(orders.o_totalprice)
  relationships:
    - name: LINE_ITEM_TO_ORDERS
      left_table: LINE_ITEMS
      right_table: ORDERS
      relationship_columns:
        - left_column: L_ORDERKEY
          right_column: O_ORDERKEY
      relationship_type: many_to_one
    - name: ORDERS_TO_CUSTOMERS
      left_table: ORDERS
      right_table: CUSTOMERS
      relationship_columns:
        - left_column: O_CUSTKEY
          right_column: C_CUSTKEY
      relationship_type: many_to_one
  $$
);
```

```
+-----------------------------------------+
| SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML   |
|-----------------------------------------|
| Semantic view was successfully created. |
+-----------------------------------------+
```
