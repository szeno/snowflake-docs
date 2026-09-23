# Enforce data protection policies on Apache Iceberg™ tables using the Scan Plan API

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic describes how to enforce Snowflake’s row access and column masking policies on all Apache Iceberg™ tables
when accessed from external query engines through the Horizon Iceberg REST Catalog (IRC) Scan Plan API.

Snowflake data protection policies follow your Iceberg data wherever it is accessed. With the Scan Plan API, any
external engine that supports the Scan Plan API such as Apache Spark, Trino, or PyIceberg, can automatically enforce
your existing Snowflake data protection policies when querying Iceberg tables through Horizon Catalog without any
additional changes.

## How policy enforcement works with Scan Plan API

Horizon Catalog leverages Iceberg REST open standards to enforce data protection policies on tables accessed by external
engines. The Iceberg REST Catalog protocol allows engines to delegate the determination of data access and scope to the
catalog itself. Horizon Catalog extends this protocol by generating filtered scan plans that carry pre-enforced
policies. Notably, this eliminates the need to trust external engines to enforce access policies correctly,
establishing the catalog as the single, central authority for data governance. All existing Snowflake policies work
seamlessly as-is without modification, ensuring consistent security across all query engines.

When an external engine requests access to a protected table, the workflow proceeds as follows:

1. **Request**: The engine issues a scan request via the Iceberg REST Catalog API.
2. **Evaluation**: Horizon Catalog evaluates the query context against active row access and masking policies on the
   table. Snowflake Horizon’s built-in optimization bypasses scan plan materialization based on policy evaluation
   whenever possible, keeping query latency low.
3. **Planning**: If the policy evaluation in the Evaluation step determines that dynamic filtering or masking is
   required, Horizon Catalog generates a precisely filtered governance enforced dataset (scan plan).
4. **Enforcement**: Only the authorized subset of data is exposed, ensuring the engine never sees restricted records.

Because enforcement occurs at the catalog during server-side planning, no custom policy or additional plugins are required
within the external engine.

[![Scan Plan API architecture showing external query engines connecting to Snowflake Horizon Catalog, which applies policy filters to Snowflake-managed and externally managed Iceberg tables](/static/images/scan-plan-api-architecture.png)](/static/images/scan-plan-api-architecture.png)

## Prerequisites

- Complete the setup to access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog. For
  instructions, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
- Define data protection policies on the Iceberg tables you want to protect in Snowflake Horizon Catalog.
- Grant the user’s role USAGE privileges on the external volume where the table is stored.

Note

When using Apache Spark, use the latest version of Iceberg, that is 1.11 and above.

## Getting started

