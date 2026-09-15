# November 11, 2024 — Snowflake Native App Framework release notes

Snowflake is pleased to announce the availability of the following new features and enhancements.

## Snowflake Native Apps with Snowpark Container Services in AWS — *General availability*

Snowflake Native App with Snowpark Container Services is now generally available on Amazon Web Services (AWS). Snowflake Native Apps built using containers can be
distributed to any Snowflake customer who can use them in production AWS commercial regions. Apps with containers
provide all of the functionality of Snowpark Container Services, including compute pools, services, jobs, external
access integrations, etc. within a Snowflake Native App.

## Snowflake Native Apps with Snowpark Container Services in Azure — *Preview*

Snowflake Native App with Snowpark Container Services is now in preview on Microsoft Azure. Snowflake Native Apps built using containers can be
distributed to any Snowflake customer who can use them in Azure commercial regions.

Providers can develop apps that can be distributed to Snowflake customers in both AWS or Azure. Apps running in
Azure can use the functionality of Snowpark Container Services, including compute pools, services, jobs, external access
integrations, etc. within a Snowflake Native App.

## Native App Framework support for Budgets

With this release, a Snowflake Native App can use [Budgets](/user-guide/budgets) to monitor credit usage. Customers can
set up spending limits for app, which include all the app’s compute resources, including compute pools and warehouses.
After installing an app, consumers can view and create budgets.
