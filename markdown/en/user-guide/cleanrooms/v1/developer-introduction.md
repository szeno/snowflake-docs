# Snowflake Data Clean Rooms developer’s guide

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This topic provides guidelines for users who want to create or manage Snowflake Data Clean Rooms programmatically.

Snowflake exposes an API of stored procedures for creating and controlling clean rooms.
These stored procedures can be run in any interface that can access the Snowflake account associated with your clean room environment,
including Snowsight notebooks and worksheets, as well as the [Snowflake CLI](/developer-guide/snowflake-cli/index). These procedures can be called in
SQL or in any language supported by your Snowflake environment.

## Setting up your environment

Here are some tips for setting up your coding environment to use the clean rooms API effectively.

- [Development tools](#development-tools)
- [Coding setup](#coding-setup)
- [Setting up accounts, users, and roles](#setting-up-accounts-users-and-roles)
- [See what’s installed with the clean rooms environment](#see-what-s-installed-with-the-clean-rooms-environment)
- [Sample data](#sample-data)

### Development tools

Here are the main developer tools for clean rooms:

- **Coding environment:** Any coding environment that can run stored procedures in your Snowflake account will work. Most developers use
  worksheets in Snowsight (the browser-based tool) or the [Snowflake CLI](/developer-guide/snowflake-cli/index).
- **The clean rooms UI:** Use the clean rooms UI to configure, manage, or create clean rooms. Most clean room analysts use the UI rather
  than code, so it’s important to see and test the experience of your clean rooms in the UI. Additionally, there are a handful of
  [features that are available only in the clean rooms UI](/user-guide/cleanrooms/getting-started#label-dcr-web-app-api-comparison).
- **Snowsight** is useful to explore databases and other objects and search for objects.
- **Clean rooms API:** API documentation is divided into [provider](/user-guide/cleanrooms/provider) and
  [consumer](/user-guide/cleanrooms/consumer) topic pages.

### Coding setup

Here is how to set up your coding environment for clean rooms:

- [Required role and warehouse](#required-role-and-warehouse)
- [About the clean rooms API](#about-the-clean-rooms-api)
- [About clean room names in API procedures](#about-clean-room-names-in-api-procedures)

#### Required role and warehouse

The clean rooms API requires the SAMOOHA\_APP\_ROLE role for full API access. Ask your clean rooms administrator to
[grant you full API access](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-add-developers). Clean rooms also supports
[creating roles with access to a subset of API procedures](/user-guide/cleanrooms/manage-dcr-users#label-dcr-grant-limited-access).

You must use the clean rooms API in a warehouse that SAMOOHA\_APP\_ROLE can use. `app_wh` is one of a
[number of warehouses](/user-guide/cleanrooms/v1/installation-details#label-cleanrooms-installation-details-warehouses) with access to the API. Choose the appropriate warehouse
for your needs.

We recommend that you use an XS warehouse for general clean room editing, creation, or deletion commands. Consider using larger warehouses, or Snowpark-optimized warehouses, when running large analyses, such as machine learning workloads.

Copy code

```
-- Set up environment.
USE ROLE SAMOOHA_APP_ROLE;
USE WAREHOUSE app_wh;

-- Call your clean rooms API functions.
...
```

If you use any other warehouse, be sure to grant SAMOOHA\_APP\_ROLE usage on that warehouse:

Copy code

```
GRANT USAGE ON WAREHOUSE <your_warehouse> TO SAMOOHA_APP_ROLE;`
```

#### About the clean rooms API

Snowflake Data Clean Rooms exposes a set of stored procedures that let a provider create, configure, and share a clean room.
These procedures can be called in any command-line environment that supports Snowflake procedures, including notebooks, worksheets, and the
Snowflake CLI. The documentation here shows SQL usage, but you can also use Python or
[any other supported Snowflake language](/developer-guide/stored-procedure/stored-procedures-overview#label-stored-procedures-handler-languages).

Procedures exist inside the following schemas:

- *samooha\_by\_snowflake\_local\_db.provider* - [Provider-specific procedures](/user-guide/cleanrooms/provider). These procedures can be
  called only on clean rooms that were created in the current account.
- *samooha\_by\_snowflake\_local\_db.consumer* - [Consumer-specific procedures](/user-guide/cleanrooms/consumer). These procedures can be
  called only on clean rooms to which the current account was invited as a consumer.
- *samooha\_by\_snowflake\_local\_db.library* - General procedures called by either the clean room creator (provider) or a clean room
  collaborator (consumer). These procedures are documented in both the provider and consumer reference pages.

Some procedures have both provider and consumer versions. The results are appropriate to the schema: for example,
*provider.view\_cleanrooms* lists all clean rooms in the current account for which you are a provider, and *consumer.view\_cleanrooms* lists
all clean rooms in the current account for which you are a consumer. Be sure to call the procedure in the namespace that you need.

#### About clean room names in API procedures

Many clean room API procedures take a `cleanroom_name` argument.

- Use the clean room name if a clean room was **created using the API**. If used as part of a package name, replace spaces with underscores:

  Copy code

  ```
  -- Spaces work here:
  CALL samooha_by_snowflake_local_db.provider.describe_cleanroom('my code created clean room');

  -- Underscores required here:
  SHOW VERSIONS IN APPLICATION PACKAGE SAMOOHA_CLEANROOM_my_code_created_clean_room;
  ```
- Use the clean room ID if the clean room was **created using the clean rooms UI**.

You can see the clean room name and ID by calling `describe_cleanroom` or `view_cleanrooms`.

Clean rooms created using the API are labeled in the clean rooms UI as **Supported with Developer APIs**.

### Setting up accounts, users, and roles

You aren’t required to use the clean rooms UI to develop clean rooms: most clean room functionality is available by calling the API.
However, a few features are [available only in the UI](/user-guide/cleanrooms/getting-started#label-dcr-web-app-api-comparison), and some are
faster to perform in the UI. And because many users use the UI exclusively, it’s important to see how your clean room behaves in the UI.
Therefore, you should ask a clean room administrator to add you as a clean room manager or higher in the appropriate clean room accounts.

Depending on your use case, you might also want to set up an additional Snowflake account in different web hosting regions to test
[cross-cloud behavior](/user-guide/cleanrooms/v1/enabling-laf).

Name your test Snowflake accounts meaningfully to indicate their typical usage: for example, “Consumer account,”
“Provider account,” and “Cross-cloud account.” This can help when you have multiple test accounts and must choose an account on the clean
rooms login page.

#### Internal testing clean rooms

You can test a clean room during development by sharing the clean room with yourself. Such a clean room is called an *internal testing clean room*. Using a single account for both provider and consumer is convenient for quick feature testing.

To create an internal testing clean room, simply pass the provider account information to `provider.add_consumers` as the sole consumer.

Internal testing clean rooms have the following restrictions:

- **An internal testing clean room cannot later be shared with other accounts**. An internal testing clean room always is an internal
  testing clean room.
- **The following features are not supported in internal testing clean rooms:**

  - Provider activation
  - Provider-run analyses
  - Mounting or viewing request logs (`provider.mount_request_logs_for_all_consumers` or `provider.view_request_logs`)
  - Consumer-defined templates
  - Multi-provider analyses
  - Differential privacy

  If you want to test features that aren’t supported in an internal testing room, you must set up separate provider and consumer Snowflake
  accounts to test both sides of a clean room.

Download a [sample worksheet](/static/samples/clean-rooms/internal-testing-cleanroom.ipynb) that demonstrates using a clean room in a
single account for both provider and consumer.

### See what’s installed with the clean rooms environment

Snowflake Data Clean Rooms creates many local databases upon installation. You can find details about tasks and objects that are run or
installed with a clean room package in [Snowflake Data Clean Rooms: Installed objects](/user-guide/cleanrooms/v1/installation-details).

### Sample data

The clean rooms environment installs [a few sample datasets](/user-guide/cleanrooms/v1/installation-details#label-dcr-samooha-sample-database) you can use.

You can also [generate synthetic test data](/user-guide/synthetic-data) using Snowflake.

## Guidelines and recommendations

Here are some guidelines to avoid problems when working with clean rooms:

- [Confirm that you are using the same account in the clean rooms UI and in code](#confirm-that-you-are-using-the-same-account-in-the-clean-rooms-ui-and-in-code)
- [Clean room names vs clean room ID](#clean-room-names-vs-clean-room-id)
- [Update your clean room whenever you make UI changes](#update-your-clean-room-whenever-you-make-ui-changes)
- [Interoperability between clean rooms created in code or the UI](#interoperability-between-clean-rooms-created-in-code-or-the-ui)

### Confirm that you are using the same account in the clean rooms UI and in code

You often need to open a coding environment and the clean rooms UI for the same Snowflake account, for example, when creating a clean room
in code, then checking its appearance in the clean rooms UI. It’s important to confirm that you’re using the same Snowflake account in each.

Snowsight does not have a shortcut to open the clean rooms UI for the same account, or the reverse, so you must be sure to log in to the
same account in each environment.

### Clean room names vs clean room ID

When using the API, for procedures that take a clean room name argument, determine whether to use the clean room name or the clean room
ID as follows:

- If the clean room was created using the API, use the clean room **name**.
- If the clean room was created in the clean rooms UI, use the clean room **ID**. You can see both the clean room name and ID by calling
  `provider.view_cleanrooms` or `provider.describe_cleanroom`.

### Update your clean room whenever you make UI changes

When you change any clean room properties that affect the UI, call
`provider.create_or_update_cleanroom_listing` to propagate the changes.

### Interoperability between clean rooms created in code or the UI

When you create a clean room using the API, some features are not modifiable in the clean rooms UI. For example, you cannot add additional
templates, even stock Snowflake templates, in code for a UI-created clean room. You also cannot change the differential privacy settings.

## Troubleshooting

Here are some common troubleshooting tips:

- [Consumer can’t set join policies or perform other basic actions on a joined clean room](#consumer-can-t-set-join-policies-or-perform-other-basic-actions-on-a-joined-clean-room)
- [Can’t find a clean room that you created](#can-t-find-a-clean-room-that-you-created)
- [Unknown function](#unknown-function)
- [See if a user has installed a clean room](#see-if-a-user-has-installed-a-clean-room)
- [Check your query or analysis history](#check-your-query-or-analysis-history)

### Consumer can’t set join policies or perform other basic actions on a joined clean room

Confirm that you installed your clean room with the proper role (SAMOOHA\_APP\_ROLE). If you didn’t use SAMOOHA\_APP\_ROLE when installing the clean room, you’ll encounter many problems, typically permission errors. If this is the case, even `consumer.uninstall_cleanroom` will fail and you must take extra steps to uninstall then reinstall the clean room with the correct role.

Copy code

```
-- Who owns the clean room?
SHOW SHARES LIKE 'SAMOOHA_CLEANROOM_REQUESTS_<cleanroom_name>';

-- If the owner role is not SAMOOHA_APP_ROLE, you must drop the share, then
-- uninstall the clean room.
DROP SHARE SAMOOHA_CLEANROOM_REQUESTS_<cleanroom_name>;
CALL samooha_by_snowflake_local_db.consumer.uninstall_cleanroom($cleanroom_name);
USE ROLE SAMOOHA_APP_ROLE;
CALL samooha_by_snowflake_local_db.consumer.install_cleanroom($cleanroom_name, '<provider_locator>');
```

### Can’t find a clean room that you created

If you created a clean room in one account but can’t see it in the collaborator’s account, here are some possible reasons:

- The clean room was created in a different cloud hosting region and you haven’t enabled
  [cross-cloud auto-fulfillment](/user-guide/cleanrooms/v1/enabling-laf).
- You didn’t publish your clean room by calling `provider.create_or_update_cleanroom_listing`.
- You are calling `consumer.view_cleanrooms()` instead of `provider.view_cleanrooms()` (or the reverse).
- You didn’t share the clean room, you shared the clean room with the wrong account, or you opened the wrong collaborator account in the
  Snowsight/Clean rooms UI/CLI. Confirm that the account where you expect to see your clean room is the one that you shared the clean room
  with, and that you’re signed in to that shared account.
- There is a small delay between publishing a clean room and when it becomes visible to the collaborator.

### Unknown function

If you call a procedure and get an error something like the following snippet:

```
Unknown user-defined function SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.CONSUMER.<procedure name>
```

Here are a few possible causes:

You typed the wrong namespace.
:   Be sure to call the proper `consumer` or `provider` version of your procedure. Many procedures have both provider and consumer
    versions.

You mistyped the name of the function.
:   Check the reference guide for the proper naming.

You have been granted a limited-access run-role, and the function you called isn’t allowed by your role.
:   Test this by running the following SQL code:

    Copy code

    ```
    USE DATABASE samooha_by_snowflake_local_db;
    CALL IS_DATABASE_ROLE_IN_SESSION('samooha_run_role');
    ```

    If the code snippet returns TRUE, you have limited-access [run-role](/user-guide/cleanrooms/manage-dcr-users#label-dcr-grant-limited-access) permissions on the clean
    room API. If you need greater access, ask a clean room administrator for full access. See the list of permitted run-role procedures in
    the [consumer.grant\_run\_on\_cleanrooms\_to\_role documentation](/user-guide/cleanrooms/consumer#label-dcr-sproc-consumer-manage-role-access).

You don’t have SAMOOHA\_APP\_ROLE
:   To see if you can use the SAMOOHA\_APP\_ROLE, run the following command:

    Copy code

    ```
    -- Get current user name.
    SELECT current_user();

    -- Add current user name in place as indicated.
    SHOW GRANTS TO USER <current_user_name> ->> select * from $1 where "role" = 'SAMOOHA_APP_ROLE';
    ```

    If you don’t get any results, ask an administrator to give you API access to the clean room.

### See if a user has installed a clean room

You can check if a given user has installed a given clean room by running the following SQL code. Replace `$consumer_locator` and
`$cleanroom_name` with the consumer locator and clean room name.

Copy code

```
SELECT * FROM snowflake.data_sharing_usage.application_state
  WHERE consumer_account_locator = $consumer_locator
    AND CONTAINS(package_name, UPPER(REPLACE($cleanroom_name, ' ', '_')));
```

### Check your query or analysis history

You can see your query history for analyses run in the UI or in code. These histories are stored and checked separately.

#### UI analysis history

The clean rooms UI shows a list of all previous analyses for this account in the **Analyses & Queries** page. These results
are only for queries run in the UI.

If you modify or delete a clean room, the analysis reports in the UI for that clean room will be deleted unless the report uses one of the
following templates:

- **Audience Overlap & Segmentation**
- **SQL Query**
- A custom template.

Query history for the templates listed above are retained even if a clean room is modified or deleted.

#### API query history

To see the account history of all calls run using the API, including template analyses, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Monitoring** » **Query History**.
3. Use the filters to find the query associated with the analysis, and select the query or analysis.

## Extended examples

To help you understand how to use various features of the Developer APIs, you can refer to the examples in the **Use cases** and
**Features** sections of the clean rooms documentation.
