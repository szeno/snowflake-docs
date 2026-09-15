# <budget\_name>!GET\_SPENDING\_HISTORY

View the spending history for a [budget](/user-guide/budgets).

See also:
:   [<budget\_name>!GET\_SERVICE\_TYPE\_USAGE](/sql-reference/classes/budget/methods/get_service_type_usage)

## Syntax

Copy code

```
<budget_name>!GET_SPENDING_HISTORY( [ TIME_LOWER_BOUND => <constant_expr> ,
                                      TIME_UPPER_BOUND => <constant_expr> ] )
```

## Optional arguments

`TIME_LOWER_BOUND => constant_expr,` `TIME_UPPER_BOUND => constant_expr`
:   Time range (in UTC timestamp format) during which the spending occurred.

    You must set both lower and upper time bounds to limit the results by a time range.

## Returns

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| MEASUREMENT\_DATE | DATE | Date when the usage occurred. |
| SERVICE\_TYPE | VARCHAR | [Type of service](/user-guide/budgets#label-budgets-supported-serverless-features) that is consuming credits, which can be one of the following:   - `AUTO_CLUSTERING` - `DATA_QUALITY_MONITORING` - `HYBRID_TABLE_REQUESTS` - `MATERIALIZED_VIEW` - `PIPE` - `QUERY_ACCELERATION` - `SEARCH_OPTIMIZATION` - `SERVERLESS_ALERTS` - `SERVERLESS_TASK` - `SNOWPIPE_STREAMING` - `WAREHOUSE_METERING` - `WAREHOUSE_METERING_READER` |
| CREDITS\_SPENT | FLOAT | Number of credits used. |

Expand

Show lessSee more

## Access control requirements

- The following minimum privileges and roles are required to view results for *custom budgets*:

  - Any [instance role](/user-guide/budgets#label-budgets-instance-roles) for the budget instance.
  - USAGE privilege on the database and schema that contains the budget instance.
  - [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER.
- The following role is required to view results for the *account budget*:

  - Any [application role](/user-guide/budgets#label-budgets-application-roles) for the account budget.
  - [Snowflake database role](/sql-reference/snowflake-db-roles) USAGE\_VIEWER.

For more information, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

View the spending history for budget `my_budget` in schema `budget_db.budget_schema`:

Copy code

```
CALL budget_db.budget_schema.my_budget!GET_SPENDING_HISTORY();
```

View the spending history for the last 7 days for the account budget:

Copy code

```
CALL snowflake.local.account_root_budget!GET_SPENDING_HISTORY(
  TIME_LOWER_BOUND=>dateadd('days', -7, current_timestamp()),
  TIME_UPPER_BOUND=>current_timestamp()
);
```
