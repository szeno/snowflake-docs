# Using variables in a semantic view

In a [semantic view](/user-guide/views-semantic/overview), you can use variables to customize the calculations performed
for a fact, dimension, or metric without having to change the definition of the view.

In the definitions of facts, dimensions, and metrics, you can include a variable and assign it a default value. When you query the
semantic view, you can specify values for each variable.

## Defining a variable with DDL

To define a variable in a semantic view, use the VARIABLES clause in the
[CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command:

Copy code

```
CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  TABLES ( logicalTable [ , ... ] )
  [ RELATIONSHIPS ( relationshipDef [ , ... ] ) ]
  [ VARIABLES ( variableDef [ , ... ] ) ]
  [ FACTS ( factExpression [ , ... ] ) ]
  [ DIMENSIONS ( dimensionExpression [ , ... ] ) ]
  [ METRICS ( { metricExpression | windowFunctionMetricExpression } [ , ... ] ) ]
  ...
```

Copy code

```
variableDef ::=
  <variable_name> [ <data_type> ]
    [ { DEFAULT | := } <default_expr> ]
    [ COMMENT '<description>' ]
```

where:

- `variable_name` is a name for the variable. The name must follow the
  [identifier rules](/sql-reference/identifiers-syntax).

  Note

  - You can’t use the same name as a fact, dimension, or metric.
  - If you use the same name as a column in the base table, unqualified references to the name resolve to the variable,
    while qualified names resolve to the column.
- `data_type` is one of the [supported data types](#label-semantic-view-variable-data-types).
- `default_expr` is a [supported SQL expression](#label-semantic-view-variable-expressions) that determines the
  default value of the variable.
- `description` is a comment that describes the variable.

You can use variables in the definitions of facts, dimensions, and metrics. You can also use variables in the WHERE clause when you
[query the semantic view](#label-semantic-view-variable-query) with `SEMANTIC_VIEW(...)`.

Note

You can’t use variables in UNIQUE, PRIMARY KEY, or RELATIONSHIP key constraints:

Copy code

```
CREATE SEMANTIC VIEW not_allowed
  TABLES (t UNIQUE (c1, my_var))
  VARIABLES (my_var INT DEFAULT 1);
```

You also can’t use variables in calculations that are used in key constraints:

Copy code

```
CREATE SEMANTIC VIEW not_allowed
  TABLES(t UNIQUE (c1, calc_dim))
  DIMENSIONS(t.calc_dim AS c1 + my_var)
  VARIABLES (my_var INT DEFAULT 1);
```

## Defining a variable with YAML

You can also define variables in the
[YAML specification](/user-guide/views-semantic/semantic-view-yaml-spec) for a semantic view.
Add a top-level `variables` section:

Copy code

```
variables:
  - name: <variable_name>
    data_type: <data_type>
    default: <default_value>
    description: <string>
```

For example:

Copy code

```
variables:
  - name: min_amount
    data_type: NUMBER
    default: "1000"
    description: "Minimum sale amount for HIGH category"
  - name: multiplier
    data_type: NUMBER
    default: "1.0"
    description: "Sales weight multiplier"
  - name: target_region
    data_type: VARCHAR
    description: "Region to filter on"
```

You can reference these variables in `expr` fields for facts, dimensions, and metrics, just as you would with DDL-defined
variables.

## Example: semantic view with variables

Suppose that you have a table containing sales data:

Copy code

```
CREATE OR REPLACE TABLE sales (
  sale_id INTEGER,
  amount NUMBER,
  region VARCHAR,
  sale_date DATE
);

INSERT INTO sales VALUES
  (1, '900.00', 'East', '2025-01-01'),
  (2, '1000.00', 'West', '2025-01-15'),
  (3, '2000.00', 'South', '2025-01-31'),
  (4, '700.00', 'North', '2025-02-01');
```

Suppose that you want to set up a semantic view that includes:

- A `sale_category` dimension that is set to `LOW` or `HIGH`, depending on a minimum amount that you specify.
- A `weighted_sales` metric that is the sum of the sales amounts adjusted by a multiplier that you specify.

Suppose that you also want to filter the regions based on a specified region.

You can create a semantic view that defines variables for the above:

Copy code

```
CREATE OR REPLACE SEMANTIC VIEW sales_analysis
  TABLES (
    sales PRIMARY KEY (sale_id)
  )
  VARIABLES (
    min_amount NUMBER DEFAULT 1000,
    multiplier NUMBER := 1.0,
    target_region VARCHAR
  )
  FACTS (
    sales.amount AS amount,
    sales.adjusted_amount AS amount * multiplier
  )
  DIMENSIONS (
    sales.region AS region,
    sales.sale_category AS
      CASE
        WHEN amount >= min_amount THEN 'HIGH'
        ELSE 'LOW'
      END
  )
  METRICS (
    sales.total_sales AS SUM(amount),
    sales.weighted_sales AS SUM(amount * multiplier)
  );
```

This example defines three variables:

- `min_amount` determines the value of the `sale_category` dimension. If the sale amount is equal to or greater than this
  variable, the category is `HIGH`.
- `multiplier` determines the calculation of the `weighted_sales` metric. The sales amounts are multiplied by this variable
  before being added up.
- `target_region` filters results by region in the query WHERE clause. Unlike the other two variables, it isn’t
  referenced in a fact, dimension, or metric definition.

Both `min_amount` and `multiplier` have default values, which means that you don’t need to set these variables when
querying the semantic view. The example also shows the two supported ways of specifying a default value:

Copy code

```
min_amount NUMBER DEFAULT 1000,
multiplier NUMBER := 1.0,
```

## Supported data types for variables

You can specify one of the following data types:

- [Numeric types](/sql-reference/data-types-numeric), including NUMBER, INTEGER, FLOAT, and DOUBLE.
- [String and binary types](/sql-reference/data-types-text), including VARCHAR, STRING, TEXT, and BINARY.
- [Date and time types](/sql-reference/data-types-datetime), including DATE, TIME, TIMESTAMP, and variants of TIMESTAMP.
- [Logical types](/sql-reference/data-types-logical), including BOOLEAN.
- [Geospatial types](/sql-reference/data-types-geospatial), including GEOGRAPHY and GEOMETRY.
- [Vector types](/sql-reference/data-types-vector), including VECTOR on INT and FLOAT.

Note

VARIANT, OBJECT, and ARRAY aren’t supported.

The following example defines variables of different types and calls functions to set the default values of some of the variables:

Copy code

```
VARIABLES (
  threshold NUMBER(10,2) DEFAULT 100.50,
  region_filter VARCHAR,
  start_date DATE DEFAULT CURRENT_DATE(),
  is_active BOOLEAN DEFAULT TRUE,
  location GEOGRAPHY DEFAULT TO_GEOGRAPHY('POINT(-122.35 37.55)')
)
```

## Supported expressions for variables

You can specify the following types of expressions for the value of a variable:

- Literal values and [arithmetic expressions](/sql-reference/operators-arithmetic) (for example, `10 + 20 + 2`)
- Calls to [scalar functions and system functions](/sql-reference-functions) (for example, `ABS(-5)`,
  `UPPER('hello')`, `CURRENT_DATE()`, and `UUID_STRING()`)
- [Conditional expressions](/sql-reference/expressions-conditional) (for example, `CASE WHEN ... THEN ... END`,
  `COALESCE()`, and `IFF()`)
- [Data type conversions](/sql-reference/functions-conversion) (for example, `TO_NUMBER('42')`,
  `TO_VARCHAR(12345)`, and `TO_DATE('2024-01-01')`)
- Calls to [user-defined functions](/developer-guide/udf/udf-overview)

You can use a [bind variable](/sql-reference/bind-variables) or
[session variable](/sql-reference/session-variables) when querying a semantic view but not when defining a semantic view.

You can’t use a subquery for the value of a variable (when creating the semantic view or when querying the semantic view).

## Setting a variable in a query

When you query the semantic view, you can set values for variables in the
[SEMANTIC\_VIEW](/sql-reference/constructs/semantic_view) expression:

Copy code

```
SEMANTIC_VIEW(
  [<namespace>.]<semantic_view_name>
  [
    {
      METRICS <metric_expr> [ [ AS ] <alias> ] [ , ... ] |
      FACTS <fact_expr>  [ , ... ]
    }
  ]
  [ DIMENSIONS <dimension_expr>  [ [ AS ] <alias> ] [ , ... ] ]
  [ WHERE <predicate> ]
  [ VARIABLES <variable> { = | => } <value> [ , ... ] ]
)
```

You can use either `=` or `=>` between the variable name and value. The two operators are equivalent.

For example, to query [the semantic view that you defined earlier](#label-semantic-view-variable-example):

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
  sales_analysis
  DIMENSIONS region, sale_category
  METRICS weighted_sales
  WHERE region = target_region
  VARIABLES min_amount = 2000,
          target_region => 'West',
          multiplier = 1.5
);
```

Copy code

```
+--------+---------------+----------------+
| REGION | SALE_CATEGORY | WEIGHTED_SALES |
|--------+---------------+----------------|
| West   | LOW           |         1500.0 |
+--------+---------------+----------------+
```

This example overrides the default values of the `min_amount` and `multiplier` variables.

The example also sets the `target_region` variable and uses the variable in the WHERE clause of the query.

Note

If you define a variable that doesn’t have a default value and you don’t set that variable in the query, the query fails.

## Limitations

Currently, variables have the following limitations:

- The [SHOW VARIABLES](/sql-reference/sql/show-variables) command doesn’t return variables in semantic views.
- Variables can’t be used in window function frame bounds.
