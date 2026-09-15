# Understand schema generation and customization

dbt uses the default macro `generate_schema_name` to decide where a model is built.

By default, it uses your target schema (`target.schema`) specified from your dbt environment or profile. When you execute a dbt project object, dbt attempts to create the target schema specified in [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` if it doesn’t already exist. Snowflake uses `dbt_projects_profiles.yml` when both files are present.

Typically, each developer has their own target schema, for example `analytics_dev`. For larger projects, you can set a custom schema to
group models and specify the schema configuration key in your `dbt_project.yml` file. dbt appends it to the target schema (for example,
`<target_schema>_<custom_schema>`) to keep intermediate and user-facing models separate.

Copy code

```
# Models in models/tasty_bytes/ will be built in the "*_staging" schema
models:
  tasty_bytes:
      +schema: staging
```

A model’s custom schema doesn’t replace the target schema; rather, dbt combines them to avoid collisions. For example, `analytics_dev_staging`.
This is because if dbt ignored the target schema and only used the custom schema (in this case, `staging`), every developer would write to
the same schema and overwrite each other.

If you want different behavior (for example, use only the custom schema, prepend user names, add environment prefixes, etc.), override
`generate_schema_name` in `/macros/` to change how the final schema name is built. For more information and examples, see
[Changing the way dbt generates a schema name](https://docs.getdbt.com/docs/build/custom-schemas#changing-the-way-dbt-generates-a-schema-name) in the dbt documentation.

## Example: Use target name in schema output

Consider a `profiles.yml` with two targets that share the same schema:

Copy code

```
finance_project:
  target: dev
  outputs:
    dev:
      schema: analytics
      ...
    prod:
      schema: analytics
      ...
```

The following `dbt_project.yml` sets a custom schema for all models in `models/analytics/`:

Copy code

```
models:
  analytics:
    +schema: finance
```

With the default `generate_schema_name` macro, all models under `models/analytics/` would be built in the schema `analytics_finance`. This means your project’s folder structure directly determines schema names, which may not suit every team. The following macro overrides this behavior to use the custom schema with a target name suffix instead:

Copy code

```
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set env_suffix = target.name | lower -%}
    {%- set default_schema = target.schema -%}
    {%- if custom_schema_name is none -%}
        {{ default_schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}_{{ env_suffix }}
    {%- endif -%}
{%- endmacro %}
```

With this override, all models under `models/analytics/` are built in `finance_dev` (when running with the `dev` target) or `finance_prod` (when running with the `prod` target).
