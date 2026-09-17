# Data movement policies

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Data movement policies (DMP) are part of Snowflake’s data exfiltration protection controls.
They help you limit, alert on, or block data movement operations based on configured policies.
You do this by defining movement rules, grouping those rules into policies, and attaching policies to tags or directly to the account.
When a supported movement operation involves tagged objects, Snowflake evaluates the active policy and can allow the operation, allow it with an alert, or block it.

## Benefits

Data movement policies help you:

- Limit large exports of sensitive data by setting row budgets per movement type.
- Reuse controls across environments by attaching policies to tags instead of individual tables and views.
- Add movement guardrails without changing access patterns for approved users.
- Improve visibility into risky movement through alert-driven monitoring.

## Prerequisites for configuring DMP

Before you configure DMP, make sure that:

- You identify sensitive data domains and classify data where needed.
- Your protected data is covered by tags. Tags can be applied at column, table, schema, or database scope.
- Tag propagation is configured correctly for movement use cases. By default, tags with a data movement policy attached must have their propagation level set to `ON_DEPENDENCY_AND_DATA_MOVEMENT`. To disable this requirement, set the [ENFORCE\_TAG\_PROPAGATION\_FOR\_DATA\_MOVEMENT\_POLICIES](/sql-reference/parameters#enforce-tag-propagation-for-data-movement-policies) account parameter to `FALSE`. When disabled, a data movement policy can be applied to tags with any propagation level, meaning the policy won’t follow and protect data through tag propagation. For more details, see [Tag propagation](/user-guide/object-tagging/propagation).
- You define approved exception roles for business workflows that need controlled movement access.
- You validate movement workflows in a non-production environment before rollout.

## How data movement policies work

### Data movement rule

A data movement rule controls one movement type, such as `COPY_INTO_EXTERNAL_STAGE`.
Each rule includes:

- A movement `TYPE` that selects which movement class the rule applies to. Supported values are `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `SNOWSIGHT_UI`, `AGENT_ACCESS`, `UI_DOWNLOAD`, and `PROGRAMMATIC_FETCH`.
- A `MAX_ROWS` expression that returns an integer.

The `MAX_ROWS` return value has the following meaning:

- `NULL`: no limit from this rule.
- `0`: block the movement operation.
- Positive integer: maximum number of rows allowed for that operation.

The `MAX_ROWS` body can call `SYS_CONTEXT` to read session and movement context; see [SYS\_CONTEXT in movement rules](#label-dmp-movement-context-syscontext).

### Data movement policy

A data movement policy groups rules into two lists:

- `ENFORCE_RULES` can block movement operations.
- `ALERT_RULES` allow the operation and generate an alert.

### Policy attachment

Policies can be attached to tags or directly to the account.

**Tag-based attachment** is the primary method. Use `ALTER TAG ... SET DATA MOVEMENT POLICY ...`
to bind a policy to a tag. When those tags are applied to objects, Snowflake evaluates DMP for
supported movement operations.

**Account-level attachment** provides a baseline policy. It is the least granular attachment level
and applies only when no tag-based policy resolves for a given column or data object. Only one
account-level policy can be active at a time. Use `ALTER ACCOUNT SET DATA MOVEMENT POLICY ...` to
set it and `ALTER ACCOUNT UNSET DATA MOVEMENT POLICY` to remove it.

#### Attachment precedence

When multiple policies are applicable, Snowflake uses the most granular attachment level that has a
policy for each column or data object involved in the operation, and ignores coarser levels for
that column or object. The precedence order from most to least granular is:

1. Column-level tag
2. Table-level tag
3. Schema-level tag
4. Database-level tag
5. Account level

**Example:** If a column is covered by a column-level tag policy, that policy governs the column.
The table-level, schema-level, database-level, and account-level policies are not consulted for
that column. However, for columns or objects that do not have a column-level tag policy, the next
most granular level with a policy applies.

The effective policy set for a statement is the union of the winning policies across all columns
and data objects involved in the operation. The strictest `MAX_ROWS` value across those effective
policies governs the whole statement.

**Example:** A query reads two columns. The `ssn` column is covered by a column-level tag policy
with `MAX_ROWS = 100`. The `name` column has no column-level tag policy: the table-level tag policy
has `MAX_ROWS = 1000`. The strictest limit wins, so the query is restricted to 100 rows.

### Supported actions for DMP

DMP evaluation supports the following actions for supported movement operations:

- Allow: Data movement completes without triggering alert or enforcement thresholds.
- Allow with alert: Data movement completes and triggers an alert.
- Block: The movement operation is rejected.

For the `UI_DOWNLOAD` movement type specifically:

- Button disabled: When a `UI_DOWNLOAD` enforce rule threshold is met, downloads are disallowed by disabling the download button in the Snowsight UI.
- Download allowed: The enforcement threshold is not met.

### Movement types and precedence

#### What each movement `TYPE` means

Each data movement rule applies to a single `TYPE` value. The `TYPE` must match the movement type Snowflake assigns to the statement when it operates on tables protected by a data movement policy, not a user-defined description of the workload.

- `COPY_INTO_EXTERNAL_STAGE`: Applies when Snowflake classifies the statement as export or `COPY INTO` to an external stage (data is written to customer-managed object storage or another external destination exposed as an external stage).
- `COPY_INTO_INTERNAL_STAGE`: Applies when Snowflake classifies the statement as `COPY INTO` to an internal stage, that is, a Snowflake-managed stage inside your account.
- `SNOWSIGHT_UI`: Applies when Snowflake classifies the statement as data access that originates from Snowsight.
- `AGENT_ACCESS`: Applies when Snowflake determines that a statement is accessing sensitive data through an agent or MCP-style client. This type applies only if the statement is not classified as `COPY_INTO_EXTERNAL_STAGE` or `COPY_INTO_INTERNAL_STAGE` under the precedence rules. If Snowflake classifies the statement as copy to a stage, use the matching `COPY_INTO_*` rule type instead, even if the SQL was issued by an agent.
- `UI_DOWNLOAD`: Applies when a user downloads query results from the Snowsight UI, specifically the **Download** button on the results pane for SQL and Python files in workspaces, result downloads from notebook cells in workspaces, and the results download in **Query History**. This movement type does not apply to all download buttons. Examples of buttons and features not covered include, but aren’t limited to, downloads in Streamlit apps, notebooks in the Visual Studio Code extension, the **Export as HTML** option in workspaces, and CoWork. Upon enforcement, the applicable download button is disabled. Alert rules are not supported for this movement type.
- `PROGRAMMATIC_FETCH`: Applies when Snowflake classifies the statement as programmatic data access from a driver or connector, SnowSQL, Snowflake CLI, SQL API, or a stored procedure. This type applies only when no higher-precedence movement type matches. Stored procedures are an exception with respect to Snowsight: statements executing inside a stored procedure classify as `PROGRAMMATIC_FETCH` rather than `SNOWSIGHT_UI`, even when the calling session originates from Snowsight.

#### How Snowflake picks the primary movement type

For one statement, Snowflake picks at most one primary movement type for DMP evaluation, in this fixed order:

1. `COPY_INTO_EXTERNAL_STAGE`
2. `COPY_INTO_INTERNAL_STAGE`
3. `AGENT_ACCESS`
4. `SNOWSIGHT_UI`
5. `PROGRAMMATIC_FETCH`

The first classification in that list that matches the statement wins. Practical effect: UI and agent requests can execute through driver-like backends, but they still classify to `SNOWSIGHT_UI` or `AGENT_ACCESS` before `PROGRAMMATIC_FETCH` is considered.

#### UI\_DOWNLOAD and post-execution evaluation

Query execution triggers the evaluation of data movement rules for `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `SNOWSIGHT_UI`, and `AGENT_ACCESS`, and can block execution. In contrast, `UI_DOWNLOAD` rules are processed independently after the query finishes. If the query runs successfully, `UI_DOWNLOAD` restrictions are enforced where applicable to control whether results can be downloaded.

### SYS\_CONTEXT in movement rules

You can use `SYS_CONTEXT` in a rule’s `MAX_ROWS` expression and anywhere else DMP allows SQL in the rule body to read system context at evaluation time. This lets you write rule logic based on values such as the active role, client, and other session context, just as you would in standard SQL. For example, you can use `SYS_CONTEXT('SNOWFLAKE$SESSION', 'ROLE')` to read the current role.

In addition to existing Snowflake-defined namespaces, DMP also exposes the `SNOWFLAKE$DATA_MOVEMENT` namespace for movement-specific context about the statement being evaluated, such as destination stage attributes, Snowsight surface flags, and agent identifiers. Use `SYS_CONTEXT('SNOWFLAKE$DATA_MOVEMENT', '<property>')` only with the documented property names listed in the relevant tables. Property names are case-insensitive, and some properties support alternate spellings, such as versions with or without underscores. If you reference an unsupported property in this namespace, `CREATE DATA MOVEMENT RULE` or `ALTER DATA MOVEMENT RULE` fails at compile time. If a supported property does not apply to the statement’s primary movement type, or if the context is unavailable, treat the value as not applicable, for example, by comparing it to NULL.

`SYS_CONTEXT` returns `VARCHAR`. Boolean-backed properties return the strings `TRUE` or `FALSE`; cast to `BOOLEAN` when you compare to Boolean literals. See [SYS\_CONTEXT](/sql-reference/functions/sys_context) for return semantics and examples.

#### Properties for every primary movement type

| Property (accepted aliases) | Type | Nullable when applicable | Description |
| --- | --- | --- | --- |
| `MOVEMENT_TYPE` (`MOVEMENTTYPE`) | STRING | No | Label for the data movement operation type for the evaluated statement. |

Expand

Show lessSee more

#### Properties for `COPY_INTO_EXTERNAL_STAGE` and `COPY_INTO_INTERNAL_STAGE`

| Property (accepted aliases) | Type | Nullable when applicable | Description |
| --- | --- | --- | --- |
| `STAGE_TYPE` (`STAGETYPE`) | STRING | Yes | Stage category: `EXTERNAL` or `INTERNAL`. |
| `STAGE_NAME` (`STAGENAME`) | STRING | Yes | Qualified name of the destination stage. |
| `DESTINATION_ENCRYPTED` (`ENCRYPTED`) | BOOLEAN | Yes | Whether encryption is enabled for the destination stage. |
| `STAGE_URL` (`STAGEURL`) | STRING | Yes | Destination stage location. |
| `CLOUD_PROVIDER` (`CLOUDPROVIDER`) | STRING | Yes | Cloud provider for the stage. |
| `FILE_FORMAT` (`FILEFORMAT`) | STRING | Yes | Export file format. |

Expand

Show lessSee more

#### Properties for `SNOWSIGHT_UI`

| Property (accepted aliases) | Type | Nullable when applicable | Description |
| --- | --- | --- | --- |
| `UI_SURFACE` (`UISURFACE`) | STRING | Yes | Snowsight execution surface for the operation. |
| `IS_WORKSPACE` (`ISWORKSPACE`) | BOOLEAN | No (defaults to false) | True when `UI_SURFACE` is `WORKSPACE`. |
| `IS_STREAMLIT` (`ISSTREAMLIT`) | BOOLEAN | No (defaults to false) | True when `UI_SURFACE` is `STREAMLIT`. |
| `IS_NOTEBOOK` (`ISNOTEBOOK`) | BOOLEAN | No (defaults to false) | True when `UI_SURFACE` is `NOTEBOOK`. |
| `IS_NOTEBOOK_PROJECT` (`ISNOTEBOOKPROJECT`) | BOOLEAN | No (defaults to false) | True when `UI_SURFACE` is `NOTEBOOK_PROJECT`. |

Expand

Show lessSee more

#### Properties for `AGENT_ACCESS`

| Property (accepted aliases) | Type | Nullable when applicable | Description |
| --- | --- | --- | --- |
| `AGENT_NAME` (`AGENTNAME`) | STRING | Yes | Qualified name of the invoking agent. |

Expand

Show lessSee more

#### Properties for `UI_DOWNLOAD`

Note

There are no specific movement context properties for `UI_DOWNLOAD`.

#### Properties for `PROGRAMMATIC_FETCH`

| Property (accepted aliases) | Type | Nullable when applicable | Description |
| --- | --- | --- | --- |
| `IS_DRIVERS` (`ISDRIVERS`) | BOOLEAN | No (defaults to false) | True when the client is in the driver or connector family (JDBC, ODBC, Python, and similar). |
| `IS_SPROC` (`ISSPROC`) | BOOLEAN | No (defaults to false) | True when the fetch occurred inside a stored procedure. |
| `IS_SNOWSQL` (`ISSNOWSQL`) | BOOLEAN | No (defaults to false) | True when the client is SnowSQL. |
| `IS_SNOWFLAKE_CLI` (`ISSNOWFLAKECLI`) | BOOLEAN | No (defaults to false) | True when the client is the Snowflake CLI. |
| `IS_SQL_API` (`ISSQLAPI`) | BOOLEAN | No (defaults to false) | True when the client used the SQL API. |

Expand

Show lessSee more

## Access control

| Privilege | Object type | Description |
| --- | --- | --- |
| `CREATE DATA MOVEMENT RULE` | Schema | Required to create a data movement rule in a schema. |
| `CREATE DATA MOVEMENT POLICY` | Schema | Required to create a data movement policy in a schema. |
| `APPLY DATA MOVEMENT POLICY` | Account | Required to attach a data movement policy to a tag or to the account. |
| `OWNERSHIP` | Rule or policy | Required to alter, drop, or rename a rule or policy. |

Expand

Show lessSee more

## Configure data movement policies

### Plan the tables and views to protect

Identify the tables that contain sensitive data and confirm that the relevant tags are in scope at table level.
If your current governance model applies tags at column level, plan how you’ll apply equivalent tags at table level for DMP-controlled datasets.

### Create data movement rules

Define one rule per movement type you want to control.
The following example creates a strict compensation rule with a role-based exception:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT RULE hr_comp_copy_guard
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (
    CASE
      WHEN SYS_CONTEXT('SNOWFLAKE$SESSION', 'ROLE') = 'COMP_TEAM_ROLE' THEN NULL
      ELSE 0
    END
  );
```

The following example creates a two-tier pattern for PII:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT RULE hr_pii_copy_hard_boundary
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (1000);

CREATE OR REPLACE DATA MOVEMENT RULE hr_pii_copy_alert_budget
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (500);
```

Create a rule that uses movement context from `SNOWFLAKE$DATA_MOVEMENT` (here, cloud provider on `COPY` to a stage):

Copy code

```
CREATE OR REPLACE DATA MOVEMENT RULE export_cloud_row_budget
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (
    CASE
      WHEN SYS_CONTEXT('SNOWFLAKE$DATA_MOVEMENT', 'CLOUD_PROVIDER') = 'AWS' THEN 1000
      ELSE NULL
    END
  );
```

Create a rule that blocks agent-driven access:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT RULE hr_comp_agent_guard
  TYPE = 'AGENT_ACCESS'
  MAX_ROWS AS () RETURNS INTEGER -> (0);
```

Add this rule to a data movement policy to block agents from accessing table data.

### Create data movement policies

Group related rules into `ENFORCE_RULES` and `ALERT_RULES`:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT POLICY hr_comp_dmp_strict
  ENFORCE_RULES = (hr_comp_copy_guard, hr_comp_agent_guard)
  COMMENT = 'Block Compensation export and Agent access';

CREATE OR REPLACE DATA MOVEMENT POLICY hr_pii_dmp_guardrails
  ENFORCE_RULES = (hr_pii_copy_hard_boundary)
  ALERT_RULES = (hr_pii_copy_alert_budget)
  COMMENT = 'PII guardrails: alert >= 500, block >= 1000';
```

### Attach policies to tags and apply tags to tables

Attach each policy to the tag representing a sensitive data domain:

Copy code

```
ALTER TAG compensation_salary SET DATA MOVEMENT POLICY hr_comp_dmp_strict;
ALTER TAG pii_ssn_full SET DATA MOVEMENT POLICY hr_pii_dmp_guardrails;
ALTER TAG pii_contact_info SET DATA MOVEMENT POLICY hr_pii_dmp_guardrails;
```

Then apply those tags to the tables you want to protect.

### Attach a policy to the account

To apply a baseline policy to all tables and views not covered by a tag-based policy, attach it at
the account level:

Copy code

```
ALTER ACCOUNT SET DATA MOVEMENT POLICY <db_name>.<schema_name>.<policy_name>;
```

To replace an existing account-level policy:

Copy code

```
ALTER ACCOUNT SET DATA MOVEMENT POLICY <db_name>.<schema_name>.<policy_name> FORCE;
```

To remove the account-level policy:

Copy code

```
ALTER ACCOUNT UNSET DATA MOVEMENT POLICY;
```

### Validate configuration

Use `SHOW` commands to verify that rules, policies, and tags are configured as expected:

Copy code

```
SHOW DATA MOVEMENT RULES IN SCHEMA mydb.myschema;
SHOW DATA MOVEMENT POLICIES IN SCHEMA mydb.myschema;
SHOW TAGS LIKE 'PII_%' IN SCHEMA mydb.myschema;
```

## Operational best practices

Start with alert-only policies to understand current movement patterns, then introduce blocking rules incrementally:

1. Use `ALERT_RULES` with generous `MAX_ROWS` values to baseline movement on sensitive tables.
2. Add `ENFORCE_RULES` for high-risk domains, such as PII and compensation data.
3. Review alerts and adjust thresholds, tagging scope, and exception-role logic before expanding coverage.

When operating DMP at scale:

- Keep rule expressions simple and readable. Prefer straightforward `CASE` logic over deeply nested expressions.
- Test deterministic scenarios under, at, and above thresholds.
- Use explicit role-aware conditions, such as `SYS_CONTEXT('SNOWFLAKE$SESSION', 'ROLE')`, for approved exception roles.
- Use `SYS_CONTEXT('SNOWFLAKE$DATA_MOVEMENT', '<property>')` only with documented properties for the statement’s primary movement type.
- Define ownership up front. Decide which administrative role owns DMP rules and policies, and which roles can manage policy-tag bindings.
- Promote changes through environments. Validate representative workloads in non-production environments before production rollout.
- Use DMP with other governance controls, such as masking policies and row access policies, and Data Exfiltration Trust Center detections for defense-in-depth protection.

## Cloning

When a schema or database is cloned, data movement rules and policies are cloned as schema objects. However, cloned policies start with no rule associations: their `ENFORCE_RULES` and `ALERT_RULES` lists are empty. You must explicitly add rules to a cloned policy before attaching it.

Tag-to-policy bindings are preserved during a clone. If the policy was in the same schema or database that was cloned, the binding on the cloned tag is updated to reference the cloned policy. If the policy is in a different schema or database, the original policy reference is retained.

## GET\_DDL

`GET_DDL` is supported for both `DATA MOVEMENT RULE` and `DATA MOVEMENT POLICY` objects. The output follows the `CREATE OR REPLACE` syntax for each object type.

## Limitations

- Unload operations that use `PARTITION BY` are always blocked when DMP is active on the relevant tables, regardless of rule configuration.
- Cross-region share protection by DMP is not supported.
- `SYS_CONTEXT('SNOWFLAKE$DATA_MOVEMENT', ...)` returns values for the statement’s primary movement type only; properties for other movement types behave as not applicable (see [Movement types and precedence](#movement-types-and-precedence) and [SYS\_CONTEXT in movement rules](#label-dmp-movement-context-syscontext)).
- Row thresholds are evaluated per statement.
- Monitoring and telemetry views can be delayed. Latency may be up to 2 hours.
- Violation records are generated for each event. However, in rare cases, such as during service interruptions or periods of excessive violations, a record may not be captured. Because enforcement and recording are independent, a missing record doesn’t indicate that enforcement didn’t occur.
- Alert rules are not supported for `UI_DOWNLOAD` rules.
- `UI_DOWNLOAD` violations are not included in the `DATA_MOVEMENT_VIOLATIONS` account usage view. Because UI\_DOWNLOAD enforcement works by disabling the download button rather than blocking a download request, no policy violation event occurs.

## Reference: SQL commands

Use the following commands to manage DMP:

| Command | Description |
| --- | --- |
| [CREATE DATA MOVEMENT RULE](/sql-reference/sql/create-data-movement-rule) | Create a data movement rule. |
| [ALTER DATA MOVEMENT RULE](/sql-reference/sql/alter-data-movement-rule) | Modify a data movement rule. |
| [DROP DATA MOVEMENT RULE](/sql-reference/sql/drop-data-movement-rule) | Remove a data movement rule. |
| [CREATE DATA MOVEMENT POLICY](/sql-reference/sql/create-data-movement-policy) | Create a data movement policy. |
| [ALTER DATA MOVEMENT POLICY](/sql-reference/sql/alter-data-movement-policy) | Modify a data movement policy, including adding or removing rules. |
| [DROP DATA MOVEMENT POLICY](/sql-reference/sql/drop-data-movement-policy) | Remove a data movement policy. |
| [SHOW DATA MOVEMENT RULES](/sql-reference/sql/show-data-movement-rules) | List data movement rules. |
| [SHOW DATA MOVEMENT POLICIES](/sql-reference/sql/show-data-movement-policies) | List data movement policies. |
| [DESCRIBE DATA MOVEMENT RULE](/sql-reference/sql/desc-data-movement-rule) | Show the definition of a data movement rule. |
| [DESCRIBE DATA MOVEMENT POLICY](/sql-reference/sql/desc-data-movement-policy) | Show the definition of a data movement policy. |
| [ALTER TAG](/sql-reference/sql/alter-tag) | Attach or detach a data movement policy on a tag (`SET / UNSET DATA MOVEMENT POLICY`). |
| [ALTER ACCOUNT](/sql-reference/sql/alter-account) | Attach or detach an account-level data movement policy (`SET / UNSET DATA MOVEMENT POLICY`). |

Expand

Show lessSee more

## Manage data movement policies (CRUD)

The following workflow shows how to create, inspect, update, and remove data movement policies and rules.

### Set context

Use an administrative role and set the target database and schema:

Copy code

```
USE ROLE ACCOUNTADMIN;
USE DATABASE <db_name>;
USE SCHEMA <schema_name>;
```

### Create

Create rules first, then create a policy, then attach the policy to a tag:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT RULE pii_copy_enforce_rule
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (800);

CREATE OR REPLACE DATA MOVEMENT RULE pii_copy_alert_rule
  TYPE = 'COPY_INTO_EXTERNAL_STAGE'
  MAX_ROWS AS () RETURNS INTEGER
  -> (500);

CREATE OR REPLACE DATA MOVEMENT RULE pii_agent_access_enforce_rule
  TYPE = 'AGENT_ACCESS'
  MAX_ROWS AS () RETURNS INTEGER
  -> (0);

CREATE OR REPLACE DATA MOVEMENT RULE pii_ui_download_enforce_rule
  TYPE = 'UI_DOWNLOAD'
  MAX_ROWS AS () RETURNS INTEGER
  -> (100);

CREATE OR REPLACE DATA MOVEMENT RULE pii_programmatic_fetch_enforce_rule
  TYPE = 'PROGRAMMATIC_FETCH'
  MAX_ROWS AS () RETURNS INTEGER
  -> (1000);

CREATE OR REPLACE DATA MOVEMENT RULE pii_programmatic_fetch_alert_rule
  TYPE = 'PROGRAMMATIC_FETCH'
  MAX_ROWS AS () RETURNS INTEGER
  -> (500);

CREATE OR REPLACE DATA MOVEMENT POLICY pii_data_policy
  ENFORCE_RULES = (pii_copy_enforce_rule, pii_agent_access_enforce_rule,
                   pii_ui_download_enforce_rule, pii_programmatic_fetch_enforce_rule)
  ALERT_RULES = (pii_copy_alert_rule, pii_programmatic_fetch_alert_rule)
  COMMENT = 'PII guardrails: alert at 500, block above 800; block agent access; disable UI download above 100 rows; alert at 500 and block programmatic fetch above 1000';

ALTER TAG pii_tag SET DATA MOVEMENT POLICY pii_data_policy;
```

To apply a baseline policy to the entire account instead of, or in addition to, a tag-based policy:

Copy code

```
ALTER ACCOUNT SET DATA MOVEMENT POLICY pii_data_policy;
```

### Read

Use SHOW and DESCRIBE commands to inspect policy and rule definitions:

Copy code

```
SHOW DATA MOVEMENT RULES IN SCHEMA <db_name>.<schema_name>;
SHOW DATA MOVEMENT POLICIES IN SCHEMA <db_name>.<schema_name>;
SHOW DATA MOVEMENT POLICIES IN ACCOUNT;

DESCRIBE DATA MOVEMENT RULE pii_copy_enforce_rule;
DESCRIBE DATA MOVEMENT POLICY pii_data_policy;

SHOW TAGS IN SCHEMA <db_name>.<schema_name>;
```

### Update

To change behavior, update rule logic or set rule references in a policy:

Copy code

```
ALTER DATA MOVEMENT RULE pii_copy_enforce_rule
  SET MAX_ROWS AS () RETURNS INTEGER
  -> (1000);

CREATE OR REPLACE DATA MOVEMENT RULE pii_ui_alert_rule
  TYPE = 'SNOWSIGHT_UI'
  MAX_ROWS AS () RETURNS INTEGER
  -> (100);

ALTER DATA MOVEMENT POLICY pii_data_policy
  SET ALERT_RULES = (pii_copy_alert_rule, pii_ui_alert_rule);

ALTER DATA MOVEMENT POLICY pii_data_policy
  SET ALERT_RULES = (pii_copy_alert_rule);
```

### Delete

Use a dependency-safe order:

1. Detach policy from tags and/or the account.
2. Remove rule mappings from policy.
3. Drop policy.
4. Drop rules.

Copy code

```
ALTER TAG pii_tag UNSET DATA MOVEMENT POLICY pii_data_policy;
ALTER ACCOUNT UNSET DATA MOVEMENT POLICY;

ALTER DATA MOVEMENT POLICY pii_data_policy
  REMOVE ENFORCE_RULES = (pii_copy_enforce_rule, pii_agent_access_enforce_rule,
                          pii_ui_download_enforce_rule, pii_programmatic_fetch_enforce_rule);
ALTER DATA MOVEMENT POLICY pii_data_policy
  REMOVE ALERT_RULES = (pii_copy_alert_rule, pii_programmatic_fetch_alert_rule);

DROP DATA MOVEMENT POLICY IF EXISTS pii_data_policy;

DROP DATA MOVEMENT RULE IF EXISTS pii_copy_enforce_rule;
DROP DATA MOVEMENT RULE IF EXISTS pii_copy_alert_rule;
DROP DATA MOVEMENT RULE IF EXISTS pii_agent_access_enforce_rule;
DROP DATA MOVEMENT RULE IF EXISTS pii_ui_download_enforce_rule;
DROP DATA MOVEMENT RULE IF EXISTS pii_programmatic_fetch_enforce_rule;
DROP DATA MOVEMENT RULE IF EXISTS pii_programmatic_fetch_alert_rule;
```

### Operational checks

- If a policy drop fails, verify that the policy is detached from all tags.
- If a rule drop fails, verify that no policy still references the rule.
- If behavior is unexpected, verify the active role and movement type.

## Reference: Account Usage views

The following views provide information about data movement policies, rules, and violations.
These views are available in both the ACCOUNT\_USAGE and ORGANIZATION\_USAGE schemas.
Organization usage must be enabled for the account to access these views.

### DATA\_MOVEMENT\_POLICIES view

Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

This Account Usage view displays a row for each data movement policy defined in your account.

#### Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the data movement policy. |
| NAME | VARCHAR | Name of the data movement policy. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the policy. |
| SCHEMA | VARCHAR | Schema of the data movement policy. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database of the policy. |
| DATABASE | VARCHAR | Database of the data movement policy. |
| OWNER | VARCHAR | Name of the role that owns the data movement policy. |
| COMMENT | VARCHAR | Comment for the data movement policy. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the data movement policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the data movement policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the data movement policy was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of the role that owns the object, for example `ROLE` or `DATABASE_ROLE`. |

Expand

Show lessSee more

#### Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
- The view only displays objects for which the current role for the session has been granted access privileges.

### DATA\_MOVEMENT\_POLICY\_RULES view

Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

This Account Usage view displays a row for each data movement rule defined in your account.

#### Columns

| Column name | Data type | Description |
| --- | --- | --- |
| ID | NUMBER | Internal/system-generated identifier for the data movement rule. |
| NAME | VARCHAR | Name of the data movement rule. |
| SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema of the rule. |
| SCHEMA | VARCHAR | Schema of the data movement rule. |
| DATABASE\_ID | NUMBER | Internal/system-generated identifier for the database of the rule. |
| DATABASE | VARCHAR | Database of the data movement rule. |
| OWNER | VARCHAR | Name of the role that owns the data movement rule. |
| OWNER\_ROLE\_TYPE | VARCHAR | Type of the role that owns the object, for example `ROLE` or `DATABASE_ROLE`. |
| COMMENT | VARCHAR | Comment for the data movement rule. |
| MOVEMENT\_TYPE | VARCHAR | Type of movement the rule applies to: `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `AGENT_ACCESS`, `SNOWSIGHT_UI`, `UI_DOWNLOAD`, `PROGRAMMATIC_FETCH`, or `UNKNOWN`. |
| FUNCTION\_SIGNATURE | VARCHAR | Parameter signature for the rule function. |
| FUNCTION\_BODY | VARCHAR | SQL expression body of the rule. |
| FUNCTION\_RETURN\_TYPE | VARCHAR | Return data type of the rule function. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the data movement rule was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the data movement rule was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the data movement rule was dropped. |

Expand

Show lessSee more

#### Usage notes

- Latency for the view may be up to 2 hours.
- The view only displays objects for which the current role for the session has been granted access privileges.

### DATA\_MOVEMENT\_VIOLATIONS view

Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

This Account Usage view displays a row for each query that violated a data movement policy in your account.
Each row consolidates all triggered policies across potentially many tables into a single entry keyed by query ID.

#### Columns

| Column name | Data type | Description |
| --- | --- | --- |
| QUERY\_ID | VARCHAR | ID of the query that violated a data movement policy. |
| ENFORCED\_POLICY | VARCHAR | FQN of the enforced rule and corresponding policy triggered by the query. NULL if no enforce rule was triggered. |
| MOVEMENT\_TYPE | VARCHAR | Movement type of the statement that triggered the violation. Possible values: `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `SNOWSIGHT_UI`, `AGENT_ACCESS`, `PROGRAMMATIC_FETCH`. `UI_DOWNLOAD` violations are not included in this view. |
| ALERTED\_POLICIES | VARCHAR | FQNs of alert rules and corresponding policies triggered by the query. |
| USER\_NAME | VARCHAR | Name of the user that ran the query. |
| DATA\_ENTITIES | ARRAY | FQNs of the tables involved in the query. |
| TIMESTAMP | TIMESTAMP\_LTZ | Timestamp of the query. |

Expand

Show lessSee more

#### Usage notes

- Latency for the view may be up to 3 hours.

### DATA\_MOVEMENT\_RULE\_REFERENCES view

Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

This Account Usage view displays a row for each rule-to-policy mapping in your account, showing which rules are assigned to which policies and whether each rule is in the enforce or alert list.

#### Columns

| Column name | Data type | Description |
| --- | --- | --- |
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the data movement policy. |
| POLICY\_NAME | VARCHAR | Name of the data movement policy. |
| POLICY\_DATABASE | VARCHAR | Database of the data movement policy. |
| POLICY\_SCHEMA | VARCHAR | Schema of the data movement policy. |
| RULE\_ID | NUMBER | Internal/system-generated identifier for the data movement rule. |
| RULE\_NAME | VARCHAR | Name of the data movement rule. |
| RULE\_DATABASE | VARCHAR | Database of the data movement rule. |
| RULE\_SCHEMA | VARCHAR | Schema of the data movement rule. |
| RULE\_MOVEMENT\_TYPE | VARCHAR | Movement type of the rule: `COPY_INTO_EXTERNAL_STAGE`, `COPY_INTO_INTERNAL_STAGE`, `AGENT_ACCESS`, `SNOWSIGHT_UI`, `UI_DOWNLOAD`, `PROGRAMMATIC_FETCH`, or `UNKNOWN`. |
| RULE\_CATEGORY | VARCHAR | Whether the rule is in the enforce or alert list: `ENFORCE` or `ALERT`. |

Expand

Show lessSee more

#### Usage notes

- Latency for the view may be up to 3 hours.
- The view only displays objects for which the current role for the session has been granted access privileges.
- Only active rule-to-policy mappings are included. Mappings removed by `ALTER DATA MOVEMENT POLICY REMOVE ENFORCE_RULES` or `REMOVE ALERT_RULES` are excluded.
