# Private connectivity for inbound network traffic in Snowflake Open Catalog

[Business Critical Feature](https://docs.snowflake.com/en/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To ask about upgrading, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Feature — Generally Available

Not available in government regions.

Your connection to Snowflake Open Catalog can be routed over the public internet or through a private IP address associated with the cloud
platform that hosts your Open Catalog account. By using your cloud platform’s private connectivity solution to create private endpoints,
you can harden your security posture so that inbound network traffic uses private connectivity.

When your query engine connects to your Snowflake Open Catalog account, inbound network traffic is generated for your account. In addition,
inbound network traffic is generated when you access the Open Catalog UI.

Note

For Snowflake to query Open Catalog–managed tables through private connectivity, Snowflake and Open Catalog must both be located
in the same deployment.

## Configuring private connectivity for your Open Catalog account

Private connectivity for inbound network traffic is supported for the following cloud platforms:

- [AWS](private-connectivity-inbound-configure-aws)
- [Azure](private-connectivity-inbound-configure-azure)

## Configuring private connectivity for the Open Catalog UI

You can access the Open Catalog UI through private connectivity. To configure this access, see
[Configure private connectivity for the Snowflake Open Catalog UI](private-connectivity-ui-configure).

## Billing

Snowflake calculates costs for inbound private connectivity based on endpoint usage. For details on pricing for inbound private connectivity,
see the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
