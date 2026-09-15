# Enforce data protection policies on Apache Iceberg™ tables from external query engines

This topic provides an overview of how to enforce data protection policies set on Apache Iceberg™ tables when accessed
from external query engines through Snowflake Horizon Catalog.

Snowflake supports enforcing row-level and column-level data protection policies on Iceberg tables queried from external
engines such as Apache Spark™, PyIceberg, and Trino. This ensures that governance policies defined in Snowflake are
consistently applied, regardless of the compute engine used to query the data.

Snowflake provides two ways to enforce data protection policies on Iceberg tables from external engines:

1. **[Snowflake Connector for Spark](/user-guide/tables-iceberg-enforce-access-policies-spark-connector)**:
   Enforces policies by routing queries through Snowflake using a JDBC connection.
   This approach offers better pushdown capabilities and supports all read and write operations on policy-protected tables.
2. **[Iceberg REST Catalog (IRC) Scan Plan API](/user-guide/tables-iceberg-enforce-access-policies-scan-plan-api)**:
   Enforces policies by sharing a temporary, policy-filtered dataset with the external engine.
   This approach works with any engine that supports the Iceberg Scan Plan API (Iceberg SDK v1.11+).

## Supported data protection policies

The following data protection policies are supported when querying Iceberg tables from external engines:

- [Masking policies](/user-guide/security-column-intro)
- [Row access policies](/user-guide/security-row-intro)
- [Tag-based masking policies](/user-guide/tag-based-masking-policies)
- [Tag-based row access policies](/user-guide/tag-based-row-access-policies)

All other policy types in Snowflake aren’t supported.

## Choosing an approach

| Consideration | Snowflake Connector for Spark | IRC Scan Plan API |
| --- | --- | --- |
| Supported engines | Apache Spark only | Any IRC-compliant engine (Spark, Trino, PyIceberg, and others) |
| Client-side changes | Requires Snowflake Connector for Spark installation | No connector required; uses standard Iceberg SDK |

Expand

Show lessSee more

Note

Customers using Snowflake Connector for Spark can continue to use the connector even when IRC Scan Plan API support
is available. If the connector is configured, it is used automatically; otherwise, the engine defaults to the IRC
Scan Plan API.

## Prerequisites

Before using an external engine to query Snowflake-protected Iceberg tables, ensure the following:

- **Set up Iceberg table storage**: Configure an external volume using Snowflake-managed storage or your own object
  storage to store Iceberg tables.
- **Define policies**: Create row access policies and column masking policies in Snowflake on the Iceberg tables you
  want to protect.
- **Configure access control**: Configure roles and permissions on the Iceberg tables. Obtain an OAuth access token or
  programmatic access token (PAT) to authenticate to the Horizon Catalog endpoint.

For approach-specific prerequisites, see the individual topics below.

## Next steps

- To enforce policies using the IRC Scan Plan API, see
  [Using the Scan Plan API](/user-guide/tables-iceberg-enforce-access-policies-scan-plan-api).
- To enforce policies using the Snowflake Connector for Spark, see
  [Using Snowflake Connector for Spark](/user-guide/tables-iceberg-enforce-access-policies-spark-connector).
