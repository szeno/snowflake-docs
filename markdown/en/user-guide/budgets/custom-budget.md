# Custom budgets

Custom budgets let you monitor compute costs for a custom group of objects. You can specify which objects you want to monitor in two ways:

- Add a tag to the budget. All objects that have the specified tag/value pair are monitored by the budget.
- Add each object to the budget individually.

The same budget can track objects added individually and added using tags. If an object is included in the budget for more than one reason (for
example, it was added individually and has the specified tag/value pair), its credit usage counts only once against the budget’s
spending limit.

When you add an object to a custom budget, the budget monitors all compute costs for the object, including background
maintenance operations and serverless features. For example, if you add a table to a custom budget, and the table has automatic
clustering enabled, the budget monitors credit usage for the background maintenance for automatic clustering.

## Using tags to monitor objects

[Tags](/user-guide/object-tagging/introduction) can be applied to budgets to monitor credit usage by objects that belong to a logical
unit within the account. Suppose you use the `cost_center` tag to track costs incurred by cost centers within the organization. You
might tag all objects attributed to the sales team with the tag/value pair `cost_center = 'sales'`. Rather than individually add
each object used by the sales team to a budget, you could simply add the tag/value pair `cost_center = 'sales'`, and the budget
will automatically monitor credit usage of all objects that have been assigned that tag/value pair.

Tip

