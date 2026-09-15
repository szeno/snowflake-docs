Schema:
:   [BILLING](/sql-reference/billing)

# COLLABORATION\_REBATE\_CONTRIBUTION view

The COLLABORATION\_REBATE\_CONTRIBUTION view in the BILLING schema shows how each consuming customer contributes to a provider organization’s monthly collaboration rebate.

## Access

| Requirement | Details |
| --- | --- |
| Database | `SNOWFLAKE` |
| Schema | `BILLING` |
| Database role | `SNOWFLAKE.ORGANIZATION_BILLING_VIEWER` |

Expand

Show lessSee more

Access requires the `ORGANIZATION_BILLING_VIEWER` database role on the `SNOWFLAKE` shared database.

Copy code

```
-- Grant the database role to a user role
GRANT DATABASE ROLE SNOWFLAKE.ORGANIZATION_BILLING_VIEWER TO ROLE <role_name>;

-- Query the view
USE ROLE <role_name>;
SELECT * FROM SNOWFLAKE.BILLING.COLLABORATION_REBATE_CONTRIBUTION LIMIT 10;
```

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| PROVIDER\_ORGANIZATION\_NAME | VARCHAR | Name of the data provider’s Snowflake organization. |
| PROVIDER\_ACCOUNT\_LOCATOR | VARCHAR | Unique identifier (locator) for the provider’s Snowflake account whose shared data was consumed. |
| PROVIDER\_ACCOUNT\_NAME | VARCHAR | Human-readable alias of the provider’s Snowflake account, as shown in Snowsight. |
| CUSTOMER\_NAME | VARCHAR | Name of the consuming customer whose compute on the provider’s shared data contributed to the rebate. |
| REBATE\_CONTRIBUTION\_PCT | NUMBER | Percentage of the provider organization’s total monthly collaboration rebate attributable to this consumer’s usage of the provider’s shared data. |
| REBATE\_DATE | DATE | Date on which the rebate credit is applied (UTC). For a provider account that is active at month end, this is the last day of the rebate month. For an account whose contract terminated within the month, this is the contract’s termination date. If an account transitions between contracts mid-month, two rows appear: one with the termination date of the old contract and one with the last day of the rebate month for the new contract. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours after month close (typically on the 3rd or 4th day of the next month).
