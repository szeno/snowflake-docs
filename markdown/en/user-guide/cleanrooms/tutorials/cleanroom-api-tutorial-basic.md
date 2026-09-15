# Tutorial: Get started with Snowflake Data Clean Rooms in code

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

## Introduction

This tutorial is aimed at developers who will create or use Snowflake Data Clean Rooms in code. This tutorial uses SQL code, but you can
adapt the information shown here to create and use clean rooms in any coding language supported by Snowflake.

### What you will learn

This tutorial shows you how to create and share a basic template in a clean room using the Snowflake Data Clean Room API. It also
shows you how to run an analysis using the API in a clean room shared with you.

This tutorial creates a clean room with one table provided by the provider, one table provided by the consumer, and a template defined
by the provider that defines a very simple JOIN query on the two tables.

### Requirements

- You should have a basic understanding of Snowflake and you should also read
  [About Snowflake Data Clean Rooms](/user-guide/cleanrooms/overview) before starting this tutorial.
- You must have access to a Snowflake account, Enterprise Edition or higher, with the Snowflake Data Clean Rooms native app and API
  installed. If you don’t have the clean rooms app installed, you can either
  [install it yourself](/user-guide/cleanrooms/getting-started), or else ask a Snowflake administrator to install it for you.
- You must be granted the SAMOOHA\_APP\_ROLE to use the clean rooms API.
- This tutorial uses a sample table named CUSTOMERS\_2 that is installed with the clean rooms environment. Search your account
  for the table SAMOOHA\_SAMPLE\_DATABASE.DEMO.CUSTOMERS\_2 using the following command:

  Copy code

  ```
  SHOW TABLES LIKE 'CUSTOMERS_2' IN SCHEMA SAMOOHA_SAMPLE_DATABASE.DEMO;
  ```

  If the response has no rows, then you, or someone with ACCOUNTADMIN role, must run the following command to install the sample table:

  Copy code

  ```
  USE ROLE ACCOUNTADMIN;
  EXECUTE IMMEDIATE FROM @SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.MOUNT_CODE_STAGE/dcr_loader.sql;
  ```

This tutorial uses the same account to act as both a provider and a consumer in a clean room. This scenario is supported only
for testing purposes and has [limitations on what features it supports](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-self-share-for-developers), compared to using
separate accounts. In the real world, providers and consumers use different accounts, and for more advanced testing you might need to use
separate accounts.

You can [download this tutorial as a worksheet file](/static/samples/clean-rooms/internal-testing-cleanroom.ipynb) to run in your
Snowflake account.

## Provider: Overview

Here is a summary of the steps that you’ll take to create a clean room as the provider:

1. Create test data to share in your clean room.
2. Create your clean room.
3. Set join permissions on your data to specify which columns can be joined on in consumer queries.
4. Create a template for your clean room. A clean room template is written in JinjaSQL and it evaluates to a SQL query at run time. Most
   templates include variables that allow collaborators to specify table and column names, WHERE clause conditions, and more, at run time.
   A clean room collaborator chooses and runs a template in a clean room.
5. Specify the default version of the clean room.
6. Add consumers who can access your clean room. In this tutorial consumers must be Snowflake users with accounts approved by your clean room administrator.
7. Publish the clean room to make it available to your invited consumers.

Note

The term *collaborator* is used above for templates because, depending on how the clean room is configured, both providers and consumers
can create or run templates. This tutorial shows only how to enable consumer-run templates.

## Provider: Create the clean room

