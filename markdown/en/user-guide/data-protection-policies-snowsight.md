# Manage data protection policies in Snowsight

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Data protection policies are Snowflake’s [fine-grained access control (FGAC)](/user-guide/security-access-control-overview) features. They
complement role-based access control (RBAC) by governing what data users actually see at query time, not just which objects they can access.
A role with `SELECT` on a table may still have its view of the data shaped by policies that mask values, filter rows, block column projection,
enforce aggregation minimums, or restrict joins.

Snowflake data protection policies let you define granular permissions once and enforce them consistently at query time, eliminating the
need to create additional roles or views as your data and teams grow.

## Data protection policy types

Snowflake supports the following data protection policy types:

[Masking policies](/user-guide/security-column-intro)
:   A column-level security feature that selectively masks plain-text data in table and view columns at query time.

[Row access policies](/user-guide/security-row-intro)
:   A row-level security feature that controls which rows in a table or view are visible or accessible to users when executing `SELECT`,
    `UPDATE`, `DELETE`, or `MERGE` statements.

[Aggregation policies](/user-guide/aggregation-policies)
:   Enforces minimum group sizes in query results, preventing privacy leaks by ensuring that no individual’s data can be isolated in small
    groups.

[Projection policies](/user-guide/projection-policies)
:   Restricts which columns can be accessed or projected in queries, so only authorized users can view sensitive fields.

[Join policies](/user-guide/join-policies)
:   Controls how and when data from different tables can be combined, protecting against unauthorized data correlation and exposure of
    sensitive relationships between datasets.