If you want to automate user tagging, you can provision users through a SCIM identity provider and
use the `snowflakeTags` attribute to apply tags automatically when users are created or updated.
For more information, see [Automating user tags with SCIM](/user-guide/cost-attributing#label-cost-attribute-scim).
For provider-specific setup steps, see:

- [SCIM with Microsoft Entra ID](/user-guide/scim-azure)
- [SCIM with Okta](/user-guide/scim-okta)
- [SCIM with a custom identity provider](/user-guide/scim-custom)

### Tag inheritance

Adding a tag to a budget tracks all objects with that tag, including objects that have inherited the tag from a parent object. For example,
if a database has a tag, then tables within the database inherit the tag and will be tracked by a budget. Because a budget tracks usage
based on a tag/value pair, if you override the value of the tag at the table-level, it might change whether the budget tracks usage
associated with the table. For example, suppose you have a budget that tracks objects with tag `team = 'eng'`. If the database has the
tag `team = 'eng'`, but a table within the database has tag `team = 'IT'`, the budget won’t monitor costs associated with that table.

In the context of budgets, tags are not inherited from an account because the account budget is intended to fulfill that use case.

For more information, including how tag values are overridden, see [Tag inheritance](/user-guide/object-tagging/inheritance).

### Tracking an object with multiple budgets

Multiple budgets can add the same tag/value pair, which means more than budget can track credit usage of the same object. For
example, suppose you add the tag `cost_center = 'eng'` to both `budget_1` and `budget_2`. As a warehouse with tag
`cost_center = 'eng'` consumes credits, it will count toward the credit limit of both `budget_1` and `budget_2`.

An object can also be tracked by more than one budget if the object has multiple tags. For example, suppose a warehouse
has two tags: `cost_center = 'finance'` and `stage = 'dev'`. You could create one budget that tracks `cost_center = 'finance'` and
another that tracks `stage = 'dev'`. Credits consumed by the warehouse would count toward the credit limit of both budgets.

### Limitations and considerations

When using tags to monitor objects, keep the following in mind:

- When you change a tag on an object, it can take up to six hours for the change to be reflected in budgets that use tags.
- Currently, alerts cannot be monitored with tags. You must add them individually.
- Changes to tags within the first two days of the month are reflected in the prior month’s usage.

## Supported objects for custom budgets

You can create a custom budget to monitor the following types of Snowflake objects:

| Object | Monitored costs |
| --- | --- |
| Alerts | Serverless alerts are monitored by the account budget. To monitor the credit usage for an alert that executes using a user-managed warehouse, you must add the warehouse to the budget. For more information about the costs of alerts, see [Understanding the costs of alerts](/user-guide/alerts#label-alerts-costs). |
| Apps   (Snowflake Native Apps) | The behavior of budgets for objects that are created and owned by an Snowflake Native App depends on whether you add the app directly or by adding a tag.   - When you add a Snowflake Native App to a budget using tags, only warehouses that have the matching tag/value combination are tracked   automatically, regardless of whether they are shared. - When you add a Snowflake Native App to a budget directly, all objects that consume credits and are created and owned by the app are   added to the budget automatically. This includes warehouses and Snowpark Container Services compute pools that are owned by   the app. Warehouses and compute pools that are shared are not tracked by the budget automatically, although you can   add these manually.   You cannot add objects created and owned by an app to a separate budget. You can add warehouses and compute pools that are shared to a separate budget.  To determine if a warehouse or compute pool is owned by an app, check the following:   - For warehouses, run the [SHOW WAREHOUSES](/sql-reference/sql/show-warehouses) command. If the value in the `owner_role_type` column   is `APPLICATION`, the warehouse is owned by a Snowflake Native App. - For compute pools, run the [SHOW COMPUTE POOLS](/sql-reference/sql/show-compute-pools) command. If the value in the `application`   column is not NULL, the compute pool is owned by a Snowflake Native App. |
| Compute pool | Compute pool usage for Snowpark Container Services. For more information, see [Compute pool cost](/developer-guide/snowpark-container-services/accounts-orgs-usage-views#label-compute-pool-cost). |
| Cortex Agent | Orchestration and tool usage. For more information, see [Cost considerations](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agent-cost-considerations). |
| Databases | When you add a database to a budget, all supported objects that the database contains are also automatically added. The budget monitors credit usage for the following objects and serverless features:   - Supported schema objects as described above. - Replication for secondary (replica) databases.   Note    Replication costs for secondary databases that are replicated in a replication or failover group can only be monitored by the account budget. |
| Materialized views | Background maintenance for the materialized view. For more information, see [Materialized Views Cost](/user-guide/views-materialized#label-materialized-views-maintenance-billing). |
| Schemas | When you add a schema to a budget, all supported objects that the schema contains are also automatically added. The budget monitors the credit usage for schema objects as described above. |
| Pipes | Resource consumption for loading data using Snowpipe. For more information, see [Snowpipe costs](/user-guide/data-load-snowpipe-billing). |
| Snowflake CoWork | Snowflake CoWork interactions, including orchestration and tool usage. |
| Tables | Background maintenance operations for [automatic clustering](/user-guide/tables-auto-reclustering) and [search optimization](/user-guide/search-optimization-service) if they are enabled on the table. |
| Tasks | Serverless tasks are monitored by a custom budget. To monitor the credit usage for a task that executes using a user-managed warehouse, you must add the warehouse to the budget. For more information, see [Task costs](/user-guide/tasks-intro#label-billing-task-runs). |
| Warehouses | Compute resources for query execution, web interface, and other features (see [Virtual warehouse credit usage](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage)), serverless tasks, and [cloud services compute](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage). |

Expand

Show lessSee more

For more information, see [Add or remove tags from a custom budget](#label-custom-budgets-add-tags).

## Create a custom budget

The next sections explain how to create a custom budget:

- [Create a custom role to create budgets](#label-custom-budgets-owner-role)
- [Use Snowsight to create a custom budget](#label-ui-create-custom-budget)
- [Use SQL commands to create a custom budget](#label-create-custom-budget-sql)

You can create a custom budget using Snowsight or by executing SQL statements.

### Create a custom role to create budgets

You can use a custom role to create budgets in your account. For a full list of privileges and roles that must be granted to a
role to create a custom budget, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

The following example creates a role named `budget_owner` role and grants the required role and privileges to create custom
budgets in the schema `budgets_db.budgets_schema`. The example must be executed using the ACCOUNTADMIN role:

Copy code

```
USE ROLE ACCOUNTADMIN;
   
CREATE ROLE budget_owner;
  
GRANT USAGE ON DATABASE budgets_db TO ROLE budget_owner;
GRANT USAGE ON SCHEMA budgets_db.budgets_schema TO ROLE budget_owner;

GRANT DATABASE ROLE SNOWFLAKE.BUDGET_CREATOR TO ROLE budget_owner;

GRANT CREATE SNOWFLAKE.CORE.BUDGET ON SCHEMA budgets_db.budgets_schema
  TO ROLE budget_owner;
```

If you want to enable a role other than the budget owner to modify a custom budget’s settings, you can create a custom role with
modify privileges. For more information, see [Create a custom role to manage a custom budget](#label-custom-budgets-admin-role).

### Use Snowsight to create a custom budget

Note

If the account budget is not [activated](/user-guide/budgets/account-budget#label-activate-account-budget) or has
been deactivated, you can’t use Snowsight to create custom budgets. However, you
can [create custom budgets using SQL](#label-create-custom-budget-sql).

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select the **Budgets** tab.
4. Select **+ Budget**.
5. On the **Basic Information** page, complete the following steps:

   1. From the **Location to store** drop-down, select the name of the database and schema where you want to create the budget.
   2. In the **Name** field, specify the name of the custom budget.
   3. In the **Budget (credits per month)** field, specify the spending limit of the budget.
   4. To decrease the [budget refresh interval](/user-guide/budgets#label-budgets-refresh-interval) so you can watch spending more closely, select
      **Enable low latency budget**.
   5. In the **Threshold** field, specify a percentage of the budget limit. Notifications are sent when Snowflake determines that
      spending will exceed this percentage of the budget limit.
   6. In the **Notify** field, enter email addresses to receive notification emails.

      Note

      Each email address added for budget notifications must be [verified](/user-guide/notifications/email-notifications#label-email-notification-verify-address). The
      notification email setup fails if any email address in the list is *not* verified.
   7. Select **Next**.
6. On the **Budget scope** page, add the objects that you want to add to the custom budget.

   - If you are [using tags](#label-custom-budget-about-tags) to track consumption by objects, compete the following steps:

     1. Select the **Tags on resources** drop-down list.
     2. Find the appropriate tag, then expand it and select one or more values.
     3. Select **Done**.
   - If you are adding individual objects to the budget, complete the following steps:

     1. Select the **Resources** drop-down list.
     2. Select one or more objects.
     3. Select **Done**.

        Note

        If you are directly adding individual objects, you can only add an object to one custom budget. In this case, if an object is currently
        included in one custom budget and you add that object to a second custom budget, Budgets removes the object from the first custom budget
        without issuing a warning.

        This behavior does not apply to using tags to add objects to budgets; an object with one or more tags can be
        included in multiple custom budgets if you are using tags to add the object to the budgets.
7. Select **Create**.

After you create and set up a custom budget, you can create a custom role to enable non-account administrators to monitor budget resources
and usage. For more information, see [Create a custom role to monitor a custom budget](/user-guide/budgets/monitor#label-custom-budgets-monitor-role).

### Use SQL commands to create a custom budget

Create a custom budget and then set the spending limit and notification email addresses.

Note

- To create a custom budget, you must use a role with the
  [required privileges to create a budget](#label-custom-budgets-owner-role).
- To modify a custom budget, you must use a role with the
  [required privileges to modify a budget](#label-custom-budgets-admin-role).

1. Review the existing budgets in your account:

   Note

   The following statement returns the budgets for which you have access privileges. Only a user with the ACCOUNTADMIN role
   can see all the budgets in the account.

   Copy code

   ```
   SELECT SYSTEM$SHOW_BUDGETS_IN_ACCOUNT();
   ```
2. Create budget `my_budget` in `budgets_db.budgets_schema` using the
   [CREATE BUDGET](/sql-reference/classes/budget/commands/create-budget) command:

   Copy code

   ```
   USE SCHEMA budgets_db.budgets_schema;

   CREATE SNOWFLAKE.CORE.BUDGET my_budget();
   ```
3. Set the monthly spending limit. For example, set the spending limit to 500 credits per month:

   Copy code

   ```
   CALL my_budget!SET_SPENDING_LIMIT(500);
   ```
4. Set up notifications for the budget so that you receive notifications when your credit usage is expected to exceed your
   spending limits.

   See [Notifications for budgets](/user-guide/budgets/notifications).

After you create and set up a custom budget, you can create a custom role to enable non-account administrators to monitor budget
resources and usage. For more information, see [Create a custom role to monitor a custom budget](/user-guide/budgets/monitor#label-custom-budgets-monitor-role).

To add objects to your new budget, see [Add or remove objects from a custom budget](#label-modifying-objects-in-custom-budgets).

## Create a custom role to manage a custom budget

To monitor and modify a custom budget, you can grant privileges and instance roles to a custom role. For a full list of privileges
and roles that must be granted to a role to modify a custom budget, see [Budgets roles and privileges](/user-guide/budgets#label-budgets-roles-and-privileges).

### Custom role example

Grant the custom role `budget_admin` the ability to monitor and modify the budget `my_budget` in schema
`budgets_db.budgets_schema`:

Note

You need OWNERSHIP privilege on the custom budget to execute the following examples.

- Grant the required privileges and instance role to custom role `budget_admin` for budget `my_budget` in schema
  `budgets_db.budgets_schema`:

  Copy code

  ```
  GRANT USAGE ON DATABASE budgets_db TO ROLE budget_admin;

  GRANT USAGE ON SCHEMA budget_db.budgets_schema TO ROLE budget_admin;

  GRANT SNOWFLAKE.CORE.BUDGET ROLE budgets_db.budgets_schema.my_budget!ADMIN
  TO ROLE budget_admin;

  GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE budget_admin;
  ```
- Grant the APPLYBUDGET privilege on objects and tags to be added to or removed from a custom budget. This step is required for each object
  or tag to be added or removed.

  For example, to enable the role `budget_admin` to add database `db1` to custom budget `my_budget`,
  execute the following statements:

  Copy code

  ```
  GRANT USAGE ON DATABASE db1 TO ROLE budget_admin;

  GRANT APPLYBUDGET ON DATABASE db1 TO ROLE budget_admin;
  ```

## Add or remove tags from a custom budget

You can add or remove tags from a custom budget using Snowsight or SQL. Each tag added to the budget includes one or more values
for the tag.

Note

To add or remove tags from a custom budget, you must use a role with the required privileges on the budget and the tag. For more
information, see [Create a custom role to manage a custom budget](#label-custom-budgets-admin-role).

### Use Snowsight to add or remove tags from a custom budget

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select **Budgets**.
4. Select the budget to edit.
5. In the dashboard, select [![Pencil icon](/static/images/snowsight/icons/pencil-icon.svg)](/static/images/snowsight/icons/pencil-icon.svg) (edit icon).
6. Select **+ Tags & resources**.
7. Expand **Tags** and navigate to the tag you want to add.
8. Do one of the following:

   - If the tag has a [list of allowed values](/user-guide/object-tagging/work#label-object-tagging-specify-tag-values), select one or more of the values.
   - If the tag can be set to any value, specify the value.
9. Select **Done**.

Note

When adding tags to the budget in Snowsight, keep the following in mind:

- A tag must be applied to at least one object before you can add it to a budget.
- It can take up to two hours for a tag to appear after adding it to an object.

### Use SQL commands to add or remove tags from a custom budget

The role used to add or remove an tag from a budget must have the APPLYBUDGET privilege on the tag. For more information, see the examples
in the [Create a custom role to manage a custom budget](#label-custom-budgets-admin-role) section.

To review the list of tags already in the custom budget, call the budget’s
[<budget\_name>!GET\_RESOURCE\_TAGS](/sql-reference/classes/budget/methods/get_resource_tags) method. For example, to see the list of tags in the budget
`my_budget` in the `budgets_db.budgets_schema` schema, execute the following statement:

Copy code

```
CALL budgets_db.budgets_schema.my_budget!GET_RESOURCE_TAGS();
```

Tags must be added to or removed from a budget by [reference](/sql-reference/references).

1. You can add tag `cost_mgmt_db.tags.cost_center` to budget `my_budget` by using the following steps:

   1. Grant the APPLYBUDGET privilege on the tag to the role `budget_admin` by executing the following statement:

      Copy code

      ```
      GRANT APPLYBUDGET ON TAG cost_center TO ROLE budget_admin;
      ```
   2. Pass a reference for tag `cost_center` to the [ADD\_RESOURCE\_TAG](/sql-reference/classes/budget/methods/add_resource_tag) instance
      method by executing the following statement. The value of the tag is set to `finance`.

      Copy code

      ```
      CALL budgets_db.budgets_schema.my_budget!ADD_RESOURCE_TAG(
         SELECT SYSTEM$REFERENCE('TAG',
      'cost_mgmt_db.tags.cost_center',
      'SESSION',
      'applybudget'),
      'finance');
      ```

      The [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function creates a reference for the tag `cost_center`, with the
      APPLYBUDGET privilege granted on the tag. This enables the budget to monitor the objects in your account that have the specified
      tag/value pair in your account. The third parameter to the function specifies the scope for the reference; in this
      case, ‘SESSION’ creates a reference with session scope. References passed to the ADD\_RESOURCE\_TAG method for a budget can be created
      with any transient reference scope (that is, the third parameter can be either ‘SESSION’ or ‘CALL’).
2. You can remove the tag *cost\_center* from the budget `my_budget` by using the following steps:

   1. Grant the APPLYBUDGET privilege on the database to the role `budget_admin` by executing the following statement:

      Copy code

      ```
      GRANT APPLYBUDGET ON TAG cost_center TO ROLE budget_admin;
      ```
   2. Remove the tag by passing a reference to the [REMOVE\_RESOURCE\_TAG](/sql-reference/classes/budget/methods/remove_resource_tag)
      instance method:

      Copy code

      ```
      CALL budgets_db.budgets_schema.my_budget!REMOVE_RESOURCE_TAG(
         SELECT SYSTEM$REFERENCE('TAG',
      'cost_mgmt_db.tags.cost_center',
      'SESSION',
      'applybudget'),
      'finance');
      ```

## Add or remove objects from a custom budget

You can add or remove objects from a custom budget using Snowsight or SQL.

Note

To add or remove objects from a custom budget, you must use a role with the required privileges on the budget and the object. For more
information, see [Create a custom role to manage a custom budget](#label-custom-budgets-admin-role).

### Use Snowsight to add or remove objects from a custom budget

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Cost management**.
3. Select **Budgets**.
4. Select the budget to edit.
5. In the dashboard, select [![Pencil icon](/static/images/snowsight/icons/pencil-icon.svg)](/static/images/snowsight/icons/pencil-icon.svg) (edit icon).
6. Select **+ Tags & resources**, then select the objects you want to add to the custom budget.

   Note

   - When you select a database or schema, all [supported objects](#label-budgets-supported-objects) (for example, tables)
     contained within the database or schema are also added to the budget.
   - If you are directly adding individual objects, you can only add an object to one custom budget. In this case, if an object is currently
     included in one custom budget and you add that object to a second custom budget, Budgets removes the object from the first custom budget
     without issuing a warning.

     This behavior does not apply to using tags to add objects to budgets; an object with one or more tags can be
     included in multiple custom budgets if you are using tags to add the object to the budgets.
7. Select **Done**.

### Use SQL commands to add or remove objects from a custom budget

The role used to add or remove an object from a budget must have the APPLYBUDGET privilege on the object. For more information, see
the examples in the [Create a custom role to manage a custom budget](#label-custom-budgets-admin-role) section.

To review the list of objects already in the custom budget, call the budget’s
[<budget\_name>!GET\_LINKED\_RESOURCES](/sql-reference/classes/budget/methods/get_linked_resources) method. For example, to see the list of objects in the budget
`my_budget` in the `budgets_db.budgets_schema` schema, execute the following statement:

Copy code

```
CALL budgets_db.budgets_schema.my_budget!GET_LINKED_RESOURCES();
```

The statement returns the following output:

```
+-------------+-----------------+-----------+-------------+---------------+
| RESOURCE_ID | NAME            | DOMAIN    | SCHEMA_NAME | DATABASE_NAME |
|-------------+-----------------+-----------+-------------+---------------|
|         326 | DB1             | DATABASE  | NULL        | NULL          |
|         157 | MY_WH           | WAREHOUSE | NULL        | NULL          |
+-------------+-----------------+-----------+-------------+---------------+
```

Note

The list does not include:

- Objects that were added automatically (for example, compute pools and warehouses created and owned by a Snowflake Native App).
- Objects that were added when a tag was added to the budget.

Objects must be added to or removed from a budget by [reference](/sql-reference/references).

1. You can add table `t1` to budget `my_budget` by using the following steps:

   1. Grant the APPLYBUDGET privilege on the table to the role `budget_admin` by executing the following statement:

      Copy code

      ```
      GRANT APPLYBUDGET ON TABLE t1 TO ROLE budget_admin;
      ```
   2. Pass a reference for table `t1` to the [ADD\_RESOURCE](/sql-reference/classes/budget/methods/add_resource) instance
      method by executing the following statement:

      Copy code

      ```
      CALL budgets_db.budgets_schema.my_budget!ADD_RESOURCE(
         SELECT SYSTEM$REFERENCE('TABLE', 't1', 'SESSION', 'applybudget'));
      ```

      The [SYSTEM$REFERENCE](/sql-reference/functions/system_reference) function creates a reference for a TABLE object, `t1`, with the
      APPLYBUDGET privilege granted on the table. This enables the budget to monitor the specified object in your account. The
      third parameter to the function specifies the scope for the reference; in this
      case, ‘SESSION’ creates a reference with session scope. References passed to the ADD\_RESOURCE method for a budget can be created
      with any transient reference scope (that is, the third parameter can be either ‘SESSION’ or ‘CALL’).

      Note

      If you want to add a Snowflake Native App to a budget, when you call SYSTEM$REFERENCE, specify `'DATABASE'` (not `'APPLICATION'`)
      for the `object_type` argument.

      For a full list of objects and privileges, see [Supported object types and privileges for references](/sql-reference/references#label-references-supported-objects-and-privileges).

      Note

      If you are directly adding individual objects, you can only add an object to one custom budget. In this case, if an object is currently
      included in one custom budget and you add that object to a second custom budget, Budgets removes the object from the first custom budget
      without issuing a warning.

      This behavior does not apply to using tags to add objects to budgets; an object with one or more tags can be
      included in multiple custom budgets if you are using tags to add the object to the budgets.
2. You can remove the database `db1` from the budget `my_budget` by using the following steps:

   1. Grant the APPLYBUDGET privilege on the database to the role `budget_admin` by executing the following statement:

      Copy code

      ```
      GRANT APPLYBUDGET ON DATABASE db1 TO ROLE budget_admin;
      ```
   2. Remove the database by passing a reference to the [REMOVE\_RESOURCE](/sql-reference/classes/budget/methods/remove_resource)
      instance method:

      Copy code

      ```
      CALL budgets_db.budgets_schema.my_budget!REMOVE_RESOURCE(
         SELECT SYSTEM$REFERENCE('DATABASE', 'db1', 'SESSION', 'applybudget'));
      ```