[Sign in to Snowsight](https://app.snowflake.com) as a user granted the SAMOOHA\_APP\_ROLE role. If you don’t have that role, ask your
account administrator to grant it to you.

[Create a new SQL worksheet](/user-guide/ui-snowsight-worksheets-gs) in Snowsight to hold your clean room code. Name the worksheet
“API tutorial - Provider”.

The following snippet creates a clean room that is accessible only within the organization (so it’s marked as INTERNAL). To share a
clean room outside of an organization requires additional steps that won’t be covered in this tutorial. When sharing a clean room with
yourself, it must be INTERNAL, of course.

You must use the SAMOOHA\_APP\_ROLE for most clean room procedures.

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
SET cleanroom_name = 'Developer Tutorial';
CALL samooha_by_snowflake_local_db.provider.cleanroom_init($cleanroom_name, 'INTERNAL');
```

## Provider: Bring data into the clean room

Next, bring your test data into the clean room. There are two steps to bring data into a clean room:

1. Register the data.
2. *Link* (import) the data into the clean room.

### Register the data

The first step in importing data is to *register* the database, schema, or object in the clean room account. Registering is to grant clean rooms the right to read and use the source data. You can register an entire database, a schema, a table, or a view.

You are using sample data installed with the clean room, which is pre-registered for you, so there’s no need to register the sample data in this tutorial.

### Link the data into the clean room

Importing data into a clean room is called *linking*. Both providers and consumers can link their data into a clean room. The generic term
for a view or table linked into a clean room is a *dataset*.

When you link data, the clean room creates a read-only view linked to your source data. This clean room view is a
secure, encrypted view inside the clean room, accessible only to templates within the clean room. Your template
accesses this secure view, not the source data, although the original source name is used whenever you need to reference the data.

Unlike registering, linking is done at the individual table or view level. You can link multiple items in one call.

Link clean room sample data into the clean room:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.link_datasets($cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS']);

CALL samooha_by_snowflake_local_db.provider.view_provider_datasets($cleanroom_name);
```

Note

If a table linked into a clean room is deleted, renamed, moved, or has restrictive permissions added, the table can’t be used in the
clean the clean room unless you restore the old table with the same location, name, and permissions.

## Provider: Set join policies on the data

Both providers and consumers can specify *join policies* on their own data. A clean room join policy specifies which columns in a table can
be joined on by your collaborators’ queries in that clean room. This provides an extra level of control over how others can use your data
in the clean room. Your own policies are not enforced on your own queries – that is, join policies on your own data are
ignored when you run a query; your policies are enforced only on queries run by other users.

Clean room join policies are set on the table, and apply to all clean rooms where the
table is used. Any columns not listed here cannot be joined using INNER JOIN or OUTER JOIN conditions in the clean room if the template
explicitly checks join policies.

Note that clean room join policies are not the same as [Snowflake join policies](/user-guide/join-policies); clean room policies
specify which columns *can* be joined on; Snowflake join policies specify which columns *can’t* be joined on.

Tip

**Snowflake** policies set on the source table are retained in the linked clean room table, but aren’t reported to
collaborators. That is, **Snowflake** join policies are enforced but are not reported by `consumer.view_provider_join_policy`, which
reports only the provider’s **clean room** join policies. Therefore you should let your collaborators know about any Snowflake policies
that you have set on your data.

Specify joinable columns for a table using the format
`database_name.schema_name.table_or_view_name:column_name` for each column. The following example allows three columns
of provider data to be joinable:

Copy code

```
-- Limit joinable columns in this table to age_band, region_code, and device_type
CALL samooha_by_snowflake_local_db.provider.set_join_policy($cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:AGE_BAND',
   'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:REGION_CODE',
   'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DEVICE_TYPE']);

CALL samooha_by_snowflake_local_db.provider.view_join_policy($cleanroom_name);
```

## Provider: Add your template

A clean room template is a JinjaSQL template that evaluates to a SELECT query. This query has access to all datasets linked into the clean
room, subject to join and column policies.

This tutorial won’t cover the details of designing a JinjaSQL template, but here is the SQL query that you’re trying to implement:

Copy code

```
SELECT
  COUNT(*),
  group_by_col
FROM Consumer_Table AS C
  INNER JOIN Provider_Table AS P
    ON c.join_col = p.join_col
GROUP BY group_col;
```

The query simply joins one provider and one consumer table on a specified join column, groups by a specified grouping column, and projects
the group value and count of each group. This is the query that will run in the clean room when the user runs the template.

Here is the JinjaSQL template for the same query, with variables added where the consumer can specify tables or columns. After the consumer
specifies the variables, it will evaluate to a SQL query similar to the one above, but with the table and column names provided by the
consumer.

Copy code

```
SELECT
  COUNT(*),
  IDENTIFIER({{group_by_col | column_policy}})
FROM IDENTIFIER({{my_table[0]}}) AS C
INNER JOIN
  IDENTIFIER({{source_table[0]}}) AS P
    ON IDENTIFIER({{consumer_join_col | join_policy}}) = IDENTIFIER({{provider_join_col | join_policy}})
GROUP BY IDENTIFIER({{group_by_col | column_policy}});
```

A few notes on the template:

- Content surrounded by {{brackets}} are named variables passed in by the consumer when they run the template. The following variables are
  passed in by the consumer: `group_by_col`, `consumer_join_col`, `provider_join_col`
- The `my_table` and `source_table` arrays are global variables created by the system, populated with consumer and
  provider table names passed in by the caller. These tables must be linked into the clean room by the consumer and provider.
- All provider tables must be aliased as `p` in the query. All consumer tables must be aliased as `c`. If you use multiple tables, alias
  them with a 1-based suffix, so: `p`, `p1`, `p2`, `p3` and so on for provider tables, and `c`, `c1`, `c2`, `c3` and so on
  for consumer table aliases. (`p` and `p0` are equivalent.)
- Snowflake Data Clean Rooms supports some custom JinjaSQL *filters* that act on variables. The `column_policy` and `row_policy`
  filters verify that the columns they are applied to conform to the column and row policies in that clean room, or else the request to run
  the template will fail. So `{{ consumer_join_col | join_policy }}` verifies that the value passed in to `consumer_join_col` conforms
  to the join policies set by the provider and consumer in this clean room.
- Variables used as identifiers must be processed by the [IDENTIFIER](/sql-reference/identifier-literal) function before they can be
  used in SQL.

Add the template to the clean room:

Copy code

```
-- Add the template
SET template_name = 'overlap_template';
CALL samooha_by_snowflake_local_db.provider.add_custom_sql_template(
    $cleanroom_name,
    $template_name,
    $$
    SELECT
      COUNT(*),
      IDENTIFIER({{group_by_col | column_policy}})
    FROM IDENTIFIER({{my_table[0]}}) AS C
    INNER JOIN
      IDENTIFIER({{source_table[0]}}) AS P
      ON IDENTIFIER({{consumer_join_col | join_policy}}) = IDENTIFIER({{provider_join_col | join_policy}})
    GROUP BY IDENTIFIER({{group_by_col | column_policy}});
    $$);

CALL samooha_by_snowflake_local_db.provider.view_added_templates($cleanroom_name);
```

## Provider: Set column policies

Each party in the clean room can limit which columns the other parties can project by setting a *column\_policy*. A column
policy in a clean room lists all the columns of your data that can be projected; no other columns can be projected. If you do not specify
a column policy for your data, all your data can be projected.

A column policy is tied to a specific table and template in a clean room. You can allow different columns to be projected in different
templates. The same column cannot be in both a join and a column policy.

Note that column and join policies are enforced only if the template uses the `column_policy` and `row_policy` filters in the template.

Here is how to allow projection of three columns of your data in the template you just created. Column syntax is
`template_name:table_name:column_name`

Copy code

```
-- Set column policies. Column policies are tied to a specific template and table, so we
-- needed to add the template first.
CALL samooha_by_snowflake_local_db.provider.set_column_policy($cleanroom_name,
  [$template_name || ':SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:STATUS',
   $template_name || ':SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DAYS_ACTIVE']);

CALL samooha_by_snowflake_local_db.provider.view_column_policy($cleanroom_name);
```

## Provider: Add a release directive

Every clean room has a [version number](/user-guide/cleanrooms/dcr-versions), consisting of major, minor, and patch values. You must
specify which version of the clean room is served to consumers: this is called the *default release directive*.

This is the first version, so the version number is 1.0.0.

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_default_release_directive(
  $cleanroom_name,
  'V1_0',
  '0');
```

Snowflake creates a new version of the clean room each time you upload code into the clean room. If you want users to get the latest
version, you’ll need to set a new default release directive with the newest version number. You won’t be uploading code, so you won’t need
to call this again for this tutorial.

## Provider: Designate consumers

Now you will specify who has access to your clean room as a consumer. For this tutorial you will add yourself as a consumer. Doing so marks
the clean room as an internal testing clean room, used only for testing, which
[limits some of its functionality](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-self-share-for-developers), but it will support all the features needed for this
tutorial.

The procedure needs two arguments to identify each consumer:

- The consumer’s account locator. Get your account locator like this:

  Copy code

  ```
  SELECT CURRENT_ACCOUNT();
  ```
- The consumer’s [consumer data sharing account ID](/user-guide/admin-account-identifier#label-account-name-data-sharing), in the format `org_name.account_name`.
  Get your consumer data sharing account ID in the proper format like this:

  Copy code

  ```
  SELECT CURRENT_ORGANIZATION_NAME() || '.' || CURRENT_ACCOUNT_NAME();
  ```

Now share the clean room with yourself as a consumer, adding your account locator and consumer data sharing account ID where indicated:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_consumers(
  $cleanroom_name,
  '<CONSUMER_LOCATOR>',
  '<CONSUMER_DATA_SHARING_ACCOUNT_ID>');

CALL samooha_by_snowflake_local_db.provider.view_consumers($cleanroom_name);
```

## Provider: Publish the clean room

Finally, publish the clean room. This makes the clean room available to the consumer you added above. The procedure takes a minute
or more to complete.

Copy code

```
-- Publish the clean room.
CALL samooha_by_snowflake_local_db.provider.create_or_update_cleanroom_listing(
  $cleanroom_name);
```

When the procedure finishes, you should see the clean room listed in the [clean rooms UI](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in), in the
**Created** tab in your provider account, and in the **Invited** tab in the consumer account, with the label
“Powered by Dev Edition.” The consumer account will receive an invitation email. (Do not install the clean room from the **Invited** tab;
you will install it in code, in a later step.)

Congratulations: You’ve published your first clean room!

Now take off your provider cap and put on your consumer cap.

## Consumer: Install (join) the clean room

You’ll use the same account for the provider and consumer roles in this tutorial, so add a new SQL worksheet named “API Tutorial -
Consumer” in Snowsight in the same account.

Set up the session environment, similar to the way you did for the provider:

Copy code

```
USE WAREHOUSE app_wh;
USE ROLE SAMOOHA_APP_ROLE;
```

Next, install the clean room that you published and shared as a provider. To install a clean room, you must specify both the clean room
name and the account locator of the provider who shared the clean room with
you. Specifying the clean room name and the account locator helps disambiguate clean rooms with identical names. Run
`SELECT CURRENT_ACCOUNT();` to get your provider locator.

Copy code

```
SET cleanroom_name = 'Developer Tutorial';
CALL samooha_by_snowflake_local_db.consumer.install_cleanroom(
  $cleanroom_name,
  <PROVIDER_LOCATOR>);
```

Installation can take a few minutes.

## Consumer: Link your data

You must register and link your data into the clean room, just as you did as a provider. Again, because you are using sample data provided
with the clean room installation, you the data is pre-registered.

You will use a different sample table installed with clean rooms. If this table is not present in your account, see the **Requirements**
section on the **Introduction** page to learn how to install it.

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL samooha_by_snowflake_local_db.consumer.link_datasets(
  $cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS_2']);

CALL samooha_by_snowflake_local_db.consumer.view_consumer_datasets($cleanroom_name);
```

## Consumer: No need to set policies

You could set policies on your data, the same way the provider did, but this template is approved for only the consumer to run, so there’s
no need to set any policies on it.

However, if you were to approve a provider request to run this template, you should first set join and column policies on your data to
control what the provider could do with it.

## Consumer: Run the analysis

To run a query, you need the following information:

- The name of the template you want to run.
- The names of your tables to use in the template.
- The names of the provider’s tables to use in the template.
- Any other name/value variables to pass in.

### Examine the template

You can examine the template to see what it does and any arguments that it accepts. The following example shows how to list the templates
in the clean room, see a template’s code, and see what arguments it accepts:

Copy code

```
-- List templates in the clean room.
CALL samooha_by_snowflake_local_db.consumer.view_added_templates($cleanroom_name);

-- See the template code.
SET template_name = 'overlap_template';
CALL samooha_by_snowflake_local_db.consumer.view_template_definition(
  $cleanroom_name,
  $template_name);

-- See what arguments can be passed in to the template:
CALL samooha_by_snowflake_local_db.consumer.get_arguments_from_template(
  $cleanroom_name,
  $template_name
);
```

You can see that you need to pass in a provider table and column name, a consumer table and column name, and a grouping column.

### List the available provider tables

See which tables the provider has added to the clean room.

Copy code

```
-- Table name to use is in the LINKED_TABLE column in the results.
CALL samooha_by_snowflake_local_db.consumer.view_provider_datasets($cleanroom_name);
```

### List the provider’s joinable and projectable columns

See which columns can be joined on or projected from the provider’s data.

Copy code

```
-- See which provider columns can be joined on.
CALL samooha_by_snowflake_local_db.consumer.view_provider_join_policy($cleanroom_name);

-- See which provider columns can be projected.
CALL samooha_by_snowflake_local_db.consumer.view_provider_column_policy($cleanroom_name);
```

### Run the analysis

Now that we know what the query needs, what provider data is available, and what can be done with that data, you can select values to pass
in.

You must fully qualify all column names in most circumstances. You must use the table alias as the
table name rather than the actual table name. Remember that the table aliases in this template are `p` for the provider table, and `c`
for the consumer table. You must use lowercase `p` and `c`.

In your first query, use the following values:

- Provider table: The only choice is `SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS`.
- Consumer table: The only choice is `SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS_2`.
- `consumer_join_col`: Use `age_band` from the consumer table; the fully qualified column name is `c.age_band`.
- `provider_join_col`: You need to join on similar columns, so the equivalent, fully qualified provider name is `p.age_band`.
- `group_by_col`: Take your pick of provider or consumer columns from the remaining projectable columns. Try `p.device_type`, but
  you can use any of the other provider or consumer columns returned by `consumer.view_provider_column_policy`.

These values are passed into `consumer.run_analysis` as shown in the following example:

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.run_analysis(
  $cleanroom_name,
  $template_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS_2'], -- Consumer table list.
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'], -- Provider table list.
  OBJECT_CONSTRUCT(                    -- Additional template arguments as name-value pairs.
    'consumer_join_col','c.age_band',
    'provider_join_col','p.age_band',
    'group_by_col','p.status'
  )
);
```

Congratulations! You should see the query results in Snowsight.

Additional features not covered here allow you to export those results directly to your own Snowflake account, or to an approved
third-party service in a process called *Activation*.

See more use cases and learn about more clean room features in the
[Snowflake Clean Rooms developer guide](/user-guide/cleanrooms/v1/developer-introduction).

## Both accounts: Clean up

Now let’s clean up all the resources that you created.

### Provider cleanup

Run the following code in your provider worksheet:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL samooha_by_snowflake_local_db.provider.drop_cleanroom($cleanroom_name);
```

### Consumer cleanup

Run the following code in your consumer worksheet:

Copy code

```
USE ROLE SAMOOHA_APP_ROLE;
CALL samooha_by_snowflake_local_db.consumer.uninstall_cleanroom($cleanroom_name);
```