You can create and manage these policies in SQL or in Snowsight. You can also use [Cortex Code](#label-data-protection-policies-cortex-code)
to create policies and apply them to objects with guided workflows.

## Data protection policies for agentic interactions

When an AI agent acts on behalf of a user, it runs in that user’s session. The session still belongs to the user, but an agent can be
present in the execution context. Call [IS\_AGENT\_ACTIVATED](/sql-reference/functions/is_agent_activated) to detect that condition:

Copy code

```
SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')::BOOLEAN = TRUE
```

You can use this check in the body of any data protection policy so governance behaves differently when an agent is active. For example,
you can mask values more aggressively, hide rows, block column projection, require aggregation, or require joins for agent-driven queries,
even when the user’s role would otherwise allow broader access.

An agent is typically active for workflows such as Cortex Agents, Cortex Code, Snowflake MCP Server connections, and Snowflake OAuth
security integrations configured with `IS_AGENTIC = TRUE`. For more about designating OAuth clients as agentic, see
[Configuring agent sessions](/user-guide/oauth-custom#configuring-agent-sessions).

The following masking policy example masks the column value when an agent is active. When no agent is active, only the `ANALYST` custom
role can view the raw value:

Copy code

```
CREATE OR REPLACE MASKING POLICY email_agent_mask AS (val STRING) RETURNS STRING ->
  CASE
    WHEN SYS_CONTEXT('SNOWFLAKE$CURRENT', 'IS_AGENT_ACTIVATED')::BOOLEAN = TRUE THEN '********'
    WHEN CURRENT_ROLE() IN ('ANALYST') THEN val
    ELSE '********'
  END;
```

For additional masking examples, see
[Mask column values when an agent is active](/user-guide/security-column-intro#label-security-column-agent-active). For a tag-based masking example that uses agent identity, see
[Example: Protect schema columns when an agent is active](/user-guide/tag-based-policies#label-tag-based-policies-agent-active).

For examples that use agent identity in other policy types, see:

- [Row access policies](/user-guide/security-row-intro#label-security-row-agent-active)
- [Projection policies](/user-guide/projection-policies#label-projection-policy-agent-active)
- [Aggregation policies](/user-guide/aggregation-policies#label-agg-policy-agent-active)
- [Join policies](/user-guide/join-policies#label-join-policy-agent-active)

## Access control privileges

To use the **Data protection policies** in Snowsight, your Snowflake account must be [Enterprise Edition or higher](/user-guide/intro-editions).

Additionally, you must do either of the following:

- Use the ACCOUNTADMIN role.
- Use an account role that is directly granted the GOVERNANCE\_VIEWER and OBJECT\_VIEWER database roles.

  You must use an account role with these database role grants. Currently, Snowsight does not evaluate role hierarchies
  for this area.

  For details about these database roles, see [SNOWFLAKE database roles](/sql-reference/snowflake-db-roles).

To create policies in the UI, your role also needs the privileges required for the policy type (for example, `CREATE MASKING POLICY` on the
schema). To apply a policy to an object, you need the privileges described in the documentation for that policy type.

## Get started in Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in) as a user with the [required access](#label-data-protection-policies-access-snowsight).
2. In the navigation menu, select **Governance & security** » **Data protection policies**.

   The **Data protection policies** page opens. Use it to create and manage policies to protect your data.
3. Select a warehouse if prompted (**Select warehouse**).
4. Use the **Dashboard**, **Policies**, and **Objects with policies** tabs to monitor posture, manage policies, and review protected
   objects.

Note

The **Data protection policies** area requires a running warehouse. Dashboard metrics refresh on a periodic schedule. Information in the
**Objects with policies** tab can be up to two hours behind.

## Dashboard

The **Dashboard** tab summarizes policy posture across your account. The page subtitle is **View policy metrics across your data, explore
further with Cortex Code**.

### Create policies

At the top of the **Dashboard**, five cards represent the supported [policy types](#label-data-protection-policies-intro). Each card
describes the policy and includes a **+** control to start creating a policy of that type:

| Card | Description |
| --- | --- |
| **Masking policy** | Dynamically hides sensitive data at query time. |
| **Row access policy** | Restricts table row visibility based on user attributes. |
| **Aggregation policy** | Limits data exposure with aggregated query results. |
| **Join policy** | Controls which datasets can be joined together. |
| **Projection policy** | Restricts which columns can be queried or viewed. |

Expand

Show lessSee more

Select **+** on a card to open the create workflow for that policy type without writing SQL.

### Policy posture summary

Below the create cards, the **Policy posture summary** section provides account-level metrics:

- **Policy overview**: A chart shows how policy assignments are distributed by type (masking, row access, aggregation, projection, and
  join). **Total assignments** counts all policy assignments in the account.
- **Policy coverage**: Shows **Total assignments**, how many are **Applied via tags**, and how many are **Directly applied** to objects.
- **Top tags driving policy enforcement**: Lists tags that apply the most policies (for example, a `SENSITIVITY` tag).

### Enforcement deep-dive

The **Enforcement deep-dive** section lists the most frequently used policies in each category, such as **Most used masking policies** and
**Most used row access policies**. Each entry shows the policy name and assignment count so you can see which policies drive the most
enforcement in your account. Categories with no assignments appear empty until policies of that type are in use.

## Policies

The **Policies** tab lists every data protection policy in the account that you are permitted to see.

At the top of the tab, use the following filters:

- **Filter by name**: Search for a policy by name.
- **Database**, **Schema**, and **Owner**: Narrow the list to policies in a specific location or owned by a specific role.

The tab header shows how many policies exist in the account and how many are not yet applied to objects (for example, `1,195 policies (317 not applied)`).

The table includes the following columns:

| Column | Description |
| --- | --- |
| **Policy name** | Name of the policy. |
| **Type** | Policy type (masking, row access, aggregation, projection, or join). |
| **Location** | Database and schema where the policy is stored. |
| **Owner** | Role that owns the policy. |
| **Modified at** | Timestamp of the last change to the policy. |

Expand

Show lessSee more

Select the actions menu ([![Three vertical dots indicating more options](/static/images/icons/vertical-more-icon.png)](/static/images/icons/vertical-more-icon.png)) on a row to **view details**, **edit**, or **delete** the policy.

After you create or update a policy, apply it to tables, views, or columns from the **Objects with policies** tab, from **Catalog** »
**Database Explorer**, or by using SQL. For policy-specific behavior and examples, see the introduction topic for each
[policy type](#label-data-protection-policies-intro).

## Objects with policies

The **Objects with policies** tab lists tables, views, and columns that have one or more data protection policies applied.

At the top of the tab, use the following controls:

- **Filter by name**: Search for an object by name.
- **Object type**: Filter to tables, columns, or all object types.

The tab shows how many protected objects match your filters (for example, `1000+ objects`). Information latency can be up to two hours.

The table includes the following columns:

| Column | Description |
| --- | --- |
| **Name** | Name of the table, view, or column. |
| **Location** | Database and schema that contain the object. |
| **Object type** | Whether the row is a **Table** or **Column**. |
| **Tags** | Governance tags on the object (for example, `SENSITIVITY` = `PII`). |
| **Policy types** | Types of policies applied (for example, **Masking** or **Row access**). |

Expand

Show lessSee more

Use this tab to verify that sensitive columns and tables have the expected policies and tags. Select a row to open the object in
**Catalog** » **Database Explorer** for more detail.

## Create and apply policies with Cortex Code

You can use [Cortex Code](/user-guide/cortex-code/cortex-code) with the [data governance skills for data protection policies](/user-guide/governance-skills#label-dg-skills-data-protection-policies)
to create policies and apply them to objects using natural-language prompts. Cortex Code can help you author masking, row access, and
projection policies, audit existing policies, and apply proven patterns such as attribute-based access control.

Example prompts:

Copy code

```
Create a masking policy for the EMAIL column in the SALES.NA.CUSTOMERS table
Help me set up row access policies for the FINANCE schema
Audit all masking policies in my account
Apply the PII masking policy to columns tagged as sensitive in PROD_DB
```

For more example prompts and supported tasks, see [Data protection policies](/user-guide/governance-skills#label-dg-skills-data-protection-policies).
