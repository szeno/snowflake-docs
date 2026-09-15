# Snowflake Postgres Cost Evaluation

When you use Snowflake Postgres instances, your account is charged based on three modes of consumption.

- **Instance compute**: Compute charges are based on the [COMPUTE\_FAMILY](/user-guide/snowflake-postgres/postgres-instance-sizes) chosen for each Snowflake Postgres
  instance created in your account and are metered on a credits per hour basis.
- **Instance storage**: Cost for storage depends on the amount of storage allocated across all Snowflake Postgres instances in your
  account. Charges are based on a flat monthly rate per terabyte (TB) per month but are metered on a byte-month basis.
- **Data transfer**: Standard [Snowflake data transfer costs](/user-guide/cost-understanding-data-transfer) apply for all data
  transfer in and out of Snowflake Postgres instances. This includes data replication between Snowflake Postgres primary instances and any
  read replicas they have.

Details on pricing specifics for each mode of consumption can be found in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Monitoring storage consumption for Snowflake Postgres instances

You can view storage usage consumption for Snowflake Postgres instances by querying the [POSTGRES\_STORAGE\_USAGE\_HISTORY view](/sql-reference/account-usage/postgres_storage_usage_history).

## Monitoring compute consumption for Snowflake Postgres instances

You can view the total compute usage for Snowflake Postgres instances by querying the following views:

- You can query the [POSTGRES\_COMPUTE\_USAGE\_HISTORY view](/sql-reference/account-usage/postgres_compute_usage_history) to see the hourly credit usage across all
  Snowflake Postgres instances for an account within the last 365 days (1 year).
- You can query the [METERING\_HISTORY view](/sql-reference/account-usage/metering_history) and specify `service_type IN ('POSTGRES_COMPUTE', 'POSTGRES_COMPUTE_HA')`
  in the WHERE clause to see the hourly credit usage across all Snowflake Postgres instances for an account within the last 365 days (1 year).
- You can query the [METERING\_DAILY\_HISTORY view](/sql-reference/account-usage/metering_daily_history) and specify `service_type IN ('POSTGRES_COMPUTE', 'POSTGRES_COMPUTE_HA')`
  in the WHERE clause to see the daily credit usage across all Snowflake Postgres instances for an account within the last 365 days (1 year).
