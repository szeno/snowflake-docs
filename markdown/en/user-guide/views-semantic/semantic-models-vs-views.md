# Migrating from the legacy stage API to semantic views

Before semantic views were introduced, the only way to define business semantics for Cortex Analyst was to
upload a YAML file to a Snowflake stage (the “stage API”). Semantic views are native schema-level objects that
replace this workflow.

Important

Snowflake recommends using semantic views for all new implementations. If you have existing YAML files on stages
that you use with the legacy stage API, they continue to work with Cortex Analyst. However, they don’t support
the direct SQL query interface, native sharing, or other features available with semantic views.

## Key differences from the legacy stage API

Semantic views (whether authored in DDL or YAML) provide the following capabilities that the legacy
stage-based approach does not:

- **Direct SQL querying**: Query business metrics directly using
  [SELECT … FROM SEMANTIC\_VIEW(…)](/user-guide/views-semantic/querying). The legacy stage API only
  works as context for Cortex Analyst to generate SQL.
- **Native Snowflake integration**: Semantic views are schema-level objects managed with standard SQL commands
  (SHOW, DESCRIBE, GRANT, REVOKE). Stage-based YAML files require reading from and writing to a stage.
- **Granular security**: Semantic views use role-based access control. The legacy approach only offers
  coarse-grained access through stage permissions.
- **Sharing and Marketplace**: Semantic views can be shared natively through Snowflake sharing, the Snowflake Marketplace,
  and listings.
- **Governance and observability**: Semantic views appear in Information Schema and Account Usage views,
  providing usage tracking and auditing.

## Migrating from stage-based YAML

If you have existing YAML files on stages, you can convert them to semantic views using
the [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml) stored
procedure. To export a semantic view back to YAML format, use
the [SYSTEM$READ\_YAML\_FROM\_SEMANTIC\_VIEW](/sql-reference/functions/system_read_yaml_from_semantic_view) function.

When converting from a stage-based YAML file to a semantic view:

1. Consider using derived metrics for view-level calculations.
2. Add `access_modifier` to facts and metrics you want to make private.
3. Move custom instructions from the YAML file to the `AI_SQL_GENERATION` and `AI_QUESTION_CATEGORIZATION`
   parameters on the semantic view.

Note

You must convert YAML files one at a time using the stored procedure. If you need bulk conversion or integration
into a CI/CD pipeline, you can script the conversions to run in sequence.

For guidance on setting up roles, privileges, and deployment pipelines for semantic views, see
[Best practices for developing and deploying semantic views](/user-guide/views-semantic/best-practices-dev).
