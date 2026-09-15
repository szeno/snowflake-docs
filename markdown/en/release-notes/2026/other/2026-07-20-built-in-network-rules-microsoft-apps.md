# July 20, 2026: Built-in network rules for additional Microsoft applications

Snowflake now maintains [built-in network rules](/user-guide/network-rules#label-snowflake-managed-network-rules) for five additional Microsoft partner applications:

- Microsoft Entra ID
- Microsoft Power Automate
- Microsoft Power Query Online
- Microsoft Azure DevOps
- Microsoft Azure Data Factory

Built-in network rules define the set of allowed IP addresses that a frequently used, third-party partner application uses to connect with Snowflake. Snowflake automatically updates these rules to reflect any changes the provider makes to their egress IP addresses, so you can add them to your network policies without ongoing maintenance.

For more information, see [Snowflake-managed network rules](/user-guide/network-rules#label-snowflake-managed-network-rules).
