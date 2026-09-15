# Code Conversion - dbt Conversion Issues

This page provides a reference for the conversion issues reported when dbt models are processed. For each issue you will find its severity, a description of when it is generated, a code example, and recommendations.

## SSC-EWI-DBT0001

dbt model contains Jinja constructs that SnowConvert cannot migrate.

### Severity

Critical

#### Description

dbt models are Jinja-templated SQL. Before conversion, each model is scanned for the Jinja constructs it contains: `{{ ref(...) }}` and `{{ source(...) }}` are supported and are tokenized so the surrounding SQL can be parsed and converted, and several block constructs — such as `{{ config(...) }}`, `{% if %}`, and `{% for %}` — are replaced with placeholders and restored afterwards.

When a model uses a construct outside that supported set, or when the Jinja cannot be parsed at all, the model is not converted. It is written to the output with its original contents preserved verbatim and a single header carrying this issue prepended at the top of the file. The header is added once per file regardless of how many unsupported constructs it contains.

#### Code Example

##### Input Code:

##### dbt

Copy code

```
SELECT * FROM {{ ref('stg_orders') }}
{% include 'order_filters.sql' %}
```

##### Output Code:

##### Snowflake

Copy code

```
!!!RESOLVE EWI!!! /*** SSC-EWI-DBT0001 - This dbt model could not be processed because it contains unsupported jinja constructs. ***/!!!
SELECT * FROM {{ ref('stg_orders') }}
{% include 'order_filters.sql' %}
```

#### Best Practices

1. **Check the header for a parse error.** When the model uses only `ref` and `source` but the template is malformed, the header reports the parse error instead of the generic message. Fixing the syntax — an unclosed `{{ ... }}`, for example — is usually enough to make the model convertible.
2. **Reduce the model to supported constructs.** Replacing an unsupported construct with plain SQL, or moving it into a macro that the model no longer needs at parse time, lets the rest of the file be converted normally.
3. **Convert the compiled SQL instead.** For models whose logic genuinely depends on unsupported templating, run `dbt compile` and convert the resulting SQL, then reapply the templating to the converted statement.
