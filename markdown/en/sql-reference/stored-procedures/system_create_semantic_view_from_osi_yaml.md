# SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_OSI\_YAML

Preview Feature — Open

Available to all accounts.

Deprecated

This stored procedure is deprecated. Use [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_OSSIE\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_ossie_yaml) instead.

Creates a [semantic view](/user-guide/views-semantic/overview) from a semantic model specification written in
[Open Semantic Interchange (OSI)](https://github.com/apache/ossie) YAML format.

OSI is an open standard for representing semantic models that enables interoperability across AI and BI tools.
This stored procedure accepts an OSI YAML document, converts it to the Snowflake semantic model format, and creates the
corresponding semantic view in the specified schema. If a semantic view with the same name already exists, the procedure
attempts to replace it while preserving existing grants. This has the same effect as running
[CREATE OR REPLACE SEMANTIC VIEW … COPY GRANTS](/sql-reference/sql/create-semantic-view).

See also:
:   [SYSTEM$READ\_OSI\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_osi_yaml_from_semantic_view),
    [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml),
    [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view)

## Syntax

Copy code

```
SYSTEM$CREATE_SEMANTIC_VIEW_FROM_OSI_YAML(
  '<fully_qualified_schema_name>' ,
  '<osi_yaml_specification>'
)
```

## Arguments

`'fully_qualified_schema_name'`
:   [Fully qualified name](/sql-reference/name-resolution) of the schema where you want to create the semantic view,
    in the form `database_name.schema_name`.

    You must qualify the schema name with the database name (for example, `my_db.my_schema`). Otherwise, an error occurs.

`'osi_yaml_specification'`
:   The semantic model definition as a YAML string conforming to the OSI Core Metadata Spec.

    If the specification contains quotes, backslashes, or newlines, you can use a
    [dollar-quoted string constant](/sql-reference/data-types-text#label-dollar-quoted-string-constants) for this argument.

## Returns

On success, returns the following VARCHAR string:

```
Semantic view was successfully created from OSI YAML.
```

If the OSI YAML is invalid, the schema isn’t found, column references can’t be resolved, or any other validation
error occurs, the procedure raises an exception with a descriptive error message.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SEMANTIC VIEW | Schema | Required to create a new semantic view. |
| SELECT | Table, view | Required on any tables or views referenced in `datasets[*].source`. |
| OWNERSHIP | Existing semantic view with the same name. | Required only if a semantic view with that name already exists and needs to be replaced.  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## OSI YAML specification

The top-level fields that Snowflake recognizes in the OSI YAML are:

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Unique identifier for the semantic model. Becomes the semantic view name. |
| `version` | Yes | OSI specification version (for example, `"0.1.1"`). Must be a supported version. |
| `description` | No | Human-readable description of the semantic model. |
| `ai_context` | No | Additional natural-language context for AI tools. Preserved in the view’s extension metadata. |
| `datasets` | No | Logical datasets (tables/views) that underlie the model. See [Dataset fields](#label-osi-dataset-fields). |
| `relationships` | No | Foreign-key relationships between datasets. See [Relationship fields](#label-osi-relationship-fields). |
| `metrics` | No | Model-level aggregate metrics. See [Metric fields](#label-osi-metric-fields). |
| `custom_extensions` | No | Vendor-specific extension metadata. Preserved as-is. |

Expand

Show lessSee more

### Dataset fields

Each entry in `datasets` maps to a table in the Snowflake semantic view.

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Logical dataset name. |
| `source` | No | Fully qualified table/view reference (`db.schema.table`) or a SQL subquery starting with `SELECT` or `WITH`. |
| `primary_key` | No | List of column names forming the primary key (for example, `["order_id"]`). |
| `unique_keys` | No | List of unique key definitions. Each entry is a list of column names. |
| `description` | No | Human-readable description of the dataset. |
| `ai_context` | No | AI-tool context for the dataset. Preserved in extension metadata. |
| `fields` | No | Row-level field definitions. See [Field classification](#label-osi-field-classification). |
| `custom_extensions` | No | Vendor-specific extension metadata. |

Expand

Show lessSee more

### Field classification

Each entry in `datasets[*].fields` is converted to one of three Snowflake column types based on its `dimension` marker:

| OSI field type | Snowflake column type |
| --- | --- |
| `dimension.is_time: true` | `time_dimensions` |
| `dimension` present (non-time) | `dimensions` |
| No `dimension` marker | `facts` |

Expand

Show lessSee more

Each field must specify an expression with at least one supported dialect entry:

Copy code

```
expression:
  dialects:
    - dialect: SNOWFLAKE
      expression: "order_date"
    - dialect: ANSI_SQL
      expression: "order_date"
```

Snowflake prefers the `SNOWFLAKE` dialect. If not present, it falls back to `ANSI_SQL`. Fields that
have no `SNOWFLAKE` or `ANSI_SQL` dialect expression are silently skipped during conversion.

### Relationship fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | No | Identifier for the relationship. |
| `from` | Yes | Dataset on the many side (contains the foreign key). Maps to `left_table`. |
| `to` | Yes | Dataset on the one side (contains the primary/unique key). Maps to `right_table`. |
| `from_columns` | Yes | Foreign key column names in the `from` dataset. |
| `to_columns` | Yes | Corresponding key column names in the `to` dataset. Must be the same length as `from_columns`. |
| `custom_extensions` | No | Vendor-specific extension metadata. |

Expand

Show lessSee more

### Metric fields

| Field | Required | Description |
| --- | --- | --- |
| `name` | Yes | Unique metric identifier. |
| `expression` | Yes | Aggregate expression with dialect support (same structure as field expressions). |
| `description` | No | Human-readable description of the metric. |
| `ai_context` | No | AI-tool context. Preserved in extension metadata. |
| `custom_extensions` | No | Vendor-specific extension metadata. |

Expand

Show lessSee more

Metrics without a `SNOWFLAKE` or `ANSI_SQL` dialect expression are silently skipped.

## Usage notes

- The `version` field in the OSI YAML must be a supported version. Currently supported: `0.1.1`.
  Unsupported versions cause the procedure to raise an error listing the supported values.
- The semantic view name is taken from the `name` field in the OSI YAML. The view is created in the schema
  identified by `fully_qualified_schema_name`.
- Expression dialect priority: `SNOWFLAKE` is used when present; otherwise `ANSI_SQL` is used as a fallback.
  Fields or metrics that have only non-supported dialects are silently omitted from the created view.
- Dataset source values are parsed as follows:
  - A string starting with `SELECT` or `WITH` is treated as an inline subquery and mapped to `base_table.definition`.
  - A dotted identifier such as `sales_db.public.orders` is resolved to `base_table.database` / `schema` / `table`.
  - Unrecognized source strings are ignored (no `base_table` is set).
- OSI metadata not natively represented in Snowflake’s semantic view format (`ai_context`, `custom_extensions`, `version`)
  is preserved in the view’s extension metadata.

If the name of the database or schema is a [double-quoted identifier](/sql-reference/identifiers-syntax#label-delimited-identifier) (for example, if the name
contains spaces), you must include double quotes around the name. For example:

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_OSI_YAML(
  '"my database"."my schema"',
  ...
);
```

## OSI field-to-Snowflake mapping reference

| OSI construct | Snowflake semantic view construct |
| --- | --- |
| `datasets` | `tables` |
| `datasets[*].source` | `tables[*].base_table` (table ref or subquery) |
| `datasets[*].primary_key` | `tables[*].primary_key.columns` |
| `datasets[*].unique_keys` | `tables[*].unique_keys[*].columns` |
| fields with `dimension.is_time: true` | `time_dimensions` |
| fields with `dimension` (non-time) | `dimensions` |
| fields without `dimension` | `facts` |
| `relationships[*].from` | `relationships[*].left_table` |
| `relationships[*].to` | `relationships[*].right_table` |
| `relationships[*].from_columns` / `to_columns` | `relationships[*].relationship_columns[*].left_column` / `right_column` |
| `metrics` | `metrics` (model-level) |
| `ai_context`, `custom_extensions`, `version` | Preserved in extension metadata |

Expand

Show lessSee more

## Examples

### Create a semantic view from a minimal OSI YAML

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_OSI_YAML(
  'my_db.my_schema',
  $$
  version: "0.1.1"
  name: sales_model
  description: "Core sales semantic model"
  datasets:
    - name: orders
      source: my_db.public.orders
      description: "Order fact table"
      primary_key:
        - order_id
      fields:
        - name: order_id
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: order_id
          dimension:
            is_time: false
        - name: order_date
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: order_date
          dimension:
            is_time: true
        - name: total_amount
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: total_amount
  metrics:
    - name: total_revenue
      description: "Sum of all order amounts"
      expression:
        dialects:
          - dialect: SNOWFLAKE
            expression: "SUM(total_amount)"
  $$
);
```

### Create a semantic view with multiple datasets and a relationship

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_OSI_YAML(
  'my_db.my_schema',
  $$
  version: "0.1.1"
  name: ecommerce_model
  description: "E-commerce semantic model with orders and customers"
  datasets:
    - name: orders
      source: my_db.public.orders
      primary_key:
        - order_id
      fields:
        - name: order_id
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: order_id
          dimension:
            is_time: false
        - name: order_date
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: order_date
          dimension:
            is_time: true
        - name: revenue
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: total_amount
    - name: customers
      source: my_db.public.customers
      primary_key:
        - customer_id
      fields:
        - name: customer_id
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: customer_id
          dimension:
            is_time: false
        - name: customer_name
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: "first_name || ' ' || last_name"
          dimension:
            is_time: false
  relationships:
    - name: orders_to_customers
      from: orders
      to: customers
      from_columns:
        - customer_id
      to_columns:
        - customer_id
  metrics:
    - name: total_revenue
      expression:
        dialects:
          - dialect: SNOWFLAKE
            expression: "SUM(total_amount)"
  $$
);
```

### Use a subquery as a dataset source

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_OSI_YAML(
  'my_db.my_schema',
  $$
  version: "0.1.1"
  name: active_orders_model
  datasets:
    - name: active_orders
      source: "SELECT * FROM my_db.public.orders WHERE status = 'active'"
      fields:
        - name: order_id
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: order_id
          dimension:
            is_time: false
  $$
);
```
