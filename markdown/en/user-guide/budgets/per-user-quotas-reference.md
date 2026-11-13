# Per-user quota method reference

The following tables list the methods available on a quota object. Call each method using the
syntax `<quota_name>!<METHOD>(...)`. For detailed descriptions, parameters, and examples, see the
linked sections.

## Create a quota

Use the following command to create a quota:

| Command | Description |
| --- | --- |
| `CREATE SNOWFLAKE.CORE.QUOTA <name>()` | Create a per-user quota object. See [Create a quota with SQL](/user-guide/budgets/per-user-quotas-create#label-per-user-quota-create). |

Expand

Show lessSee more

## Monitored domains

Use the following methods to choose what the quota monitors:

| Method | Description |
| --- | --- |
| `ADD_SHARED_RESOURCE('<domain>'[, '<resource>'])` | Add a monitored domain, or a specific resource within a domain, to the quota. See [Supported domains](/user-guide/budgets/per-user-quotas#label-per-user-quota-supported-resources). |
| `REMOVE_SHARED_RESOURCE('<domain>'[, '<resource>'])` | Remove a monitored domain, or a specific resource within a domain, from the quota. See [REMOVE\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/remove_shared_resource). |

Expand

Show lessSee more

## User scope

Use the following methods to define and inspect which users the quota covers:

| Method | Description |
| --- | --- |
| `SET_USER_TAGS([[<tag_ref>, '<value>'], ...], '<operator>')` | Scope the quota to users selected by tag. The operator (`UNION` or `INTERSECTION`) is required. See [Scope users with tags](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-tag-scope). |
| `SET_USER_TAGS([], 'ALL_USERS')` | Return the quota to all users. Pass an empty tag array. Also clears tag exclusions. See [Scope users with tags](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-tag-scope). |
| `EXCLUDE_USERS('TAG', [[<tag_ref>, '<value>'], ...])` | Replace the tag exclusions. Users matching any of the given tags are removed from the scope. See [Exclude users by tag](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-exclude-by-tag). |
| `INCLUDE_USERS(['<user>', ...])` | Add specific users to the quota by name, or reverse an earlier exclusion. See [Include or exclude individual users](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-user-membership). |
| `EXCLUDE_USERS('USER', ['<user>', ...])` | Exclude specific users from the quota by name. See [Include or exclude individual users](/user-guide/budgets/per-user-quotas-user-scope#label-per-user-quota-user-membership). |
| `GET_QUOTA_SCOPE()` | Return the attached monitored domains, the users included and excluded by name, and the configured user tags and operator. |
| `GET_USERS()` | Return the users currently resolved into the quota’s scope. |

Expand

Show lessSee more

## Spending limits

Use the following methods to set and read per-user limits:

| Method | Description |
| --- | --- |
| `SET_PER_USER_LIMIT(<credits>[, '<cycle>'])` | Set the per-user credit limit. The value must be a whole number from 1 to 1,000,000,000; zero, negative, `NULL`, and decimal values return an error. The optional cycle argument accepts `'WEEKLY'` or `'DAILY'`; the default is monthly. See [Set per-user spending limits](/user-guide/budgets/per-user-quotas-create#label-per-user-quota-spending-limit). |
| `UNSET_PER_USER_LIMIT('<cycle>')` | Remove the per-user limit for a cycle: `'MONTHLY'`, `'WEEKLY'`, or `'DAILY'`. The cycle is required. |
| `GET_CONFIG()` | Return the quota configuration, including `PER_USER_LIMIT`, `PER_USER_LIMIT_WEEKLY`, `PER_USER_LIMIT_DAILY`, and `BLOCK_ENFORCEMENT_ENABLED`. |

Expand

Show lessSee more

## Enforcement

Use the following methods to manage and review block enforcement:

| Method | Description |
| --- | --- |
| `SET_BLOCK_ENFORCEMENT_ENABLED(<enabled>, <notify_user>)` | Turn built-in block enforcement on or off. The first Boolean argument enables or disables enforcement. The second Boolean argument specifies whether users are emailed when they’re blocked. See [Block users at the limit](/user-guide/budgets/per-user-quotas-enforcement#label-per-user-quota-enforcement). |
| `GET_ACTIVE_BLOCKS_V2()` | Return the users currently blocked by this quota. |
| `GET_ENFORCEMENT_HISTORY('<start>', '<end>')` | Return the blocking and unblocking history for this quota over a date range. |

Expand

Show lessSee more

## Notifications

Use the following methods to manage user notifications and admin summaries:

| Method | Description |
| --- | --- |
| `ADD_NOTIFICATION_THRESHOLD(<threshold>, '<strategy>', <notify_user>, '<cycle>')` | Add an individual-user notification threshold. The cycle accepts `'MONTHLY'`, `'WEEKLY'`, or `'DAILY'`. See [Configure notifications](/user-guide/budgets/per-user-quotas-notifications#label-per-user-quota-notifications). |
| `REMOVE_NOTIFICATION_THRESHOLD(<threshold>, '<strategy>')` | Remove a notification threshold. |
| `GET_NOTIFICATION_THRESHOLDS()` | List configured notification thresholds. |
| `ADD_NOTIFICATION_INTEGRATION('<name>')` | Add a notification integration for admin summaries. |
| `REMOVE_NOTIFICATION_INTEGRATION('<name>')` | Remove a notification integration. |
| `GET_NOTIFICATION_INTEGRATIONS()` | List configured notification integrations. |
| `SET_ADMIN_EMAILS('<email>, ...')` | Set admin summary email recipients. |

Expand

Show lessSee more

## Custom actions

Use the following methods to manage stored procedures that run at thresholds:

| Method | Description |
| --- | --- |
| `ADD_CUSTOM_ACTION(<sproc_ref>, <args>, '<strategy>', <threshold>)` | Register a stored procedure to run when a threshold is crossed. See [Configure custom actions](/user-guide/budgets/per-user-quotas-notifications#label-per-user-quota-custom-actions). |
| `REMOVE_CUSTOM_ACTIONS([<threshold>[, '<sproc_fqn>']])` | Remove all custom actions, those at a threshold, or a specific procedure at a threshold. |
| `GET_CUSTOM_ACTIONS()` | List configured custom actions. |
| `CONFIRM_CUSTOM_ACTIONS_ACCESS()` | Verify the quota’s owner role can invoke the configured procedures. |

Expand

Show lessSee more

## Cycle-start action

Use the following methods to manage the procedure that runs at the start of each month:

| Method | Description |
| --- | --- |
| `SET_CYCLE_START_ACTION(<sproc_ref>, <args>)` | Set the procedure to run at the start of each UTC calendar month. See [Configure a cycle-start action](/user-guide/budgets/per-user-quotas-notifications#label-per-user-quota-cycle-start). |
| `GET_CYCLE_START_ACTION()` | Return the configured cycle-start action. |
| `REMOVE_CYCLE_START_ACTION()` | Remove the cycle-start action. |

Expand

Show lessSee more

## View spending

Use the following methods to review spending:

| Method | Description |
| --- | --- |
| `GET_SPENDING_DETAILS_BY_USERS('<start>', '<end>')` | Return finalized per-user usage for a date range. See [View user spending](/user-guide/budgets/per-user-quotas-monitor#label-per-user-quota-view-spending). |
| `SNOWFLAKE.LOCAL.MY_BUDGET_SUMMARY()` | Return the calling user’s limits, usage, and block status for each of their quotas. Any user can call it. See [Check your quota usage](/user-guide/budgets/per-user-quotas-monitor#label-per-user-quota-check-quota-usage). |

Expand

Show lessSee more

## Related content

- [Per-user quotas](/user-guide/budgets/per-user-quotas)
- [Create and configure a per-user quota](/user-guide/budgets/per-user-quotas-create)
- [Specify users in scope for a per-user quota](/user-guide/budgets/per-user-quotas-user-scope)
- [Block users at a per-user quota limit](/user-guide/budgets/per-user-quotas-enforcement)
- [Notifications and actions for per-user quotas](/user-guide/budgets/per-user-quotas-notifications)
- [Monitor per-user quota spending](/user-guide/budgets/per-user-quotas-monitor)
