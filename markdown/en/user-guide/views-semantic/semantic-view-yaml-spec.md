# YAML specification for semantic views

Semantic views are schema-level objects that define business concepts over your data, making it easier for users to query and analyze data using business terminology. You can use the YAML specification to create a semantic view in Cortex Analyst or use the [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml) stored procedure to create a semantic view from a YAML specification.

For a comparison of YAML and DDL authoring approaches, see
[Choosing between YAML and DDL for semantic views](/user-guide/views-semantic/yaml-vs-ddl).

## Overview

**Semantic views are the recommended approach** for defining business semantics in Snowflake. They are schema-level objects
that integrate with Snowflake’s privilege system, sharing mechanisms, and metadata catalog.

Note

Legacy semantic model YAML files (stored on stages) can still be used with Cortex Analyst for backward compatibility,
but we recommend using semantic views for new implementations.

The benefits of semantic views over legacy semantic models are:

- **Native Snowflake integration**: Schema-level objects with full RBAC, sharing, and catalog support
- **Advanced features**: Support for derived metrics and access modifiers (public/private)
- **Better governance**: Integrated with Snowflake’s privilege and sharing systems
- **Simplified management**: No need to manage YAML files on stages

## YAML format

Semantic views can take a [YAML](https://yaml.org/) specification to define their behavior, allowing for readable, plain-text definitions.

The general syntax of a semantic view YAML specification is:

Copy code

```
# Name and description of the semantic view.
name: <name>
description: <string>

# Logical table-level concepts
# A semantic view can contain one or more logical tables.
tables:
  # A logical table on top of a base table.
  - name: <name>
    description: <string>
    # The fully qualified name of the base table, or a SQL query definition.
    base_table:
      database: <database>
      schema: <schema>
      table: <base table name>
      # Or, instead of database/schema/table, specify a SQL query:
      # definition: <SQL query>

    primary_key:                          # Optional: 0 or 1 primary key.
      columns: [<col1>, <col2>, ...]
    unique_keys:                          # Optional: 0 to N unique keys.
      - columns: [<col1>, <col2>, ...]

    # Dimension columns in the logical table.
    dimensions:
      - name: <name>
        synonyms: <array of strings>
        description: <string>
        expr: <SQL expression>
        data_type: <data type>
        cortex_search_service:
          service: <string>
          literal_column: <string>
          database: <string>
          schema: <string>
        is_enum: <boolean>
        labels:                       # Optional: specify "filter" to use as a WHERE clause condition.
          - filter
        tags:                         # Optional tags for the dimension.
          - name:
              database: <database>
              schema: <schema>
              tag: <tag_name>
            value: <tag_value>
    - ...
    # Time dimension columns in the logical table.
    time_dimensions:
      - name: <name>
        synonyms: <array of strings>
        description: <string>
        expr: <SQL expression>
        data_type: <data type>

    # Fact columns in the logical table.
    facts:
      - name: <name>
        synonyms: <array of strings>
        description: <string>
        access_modifier: <public_access | private_access>  # Default is public_access.
        expr: <SQL expression>
        data_type: <data type>
        labels:                       # Optional: specify "filter" to use as a WHERE clause condition.
          - filter
        tags:                         # Optional tags for the fact.
          - name:
              database: <database>
              schema: <schema>
              tag: <tag_name>
            value: <tag_value>

    # Regular metrics scoped to the logical table.
    metrics:
      - name: <name>
        synonyms: <array of strings>
        description: <string>
        access_modifier: <public_access | private_access>  # Default is public_access.
        expr: <SQL expression>
        non_additive_dimensions:
        - table: <table name>
          dimension: <dimension name>
          sort_direction: <ascending | descending>
          null_order: <first | last>
        using_relationships:
        - <relationship_name>
        tags:                         # Optional tags for the metric.
          - name:
              database: <database>
              schema: <schema>
              tag: <tag_name>
            value: <tag_value>

    # Standalone filters (entity-level filters are recommended instead).
    filters:
      - name: <name>
        synonyms: <array of strings>
        description: <string>
        expr: <SQL expression>

    # Optional tags for the logical table.
    tags:
      - name:
          database: <database>
          schema: <schema>
          tag: <tag_name>
        value: <tag_value>

# View-level concepts
# Relationships between logical tables
relationships:
  - name: <string>
    left_table: <table>
    right_table: <table>
    relationship_columns:
      - left_column: <column>
        right_column: <column>
        type: <asof | range>             # Optional: defaults to equality join.
        right_range:                     # Required when type is "range".
          start_column: <column>
          end_column: <column>
      - left_column: <column>
        right_column: <column>

# Variables for parameterized semantic views
variables:
  - name: <name>
    data_type: <data type>
    default_value: <string>              # Optional: default value for the variable.
    description: <string>                # Optional: description of the variable.

# Derived metrics scoped to the semantic view.
# Derived metrics combine metrics from multiple tables.
metrics:
  - name: <name>
    synonyms: <array of strings>
    description: <string>
    access_modifier: <public_access | private_access>  # Default is public_access
    expr: <SQL expression>
    tags:                           # Optional tags for the derived metric.
      - name:
          database: <database>
          schema: <schema>
          tag: <tag_name>
        value: <tag_value>

# Additional context concepts
# Verified queries with example questions and queries that answer them
verified_queries:
  - name: <string>       # A descriptive name of the query.
    question: <string>   # The natural language question that this query answers.
    verified_at: <int>   # Optional: Time (in seconds since the UNIX epoch, January 1, 1970) when the query was verified.
    verified_by: <string> # Optional: Name of the person who verified the query.
    use_as_onboarding_question: <boolean>  # Optional: Marks this question as an onboarding question for the end user.
    sql: <string>        # The SQL query for answering the question

# Custom instructions for Cortex Analyst
# Freeform guidance for SQL generation (legacy; prefer module_custom_instructions).
custom_instructions: <string>

# Module-scoped custom instructions for Cortex Analyst
module_custom_instructions:
  sql_generation: <string>            # Instructions for SQL generation
  question_categorization: <string>   # Instructions for classifying user questions

# Maximum staleness for materializations (in seconds).
# Required to add materializations to the semantic view.
# Example: 7200 sets a 2-hour maximum staleness.
max_staleness: <integer>

# Optional tags for the semantic view itself.
tags:
  - name:
      database: <database>
      schema: <schema>
      tag: <tag_name>
    value: <tag_value>
```

Important

**Semantic views do not require** the `join_type` or `relationship_type` fields that were used in legacy semantic
models. The relationship type is automatically inferred from the data.

## Key concepts

### Tables

Logical tables represent business entities (such as customers, orders, or products) and map to physical database tables
or SQL queries. Each logical table can define:

- **Base table**: The fully qualified name of the physical table, or a SQL query using the `definition` property
- **Primary key**: The column whose values uniquely identify each row (0 or 1 per table)
- **Unique keys**: Additional columns whose values are each unique across rows (0 to N per table)
- **Synonyms**: Alternative names for the table
- **Description**: Business-friendly explanation of what the table represents

#### `primary_key`

The column whose values uniquely identify each row. A table can have 0 or 1 primary key.

Copy code

```
primary_key:
  columns: [customer_id]
```

#### `unique_keys`

Additional columns whose values are each unique across rows. A table can have 0 to N unique keys.

Copy code

```
unique_keys:
  - columns: [email]
  - columns: [region, account_number]
```

To specify a SQL query instead of a physical table, use the `definition` property under `base_table` (instead of
`database`, `schema`, and `table`). For more information, see
[Using an SQL query as a logical table](/user-guide/views-semantic/inline-view#label-semantic-view-logical-table-sql-query-yaml).

### Dimensions

Dimensions represent categorical attributes that provide context for analysis. They answer “who,” “what,” “where,” and
“when” questions. Dimensions can be:

- **Regular dimensions**: Text, numeric, or other categorical values
- **Time dimensions**: Date or timestamp columns with special time-based handling

#### Properties of dimensions

- `expr`: SQL expression to calculate the dimension value
- `synonyms`: Alternative terms users might use
- `is_enum`: Whether the dimension has a fixed set of values
- `cortex_search_service`: Optional Cortex Search service for semantic search
- `labels`: Set to `[filter]` to indicate this dimension can be used as a condition in a WHERE clause (expression must resolve to BOOLEAN)

#### Optional properties for physical dimensions

These fields are optional, but recommended for producing higher-quality results from a semantic view search.

`synonyms`
:   A list of other terms/phrases used to refer to this dimension. Must be unique across all synonyms in this semantic model.

`description`
:   A brief description of this dimension. Include information that provides useful context, such as the data this dimension represents.

`sample_values`
:   Sample values of this column, if any. Add any value that is likely to be referenced in the user questions.

`is_enum`
:   A boolean value. If `True`, the values in the `sample_values` field are taken to be the full list of possible values,
    and the model only chooses from those values when filtering on that column.

`cortex_search_service`
:   Specifies the Cortex Search Service to use for this dimension. It has the following fields:

    - `service`: The name of the Cortex Search Service.
    - `literal_column`: (optional) The column in the Cortex Search Service that contains the literal values.
    - `database`: (optional) The database where the Cortex Search Service is located. Defaults to `base_table`’s database.
    - `schema`: (optional) The schema where the Cortex Search Service is located. Defaults to `base_table`’s schema.

    `cortex_search_service` replaces the `cortex_search_service_name` field, which could only specify the name. `cortex_search_service_name` has been deprecated.

#### Optional properties for time dimensions

These fields are optional, but recommended for producing higher-quality results from a semantic view search.

`synonyms`
:   A list of other terms/phrases used to refer to this time dimension. Must be unique across all synonyms in this semantic model.

`description`
:   A brief description of this dimension. Include information that provides useful context, such as the time zone that this dimension uses as a reference point.

`sample_values`
:   Sample values of this column, if any. Add any values that are likely to be referenced in the user questions.

### Facts

Facts are row-level quantitative attributes that represent specific business events or transactions. Facts capture
“how much” or “how many” at the most granular level, such as individual sales amounts, quantities purchased, or costs.

Facts typically function as “helper” concepts within the semantic view to help construct dimensions and metrics.

The properties of facts are:

- `expr`: SQL expression to calculate the fact value
- `access_modifier`: Set to `private_access` to hide from queries (useful for intermediate calculations)
- `data_type`: The data type of the fact
- `labels`: Set to `[filter]` to indicate this fact can be used as a condition in a WHERE clause (expression must resolve to BOOLEAN)

### Metrics

Metrics are quantifiable measures of business performance calculated by aggregating facts or other columns using functions
like SUM, AVG, and COUNT.

Two types of metrics:

1. **Table-level metrics**: Scoped to a specific logical table, aggregating data within that table
2. **Derived metrics**: View-level metrics that combine metrics from multiple tables

#### Properties of metrics

- `expr`: SQL expression with aggregation function
- `access_modifier`: Set to `private_access` to hide from queries (useful for intermediate calculations)
- `synonyms`: Alternative terms for the metric

#### Optional properties of metrics

- If you want to
  [specify the dimensions that should be non-additive for the metric](/user-guide/views-semantic/sql#label-semantic-views-metrics-semi-additive), use the
  following fields:

  **`non_additive_dimensions`**

  Specifies the dimensions that the metric should not be aggregated across.

  **`table`**

  Name of the logical table containing the dimension.

  **`dimension`**

  Name of the dimension.

  **`sort_direction`**

  [Sort order for the non-additive dimension](/user-guide/views-semantic/sql#label-semantic-views-metrics-semi-additive-order). You can specify one of
  the following values:

  - `ascending`: Sort the dimension values in ascending order.
  - `descending`: Sort the dimension values in descending order.

  Default: `ascending`

  **`null_order`**

  Specifies whether NULLs are
  [sorted before or after non-NULL values](/user-guide/views-semantic/sql#label-semantic-views-metrics-semi-additive-order).
  You can specify one of the following values:

  - `first`: NULLs are sorted before non-NULL values.
  - `last`: NULLs are sorted after non-NULL values.

  Default: Depends on the value in the `sort_direction` field (`ascending` or `descending`); see
  [the usage notes in the ORDER BY documentation](/sql-reference/constructs/order-by#label-order-by-nulls).

  Note

  Because the rows are sorted by the non-additive dimensions, the order in which you specify the dimensions is important. This
  is similar to the order in which you specify columns in the [ORDER BY](/sql-reference/constructs/order-by) clause.

  The following example specifies that the `m_account_balance` metric cannot be aggregated by the `year_dim` and `month_dim`
  dimensions:

  Copy code

  ```
  metrics:
    - name: m_account_balance
   ...
   non_additive_dimensions:
   - table: bank_accounts
     dimension: year_dim
     sort_direction: ascending
     null_order: last
   - table: bank_accounts
     dimension: month_dim
     sort_direction: descending
     null_order: first
  ```
- If there are multiple relationship paths between two specific logical tables in a semantic view, use the following field to
  [specify the relationship path to use](/user-guide/views-semantic/sql#label-semantic-views-create-logical-tables-relations):

  `using_relationships`

  [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

  Available to all accounts.

  Specifies the name of the relationship to use to join the logical tables when calculating the metric.

### Derived metrics

Derived metrics are view-level metrics not tied to a specific table. They can combine metrics from multiple tables
or perform calculations across the entire view.

Example of a derived metric:

Copy code

```
metrics:
  - name: total_profit_margin
    description: "Overall profit margin across all products"
    expr: (orders.total_revenue - orders.total_cost) / orders.total_revenue
    access_modifier: public_access
```

### Relationships

Relationships define how logical tables join together. Each relationship specifies:

- `left_table`: The table containing the foreign key
- `right_table`: The table being referenced
- `relationship_columns`: Pairs of columns to join on, as `left_column` and `right_column`

The relationship type (one-to-one, many-to-one) is automatically inferred from the data and primary key definitions.

Note

Unlike legacy semantic models, semantic views do not require explicit `join_type` or `relationship_type`
specifications. These are determined automatically.

#### Basic relationships

Copy code

```
relationships:
  - name: orders_to_customers
    left_table: orders
    right_table: customers
    relationship_columns:
      - left_column: customer_id
        right_column: customer_id
```

#### Multi-column joins

When a relationship requires multiple columns (composite foreign keys), list each pair in `relationship_columns`:

Copy code

```
relationships:
  - name: lineitem_to_partsupp
    left_table: lineitem
    right_table: partsupp
    relationship_columns:
      - left_column: l_partkey
        right_column: ps_partkey
      - left_column: l_suppkey
        right_column: ps_suppkey
```

#### One-to-one relationships

One-to-one relationships are inferred automatically when both sides of a relationship have the join column
declared as part of the primary key:

Copy code

```
tables:
  - name: customer_basic
    primary_key:
      columns: [customer_id]
  - name: customer_details
    primary_key:
      columns: [customer_id]

relationships:
  - name: details_to_basic
    left_table: customer_details
    right_table: customer_basic
    relationship_columns:
      - left_column: customer_id
        right_column: customer_id
```

#### ASOF relationships

ASOF relationships join tables based on a point-in-time lookup, commonly used for slowly changing dimensions.
Set `type: asof` on the relationship column that should match by finding the most recent value rather
than an exact match:

Copy code

```
relationships:
  - name: orders_to_address
    left_table: orders
    right_table: customer_address
    relationship_columns:
      - left_column: o_custid
        right_column: ca_custid
      - left_column: o_orddate
        right_column: ca_start_date
        type: asof
```

In this example, each order is matched to the customer address that was most recently valid as of the order
date.

#### Range relationships

Range relationships join tables where a value falls within a range defined by two columns on the target table
(for example, a date between a start date and an end date). Set `type: range` and provide a `right_range`
with the start and end columns:

Copy code

```
relationships:
  - name: orders_to_address
    left_table: orders
    right_table: customer_address
    relationship_columns:
      - left_column: o_custid
        right_column: ca_custid
      - left_column: o_orddate
        right_column: ca_start_date
        type: range
        right_range:
          start_column: ca_start_date
          end_column: ca_end_date
```

In this example, each order is matched to the customer address whose validity period contains the order date.

#### Many-to-many relationships via bridge tables

Many-to-many relationships are expressed by defining two relationships from a bridge (junction) table to two
entity tables. The system infers the many-to-many path from the relationship graph:

Copy code

```
tables:
  - name: authors
    primary_key:
      columns: [author_id]
  - name: books
    primary_key:
      columns: [book_id]
  - name: book_authors
    primary_key:
      columns: [book_id, author_id]

relationships:
  - name: ba_to_authors
    left_table: book_authors
    right_table: authors
    relationship_columns:
      - left_column: author_id
        right_column: author_id
  - name: ba_to_books
    left_table: book_authors
    right_table: books
    relationship_columns:
      - left_column: book_id
        right_column: book_id
```

#### Role-playing tables

A single physical table can appear multiple times under different logical table names to model different
roles. Use different `name` values that point to the same `base_table`:

Copy code

```
tables:
  - name: customer_region
    base_table:
      database: my_db
      schema: my_schema
      table: region
    primary_key:
      columns: [r_regionkey]
  - name: supplier_region
    base_table:
      database: my_db
      schema: my_schema
      table: region
    primary_key:
      columns: [r_regionkey]

relationships:
  - name: customer_nation_to_region
    left_table: customer_nation
    right_table: customer_region
    relationship_columns:
      - left_column: n_regionkey
        right_column: r_regionkey
  - name: supplier_nation_to_region
    left_table: supplier_nation
    right_table: supplier_region
    relationship_columns:
      - left_column: n_regionkey
        right_column: r_regionkey
```

### Filters

There are two ways to define filters in a semantic view YAML specification:

**Entity-level filters (using `labels`)**: You can mark a dimension or fact as a filter by adding `labels: [filter]` to its
definition. The expression must resolve to a BOOLEAN value. This is the YAML equivalent of `LABELS = (FILTER)` in the
[CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command.

Copy code

```
dimensions:
  - name: high_value
    expr: loyalty_points > 100
    labels:
      - filter

facts:
  - name: completed_only
    expr: is_completed
    labels:
      - filter
```

For more information, see [Defining a filter](/user-guide/views-semantic/filters#label-semantic-view-filter-defining).

**Standalone filters**: You can define standalone filter expressions at the table level using the `filters` field.
Standalone filters are supported for Cortex Analyst SQL generation, but the Snowflake semantic SQL compiler uses
entity-level filters (defined with `labels`). For broader compatibility, we recommend using entity-level filters instead.

Copy code

```
filters:
  - name: active_customers
    description: "Customers who have made a purchase in the last 12 months"
    expr: "customer_last_purchase_date >= DATEADD(month, -12, CURRENT_DATE())"
```

### Verified queries

Verified queries are example questions with their corresponding SQL queries. They help Cortex Analyst understand
how to answer similar questions and serve as documentation for users.

Properties:

- `question`: Natural language question
- `sql`: SQL query that answers the question
- `verified_by`: Optional person who verified the query is correct
- `verified_at`: Optional timestamp when verified
- `use_as_onboarding_question`: Optional flag to show this as a suggestion to users

### Tags

You can assign [tags](/user-guide/object-tagging/introduction) to a semantic view and the attributes within it, including
logical tables, dimensions, facts, and metrics. Tags help you track sensitive data, manage governance policies, and organize
your semantic view objects.

Each tag reference specifies the fully qualified tag name (`database`, `schema`, `tag`) and a `value`:

Copy code

```
tags:
  - name:
      database: my_db
      schema: my_schema
      tag: pii_type
    value: "email"
```

You can assign tags at the following levels:

- **Semantic view** (top-level `tags`): Tags on the semantic view object itself.
- **Logical table** (`tags` under a table): Tags on a logical table within the semantic view.
- **Dimension** (`tags` under a dimension): Tags on a specific dimension.
- **Fact** (`tags` under a fact): Tags on a specific fact.
- **Metric** (`tags` under a metric): Tags on a specific metric, including derived metrics.

You can assign multiple tags at each level.

For more information about object tagging, see [Introduction to object tagging](/user-guide/object-tagging/introduction).

## Access modifiers

Semantic views support access modifiers for facts and metrics, allowing you to control visibility:

- `public_access` (default): Visible and queryable by users
- `private_access`: Hidden from queries, used only for intermediate calculations

Example:

Copy code

```
facts:
  - name: internal_cost
    expr: unit_cost * quantity
    data_type: NUMBER
    access_modifier: private_access  # Not visible in queries

metrics:
  - name: total_revenue
    expr: SUM(sale_amount)
    access_modifier: public_access  # Visible in queries
```

## Custom instructions for Cortex Analyst

Custom instructions let you control how Cortex Analyst generates SQL and classifies user questions. You can specify
custom instructions in the YAML specification as top-level keys, or set them through the
[CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view) command (see [Providing custom instructions for Cortex Analyst](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions)).

For detailed guidance and examples, see [Custom instructions in Cortex Analyst](/user-guide/views-semantic/custom-instructions).

### `custom_instructions`

A single freeform string that provides guidance for SQL generation. For example:

Copy code

```
custom_instructions: "Ensure that all numeric columns are rounded to 2 decimal points in the output."
```

Important

Migrate any existing `custom_instructions` to the `sql_generation` component of `module_custom_instructions`,
as described in the following section.

### `module_custom_instructions`

Module-scoped custom instructions provide more granular control by targeting specific components
in the Cortex Analyst pipeline. Set the `module_custom_instructions` key at the top level of your YAML
specification with one or both of the following components:

`sql_generation`
: Instructions for how SQL should be generated (for example, data formatting and filtering).

`question_categorization`
: Instructions for how Cortex Analyst should classify user questions (for example, blocking certain topics or
prompting for missing details).

Example:

Copy code

```
module_custom_instructions:
  sql_generation: |
    Ensure that all numeric columns are rounded to 2 decimal points.
    For any percentage or rate calculation, multiply the result by 100.
  question_categorization: |
    If the question asks for users without providing a product_type, consider this question
    UNCLEAR and ask the user to specify product_type.
    Reject all questions about salary data.
```

When you use Cortex Analyst through a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents), the agent
follows your custom instructions directly. You can write question categorization instructions in plain natural language
without referencing categorization state keywords like `UNCLEAR`. For details, see
[Custom instructions through Cortex Agents](/user-guide/views-semantic/custom-instructions#label-cortex-analyst-custom-instructions-agents).

## Variables

Variables let consumers pass parameters at query time to parameterize dimension, fact, and metric expressions.
Define variables at the top level of the YAML specification:

Copy code

```
variables:
  - name: threshold
    data_type: NUMBER(5,1)
    default_value: "42"
  - name: category_filter
    data_type: STRING
    description: Filter by product category
```

Properties:

- `name`: The variable name, referenced in expressions.
- `data_type`: The Snowflake data type for the variable (for example, `NUMBER`, `STRING`, `FLOAT`).
- `default_value`: Optional default value used when the variable isn’t supplied at query time.
- `description`: Optional description of the variable’s purpose.

Use variables in dimension, fact, or metric expressions by referencing the variable name directly:

Copy code

```
tables:
  - name: orders
    dimensions:
      - name: above_threshold
        expr: order_total > threshold
        data_type: BOOLEAN
    metrics:
      - name: total_above_threshold
        expr: SUM(CASE WHEN order_total > threshold THEN order_total ELSE 0 END)

variables:
  - name: threshold
    data_type: NUMBER
    default_value: "100"
```

When querying the semantic view, pass variable values using the `VARIABLES` clause:

Copy code

```
SELECT * FROM SEMANTIC_VIEW(
  my_sv
  DIMENSIONS orders.above_threshold
  METRICS orders.total_above_threshold
  VARIABLES threshold => 500
);
```

## Pre-aggregated facts

Facts can include aggregate expressions over related tables, creating pre-aggregated values at the
table’s grain. This is useful when a higher-grain table needs a summary of data from a lower-grain
related table:

Copy code

```
tables:
  - name: customer
    facts:
      - name: f_revenue
        expr: SUM(orders.f_order_total)
        data_type: NUMBER
      - name: f_order_count
        expr: COUNT(orders.f_orderkey)
        data_type: NUMBER
  - name: orders
    facts:
      - name: f_order_total
        expr: o_totalprice
        data_type: NUMBER
      - name: f_orderkey
        expr: o_orderkey
        data_type: NUMBER
```

## Window functions in dimensions and facts

Dimensions and facts support window function expressions for rankings, running calculations, and lag/lead
values:

Copy code

```
tables:
  - name: sales
    dimensions:
      - name: category_rank
        expr: "DENSE_RANK() OVER (PARTITION BY quarter ORDER BY revenue DESC)"
        data_type: NUMBER
      - name: prev_quarter_category
        expr: "LAG(subcategory, 1) OVER (PARTITION BY quarter ORDER BY id)"
        data_type: TEXT
    facts:
      - name: running_total_units
        expr: "SUM(units_sold) OVER ()"
        data_type: NUMBER
      - name: rolling_avg_revenue
        expr: "AVG(revenue) OVER (PARTITION BY category ORDER BY quarter ROWS BETWEEN 1 PRECEDING AND CURRENT ROW)"
        data_type: NUMBER
```

Window functions are also supported in metric expressions. The `PARTITION BY EXCLUDING` syntax partitions
by all selected dimensions except the named one(s):

Copy code

```
metrics:
  - name: sales_moving_avg_7_day
    expr: "AVG(lineitem.sales) OVER (ORDER BY orders.dim_day ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)"
  - name: running_total
    expr: "SUM(store_sales.sales_amount) OVER (PARTITION BY EXCLUDING date_dim.day ORDER BY date_dim.day)"
```

### `max_staleness`

Set `max_staleness` at the top level of your YAML specification to enable [materializations](/user-guide/views-semantic/materializations)
on the semantic view. The value is an integer number of seconds representing the maximum acceptable staleness for
materialized data before a refresh is triggered.

Copy code

```
max_staleness: 7200  # 2 hours
```

The minimum allowed value is 120 seconds. You can’t unset `max_staleness` while materializations exist on the
semantic view. Drop all materializations first if you need to remove the property.

For more information, see [Setting the maximum staleness of the materialized dimensions and metrics](/user-guide/views-semantic/materializations#label-semantic-views-materializing-prereqs-staleness).

## Example semantic view YAML

Here’s a complete example of a semantic view YAML specification:

Copy code

```
name: revenue_analysis
description: "Semantic view for analyzing revenue across products and customers"

tables:
  - name: customers
    description: "Customer information"
    base_table:
      database: sales_db
      schema: public
      table: customers
    dimensions:
      - name: customer_name
        synonyms: ["client name", "customer"]
        description: "Full name of the customer"
        expr: c_name
        data_type: VARCHAR
        tags:
          - name:
              database: sales_db
              schema: public
              tag: pii_type
            value: "name"
      - name: customer_segment
        synonyms: ["segment", "market segment"]
        description: "Customer market segment"
        expr: c_mktsegment
        data_type: VARCHAR
        is_enum: true

  - name: orders
    description: "Order information"
    base_table:
      database: sales_db
      schema: public
      table: orders
    dimensions:
      - name: order_date
        description: "Date when order was placed"
        expr: o_orderdate
        data_type: DATE
    time_dimensions:
      - name: order_year
        description: "Year when order was placed"
        expr: YEAR(o_orderdate)
        data_type: NUMBER
    facts:
      - name: order_total
        description: "Total order amount"
        expr: o_totalprice
        data_type: NUMBER
    metrics:
      - name: total_orders
        description: "Total number of orders"
        expr: COUNT(*)
      - name: average_order_value
        description: "Average order value"
        expr: AVG(o_totalprice)

relationships:
  - name: orders_to_customers
    left_table: orders
    right_table: customers
    relationship_columns:
      - left_column: o_custkey
        right_column: c_custkey

variables:
  - name: min_order_amount
    data_type: NUMBER
    default_value: "100"
    description: "Minimum order amount to include"

metrics:
  - name: revenue_per_customer
    description: "Average revenue per customer"
    expr: orders.total_revenue / customers.customer_count
    access_modifier: public_access

module_custom_instructions:
  sql_generation: |
    Always use fiscal year (April-March) for date grouping
    unless the user explicitly asks for calendar year.
  question_categorization: |
    Classify questions about order totals and revenue as
    financial questions.

verified_queries:
  - name: top_customers_by_revenue
    question: "Who are the top 10 customers by revenue?"
    sql: |
      SELECT
        customer_name,
        SUM(order_total) as total_revenue
      FROM revenue_analysis
      GROUP BY customer_name
      ORDER BY total_revenue DESC
      LIMIT 10
    use_as_onboarding_question: true

tags:
  - name:
      database: sales_db
      schema: public
      tag: department
    value: "sales"
```

## Creating a semantic view from YAML

To create a semantic view from a YAML specification, use the
[SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml) stored procedure.

For more information, see [Creating a semantic view from a YAML specification](/user-guide/views-semantic/sql#label-semantic-views-create-from-yaml).

## Getting YAML from a semantic view

To export a semantic view to YAML format, use the
[SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_yaml_from_semantic_view) function.

For more information, see [Getting the YAML specification for a semantic view](/user-guide/views-semantic/sql#label-semantic-views-get-yaml).

## Differences from legacy semantic models

If you’re migrating from stage-based YAML files to semantic views, see
[Migrating from the legacy stage API](/user-guide/views-semantic/semantic-models-vs-views) for
migration guidance.
