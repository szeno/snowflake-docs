# Organization Hub Insights

The **Insights** page in [Organization Hub](/user-guide/organization-hub) presents organization-level metrics through interactive
tiles that display trends, alerts, and summary data from all accounts in your organization. Use Insights to monitor and analyze
cost, security posture, query health, and storage.

Insights requires an [organization account](/user-guide/organization-accounts) with
[premium views](/user-guide/organization-accounts-premium-views) enabled.

## Get started

1. Use [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) to sign in to the organization account.
2. Switch to the `GLOBALORGADMIN` role, or to a role that has been granted the appropriate `ORGANIZATION_USAGE` application roles.
   For more information, see [Access control requirements](#label-org-hub-access-control).
3. In the navigation menu, select **Organization Hub** » **Insights**.

## High-level highlights

The top of Insights contains highlights from each section. Select a tile to switch to the corresponding tile further down the page.

Note

A tile labeled **Coming soon** is in private preview. In private preview, that tile includes organization budgets.
To request access, use the feedback button in Snowsight or contact your Snowflake account team.

## Billing and Cost

The **Billing and Cost** section of Insights contains the following tiles:

| Tile | Description |
| --- | --- |
| **Total cost** | Displays the total cost average cost per month for your organization. View a graph showing cost trends over time. |
| **Cost by service type** | Shows a breakdown of costs by different Snowflake service types, such as data quality monitoring, logging, and warehouses |
| **Total storage** | Displays the current total storage usage across your organization with percentage change over time. Shows storage breakdown by category, which can be one of the following:   - Active - Retained for clone - Time travel - Failsafe |
| **Contract utilization** | Tracks your contract utilization percentage, showing total cost, remaining capacity on the contract, and any overage costs since the start of the contract. |

Expand

Show lessSee more

## Security

The **Security** section of Insights contains the following tiles:

| Tile | Description |
| --- | --- |
| **Trust center violations** | Displays the total number of open Trust Center violations across your organization, grouped by severity level. Shows the percentage change from the previous week. Select **Trust Center** to open the Trust Center and drill down into the information. |
| **Trust center scanner package coverage** | Shows the percentage of accounts with Trust Center scanner packages enabled, excluding security essentials and extension packages (that is, custom-defined packages). |
| **Strong Authentication progress** | Tracks strong authentication readiness across your accounts, showing the number and percentage of accounts that are Strong Authentication ready versus not ready. |
| **Login failures by type** | Displays total login failures and the percentage change over the last 28 days, broken down by failure type. |
| **Authentication methods (human)** | Shows the distribution of [authentication methods](/user-guide/security-authentication-overview) used by human users (that is, users of type PERSON). |
| **Authentication methods (service)** | Displays the [authentication methods](/user-guide/security-authentication-overview) used by service users (that is, users of type SERVICE). |
| **Account admins** | Lists all accounts in the organization and the users who have the ACCOUNTADMIN role. |
| **Security admins** | Lists all accounts in the organization and the users who have the SECURITYADMIN role. |
| **Dormant users** | Shows the number of users with no logins in the last 3 months, with percentage change and a trend graph over time. |

Expand

Show lessSee more

## Query health

The **Query health** section of Insights contains the following tiles:

| Tile | Description |
| --- | --- |
| **Failed queries** | Displays the total number of failed grouped queries with percentage change over time. Failed queries are categorized by error type. Queries are grouped by their parameterized hash  The tile gathers its data from the [QUERY\_HISTORY](/sql-reference/organization-usage/query_history) view of the ORGANIZATION\_USAGE schema. |
| **Warehouse concurrency load** | Shows queue wait times and queued load across warehouses, helping identify warehouses with the highest query queuing. Displays queue events, total queries, and queue rate per warehouse.  The tile gathers its data from the [WAREHOUSE\_LOAD\_HISTORY](/sql-reference/organization-usage/warehouse_load_history) and [QUERY\_HISTORY](/sql-reference/organization-usage/query_history) views of the ORGANIZATION\_USAGE schema. |
| **Top grouped queries by cost** | Lists the top grouped queries ordered by credits per query. Queries are grouped by their parameterized hash, showing the highest cost query patterns and percentage change over time.  The tile gathers its data from the [QUERY\_HISTORY](/sql-reference/organization-usage/query_history) view of the ORGANIZATION\_USAGE schema. |
| **Warehouse load and queueing** | Displays the average queued load across all warehouses with percentage change over time. Helps investigate overall warehouse congestion level, where higher values indicate more queries are waiting in queue.  The tile gathers its data from the [WAREHOUSE\_LOAD\_HISTORY](/sql-reference/organization-usage/warehouse_load_history) view of the ORGANIZATION\_USAGE schema. |

Expand

Show lessSee more

## Access control requirements

Every Insights tile reads from a view in the `ORGANIZATION_USAGE` schema, so access to Insights is determined entirely by which
[ORGANIZATION\_USAGE application roles](/sql-reference/organization-usage#label-org-usage-access-org-account) a user’s role holds.
There is no separate Insights privilege.

Users with the `GLOBALORGADMIN` role can read every `ORGANIZATION_USAGE` view, so they see all tiles. To give someone access without
granting `GLOBALORGADMIN`, grant one or more of the granular application roles described in this section.

### How access is evaluated

Snowflake evaluates access at two levels:

- **Page access.** Insights appears in the navigation menu, and the page opens, for a user whose role holds `GLOBALORGADMIN` or at
  least one of the granular application roles in the following table.
- **Tile access.** Each tile is authorized separately when it queries its underlying view. Tiles that the current role can read
  render normally. Tiles that it can’t read display a message stating that your role doesn’t hold the required application role,
  and the rest of the page continues to work.

Because the two levels are independent, a role with a single granular application role can open Insights and see a partially
populated page. This is expected: grant additional application roles to fill in the remaining tiles.

### Application roles used by Insights

Insights uses the following application roles:

| Application role | Data it makes visible in Insights |
| --- | --- |
| `ORGANIZATION_ACCOUNTS_VIEWER` | The list of accounts in the organization. Required for the account filter and for tiles that break results down by account. |
| `ORGANIZATION_BILLING_VIEWER` | Cost in currency and contract utilization. |
| `ORGANIZATION_GOVERNANCE_VIEWER` | Query-level data, which comes from the [QUERY\_HISTORY](/sql-reference/organization-usage/query_history) view. |
| `ORGANIZATION_SECURITY_VIEWER` | Users, logins, administrator role membership, and Trust Center findings. |
| `ORGANIZATION_USAGE_VIEWER` | Credit consumption, storage, and warehouse load. |

Expand

Show lessSee more

Note

`ORGANIZATION_OBJECT_VIEWER` grants access to object inventory views such as
[DATABASES](/sql-reference/organization-usage/databases), which no Insights tile reads. Granting it alone does not make Insights
usable.

### Application roles required by each section

Some sections of Insights combine data from more than one domain and therefore require more than one application role:

| Section | Application roles |
| --- | --- |
| **Billing and Cost** | `ORGANIZATION_BILLING_VIEWER` for the cost and contract utilization tiles, and `ORGANIZATION_USAGE_VIEWER` for the storage tile. |
| **Security** | `ORGANIZATION_SECURITY_VIEWER`. |
| **Query health** | `ORGANIZATION_GOVERNANCE_VIEWER` for the query tiles, and `ORGANIZATION_USAGE_VIEWER` for the warehouse load tile. |

Expand

Show lessSee more

The [high-level highlights](#label-org-hub-highlights) at the top of the page summarize the sections that follow, so each highlight
follows the same rules as the tile it summarizes.

To confirm which application role a specific view requires, see
[Access schema in the organization account](/sql-reference/organization-usage#label-org-usage-access-org-account).

### Example: Grant granular access to Insights

The following example creates a role for a security analyst who needs the **Security** section of Insights, but no cost or query
data. Run these statements in the organization account:

Copy code

```
USE ROLE GLOBALORGADMIN;

CREATE ROLE org_security_analyst;

-- Security tiles: users, logins, admin role membership, and Trust Center findings.
GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_SECURITY_VIEWER TO ROLE org_security_analyst;

-- Account list, so the analyst can filter and group results by account.
GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_ACCOUNTS_VIEWER TO ROLE org_security_analyst;

-- Organization Hub runs queries on a warehouse.
GRANT USAGE ON WAREHOUSE org_hub_wh TO ROLE org_security_analyst;

GRANT ROLE org_security_analyst TO USER jsmith;
```

When `jsmith` switches to `org_security_analyst` and opens **Organization Hub** » **Insights**, the **Security** section is
populated, and the **Billing and Cost** and **Query health** tiles report that the role doesn’t hold the required application role.

To extend the same role to the rest of Insights, grant the remaining application roles:

Copy code

```
USE ROLE GLOBALORGADMIN;

GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_BILLING_VIEWER TO ROLE org_security_analyst;
GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_GOVERNANCE_VIEWER TO ROLE org_security_analyst;
GRANT APPLICATION ROLE SNOWFLAKE.ORGANIZATION_USAGE_VIEWER TO ROLE org_security_analyst;
```

Alternatively, grant `SNOWFLAKE.ORG_USAGE_ADMIN`, which grants access to every view in the `ORGANIZATION_USAGE` schema, including views
that Insights doesn’t use.

To review what a role can already read, use
[SHOW GRANTS](/sql-reference/sql/show-grants):

Copy code

```
SHOW GRANTS TO ROLE org_security_analyst;
```

Command Center is documented separately and requires GLOBALORGADMIN. See
[Organization Command Center](/user-guide/organization-hub-command-center).

## Analyze organization insights with Cortex Code

You can investigate organization-wide cost, security, and usage in [Cortex Code](/user-guide/cortex-code/cortex-code) without signing
in to each account separately.

In Cortex Code (CLI, Desktop, or the Snowsight panel), type `/organization-management` to invoke the skill, then describe what you
want to know. For more information, see
[`organization-management`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-organization-management).

Example prompts:

```
Give me a 30-day executive summary of all accounts in my organization, including costs, usage, and reliability.

Review our organization-wide security posture: MFA adoption, login failures, and authentication settings.

Analyze cross-account credit and storage spending trends for a quarterly business review.
```