Update the external engine configuration to enforce policies. In this step, you modify your external engine setup
(as configured in [Connect an external query engine without enforcing data policies](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon#label-tables-iceberg-query-using-external-query-engine-snowflake-horizon-connect-external-oauth-key-pair-no-access-policies))
to pull in the latest updates on the Scan Plan API.

Add the following code to your existing Spark configuration:

Copy code

```
.config("spark.jars.packages", "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.11.0,org.apache.iceberg:iceberg-aws-bundle:1.11.0")
```

## Writing to policy-protected tables

By default, the open-source Apache Iceberg Scan Plan API doesn’t support write operations to
policy-protected tables, returning an HTTP 403 error whenever a write is attempted. However, Snowflake
Horizon Catalog extends this capability to allow writes on policy-protected tables. For a write
operation to succeed, the principal attempting the write must hold the required privileges, and the
underlying policy definition must use one of the supported predicate patterns detailed below. Attempts
to write using any other policy pattern might result in an HTTP 403 error.

| Policy type | Supported predicate | Example |
| --- | --- | --- |
| Masking | `CURRENT_ROLE()` in a list of roles | `CASE WHEN CURRENT_ROLE() IN ('FULL_ACCESS') THEN val ELSE '***' END` |
| Masking | `CURRENT_ACCOUNT()` in a list of accounts | `CASE WHEN CURRENT_ACCOUNT() IN ('DEMO91') THEN val ELSE '***' END` |
| Masking | `CURRENT_USER()` equal to a literal user name | `CASE WHEN CURRENT_USER() = 'alice' THEN value ELSE '***' END` |
| Masking | Nested `IFF` with `ARRAY_CONTAINS` on `CURRENT_ROLE()` | `IFF(ARRAY_CONTAINS(CAST(CURRENT_ROLE() AS VARIANT), ['ROLE_A']) OR CURRENT_ROLE() LIKE '...', val, mask(...))` |
| Row access | `IS_ROLE_IN_SESSION()` with a literal role name | `IS_ROLE_IN_SESSION('ANALYST_ROLE')` |
| Row access | A context function or `EXISTS` on a mapping table | `CURRENT_ACCOUNT() IN ('ACCT1') OR EXISTS(SELECT 1 FROM mapping WHERE ...)` |
| Row access | A context function or a scalar `IN (SELECT DISTINCT ...)` subquery | `CURRENT_ACCOUNT() IN ('ACCT1') OR col IN (SELECT DISTINCT val FROM mapping)` |
| Row access | `CURRENT_ROLE()` in a list of roles or `EXISTS` on a mapping table | `CURRENT_ROLE() IN ('R1') OR EXISTS(SELECT 1 FROM access_view WHERE ...)` |
| Row access | `UPPER(CURRENT_USER())` equal to an upper-cased literal or `EXISTS` on an allow-list | `CASE WHEN UPPER(CURRENT_USER()) = UPPER('bob') OR EXISTS(...) THEN TRUE ELSE COALESCE(...) END` |
| Row access | `SYSTEM$GET_TAG()` on a tag assigned to the writer’s user | `SYSTEM$GET_TAG('governance_db.public.dept_code', CURRENT_USER(), 'USER') = 'SALES'` |

Expand

Show lessSee more

Even when a policy uses a supported predicate, consider the following behaviors:

- Policy definitions with predicates that result in NULL are not supported.
- If a row access policy combines a context function with `EXISTS` or `IN (SELECT DISTINCT ...)` and
  the context function matches the writer, Snowflake doesn’t evaluate the subquery. The writer gets
  access based on the context function alone.
- A row access policy that uses `IS_ROLE_IN_SESSION()` with a literal role name can allow or deny the
  write, depending on which roles are active in the writer’s session. Make sure the role that the
  policy checks for is active when the engine loads the table.

### Example

You can use [attribute-based access control (ABAC)](/user-guide/tag-based-policies) to control which
writers can write to a policy-protected table from an external engine. Assign a
[tag](/user-guide/object-tagging/introduction) that carries the attribute to each user, then define a
[row access policy](/user-guide/security-row-intro) that calls
[SYSTEM$GET\_TAG](/sql-reference/functions/system_get_tag) to read that tag for the current user. Only the users whose
tag value satisfies the policy condition can access and write the rows of the table.

The following example tags a writer with a department code, then protects an Iceberg table with a row
access policy that checks the tag:

Copy code

```
CREATE TAG governance_db.public.dept_code;

ALTER USER data_writer SET TAG governance_db.public.dept_code = 'SALES';

-- Confirm the tag value that the policy evaluates for the current user.
SELECT SYSTEM$GET_TAG('governance_db.public.dept_code', CURRENT_USER(), 'USER');

CREATE ROW ACCESS POLICY governance_db.public.rap_user_attribute
  AS (id NUMBER) RETURNS BOOLEAN ->
    CASE
      WHEN SYSTEM$GET_TAG('governance_db.public.dept_code', CURRENT_USER(), 'USER') = 'SALES' THEN TRUE
      ELSE FALSE
    END;

ALTER ICEBERG TABLE governance_db.public.customer_iceberg
  ADD ROW ACCESS POLICY governance_db.public.rap_user_attribute ON (id);
```

Use the fully qualified tag name in the `SYSTEM$GET_TAG` arguments. Snowflake returns an error at query
runtime if the tag name in the policy conditions isn’t sufficiently qualified. Because `SYSTEM$GET_TAG`
returns an error when a tag has more than one value, use a single-value tag in the policy condition
rather than a [multi-value tag](/user-guide/object-tagging/multi-value-tags).

## Auditing access from external engines on policy-protected tables

You can audit access from external engines on policy-protected tables by querying the
[ACCESS\_HISTORY](/sql-reference/account-usage/access_history) view. Filter on the
`event_source` column for values such as `horizon_irc` to isolate Horizon Iceberg REST
Catalog (IRC) and Scan Plan API traffic. For Horizon IRC operations more generally, see
[Horizon Iceberg REST Catalog operations in ACCESS\_HISTORY](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon-access-history).

The following query returns recent ACCESS\_HISTORY records for that traffic:

Copy code

```
SELECT *
FROM SNOWFLAKE.ACCOUNT_USAGE.ACCESS_HISTORY
WHERE event_source LIKE 'horizon_irc'
ORDER BY query_start_time DESC
LIMIT 50;
```

The following sample result shows a Scan Plan API request (`PlanTableScan`) against a
table protected by a row access policy. Review `policies_referenced` to see which
policies Snowflake evaluated for the request.

Copy code

```
{
  "query_id": "6aa5d7a8-8f6b-9e1c-80ed-251fe0df8f9c",
  "query_start_time": "2026-08-11 13:58:27.784 -0700",
  "user_name": "HORIZON_SPARK_USER",
  "event_source": "horizon_irc",
  "direct_objects_accessed": [
    {
      "columns": [
        {
          "columnId": 1,
          "columnName": "ID"
        },
        {
          "columnId": 2,
          "columnName": "NAME"
        },
        {
          "columnId": 3,
          "columnName": "CREATED_AT"
        }
      ],
      "objectDomain": "TABLE",
      "objectId": 78859896139074,
      "objectName": "HORIZON_IRC_TEST.MY_SCHEMA.MY_TABLE"
    }
  ],
  "objects_modified": [],
  "policies_referenced": [
    {
      "objectDomain": "Table",
      "objectId": 404304,
      "objectName": "HORIZON_IRC_TEST.MY_SCHEMA.MY_TABLE",
      "policies": [
        {
          "policyId": 1,
          "policyKind": "ROW_ACCESS_POLICY",
          "policyName": "HORIZON_IRC_TEST.MY_SCHEMA.ID_RAP"
        }
      ]
    }
  ],
  "additional_properties": {
    "access_delegation_mode": "[VENDED_CREDENTIALS]",
    "case_sensitive": false,
    "irc_event_type": "PlanTableScan",
    "plan_id": "739334_0",
    "plan_status": "SUBMITTED",
    "use_snapshot_schema": false
  }
}
```

## Considerations

- Queries running longer than 24 hours may fail because Snowflake automatically deletes the intermediate filtered
  dataset 24 hours after creation.
- The `CURRENT_STATEMENT()` context function is not supported in policies evaluated through the Scan Plan API.
- Filtered datasets are stored in the customer’s external volume. Snowflake cannot enforce data privacy on users who
  have direct access to the underlying storage outside Snowflake’s access model.
- Cross-region egress charges apply if the catalog/database region differs from the storage volume and client engine
  region.
- Queries with explicit snapshot IDs are blocked. Only the latest snapshot of the table is supported.
- Aggregation pushdown, TopN, join pushdown between two protected tables, and arbitrary filter pushdown (for example,
  `substr()`) are not supported. This is a limitation from the Iceberg REST Scan API.
- All considerations for accessing Iceberg tables with an external query engine also apply when using the Scan Plan API.
  For more information, see [Access Apache Iceberg™ tables with an external engine through Snowflake Horizon Catalog](/user-guide/tables-iceberg-access-using-external-query-engine-snowflake-horizon).
- Policies enforcement on externally managed tables without an external volume are currently not supported.
- Using the Scan Plan API consumes Snowflake compute for policy evaluation and enforcement in addition to temporary
  storage and cross-region data transfer charges, as applicable, when querying over external engines. For current
  credit consumption rates, refer to “External Governance” in Table 5: Serverless Feature Table in the
  [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf).
