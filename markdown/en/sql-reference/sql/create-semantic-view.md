# CREATE SEMANTIC VIEW

Creates a new [semantic view](/user-guide/views-semantic/overview) in the current/specified schema.

The semantic view must comply with [these validation rules](/user-guide/views-semantic/validation-rules).

This command supports the following variants:

- [CREATE OR ALTER SEMANTIC VIEW](#label-create-or-alter-semantic-view-syntax): Creates a semantic view if it doesn’t exist or alters an existing semantic view.

See also:
:   [ALTER SEMANTIC VIEW](/sql-reference/sql/alter-semantic-view) , [DESCRIBE SEMANTIC VIEW](/sql-reference/sql/desc-semantic-view) , [DROP SEMANTIC VIEW](/sql-reference/sql/drop-semantic-view) , [SHOW SEMANTIC VIEWS](/sql-reference/sql/show-semantic-views) , [SHOW SEMANTIC DIMENSIONS](/sql-reference/sql/show-semantic-dimensions) , [SHOW SEMANTIC DIMENSIONS FOR METRIC](/sql-reference/sql/show-semantic-dimensions-for-metric) , [SHOW SEMANTIC FACTS](/sql-reference/sql/show-semantic-facts) , [SHOW SEMANTIC METRICS](/sql-reference/sql/show-semantic-metrics) , [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SEMANTIC VIEW [ IF NOT EXISTS ] <name>
  TABLES ( logicalTable [ , ... ] )
  [ RELATIONSHIPS ( relationshipDef [ , ... ] ) ]
  [ FACTS ( factExpression [ , ... ] ) ]
  [ DIMENSIONS ( dimensionExpression [ , ... ] ) ]
  [ METRICS ( { metricExpression | windowFunctionMetricExpression } [ , ... ] ) ]
  [ COMMENT = '<comment_about_semantic_view>' ]
  [ MAX_STALENESS = <integer> ]
  [ AI_SQL_GENERATION '<instructions_for_sql_generation>' ]
  [ AI_QUESTION_CATEGORIZATION '<instructions_for_question_categorization>' ]
  [ AI_VERIFIED_QUERIES ( verifiedQuery [ , ... ] ) ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  [ COPY GRANTS ]
```

where:

- The [parameters for logical tables](#label-create-semantic-view-tables) are:

  Copy code

  ```
  logicalTable ::=
    [ <table_alias> AS ] <table_name>
    [ PRIMARY KEY ( <primary_key_column_name> [ , ... ] ) ]
    [
   UNIQUE ( <unique_column_name> [ , ... ] )
   [ ... ]
    ]
    [
   CONSTRAINT [ <constraint_name> ]
     DISTINCT RANGE BETWEEN <start_column> AND <end_column> EXCLUSIVE
    ]
    [ WITH SYNONYMS [ = ] ( '<synonym>' [ , ... ] ) ]
    [ COMMENT = '<comment_about_table>' ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
  ```
- The [parameters for relationships](#label-create-semantic-view-relationships) are:

  Copy code

  ```
  relationshipDef ::=
    [ <relationship_identifier> AS ]
    <table_alias> ( <column_name> [ , ... ] )
    REFERENCES
    <ref_table_alias> [ (
   [ ASOF ] <ref_column_name> [ , ... ] |
   BETWEEN <start_column> AND <end_column> EXCLUSIVE
    ) ]
  ```
- The [parameters for expressions in the definitions of facts](#label-create-semantic-view-expressions) are:

  Copy code

  ```
  factExpression ::=
    [ { PRIVATE | PUBLIC } ] <table_alias>.<fact>
   [ LABELS = ( FILTER ) ]
   AS <sql_expr>
    [ WITH SYNONYMS [ = ] ( '<synonym>' [ , ... ] ) ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ COMMENT = '<comment_about_the_fact>' ]
  ```
- The [parameters for expressions in the definitions of dimensions](#label-create-semantic-view-expressions) are:

  Copy code

  ```
  dimensionExpression ::=
    [ PUBLIC ] <table_alias>.<dimension>
   [ LABELS = ( FILTER ) ]
   AS <sql_expr>
    [ WITH SYNONYMS [ = ] ( '<synonym>' [ , ... ] ) ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ COMMENT = '<comment_about_the_dimension>' ]
    [ WITH CORTEX SEARCH SERVICE <search_service_name> [ USING <search_service_column_name> ] ]
  ```
- The [parameters for expressions in the definitions of metrics](#label-create-semantic-view-expressions) are:

  Copy code

  ```
  metricExpression ::=
    [ { PRIVATE | PUBLIC } ] <table_alias>.<metric>
   [ USING ( <relationship_name> [ , ... ] ) ]
   [
     NON ADDITIVE BY (
       <dimension> [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ]
       [ , ... ]
     )
   ]
   AS <sql_expr>
    [ WITH SYNONYMS [ = ] ( '<synonym>' [ , ... ] ) ]
    [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
    [ COMMENT = '<comment_about_the_metric>' ]
  ```

- You can define a metric that uses a window function (a *window function metric*) by using the following syntax:

  Copy code

  ```
  windowFunctionMetricExpression ::=
    [ { PRIVATE | PUBLIC } ] <table_alias>.<metric> AS
   <window_function>( <metric> ) OVER (
     [ PARTITION BY { <exprs_using_dimensions_or_metrics> | EXCLUDING <dimensions> } ]
     [ ORDER BY <exprs_using_dimensions_or_metrics> [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ...] ]
     [ <windowFrameClause> ]
   )
  ```

  For information about this syntax, see [Parameters for window function metrics](#label-create-semantic-view-window-function).

- The [parameters for verified queries](#label-create-semantic-view-verified-queries) are:

  Copy code

  ```
  verifiedQuery ::=
    <verified_query_name> AS (
   QUESTION '<question>'
   [ VERIFIED_AT <timestamp> ]
   [ ONBOARDING_QUESTION <boolean> ]
   [ VERIFIED_BY '( <purpose> = <contact> )' ]
   SQL '<verified_query>'
    )
  ```

Note

The order of the clauses is important. For example, you must specify the FACTS clause before the DIMENSIONS clause.

You can refer to semantic expressions that are defined in later clauses. For example, even if `fact_2` is defined after
`fact_1`, you can still use `fact_2` in the definition of `fact_1`.

## Required parameters

`name`
:   Specifies the name of the semantic view; the name must be unique for the schema in which the semantic view is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`COMMENT = 'comment_about_semantic_view'`
:   Specifies a comment about the semantic view.

`MAX_STALENESS = integer`
:   Sets the maximum number of seconds that a [materialization](/user-guide/views-semantic/materializations) can be stale
    before Snowflake automatically suspends it. Required before you can add materializations to the semantic view.
    Minimum value: `120` (2 minutes). Can’t be unset while materializations exist on the semantic view.

`AI_SQL_GENERATION 'instructions_for_sql_generation'`
:   Specifies [instructions for Cortex Analyst](/user-guide/views-semantic/custom-instructions) that explain
    how to generate the SQL statement.

    For more information, see [Providing custom instructions for Cortex Analyst](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions).

`AI_QUESTION_CATEGORIZATION 'instructions_for_question_categorization'`
:   Specifies [instructions for Cortex Analyst](/user-guide/views-semantic/custom-instructions) that explain
    how to classify questions.

    For more information, see [Providing custom instructions for Cortex Analyst](/user-guide/views-semantic/sql#label-semantic-views-custom-instructions).

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`COPY GRANTS`
:   When you specify OR REPLACE to replace an existing semantic view with a new semantic view, you can set this parameter to copy
    any privileges granted on the existing semantic view to the new semantic view.

    The command copies all privilege grants except OWNERSHIP from the existing semantic view to the new semantic view. The
    role that executes the CREATE SEMANTIC VIEW statement owns the new view.

    The new semantic view does not inherit any future grants defined for the object type in the schema.

    The operation to copy grants occurs atomically with the CREATE SEMANTIC VIEW statement (in other words, within the same
    transaction).

    If you omit COPY GRANTS, the new semantic view does not inherit any explicit access privileges granted on the existing
    semantic view but does inherit any future grants defined for the object type in the schema.

## Parameters for logical tables

These parameters are part of the [syntax for logical tables](/sql-reference/sql/create-semantic-view#label-create-semantic-view-syntax-logical-table):

`table_alias AS`
:   Specifies an optional alias for the logical table.

    - If you specify an alias, you must use this alias when referring to the logical table in relationships, facts, dimensions,
      and metrics.
    - If you do not specify an alias, you use the unqualified logical table name to refer to the table.

`table_name`
:   Specifies the name of the logical table.

`PRIMARY KEY ( primary_key_column_name [ , ... ] )`
:   Specifies the names of one or more columns in the logical table that serve as the primary key of the table.

`UNIQUE ( unique_column_name [ , ... ] )`
:   Specifies the name of a column containing a unique value or the names of columns that contain unique combinations of values.

    For example, if the column `service_id` contains unique values, specify:

    Copy code

    ```
    TABLES(
      ...
      product_table UNIQUE (service_id)
    ```

    If the combination of values in the `product_area_id` and `product_id` columns is unique, specify:

    Copy code

    ```
    TABLES(
      ...
      product_table UNIQUE (product_area_id, product_id)
      ...
    ```

    You can identify multiple columns and multiple combinations of columns as unique in a given logical table:

    Copy code

    ```
    TABLES(
      ...
      product_table UNIQUE (product_area_id, product_id) UNIQUE (service_id)
      ...
    ```

    Note

    If you already identified a column as a primary key column (by using PRIMARY KEY), do not add the UNIQUE clause for that
    column.

`CONSTRAINT [ constraint_name ]`
  
`DISTINCT RANGE BETWEEN start_column AND end_column EXCLUSIVE`
> [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
>
> Available to all accounts.
>
> Specifies a constraint for a [range join](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins).
>
> `constraint_name`
> :   Specifies an optional name for the constraint.
>
>     If you omit this name, the command uses a system-generated name for the constraint.
>
> `DISTINCT RANGE BETWEEN start_column AND end_column EXCLUSIVE` specifies that in each row, the range
> between `start_column` and `end_column` is a distinct range:
>
> - The range is a [half-open interval](https://en.wikipedia.org/wiki/Interval_(mathematics)#Definitions_and_terminology),
>   where the range is closed on the left side (`start_column`) and open on the right
>   (`end_column`).
>
>   In other words, the time on the left is included in the range, but the time on the right is excluded from the range.
>
>   For example, for a row in this table, if the value in `start_column` is `2024-01-15 00:00:00.000` and the value
>   in `end_column` is `2024-02-01 00:00:00.000`, the range is:
>
>   `2024-01-15 00:00:00.000 <= timestamp_from_other_table < 2024-02-01 00:00:00.000`
>
>   The timestamp `2024-01-15 00:00:00.000` is included in this range, but the timestamp `2024-02-01 00:00:00.000` is not.
> - `start_column` and `end_column` must be physical columns from the same table or facts or dimensions from
>   the same table.

`WITH SYNONYMS [ = ] ( 'synonym' [ , ... ] )`
:   Specifies one or more synonyms for the logical table. Unlike aliases, synonyms are used for informational purposes only. You do
    not use synonyms to refer to the logical table in relationships, dimensions, metrics, and facts.

`COMMENT = 'comment_about_table'`
:   Specifies a comment about the logical table.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Parameters for relationships

These parameters are part of the [syntax for relationships](/sql-reference/sql/create-semantic-view#label-create-semantic-view-syntax-relationship):

`relationship_identifier AS`
:   Specifies an optional identifier for the relationship.

`table_alias ( column_name [ , ... ] )`
:   Specifies one of the logical tables and one or more of its columns that refers to columns in another logical table.

`ref_table_alias [ ( ... ) ]`
:   Specifies the other logical table referred to by the first logical table.

    You can specify one of the following in parentheses, depending on how you want to join the tables:

    `ref_column_name [ , ... ]`
    :   Specifies a column identified with the PRIMARY KEY or UNIQUE constraint in the
        [logical table definition](#label-create-semantic-view-tables).

    `ASOF ref_column_name [ , ... ]`
    :   For an [ASOF join](/user-guide/views-semantic/sql#label-semantic-views-create-relationships-asof), specifies a column of one of
        [the supported types](/sql-reference/constructs/asof-join#label-asof-join-data-types).

        Note

        You can specify at most one ASOF keyword in the definition of a given relationship. You can specify this keyword before any
        column in the list.

    `BETWEEN start_column AND end_column EXCLUSIVE`
    > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
    >
    > Available to all accounts.
    >
    > For a [range join](/user-guide/views-semantic/sql#label-semantic-views-custom-range-joins), specifies the range of possible values in the first table.
    >
    > `start_column` `end_column`
    > :   Specifies the columns that define the start and end of the range.
    >
    >     - You must [define a constraint for these columns](/sql-reference/sql/create-semantic-view#label-create-semantic-view-tables-constraint).
    >     - You cannot use the same column for both `start_column` and `end_column`.
    >
    >       If you want to use the same column, use an [ASOF relationship](/user-guide/views-semantic/sql#label-semantic-views-create-relationships-asof).
    >
    >     Note
    >
    >     `column_name` must have a data type that can be [coerced](/sql-reference/data-type-conversion) to the
    >     data types for `start_column` and `end_column`.

## Parameters for facts, dimensions, and metrics

In a semantic view, you must define at least one dimension or metric, which means that you must specify at least the DIMENSIONS
clause or the METRICS clause.

These parameters are part of the syntax for defining a [fact](/sql-reference/sql/create-semantic-view#label-create-semantic-view-syntax-fact-expression),
[dimension](/sql-reference/sql/create-semantic-view#label-create-semantic-view-syntax-dimension-expression), or
[metric](/sql-reference/sql/create-semantic-view#label-create-semantic-view-syntax-metric-expression):

`{ PRIVATE | PUBLIC }`
:   Specifies whether a fact or metric is [private](/user-guide/views-semantic/sql#label-semantic-views-private) or public. Facts and metrics that are
    marked as private cannot be queried or used in a query condition.

    Note

    You cannot mark a dimension as private. Dimensions are always public. For a dimension, the effect is the same whether you
    specify or omit PUBLIC.

    If you omit PRIVATE and PUBLIC, the dimension, fact, or metric is public by default.

`table_alias.semantic_expression_name`
:   Specifies a name for a dimension, fact, or metric.

`USING ( relationship_name [ , ... ] )`
> [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
>
> Available to all accounts.
>
> For metric definitions, specifies the relationship that should be used to join the tables and calculate the metric, when
> [multiple relationship paths exist between two logical tables](/user-guide/views-semantic/sql#label-semantic-views-create-logical-tables-relations).
>
> To define a [derived metric](/user-guide/views-semantic/sql#label-semantic-views-create-derived-metrics) (a metric that combines multiple metrics from
> different logical tables), omit `table_alias.` from the name.
>
> See [How Snowflake validates semantic views](/user-guide/views-semantic/validation-rules) for the rules for defining a valid semantic view.

`NON ADDITIVE BY ( dimension [ { ASC | DESC } ] [ NULLS { FIRST | LAST } ] [ , ... ] )`
:   Specifies a list of dimensions that should not be used when summing the metric.

    Instead, during query processing, the rows are sorted by the non-additive dimensions, and the values from the last rows
    in the sorted order are aggregated to compute the metric.

    With the default ascending sort order (ASC), the last value is the *latest* value for time-based dimensions. With descending
    sort order (DESC), the last value is the *earliest* value.

    `{ ASC | DESC }`
    :   Optionally sorts the values of the non-additive dimensions in ascending (lowest to highest) or descending (highest to lowest)
        order. The engine always retrieves the **last** value in the sorted order, so ASC returns the latest snapshot and DESC returns
        the earliest snapshot for time-based dimensions.

        Default: ASC

    `NULLS { FIRST | LAST }`
    :   Optionally specifies whether NULL values are sorted before/after non-NULL values, based on the sort order (ASC or DESC). The
        sort order determines what the last snapshot is.

        Default: Depends on the sort order (ASC or DESC); see
        [the usage notes in the ORDER BY documentation](/sql-reference/constructs/order-by#label-order-by-nulls).

    Specifying the NON ADDITIVE BY clause makes the metric a *semi-additive* metric.

    For information, see [Identifying the dimensions that should be non-additive for a metric](/user-guide/views-semantic/sql#label-semantic-views-metrics-semi-additive).

`LABELS = ( FILTER )`
:   Specifies that the fact or dimension can also be used as a filter in the WHERE clause of a query. The SQL expression for the
    fact or dimension must resolve to a BOOLEAN value.

    You can only specify this parameter for facts and dimensions (not for metrics).

    For more information, see [Defining a filter](/user-guide/views-semantic/filters#label-semantic-view-filter-defining).

`AS sql_expr`
:   Specifies the SQL expression for computing the dimension, fact, or metric.

    See [Defining facts, dimensions, and metrics](/user-guide/views-semantic/sql#label-semantic-views-create-facts-dimensions-metrics). For the validation rules for these expressions, see
    [How Snowflake validates semantic views](/user-guide/views-semantic/validation-rules).

`WITH SYNONYMS [ = ] ( 'synonym' [ , ... ] )`
:   Specifies one or more optional synonyms for the dimension, fact, or metric. Note that synonyms are used for informational
    purposes only. You cannot use a synonym to refer to a dimension, fact, or metric in another dimension, fact, or metric.

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`COMMENT = 'comment_about_dim_fact_or_metric'`
:   Specifies an optional comment about the dimension, fact, or metric.

`WITH CORTEX SEARCH SERVICE search_service_name [ USING search_service_column_name ]`
:   Specifies the
    [Cortex Search Service to use for this dimension](/user-guide/views-semantic/sql#label-semantic-views-create-cortex-search-service-dimension).

    You can only specify this parameter for dimensions (and not for facts or metrics).

    If the Cortex Search Service is in a different database or schema,
    [qualify the name of the service](/sql-reference/name-resolution) (for example, `my_db.my_schema.my_service`).

    You can set the optional USING clause to the name of the column in the Cortex Search Service.

## Parameters for window function metrics

These parameters are part of the
[syntax for defining window function metrics](/sql-reference/sql/create-semantic-view#label-create-semantic-view-window-function-syntax):

`metric`
:   Specifies a metric expression for this window function. You can specify a metric or any valid metric expression that you can use
    to define a metric in this entity.

`PARTITION BY ...`
:   Groups rows into partitions. You can either partition by a specified set of expressions or by all dimensions (except selected
    dimensions) specified in the query:

    `PARTITION BY exprs_using_dimensions_or_metrics`
    :   Groups rows into partitions by SQL expressions. In the SQL expression:

        - Any dimensions in the expression must be accessible from the same entity that defines the window function metric.
        - Any metrics must belong to the same table where this metric is being defined.
        - You cannot specify aggregates, window functions, or subqueries.

    `PARTITION BY EXCLUDING dimensions`
    :   Groups rows into partitions by all of the dimensions specified in the [SEMANTIC\_VIEW](/sql-reference/constructs/semantic_view) clause of
        the query, except for the dimensions specified by `dimensions`.

        `dimensions` must only refer to dimensions that are accessible from the entity that defines the window function
        metric.

        For example, suppose that you exclude the dimension `table_1.dimension_1` from partitioning:

        Copy code

        ```
        CREATE SEMANTIC VIEW sv
          ...
          METRICS (
            table_1.metric_2 AS SUM(table_1.metric_1) OVER
              (PARTITION BY EXCLUDING table_1.dimension_1 ORDER BY table_1.dimension_2)
          )
          ...
        ```

        Suppose that you run a query that specifies the dimension `table_1.dimension_1`:

        Copy code

        ```
        SELECT * FROM SEMANTIC VIEW(
          sv
          METRICS (
            table_1.metric_2
          )
          DIMENSIONS (
            table_1.dimension_1,
            table_1.dimension_2,
            table_1.dimension_3
          )
        );
        ```

        In the query, the metric `table_1.metric_2` is evaluated as:

        Copy code

        ```
        SUM(table_1.metric_1) OVER (
          PARTITION BY table_1.dimension_2, table_1.dimension_3
          ORDER BY table_1.dimension_2
        )
        ```

        Note how `table_1.dimension_1` is excluded from the PARTITION BY clause.

        Note

        You cannot use EXCLUDING outside of metric definitions in semantic views. EXCLUDING is not supported in window function
        calls in any other context.

`ORDER BY exprs_using_dimensions_or_metrics [ ASC | DESC ] [ NULLS { FIRST | LAST } ] [, ... ]`
:   Orders rows within each partition. In the SQL expression:

    - Any dimensions in the expression must be accessible from the same entity that defines the window function metric.
    - Any metrics must belong to the same table where this metric is being defined.
    - You cannot specify aggregates, window functions, or subqueries.

`windowFrameClause`
:   See [Window function syntax and usage](/sql-reference/functions-window-syntax).

For additional information about the parameters for window functions and examples, see
[Defining and querying window function metrics](/user-guide/views-semantic/querying#label-semantic-views-querying-window).

## Parameters for verified queries

`verified_query_name`
:   Specifies an identifier for the verified query.

`QUESTION 'question'`
:   Specifies the natural language question that the query answers.

    The question doesn’t need to be a complete sentence or in the form of a question. However, the question should reflect something
    that a user might ask.

`VERIFIED_AT timestamp`
:   Specifies the date and time when the query was verified. For `timestamp`, specify the number of seconds since the
    beginning of the [Unix epoch](https://en.wikipedia.org/wiki/Unix_time) (midnight on January 1, 1970).

`ONBOARDING_QUESTION boolean`
:   If TRUE, specifies that this question will be used as an
    [onboarding question](/user-guide/snowflake-cortex/cortex-analyst/suggested-questions-feature) to help users get started.

    Default: FALSE

`VERIFIED_BY '( purpose = contact )'`
:   Specifies the [contact](/user-guide/contacts-using) who verified the query. For `purpose`, specify one of the
    [predefined purposes](/user-guide/contacts-using#label-contacts-associate-purposes).

`SQL 'verified_query'`
:   Specifies the SQL query that returns the answer for the question.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SEMANTIC VIEW | Schema | Required to create a new semantic view. |
| OWNERSHIP | Semantic view | Required to execute a CREATE OR ALTER statement for an existing semantic view. |
| SELECT | Table, view | Required on any tables and/or views used in the semantic view definition. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The semantic view must be valid and must follow the rules described in
  [How Snowflake validates semantic views](/user-guide/views-semantic/validation-rules).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Variant syntax

### CREATE OR ALTER SEMANTIC VIEW

Creates a semantic view if it doesn’t already exist, or alters an existing semantic view to match the definition in the statement.

The following modifications are supported:

- Adding, removing, or modifying tables, relationships, facts, dimensions, and metrics.
- Adding, overwriting, or removing the comment for the semantic view.
- Modifying the AI\_SQL\_GENERATION and AI\_QUESTION\_CATEGORIZATION instructions.
- Adding, removing, or modifying verified queries.

For more information, see [CREATE OR ALTER SEMANTIC VIEW usage notes](#label-create-or-alter-semantic-view-usage-notes) and [CREATE OR ALTER <object>](/sql-reference/sql/create-or-alter).

Copy code

```
CREATE OR ALTER SEMANTIC VIEW <name>
  TABLES ( logicalTable [ , ... ] )
  [ RELATIONSHIPS ( relationshipDef [ , ... ] ) ]
  [ FACTS ( factExpression [ , ... ] ) ]
  [ DIMENSIONS ( dimensionExpression [ , ... ] ) ]
  [ METRICS ( { metricExpression | windowFunctionMetricExpression } [ , ... ] ) ]
  [ COMMENT = '<comment_about_semantic_view>' ]
  [ MAX_STALENESS = <integer> ]
  [ AI_SQL_GENERATION '<instructions_for_sql_generation>' ]
  [ AI_QUESTION_CATEGORIZATION '<instructions_for_question_categorization>' ]
  [ AI_VERIFIED_QUERIES ( verifiedQuery [ , ... ] ) ]
```

For the definitions of `logicalTable`, `relationshipDef`, `factExpression`, `dimensionExpression`,
`metricExpression`, `windowFunctionMetricExpression`, and `verifiedQuery`, see the
[syntax](#label-create-semantic-view-syntax) for the CREATE SEMANTIC VIEW command.

## CREATE OR ALTER SEMANTIC VIEW usage notes

- All [general usage notes](/sql-reference/sql/create-or-alter#label-create-or-alter-usage-notes) for the CREATE OR ALTER command apply.
- This command doesn’t support adding or changing tags on the semantic view or on tables, facts, dimensions, or metrics within
  the semantic view. Any existing tags are preserved.
- If a previously set property (for example, COMMENT) is absent in the CREATE OR ALTER SEMANTIC VIEW statement, the property
  is unset.
- To execute a CREATE OR ALTER SEMANTIC VIEW statement for an existing semantic view, a role must have the OWNERSHIP privilege
  on the semantic view.

## Examples

See [Creating a semantic view by using the CREATE SEMANTIC VIEW command](/user-guide/views-semantic/sql#label-semantic-views-create).
