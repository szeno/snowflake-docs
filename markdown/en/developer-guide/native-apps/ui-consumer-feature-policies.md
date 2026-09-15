# Use feature policies to limit the objects an app can create

This topic describes how to use feature policies to limit the objects that a Snowflake Native App
can create. For information about creating and managing feature policies — including privileges
required, replication, and account-level management — see
[Feature policies](/user-guide/feature-policies).

## About feature policies for native apps

If an app is configured to use
[automated granting of privileges](/developer-guide/native-apps/requesting-auto-privs), the app can request to use
the following privileges:

- EXECUTE TASK
- EXECUTE MANAGED TASK
- CREATE WAREHOUSE
- CREATE COMPUTE POOL
- BIND SERVICE ENDPOINT
- CREATE DATABASE
- CREATE EXTERNAL ACCESS INTEGRATION

If the app is configured to use these privileges, a consumer cannot directly revoke these privileges
after the app is installed. However, consumer administrators can use feature policies
to limit the objects an app can create in the consumer account.

For example, if a consumer does not want an app to create warehouses or compute pools, a consumer account
administrator can create a feature policy that prohibits a particular app or all apps from
creating warehouses or compute pools.

Feature policies also let consumers block many other object types, including Cortex Agents and
MCP servers, which apps can create without requesting account-level privileges. For more
information about app-created agents and MCP servers, see
[Use Cortex Agents and MCP servers in an app](/developer-guide/native-apps/agents-mcp-servers). For the full list of blockable object
types, see [Blockable object types](/user-guide/feature-policies#label-feature-policy-blockable-object-types).

Warning

Blocking object types that an app requires for installation or upgrade may prevent the app from
functioning properly.

Note

External access integrations can’t be blocked using feature policies. Instead, consumers
can choose to approve or decline the endpoints for an app using app specifications.

## Workflow

The general workflow for using feature policies to limit the objects an app can create is:

1. View the listing for the app to determine the privileges the app is
   requesting.
2. Create a feature policy to block the objects you want to restrict.

   For more information, see [Feature policies](/user-guide/feature-policies).
3. Apply the feature policy to the account or to a specific app.

   For more information, see [Assign a feature policy at the account level](#label-native-apps-feature-policy-assign-account) and
   [Apply a feature policy to a specific app](#label-native-apps-feature-policy-assign-object).

## Assign a feature policy at the account level

Consumers can apply a feature policy to all apps in the account by using the
[ALTER ACCOUNT](/sql-reference/sql/alter-account) command, as shown in the following example:

Copy code

```
ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.block_create_db_policy
  FOR ALL APPLICATIONS;
```

This command applies the `block_create_db_policy` policy for any app that is installed
in the account. After applying this policy, apps can no longer create databases.

To unapply the policy from all apps:

Copy code

```
ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL APPLICATIONS;
```

## Apply a feature policy to a specific app

To apply a feature policy when creating an app manually, use the `WITH FEATURE POLICY` clause of the
[CREATE APPLICATION](/sql-reference/sql/create-application) command,
as shown in the following example:

Copy code

```
CREATE APPLICATION hello_snowflake_app
  WITH FEATURE POLICY = feature_policy_db.sch.block_create_db_policy;
```

To apply a feature policy to an existing app, use the
[ALTER APPLICATION](/sql-reference/sql/alter-application) command,
as shown in the following example:

Copy code

```
ALTER APPLICATION hello_snowflake_app
  SET FEATURE POLICY feature_policy_db.sch.block_create_db_policy;
```

To unapply a feature policy from a specific app:

Copy code

```
ALTER APPLICATION hello_snowflake_app UNSET FEATURE POLICY;
```

## View feature policies on an app

To view the feature policies applied to a specific app:

Copy code

```
SHOW FEATURE POLICIES ON APPLICATION hello_snowflake_app;
```
