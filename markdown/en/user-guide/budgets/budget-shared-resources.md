# Using budgets for AI features (shared resources)

A shared resource is a Snowflake resource that is used by more than one business unit or team. AI features (such as AI Functions, Snowflake CoWork, Cortex Agents, Cortex Code, and the AI Gateway) are examples of shared resources. You can add these resources to a budget and configure the budget so that credits consumed by them count toward the budget’s spending limit only when selected users consume those credits. This enables tracking and controlling usage across different teams or cost centers.

For example, suppose multiple teams use the same AI function. You can track consumption for each of the teams in separate budgets based
on which users are calling the function — one budget for engineering users and another for finance users.

## Workflow for tracking consumption by shared resources

Tracking consumption by a shared resource based on the user who is using the resource consists of the following workflow:

1. [Apply a tag-value pair to a user](#label-budget-shared-resource-apply-tag) who uses the shared resource.
2. [Add to the budget the tag-value pair that you applied to the user](#label-budget-shared-resource-add-tag).
3. [Add the shared resource to the budget](#label-budget-shared-resource-add-resource).

## Apply a tag to a user

A [tag](/user-guide/object-tagging/introduction) is a schema-level object that can be applied to another object. When you apply a
tag to an object, you can set the tag to a value, thereby creating a tag-value pair.

You can group users into logical units such as cost centers by applying the same tag-value pair to each of the users. The first step in
tracking consumption of shared resources is to apply a tag-value pair to every user that belongs to a unit. You can then use a budget to
track consumption by these users while ignoring the consumption of the same shared resource by other users.

Use the [ALTER USER](/sql-reference/sql/alter-user) command to apply a tag to users. Suppose you use the `cost_center` tag to identify cost
centers within your organization, and that the user `joe` belongs to the cost center `finance`. To apply the correct tag-value pair to
the user, run the following command:

Copy code

```
ALTER USER joe SET TAG cost_management.tags.cost_center = 'FINANCE';
```

Tip

If you want to automate user tagging, you can provision users through a SCIM identity provider and
use the `snowflakeTags` attribute to apply tags automatically when users are created or updated.
For more information, see [Automating user tags with SCIM](/user-guide/cost-attributing#label-cost-attribute-scim).
For provider-specific setup steps, see:

- [SCIM with Microsoft Entra ID](/user-guide/scim-azure)
- [SCIM with Okta](/user-guide/scim-okta)
- [SCIM with a custom identity provider](/user-guide/scim-custom)

## Add the user tag to the budget

After tagging all users in the logical unit, you must add the tag-value pair to the budget so it can track consumption by the users. Use
the [SET\_USER\_TAGS](/sql-reference/classes/budget/methods/set_user_tags) method to add the tag to the budget.

In the following example, when a shared resource consumes credits, the `finance_budget` budget will only track consumption by users with
the `cost_center = 'FINANCE'` tag-value pair.

Copy code

```
CALL finance_budget!SET_USER_TAGS(
  [
    [(SELECT SYSTEM$REFERENCE('TAG', 'COST_MANAGEMENT.TAGS.COST_CENTER', 'SESSION', 'APPLYBUDGET')),
    'FINANCE']
  ],
  'UNION');
```

The SET\_USER\_TAGS method lets you add all of your user tags to the budget at once. It also lets you configure the budget so that usage is
included if a user is tagged with *any* of the user tags (UNION) or configure it so usage is included only if the user is tagged with *all*
of the user tags (INTERSECTION).

In the following example, the `my_budget` budget tracks consumption when shared resources are acted upon by users tagged with *both*
the tag-value combination `cost_center = 'sales'` and the tag-value combination `project = 'phoenix'`.

Copy code

```
CALL budget_db.budget_schema.my_budget!SET_USER_TAGS(
  [
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.cost_center', 'SESSION', 'APPLYBUDGET')), 'SALES'],
    [(SELECT SYSTEM$REFERENCE('TAG', 'cost_mgmt_db.tags.project', 'SESSION', 'APPLYBUDGET')), 'PHOENIX']
  ],
  'INTERSECTION');
```

To verify the results of the method, call the [GET\_BUDGET\_SCOPE](/sql-reference/classes/budget/methods/get_budget_scope) method.

## Add AI features (shared resources) to a budget

After you have configured the users who are using AI features, you must specify which of these features will be tracked by the budget.
Use the [ADD\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/add_shared_resource) method to add an AI feature to the budget.

Supported AI feature domains include:

- `AI FUNCTION` — Model inference functions
- `CORTEX CODE` — Cortex Code workloads (CLI, Snowsight)
- `CORTEX AGENT` — Cortex agent-based workflows
- `SNOWFLAKE INTELLIGENCE` — Snowflake CoWork workloads
- `AI GATEWAY` — Cortex AI Gateway

  [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

  Available to all accounts.

Tip

You can use the [SYSTEM$SHOW\_BUDGET\_SHARED\_RESOURCE\_CANDIDATES](/sql-reference/functions/system_show_budget_shared_resource_candidates) function to return a list of resources that can be added as
shared resources to a budget.

**Example: Add all AI functions to the budget**

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('AI FUNCTION');
```

---

**Example: Add the AI\_CLASSIFY function to the budget**

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('AI FUNCTION', 'AI_CLASSIFY');
```

**Example: Add a specific Cortex Agent to the budget**

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE(
     'CORTEX AGENT',
     (SELECT SYSTEM$REFERENCE('CORTEX AGENT', 'myagent'))
);
```

**Example: Add a specific Snowflake CoWork resource to the budget**

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE(
     'SNOWFLAKE INTELLIGENCE',
     (SELECT SYSTEM$REFERENCE('SNOWFLAKE INTELLIGENCE', 'my_si'))
);
```

Note

For the SNOWFLAKE INTELLIGENCE domain, specifying an explicit object reference in ADD\_SHARED\_RESOURCE is optional as there is only one Snowflake CoWork object per account.

### Add the AI Gateway

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Add the AI Gateway by domain. Each account has a single gateway, named `SNOWFLAKE`, so the domain
covers it.

Copy code

```
CALL finance_budget!ADD_SHARED_RESOURCE('AI GATEWAY');
```

## Creating a budget for AI workloads in Snowsight

You can create and configure budgets for AI workloads directly in Snowsight using a guided user interface.

Note

Using tags to define the scope of a budget is required for shared resources such as AI workloads.

1. Sign in to Snowsight.
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select the **Budgets** tab.
4. Select **+ Budget** on the top right corner.
5. On the **Basic Information** page, complete the required fields.
6. On the **Budget scope** page, add the objects that you want to include in the budget.
7. For setting budgets on AI features (shared resources), move to the **Budgets Scope** page and update as follows.

   In the **Tags on users** section:

   - Search for and select relevant tags (for example, cost center or team).
   - This enables tracking activity for tagged users, which is required when monitoring shared resources.
   - Select AI resources to monitor.

   In the **Select resources to monitor** section, enable one or more of the following:

   - **AI Functions**
   - **Cortex Code**
   - **Cortex Agents**
   - **AI Gateway**

     [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open

     Available to all accounts.
   - **Snowflake CoWork**
8. Configure AI Functions.

   - By default, all AI functions are selected, and future AI functions are automatically included.
   - You can also choose to selectively choose specific functions (for example, `AI_CLASSIFY`, `AI_COMPLETE`). For a complete list, see [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql).
9. Configure Cortex Code.

   - By default, future Cortex Code interfaces are automatically included.
   - You can also choose to select specific instances (for example, `CLI`, `Snowsight`).
10. Configure Snowflake CoWork.

    - By default, all Snowflake CoWork workloads are automatically included.
    - You can also choose to select a specific Snowflake CoWork.
11. Configure Cortex Agents.

    - By default, all Cortex Agents are automatically included.
    - You can also choose to select specific Cortex Agent.
12. Configure AI Gateway.

    - The account’s single gateway, `SNOWFLAKE`, is selected by default. There’s nothing to choose.
13. Review your selections.

Confirm that the correct resources are selected, ensure that any selected tags correctly reflect the intended scope.

14. Complete the remaining configuration and click **Create**

Note

- AI workloads are tracked as shared resources and are attributed based on user activity and applied tags.
- Selecting **All (auto)** ensures that new instances for the domain are automatically included as they become available.

## Limitations and considerations

- For AI functions, the budget tracks the AI\_SERVICES service type.

## Related methods

- [ADD\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/add_shared_resource)
- [GET\_SHARED\_RESOURCES](/sql-reference/classes/budget/methods/get_shared_resources)
- [REMOVE\_SHARED\_RESOURCE](/sql-reference/classes/budget/methods/remove_shared_resource)
- [SET\_USER\_TAGS](/sql-reference/classes/budget/methods/set_user_tags)
