# YAML vs DDL authoring for semantic views

Semantic views can be authored in three ways: using SQL DDL statements, using a YAML specification, or using the
Snowsight wizard. This page compares the DDL and YAML approaches to help you choose the right one for your workflow.
For information about the Snowsight wizard, see [Semantic View Autopilot](/user-guide/views-semantic/autopilot).

YAML and DDL have near-complete feature parity. Both formats produce the same semantic view object in
Snowflake. YAML includes a few features not in DDL (such as `time_dimensions` and standalone
`filters`). DDL includes a few features not available in YAML (such as cross-table dimension
references). See the [feature comparison](#feature-comparison) for a complete mapping.

## When to use DDL

DDL (SQL) is a good choice when:

- Your team primarily works in SQL and is comfortable with SQL syntax.
- You’re deploying semantic views through [dbt](https://hub.getdbt.com/Snowflake-Labs/dbt_semantic_view/latest/) or [Terraform](https://registry.terraform.io/providers/snowflakedb/snowflake/latest/docs/resources/semantic_view), both of which use DDL syntax.
- You need programmatic creation through JDBC, ODBC, or the [SQL API](/developer-guide/sql-api/index).

For the full DDL syntax reference, see [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view). For step-by-step
instructions and examples, see [Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql).

## When to use YAML

YAML is a good choice when:

- You prefer a concise, readable format for defining complex semantic views with many tables and columns.
- You’re migrating from existing stage-based semantic models that are already in YAML format.
- Your CI/CD pipeline is built around YAML configuration files.
- You want a format that’s easy to review in pull requests and diffs.

For the full YAML specification, see [YAML specification for semantic views](/user-guide/views-semantic/semantic-view-yaml-spec).

## Feature comparison

The following table provides a comprehensive mapping of every modeling feature across YAML and DDL.
Both formats produce the same semantic view object. Where syntax differs, the table notes the
YAML and DDL conventions.

| Feature | YAML | DDL | Notes |
| --- | --- | --- | --- |
| Tables with primary keys | Yes (`primary_key.columns`) | Yes (`PRIMARY KEY (...)`) | YAML uses a structured object; DDL uses a clause on the table definition. |
| SQL query as a logical table | Yes (`base_table.definition: <sql_query>`) | Yes (`<alias> AS ( <query> )`) | Both support using a SQL query instead of a physical table. See [Using a SQL query as a logical table](/user-guide/views-semantic/inline-view). |
| Unique keys | Yes (`unique_keys`) | Yes (`UNIQUE (...)`) | Both support composite unique keys at the table level. |
| Dimensions (direct and computed) | Yes | Yes | YAML uses `expr`; DDL uses `AS <sql_expr>`. DDL infers data types from expressions. |
| Time dimensions | Yes (`time_dimensions`) | No (use `DIMENSIONS`) | **YAML only.** A separate category for date/timestamp columns. DDL declares them as regular dimensions. |
| Facts | Yes | Yes | Both support direct column references, computed expressions, and aggregate expressions (pre-aggregated facts). |
| Metrics (table-scoped) | Yes | Yes (`<table>.<metric> AS <agg_expr>`) | Equivalent. |
| Derived metrics (view-scoped) | Yes (model-level `metrics`) | Yes (no table prefix in `METRICS`) | Both support entity-scoped and cross-entity derived metrics. |
| Window function metrics | Yes (in `expr`) | Yes (full syntax with `PARTITION BY EXCLUDING`) | Both support window functions in metric expressions. DDL has explicit `PARTITION BY EXCLUDING` syntax. |
| Semi-additive metrics | Yes (`non_additive_dimensions`) | Yes (`NON ADDITIVE BY (...)`) | YAML uses `ascending`/`descending`; DDL uses `ASC`/`DESC`. DDL also supports `NON ADDITIVE ALIGNED BY`. |
| Window functions in dimensions/facts | Yes (in `expr`) | Yes | Both support `ROW_NUMBER`, `DENSE_RANK`, `LAG`, `LEAD`, and other window functions. |
| Descriptions / Comments | Yes (`description`) | Yes (`COMMENT = '...'`) | Different field names, same purpose. Supported at every level (view, table, dimension, fact, metric). |
| Synonyms | Yes (`synonyms`) | Yes (`WITH SYNONYMS = (...)`) | Supported on tables, dimensions, facts, and metrics in both formats. |
| Sample values | Yes (`sample_values`) | Yes (`SAMPLE_VALUES (...)`) | Supported in both. Helps Cortex Analyst understand the range of values for a column. |
| `is_enum` | Yes (`is_enum: true`) | Yes (`IS_ENUM`) | Indicates the sample values represent the complete set of possible values. Valid on dimensions only. |
| Filters (standalone) | Yes (`filters`) | No | **YAML only.** Standalone filter expressions at the table level. Used by Cortex Analyst but not used by the semantic SQL compiler. |
| Filters (entity-level) | Yes (`labels: [filter]`) | Yes (`LABELS = (FILTER)`) | Recommended approach in both formats. Attach filter behavior to a dimension or fact. |
| Cortex Search Service | Yes (`cortex_search_service`) | Yes (`WITH CORTEX SEARCH SERVICE`) | YAML uses structured sub-fields (`service`, `literal_column`, `database`, `schema`); DDL uses a qualified name. |
| Verified queries | Yes (`verified_queries`) | Yes (`AI_VERIFIED_QUERIES (...)`) | `verified_by` is a free-text string in both formats. |
| Custom instructions | Yes (`module_custom_instructions`) | Yes (`AI_SQL_GENERATION`, `AI_QUESTION_CATEGORIZATION`) | Both support SQL generation and question categorization instructions. YAML also supports the legacy `custom_instructions` field. |
| Relationships (basic) | Yes | Yes | Both support named and unnamed relationships, single-column and multi-column joins. |
| One-to-one relationships | Yes | Yes | Inferred automatically when both sides have the join column as a primary key. |
| ASOF relationships | Yes (`type: asof`) | Yes (`ASOF <column>`) | Both support point-in-time lookups for slowly changing dimensions. |
| Range relationships | Yes (`type: range`, `right_range`) | Yes (`BETWEEN <start> AND <end> EXCLUSIVE`) | Both support range-based joins with `CONSTRAINT DISTINCT RANGE` on the target table. |
| Many-to-many (through bridge table) | Yes | Yes | Expressed through two relationships from a bridge table. The system infers the M2M path. |
| Role-playing tables | Yes (multiple `name` entries with same `base_table`) | Yes (multiple aliases: `alias1 AS table`, `alias2 AS table`) | Both support aliasing a single physical table for different roles. |
| Cross-table dimension references | No | Yes (`<table>.<dim> AS <other_table>.<dim>`) | **DDL only.** A dimension on one table can reference a dimension from a related table. |
| Metrics using specific relationship | Yes (`using_relationships`) | Yes (`USING (<relationship>)`) | Both support specifying which relationship path a metric should use. |
| Access modifiers (PUBLIC / PRIVATE) | Yes (`access_modifier`) | Yes (`PUBLIC` / `PRIVATE` keyword) | Supported on facts, metrics, and derived metrics. Dimensions are always public. |
| Variables | Yes (`variables`) | Yes (`VARIABLES (...)`) | Both support parameterized semantic views with typed variables and default values. |
| Object tagging | Yes (`tags`) | Yes (`[ WITH ] TAG (...)`) | Supported on views, tables, dimensions, facts, and metrics. |
| `data_type` | Yes (set in YAML, inferred on read) | No | **YAML only.** You can set `data_type` in YAML, but the value returned on the read path is what the compiler infers. DDL always infers types. |
| `OR REPLACE` / `IF NOT EXISTS` | No | Yes | **DDL only.** Standard object creation modifiers. |
| `COPY GRANTS` | Always applied (not configurable) | Yes (opt-in clause) | YAML always preserves grants when replacing a view. DDL requires the explicit `COPY GRANTS` clause. |

Expand

Show lessSee more

## Converting between formats

You can convert between DDL and YAML at any time:

- **YAML to semantic view**: Use the
  [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml)
  stored procedure. You can pass `TRUE` as the third argument to validate the YAML without creating the view.
- **Apache Ossie (incubating) YAML to semantic view**: Use the
  [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_OSSIE\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_ossie_yaml)
  stored procedure to create a semantic view from an [Apache Ossie (incubating)](https://github.com/apache/ossie) YAML document.
- **Semantic view to YAML**: Use the
  [SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_yaml_from_semantic_view)
  function to export any existing semantic view to YAML.
- **Semantic view to Apache Ossie (incubating) YAML**: Use the
  [SYSTEM$READ\_OSSIE\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_ossie_yaml_from_semantic_view)
  function to export any existing semantic view to Ossie YAML format.
- **Semantic view to DDL**: Use the
  [GET\_DDL](/sql-reference/functions/get_ddl) function to export the SQL definition of an existing semantic view.

These stored procedures and functions support round-tripping between formats, which is useful for version control, CI/CD pipelines,
and migrating definitions between environments.
