# Access a billing usage statement

Snowflake generates a monthly usage statement for customers who have at least one active contract, also known as the Snowflake Order Form.
This statement itemizes usage for the month as expressed in credits consumed and currency spent. It also contains a summary of usage during
the life of the contract.

Snowsight allows you to view and download monthly usage statements, starting with July 2023. To access these statements, either of
the following must be true:

- You have been granted the GLOBALORGADMIN role, and you are in the [organization account](/user-guide/organization-accounts).
- You have been granted the ACCOUNTADMIN and ORGADMIN roles, and you are in an account that has the ORGADMIN role enabled.

Keep the following in mind when accessing usage statements:

- If your organization has multiple contracts, Snowflake generates a separate usage statement for each contract.
- If you renew a contract in the middle of the month, Snowflake generates two separate usage statements for the contract.
- Customers who signed a contract through a Snowflake reseller cannot view or download usage statements.
- You cannot access usage statements from an account in [US SnowGov Regions](/user-guide/intro-regions#label-intro-regions-snowgov-regions) on AWS
  GovCloud and Microsoft Azure Government.

To access a usage statement:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Billing**.
3. On the **Snowflake billing** tab, view or download the usage statement.
