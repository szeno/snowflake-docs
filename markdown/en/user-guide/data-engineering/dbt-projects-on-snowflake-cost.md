# Understanding costs for dbt Projects on Snowflake

This topic provides an overview of the costs associated with dbt Projects on Snowflake. For
general information about Snowflake costs, see [Understanding overall cost](/user-guide/cost-understanding-overall).

## Compute costs

Running `EXECUTE DBT PROJECT` uses a virtual warehouse and consumes standard compute credits, the
same as any warehouse workload. The warehouse set in your `profiles.yml` runs the dbt models and is
billed at the standard credit rate for the time it’s active during the execution.

Depending on how you run your project, more than one warehouse can be billed for a single run:

- The warehouse of the outer session that issues the `CREATE DBT PROJECT` or `EXECUTE DBT PROJECT`
  command, such as a [Snowflake task](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution),
  the Snowflake CLI, or an interactive worksheet.
- The warehouse set in your `profiles.yml` that runs the dbt models.

Each of these warehouses is billed for the duration it’s active. To keep costs consolidated and cost
tracking simple, try to ensure that the outer session’s warehouse and the `profiles.yml` warehouse
for production runs are the same. For more information, see [Align your warehouse configuration](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#align-your-warehouse-configuration).

No additional licensing fees and no per-user costs apply to dbt Projects on Snowflake.

To control compute costs, consider:

- Choosing an appropriate warehouse size for your dbt workload. Smaller warehouses cost fewer credits
  per hour, and dbt builds are often not bottlenecked on warehouse size.
- Using [auto-suspend](/user-guide/cost-controlling-controls#use-auto-suspension) on the warehouse so it shuts down immediately after the execution completes.
- Using [Slim CI and defer to production](/user-guide/data-engineering/dbt-projects-on-snowflake-slim-ci-defer-to-prod) to process only changed
  resources and their downstream dependencies while resolving unchanged upstream references against production.

For more information about exploring and controlling compute costs, see [Exploring compute cost](/user-guide/cost-exploring-compute).
