# Using budgets for warehouses (shared resources)

Warehouses are typically the largest compute domain in a Snowflake account and are commonly
shared across multiple business units or teams. You can add warehouses to a budget as a shared
resource and configure it so that credits consumed by them count toward the budget’s spending
limit only when selected users run queries on those warehouses. This enables tracking and
controlling warehouse usage across different teams or cost centers.

For example, suppose multiple teams run queries on the same warehouse. You can track consumption
for each team in separate budgets based on which users are executing queries: one budget for the
engineering team and another for the finance team.

This feature extends the same user-level sharing model that is already generally available for
AI Functions, Cortex Code, Cortex Agents, and Snowflake CoWork. For the general workflow
(tagging users and adding user tags to the budget), see
[Using budgets for AI features (shared resources)](/user-guide/budgets/budget-shared-resources).

Important

Warehouse attribution has product-specific behaviors that differ meaningfully from AI feature
domains. Before using this feature, review the [Usage notes](#label-wh-budget-usage-notes)
section below, especially the sections on attribution semantics and data latency.

## Add warehouses to a budget

After you have configured the users who are using the warehouse, you must specify which warehouses
will be tracked by the budget. Use the
[ADD\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/add_shared_resource) method.

Tip

To see all warehouses available in your account, run [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses).

**Example: Add all warehouses to the budget**

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('WAREHOUSE');
```

The `finance_budget` tracks consumption across all warehouses for users who are tagged with the
tag-value pair added to the budget. Future warehouses are automatically included.

---

**Example: Add a specific warehouse to the budget**

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE(
    'WAREHOUSE',
    (SELECT SYSTEM$REFERENCE('WAREHOUSE', 'SNOWADHOC')));
```

The `finance_budget` tracks consumption by the `SNOWADHOC` warehouse, but only for users who
are tagged with the tag-value pair that was added to the budget.

Note

Warehouses are object instances, so the second argument must be a `SYSTEM$REFERENCE` to the
specific warehouse rather than a plain warehouse name.

## Creating a budget for warehouses in Snowsight

You can create and configure budgets for warehouses directly in Snowsight using a guided user
interface.

Note

Using tags to define the scope of a budget is required for shared resources such as warehouses.

1. Sign in to Snowsight.
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select the **Budgets** tab.
4. Select **+ Budget** in the top right corner.
5. On the **Basic Information** page, complete the required fields.
6. On the **Budget scope** page, add the objects that you want to include in the budget.
7. For setting budgets on warehouses, move to the **Budget scope** page and update as follows.

   In the **Tags on users** section:

   - Search for and select relevant tags (for example, cost center or team).
   - This enables tracking activity for tagged users, which is required when monitoring shared
     resources.

   In the **Select resources to monitor** section, enable **Warehouses**.
8. Configure warehouses.

   - By default, all warehouses are selected, and any warehouses created in the future are
     automatically included.
   - To track only specific warehouses, select them individually.
9. Review your selections.

   Confirm that the correct warehouses are selected and that the selected tags correctly reflect
   the intended scope.
10. Complete the remaining configuration and click **Create**.

After configuration, the Budget details page lists the selected warehouses under the
shared-resources section, confirming that the warehouse is now in scope for the budget’s
measurement.

## Usage notes

A budget with user-scoped shared warehouses measures a subset of total warehouse spend,
because not all warehouse costs can be attributed to individual users. Data freshness also
differs from other budget types. For details, see
[Attribution semantics](#label-wh-budget-attribution) and
[Data freshness](#label-wh-budget-pipeline) below.

### Attribution semantics

This warehouse budget tracks a user’s share of interactively issued query costs:
**not** their share of total warehouse cost. The following types of spend are not attributed
to individual users and are therefore not included in the budget measurement:

- **Idle time**: warehouse uptime between queries cannot be attributed to any user.
- **Very short queries**: queries below a minimum duration threshold are not tracked.
- **Overhead costs**: some warehouse-level costs, such as cloud services credits, are not
  broken down per user.
- **Automated workloads**: tasks, dynamic table refreshes, materialized view refreshes, and
  similar system-initiated work do not have an end-user identity to attribute.

These are the same attribution boundaries documented for the
[QUERY\_ATTRIBUTION\_HISTORY](/sql-reference/account-usage/query_attribution_history) view.

**When a warehouse is in scope as both a direct resource and a shared resource, the direct
resource measurement takes precedence.** If a warehouse is added to a budget both via a
resource tag and via `ADD_SHARED_RESOURCE`, the budget counts the warehouse’s spend once,
through the direct path. The user-scoped portion is not added on top.

### Data freshness

Data for warehouse budgets is available with higher latency than other budget types.
For shared warehouses (this feature), data freshness is up to 11 hours for standard budgets and up to 6 hours for low-latency budgets.

Plan alert thresholds and reporting cadences accordingly.

**Spend for long-running queries is recorded when the query completes.** A query does not
appear in the budget until it finishes, so the effective delay for a long-running query
may exceed the figures above.

**Configuration changes take up to approximately 2 hours to reflect.** After you add or remove
a shared warehouse, or change the user-tag set, expect up to approximately 2 hours before the
next budget measurement reflects the updated configuration.

## Limitations and considerations

- For warehouses, the budget tracks the `WAREHOUSE_METERING` and `QUERY_ACCELERATION`
  service types.
- A warehouse budget measures only the portion of warehouse spend attributable
  to individual users. See [Attribution semantics](#label-wh-budget-attribution) above.
- End-to-end data freshness for shared warehouses is up to approximately 11 hours for standard
  budgets and up to 6 hours for low-latency budgets. See
  [Data freshness](#label-wh-budget-pipeline) above for details.
- Configuration changes (adding/removing warehouses or user tags) take up to approximately
  2 hours to reflect in budget measurements.

## Related methods

- [ADD\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/add_shared_resource)
- [GET\_SHARED\_RESOURCES](/sql-reference/classes/budget/methods/get_shared_resources)
- [REMOVE\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/remove_shared_resource)
- [SET\_USER\_TAGS](/sql-reference/classes/budget/methods/set_user_tags)
