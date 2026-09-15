# <budget\_name>!GET\_MEASUREMENT\_TABLE

View the credit usage data collected by the [budget](/user-guide/budgets) maintenance task. For more
information, see [Understand budget costs](/user-guide/budgets/cost).

## Syntax

Copy code

```
<budget_name>!GET_MEASUREMENT_TABLE()
```

## Access control requirements

- The following minimum privileges and roles are required to view results for *custom budgets*:

  - Any [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contains the budget instance.
  - [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER.
- The following role is required to view results for the *account budget*:

  Any [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Returns

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| MEASUREMENT\_TIME | NUMBER | UTC timestamp when the measurement was taken. |
| SERVICE\_TYPE | VARCHAR | [Type of service](/user-guide/budgets#label-budgets-supported-serverless-features) that is consuming credits, which can be one of the following:   - `AUTO_CLUSTERING` - `DATA_QUALITY_MONITORING` - `HYBRID_TABLE_REQUESTS` - `MATERIALIZED_VIEW` - `PIPE` - `QUERY_ACCELERATION` - `SEARCH_OPTIMIZATION` - `SERVERLESS_ALERTS` - `SERVERLESS_TASK` - `SNOWPIPE_STREAMING` - `WAREHOUSE_METERING` - `WAREHOUSE_METERING_READER` |
| CREDITS\_SPENT | NUMBER | Number of credits spent. |
| UPDATED\_TIME | NUMBER | UTC timestamp when the measurement was updated. |

Expand

Show lessSee more

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

View the credit usage data collected for budget `my_budget` in schema `budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_MEASUREMENT_TABLE();
```

View the credit usage data collected for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!GET_MEASUREMENT_TABLE();
```
