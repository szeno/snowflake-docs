# <budget\_name>!GET\_SERVICE\_TYPE\_USAGE\_V2

View the credit usage for a [budget](/user-guide/budgets) by service type.

## Syntax

Copy code

```
<budget_name>!GET_SERVICE_TYPE_USAGE_V2( '<start_month>' , '<end_month>' )
```

## Arguments

`'start_month'`
:   Specifies the start of the time period for which you want to return usage information. Specified in the format `YYYY-MM`.

`'end_month'`
:   Specifies the end of the time period for which you want to return usage information. Specified in the format `YYYY-MM`.

## Returns

The function returns the following columns:

| Column Name | Data Type | Description |
| --- | --- | --- |
| SERVICE\_TYPE | VARCHAR | Lists the [service](/user-guide/budgets#label-budgets-supported-serverless-features) that used credits. |
| ENTITY\_TYPE | VARCHAR | Type of object associated with the credit consumption. All table-like objects such as tables, views, materialized views, and external tables have a value of `TABLE`. |
| ENTITY\_ID | NUMBER | Internal identifier for the object in the budget. |
| NAME | VARCHAR | Name of the object associated with the credit consumption. |
| CREDITS\_USED | FLOAT | Number of credits used. This is the sum of CREDITS\_COMPUTE and CREDITS\_CLOUD. |
| CREDITS\_COMPUTE | FLOAT | Number of compute credits used. |
| CREDITS\_CLOUD | FLOAT | Number of cloud service credits used. |

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

## Example

Return credits consumed by objects associated with the budget `my_budget` in January, February, and March of 2025:

Copy code

```
CALL db.sch1.my_budget!GET_SERVICE_TYPE_USAGE_V2('2025-01', '2025-03');
```
