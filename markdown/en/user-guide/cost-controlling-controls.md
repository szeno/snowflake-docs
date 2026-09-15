# Cost controls for warehouses

This topic discusses *controls* that you can use to limit how much is spent on [virtual warehouse](/user-guide/warehouses-overview)
usage. These controls help ensure that the actual cost of using virtual warehouses does not exceed expected cost.

These controls do not apply to [cloud services](/user-guide/cost-understanding-compute#label-cloud-services-credit-usage) and
[serverless features](/user-guide/cost-understanding-compute#label-serverless-credit-usage).

## Control access to warehouses

Carefully defining who can work with warehouses and what they can do with those warehouses helps control cost by limiting compute resource
usage to known warehouses that have cost-effective configurations. Snowflake’s granular
[access control](/user-guide/security-access-control-overview) allows you to grant the following privileges for warehouses:

- **CREATE WAREHOUSE** — Global privilege (that is, granted on the account) that restricts which roles can create a new warehouse, allowing
  you to force individuals to use existing warehouses that have cost controls in place.
- **MODIFY** — Privilege on a specific warehouse that allows changing the settings that affect cost, including resizing a warehouse and
  disabling the [auto-suspend](#label-cost-control-auto-suspend) setting. Commonly, users increase the size of a warehouse for a
  particular workload and then forget to change it back to its original size, which can have a significant effect on cost.
- **USAGE** — Privilege on a specific warehouse that allows activating the warehouse to provide compute resources for queries and other
  SQL actions. Carefully assigning this privilege ensures that users can only use warehouses with the appropriate size and configuration
  for their workloads.

Centralizing the responsibility of creating and scaling warehouses to just a few members of your team is considered a best practice. You can
create a dedicated role with permissions to create and modify all warehouses, and then grant that role to a limited number of users. This
allows you to control your warehouse policies and prevent accidental cost overruns resulting from warehouses being created or upsized
unexpectedly.

Tip

If you want the ability to scale a warehouse to handle more demanding workloads, but do not want to give users the ability to increase
the size of a warehouse because they might forget to resize it later, consider using a
[multi-cluster warehouse](/user-guide/warehouses-multicluster). A multi-cluster warehouse scales automatically as workloads
fluctuate.

For a list of all the privileges that can be set for a warehouse, see [Virtual warehouse privileges](/user-guide/security-access-control-privileges#label-warehouse-privileges).

## Limit query times

Hung queries consume excessive credits because they run longer than expected. To avoid the excess cost associated with a
runaway query, you can set the `STATEMENT_TIMEOUT_IN_SECONDS` parameter to define the maximum amount of time a SQL statement can run
before it is canceled.

The `STATEMENT_TIMEOUT_IN_SECONDS` parameter can be set for an entire account, a user, a session, or a specific warehouse so that you can
carefully set time limits that match the expected run times for various workloads. This parameter is set at the account level by default.
When the parameter is set for a warehouse in addition to the session, the lowest non-zero value is enforced.

Use the following commands to view the current query time limits:

Copy code

```
SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN ACCOUNT;
SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN USER <username>;
SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN SESSION;
SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN WAREHOUSE <warehouse_name>;
```

If you need to adjust the time limits, use one of the following commands:

Copy code

```
ALTER ACCOUNT SET STATEMENT_TIMEOUT_IN_SECONDS = <number_of_seconds>;
ALTER USER <username> SET STATEMENT_TIMEOUT_IN_SECONDS = <number_of_seconds>;
ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = <number_of_seconds>;
ALTER WAREHOUSE <warehouse_name> SET STATEMENT_TIMEOUT_IN_SECONDS = <number_of_seconds>;
```

## Limit statement queue times

SQL statements that are in a queue to use a warehouse do not consume credits. However, if a query stays in the queue too long, it might no
longer be relevant by the time it executes. Running a query that is no longer relevant wastes credits, so you can implement a
cost control by setting a maximum amount of time that a SQL statement can be queued before it is canceled.

The parameter that controls the amount of time that a SQL statement stays in the queue is `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS`. This
parameter can be set for an entire account, a user, a session, or a specific warehouse. This parameter is set at the account level by
default. When the parameter is set for a warehouse in addition to the session, the lowest non-zero value is enforced.

Use the following commands to view the current queue time limits:

Copy code

```
SHOW PARAMETERS LIKE 'STATEMENT_QUEUED_TIMEOUT_IN_SECONDS' IN ACCOUNT;
SHOW PARAMETERS LIKE 'STATEMENT_QUEUED_TIMEOUT_IN_SECONDS' IN USER <username>;
SHOW PARAMETERS LIKE 'STATEMENT_QUEUED_TIMEOUT_IN_SECONDS' IN SESSION;
SHOW PARAMETERS LIKE 'STATEMENT_QUEUED_TIMEOUT_IN_SECONDS' IN WAREHOUSE <warehouse_name>;
```

If you need to adjust the time limits, use one of the following commands:

Copy code

```
ALTER ACCOUNT SET STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <number_of_seconds>;
ALTER USER <username> SET STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <number_of_seconds>;
ALTER SESSION SET STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <number_of_seconds>;
ALTER WAREHOUSE <warehouse_name> SET STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <number_of_seconds>;
```

## Use auto-suspension

By default, all warehouses have the auto-suspend setting enabled, which means a warehouse automatically shuts down when it is inactive
for a defined period of time. A suspended warehouse does not consume credits, so the warehouse only incurs cost when it is processing a
workload.

Restricting users from disabling the auto-suspend setting helps to prevent an unused warehouse from wasting credits. You can use
[access control](#label-cost-control-access-control) to allow someone to use a warehouse but also prevent them from modifying its Auto
Suspend setting.

**Query: Find warehouses without auto-suspend**

Use the following query to periodically check whether the auto-suspend setting was disabled for any warehouses.

Copy code

```
SHOW WAREHOUSES
  ->> SELECT "name" AS WAREHOUSE_NAME,
             "size" AS WAREHOUSE_SIZE
        FROM $1
        WHERE IFNULL("auto_suspend", 0) = 0;
```

To enable auto-suspend for the warehouses that have it turned off, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). In the navigation menu, select **Compute** » **Warehouses**. You can also use the `AUTO_SUSPEND` parameter of the [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) command.

### Using auto-resume with auto-suspend

In general, every warehouse that has auto-suspend enabled should also have auto-resume enabled. The combination of these two settings
stops and starts a warehouse automatically as the warehouse’s workload fluctuates.

**Query: Find warehouses without Auto Resume**

The following query lists the warehouses that do not have auto-resume enabled, letting you know which ones need to be modified.

Copy code

```
SHOW WAREHOUSES
  ->> SELECT "name" AS WAREHOUSE_NAME,
             "size" AS WAREHOUSE_SIZE
        FROM $1
        WHERE "auto_resume" = 'false';
```

To enable auto-resume for the warehouses that have it turned off, sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in). In the navigation menu, select **Compute** » **Warehouses**. You can also use the `AUTO_RESUME` parameter of the [ALTER WAREHOUSE](/sql-reference/sql/alter-warehouse) command.

## Enforce spending limits

*Resource monitors* provide the ability to set limits on credits consumed by a warehouse during a specific time interval or date range.
This can help prevent warehouses from unintentionally consuming more credits than typically expected.

Sometimes a resource monitor simply notifies an administrator when a credit limit is reached, but you can also *enforce* a limit by
configuring a resource monitor to suspend a warehouse as soon as the limit is reached. There are two options when enforcing a limit: suspend
the warehouse after pending statements are executed or suspend immediately without waiting for statements to complete.

Because a single resource monitor can be set for multiple warehouses or an entire account, you can effectively suspend multiple warehouses
when an overall spending limit is reached. A warehouse can be assigned to its own resource monitor and an account-specific resource monitor
at the same time; the warehouse is suspended when either of the credit limits is reached.

For more information about suspending warehouses when spending limits are reached, see [Working with resource monitors](/user-guide/resource-monitors).

**Query: Find warehouses without resource monitors**

The following query lists the warehouses that aren’t assigned to a warehouse-specific resource monitor, which makes them vulnerable
to runaway costs. The query doesn’t check for account-level resource monitors; warehouses in the list that belong to an account
that has an account-level resource monitor are still subject to credit limits.

Copy code

```
SHOW WAREHOUSES
  ->> SELECT "name" AS WAREHOUSE_NAME,
             "size" AS WAREHOUSE_SIZE
        FROM $1
        WHERE "resource_monitor" = 'null';
```

Note

The cloud services layer of the Snowflake architecture can still incur a small cost if queries are run against a warehouse that was
suspended by a resource monitor.
