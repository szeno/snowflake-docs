Categories:
:   [System functions](/sql-reference/functions-system) (Information)

# SYSTEM$READ\_OSSIE\_YAML\_FROM\_SEMANTIC\_VIEW

Preview Feature — Open

Available to all accounts.

Reads an existing [semantic view](/user-guide/views-semantic/overview) and returns its definition as an
[Apache Ossie (incubating)](https://github.com/apache/ossie) YAML document.

Apache Ossie (incubating) is an open standard for representing semantic models that enables interoperability across AI and BI tools.
This function converts the semantic view’s internal representation to Ossie format and returns the resulting YAML string.
Snowflake-specific features that have no Ossie equivalent are preserved in vendor custom extensions so they survive a
round-trip through external tools.

See also:
:   [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_OSSIE\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_ossie_yaml) ,
    [SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_yaml_from_semantic_view)

## Syntax

Copy code

```
SYSTEM$READ_OSSIE_YAML_FROM_SEMANTIC_VIEW( '<fully_qualified_semantic_view_name>' )
```

## Arguments

`'fully_qualified_semantic_view_name'`
:   The fully qualified name of an existing semantic view, in the form `database_name.schema_name.semantic_view_name`.

    If any part of the name contains special characters (spaces, mixed case), wrap each part in double quotes inside
    the single-quoted argument string. For example: `'"my database"."my schema"."My Model"'`.

## Returns

On success, returns a VARCHAR containing the Ossie YAML document in the standard document wrapper format:

Copy code

```
version: "0.1.1"
semantic_model:
  - name: <model_name>
    ...
```

If the semantic view doesn’t exist or the calling role lacks privileges, the function raises an exception with a
descriptive error message.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this SQL command must have at least one of the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| SELECT or USAGE | Semantic view | Required to read the semantic view definition. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Snowflake-to-Ossie mapping reference

| Snowflake semantic view construct | Ossie construct | Notes |
| --- | --- | --- |
| `tables` | `datasets` | Each table becomes a dataset. |
| `tables[*].base_table` (table ref) | `datasets[*].source` | Reconstructed as `db.schema.table` dotted name. |
| `tables[*].base_table` (subquery) | `datasets[*].source` | Returned as the raw SQL definition string. |
| `tables[*].primary_key.columns` | `datasets[*].primary_key` | List of column names. |
| `tables[*].unique_keys[*].columns` | `datasets[*].unique_keys` | List of lists of column names. |
| `dimensions` | fields with `dimension` (`is_time: false`) | Dimension marker added, `is_time` defaults to `false`. |
| `time_dimensions` | fields with `dimension.is_time: true` | Dimension marker added with `is_time` set to `true`. |
| `facts` | fields without `dimension` | No dimension marker on the field. |
| `metrics` (model-level) | `metrics` | Preserved at the top level of the semantic model. |
| relationships (EQUI only) | `relationships` | Only equi-join relationships are exported. |
| Extension metadata (`version`, `ai_context`, `custom_extensions`) | Restored to top-level Ossie fields | Round-tripped from the write path’s stored extension properties. |

Expand

Show lessSee more

### Field expression handling

Every field and metric expression is emitted with a single `SNOWFLAKE` dialect entry:

Copy code

```
expression:
  dialects:
    - dialect: SNOWFLAKE
      expression: "<sql_expression>"
```

If the view was originally created from Ossie YAML that included an `ANSI_SQL` dialect, only the `SNOWFLAKE` expression
is returned (since Snowflake stores a single resolved expression internally).

### Snowflake-specific data in custom\_extensions

Snowflake features that have no direct Ossie representation are serialized into a `SNOWFLAKE` vendor custom extension
at the appropriate level. External tools can ignore these extensions or pass them through unchanged.

**Model-level SNOWFLAKE extension:**

| Field | Included when |
| --- | --- |
| `max_staleness` | Model has a staleness policy. |
| `custom_instructions` | Model has AI instructions. |
| `module_custom_instructions` | Model has module-level instructions. |
| `variables` | Model defines variables. |
| `verified_queries` | Model has verified query examples. |
| `tags` | Model has tags. |

Expand

Show lessSee more

**Dataset-level SNOWFLAKE extension:**

| Field | Included when |
| --- | --- |
| `synonyms` | Dataset has synonym names. |
| `metrics` | Dataset has table-level metrics (not representable as Ossie global metrics). |
| `filters` | Dataset has table-level filters. |
| `tags` | Dataset has tags. |
| `constraints` | Dataset has constraint definitions. |

Expand

Show lessSee more

**Field-level SNOWFLAKE extension:**

| Field | Applies to | Included when |
| --- | --- | --- |
| `synonyms` | Dimensions | Field has synonym names. |
| `tags` | Dimensions | Field has tags. |
| `sample_values` | Dimensions, TimeDimensions, Facts | Field has sample values. |
| `cortex_search_service` | Dimensions | Field is backed by a Cortex Search service. |
| `is_enum` | Dimensions | Field is marked as an enumeration. |
| `access_modifier` | Facts | Field has a non-default access modifier. |

Expand

Show lessSee more

**Metric-level SNOWFLAKE extension:**

| Field | Included when |
| --- | --- |
| `synonyms` | Metric has synonym names. |
| `access_modifier` | Metric has a non-default access modifier. |
| `non_additive_dimensions` | Metric specifies non-additive dimensions. |
| `additive_dimensions` | Metric specifies additive dimensions. |
| `using_relationships` | Metric declares relationship usage. |
| `tags` | Metric has tags. |

Expand

Show lessSee more

## What is converted faithfully

The following survive a full round-trip (write Ossie YAML then read it back):

- Model name, description, and version
- Dataset names, descriptions, sources (qualified names and subqueries)
- Primary keys and unique keys
- All field names, descriptions, and expressions
- Field classification (dimension vs. time\_dimension vs. fact)
- Equi-join relationships (name, from/to tables, column mappings)
- Model-level metrics (name, description, expression)
- `ai_context` at model, dataset, and field levels
- `custom_extensions` from any vendor (DBT, SALESFORCE, DATABRICKS, COMMON, SNOWFLAKE)

## What is lost or not converted

| Ossie concept / Snowflake feature | Behavior | Reason |
| --- | --- | --- |
| Non-EQUI relationships (ASOF, RANGE) | Silently dropped from output. | Ossie spec only defines equi-join semantics. |
| Field labels | Lost on round-trip. | The write path doesn’t persist the label property. |
| Data types | Not included in output. | By design, Ossie fields carry expressions, not storage types. |
| Multi-dialect expressions | Only `SNOWFLAKE` dialect returned. | Snowflake stores a single resolved expression. |
| Table-level metrics | Moved to dataset `custom_extensions`. | Ossie only supports model-level metrics. |
| Table-level filters | Moved to dataset `custom_extensions`. | No Ossie equivalent. Preserved for round-trip via extension. |

Expand

Show lessSee more

## Usage notes

- The output always uses the document wrapper format (top-level `version` + `semantic_model` array with one entry),
  regardless of whether the view was created from the flat or wrapper format.
- Semantic views created by any method (native YAML, DDL, or Ossie YAML) can be exported with this function.
  Snowflake-specific features appear in the `SNOWFLAKE` vendor extension.
- Null fields are omitted from the output YAML (no empty keys cluttering the document).
- The output `version` field is determined as follows:
  - If the semantic view was originally created from Ossie YAML, the version stored in extension metadata is used.
  - If the semantic view was created through native YAML or SQL (no stored Ossie version), the default version `"0.1.1"` is used.

If the name of the database, schema, or view is a [double-quoted identifier](/sql-reference/identifiers-syntax#label-delimited-identifier) (for example, if
the name contains spaces), you must include double quotes around the name. For example:

Copy code

```
SELECT SYSTEM$READ_OSSIE_YAML_FROM_SEMANTIC_VIEW(
  '"my database"."my schema"."My Model"'
);
```

## Examples

### Read a semantic view as Ossie YAML

Copy code

```
SELECT SYSTEM$READ_OSSIE_YAML_FROM_SEMANTIC_VIEW(
  'my_db.my_schema.sales_model'
);
```

Returns:

Copy code

```
version: "0.1.1"
semantic_model:
  - name: sales_model
    description: "Core sales semantic model"
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
```

### Read a view that has Snowflake-specific features

Copy code

```
SELECT SYSTEM$READ_OSSIE_YAML_FROM_SEMANTIC_VIEW(
  'analytics_db.public.customer_model'
);
```

Returns (Snowflake-specific features appear in `custom_extensions`):

Copy code

```
version: "0.1.1"
semantic_model:
  - name: customer_model
    custom_extensions:
      - vendor: SNOWFLAKE
        content: '{"custom_instructions":"Answer in metric units"}'
    datasets:
      - name: customers
        source: analytics_db.public.customers
        fields:
          - name: region
            expression:
              dialects:
                - dialect: SNOWFLAKE
                  expression: region
            dimension:
              is_time: false
            custom_extensions:
              - vendor: SNOWFLAKE
                content: '{"synonyms":["area","territory"],"is_enum":true}'
```

### Round-trip example: write then read

Copy code

```
-- Write an Ossie model
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_OSSIE_YAML(
  'my_db.my_schema',
  $$
  version: "0.1.1"
  name: round_trip_model
  datasets:
    - name: sales
      source: my_db.public.sales
      primary_key:
        - sale_id
      fields:
        - name: sale_id
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: sale_id
          dimension:
            is_time: false
        - name: sale_date
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: sale_date
          dimension:
            is_time: true
        - name: amount
          expression:
            dialects:
              - dialect: SNOWFLAKE
                expression: amount
  $$
);

-- Read it back as Ossie YAML
SELECT SYSTEM$READ_OSSIE_YAML_FROM_SEMANTIC_VIEW(
  'my_db.my_schema.round_trip_model'
);
```
