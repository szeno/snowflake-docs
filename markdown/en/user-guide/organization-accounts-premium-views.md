# Premium views in the organization account

The [ORGANIZATION\_USAGE schema](/sql-reference/organization-usage) contains views that provide organization-level data. The
ORGANIZATION\_USAGE schema in the [organization account](/user-guide/organization-accounts)
contains views that are not available in the ORGANIZATION\_USAGE schema of a regular account. These views are considered *premium views*
because they aggregate usage and object data from all accounts into a single view that is not otherwise available, and therefore incur
additional costs.

Premium views correspond to views in the ACCOUNT\_USAGE schema, but provide organization-level data rather than account-level data. For
example, someone could query the TAG\_REFERENCES view in the ACCOUNT\_USAGE schema to learn about how tags are used in a specific account, but
someone could query the TAG\_REFERENCES view in the ORGANIZATION\_USAGE schema of the organization account to learn how tags are used
throughout the organization.

For a list of premium views, see [Organization Usage](/sql-reference/organization-usage).

Note

It can take two weeks from the time the organization account is created until premium views are fully populated with 365 days of
historical data from accounts.

## Costs associated with premium views

Premium views incur additional costs based on how many records were processed to generate the views. For the current rate for premium views, find the Organization Usage table in the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).

## Grant access to the premium views

For information about granting access to premium views, see [Access schema in the organization account](/sql-reference/organization-usage#label-org-usage-access-org-account).

## Organizations without a capacity contract

By default, premium views are only available in organizations that have a capacity contract. If you have on demand accounts and want to
access premium views, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Effect on views in the ACCOUNT\_USAGE schema

Snowflake uses the hidden schema `snowflake.organization_usage_local` to store internal objects used in conjunction with premium views.
These objects might be visible in the ACCOUNT\_USAGE views in the organization account. Because these objects are internal, they might
change without notice in the future.
