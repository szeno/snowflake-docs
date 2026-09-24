# Basic consumer-run data analysis

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

## Overview

This topic demonstrates a basic consumer-run analysis using the clean rooms API. The example shows how a provider can programmatically
create and share a clean room with data, and a consumer can run an analysis against the provider’s data. The provider defines the SQL
queries that can be run against their data. A provider can define queries that query only the provider’s data, only the consumer’s data, or
that join provider and consumer data.

You can download [the full code example](#label-dcr-basic-clean-room-example) to upload and run on your Snowflake account.

The following diagram shows the data flow through the main components in a basic consumer-run analysis.

[![Basic data flow direction in a consumer-run analysis](/static/images/cleanrooms/consumer-run-analysis.svg)](/static/images/cleanrooms/consumer-run-analysis.svg)

In a basic consumer-run analysis involving two parties, the provider and consumers link data into the clean room. This data is accessed
using a secure view stored in the consumer DB in the clean room application package on the consumer’s account.

During an analysis, the clean room app on the consumer’s account uses the specified consumer and provider secure views, and the results are
shared with the consumer.

## Provider steps

The following list shows the main steps to create, publish, and share a clean room with a consumer:

- [Set up the environment](#set-up-the-environment)
- [Create the clean room](#create-the-clean-room)
- [Link data into the clean room](#link-data-into-the-clean-room)
- [Set the join policy](#set-the-join-policy)
- [Add templates to a clean room](#add-templates-to-a-clean-room)
- [Set column policies](#set-column-policies)
- [Share with consumers](#share-with-consumers)
- [Set the default version](#set-the-default-version)
- [Publish the clean room](#publish-the-clean-room)

### Set up the environment

To use the API, you must use a warehouse that SAMOOHA\_APP\_ROLE has privileges in.
app\_wh is one of a [number of warehouses](/user-guide/cleanrooms/v1/installation-details#label-cleanrooms-installation-details-warehouses) with access to the API. Choose the
warehouse that is appropriate for your needs. (You can also [use your own warehouse](/user-guide/cleanrooms/admin-tasks#label-cleanrooms-admin-add-warehouse), if you
choose.)

The `SAMOOHA_APP_ROLE` role is required to access the API.

Copy code

```
USE WAREHOUSE app_wh;
USE ROLE SAMOOHA_APP_ROLE;
```

### Create the clean room

The next step is to create a new clean room. This is done with a single API call that specifies whether the clean room is for internal or
external use. Internal clean rooms can be accessed only by consumers within the same organization; external clean rooms can be used by
consumers outside the organization. For both clean room types, consumers must be invited to use the clean room to be able to access it.

External clean rooms trigger additional security checks when certain actions are taken. When this happens, you must call
`provider.view_cleanroom_scan_status` to see when the security scan is done, and you can continue with the next action.

The following example creates an internal clean room:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.cleanroom_init($cleanroom_name, 'INTERNAL');
```

### Link data into the clean room

Both the provider and consumer can *link* (import) tables, views, and
[other supported data objects](/user-guide/cleanrooms/register-data#label-dcr-supported-linkable-objects) into a clean room. When you link data, the API creates a hidden,
secure view inside the clean room that is based on the linked source object. You reference the linked object by its source name, not
its internal view name, in all clean room procedures.

Data linked into the clean room can’t be accessed directly by any clean room collaborators. Linked data is accessed using a template
imported into the clean room (unless you enable [free-form SQL queries](/user-guide/cleanrooms/v1/web-app-sql-template) on your data).

Before an object can be linked into a clean room, the object must be *registered*. Registering an object grants proper access privileges to
the SAMOOHA\_APP\_ROLE on the object. You can either register an object directly, or register a parent object (such as a database or
schema) to access child objects. You can register an object in either the UI or the API.

Tip

Registration is easier to perform and manage in the UI than the API.

Objects are registered at the account level, not the clean room level; you need to register an object only once per account, and it can be
linked into any clean room in the account. (You can link only objects registered in your own account.) After you register an object, the
object is available for linking by any clean room in the account. [Learn more about registration.](/user-guide/cleanrooms/register-data)

The following example links in the CUSTOMERS table from the sample database SAMOOHA\_SAMPLE\_DATABASE. This database is registered
automatically when you install the clean room environment in an account, so you don’t need to register it. You can link or unlink objects
at any time in a clean room, and the results propagate quickly to all collaborators.

Copy code

```
CALL samooha_by_snowflake_local_db.provider.link_datasets(
  $cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS']);
```

### Set the join policy

If you add a template to the clean room that allows the consumer to join on your data, you should set a
[clean room join policy](/user-guide/cleanrooms/v1/policies#label-dcr-join-policies) on your data. A clean room join policy specifies which columns can be
joined on in queries run by collaborators. Your own join policies don’t constrain your own
queries.

Clean rooms support a [few types of data policies](/user-guide/cleanrooms/v1/policies) that you can set on linked data. These policies
are similar to, but not the same as, the equivalent Snowflake policies, and are applied only on the internal view, not on the source data.
Any Snowflake policies that are set on the source data are propagated to the views linked into a clean room. Clean room policies are set on
the linked data only, not on the source data.

Important

The template is responsible for [using JinjaSQL filters to enforce policies](/user-guide/cleanrooms/custom-templates#label-dcr-template-policies). If the template does
not use policy filters, the policies will not be respected. Always put policy filters on templates that you write, and
examine any templates that you run to confirm that they enforce clean room policies.

You can set policies only on the data that you link in; you can’t set policies on any other party’s data.

The following example shows how to set a join policy that allows two columns from the linked table to be joinable:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_join_policy(
  $cleanroom_name,
  ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_EMAIL',
   'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:HASHED_PHONE']);
```

[Learn more about join policies.](/user-guide/cleanrooms/v1/policies#label-dcr-join-policies)

### Add templates to a clean room

A clean room template is a valid JinjaSQL template that typically evaluates to a SQL query. A template, sometimes called an
*analysis*, can be passed arguments by the caller, and can access any data linked into the clean room. Both providers and consumers can add
templates into a clean room and run them.

Snowflake provides a few standard templates, but you will probably write your own custom templates.

Any clean room policies that you set are enforced only if the template includes policy filters
in the template, so make sure that the templates you add to a clean room include these filters. For more information about policies, see
[Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

By default, only consumers can run templates. If a
[provider wants to run a template](/user-guide/cleanrooms/demo-flows/provider-run-analysis), they must ask permission from the
consumer. Similarly, if a [consumer wants to upload a template](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates), they must ask permission from
the provider.

For more information about creating a custom template, read [Add custom templates to a clean room](/user-guide/cleanrooms/demo-flows/custom-templates) and
[Design custom templates](/user-guide/cleanrooms/custom-templates).

The following example shows how to add a Snowflake-provided template to the clean room:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_templates(
  $cleanroom_name,
  ['prod_overlap_analysis']);
```

### Set column policies

Clean room column policies specify which columns from your tables can be projected in queries run by collaborators. A column policy is tied
to both a column and a template, so different columns can be defined as projectable with different templates. A template must be present in
a clean room before you can set column policies for that template.

Column policies, like all policies, are *overwrite-only*; this means that setting column policies completely overwrites any existing column
policies set by that account. Both the provider and the consumer can set column policies on their data.
[Learn more about column policies.](/user-guide/cleanrooms/v1/policies#label-dcr-column-policies)

The following example shows how to allow four columns to be projected from the clean rooms sample database that was linked previously:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_column_policy($cleanroom_name, [
  'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:STATUS',
  'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:AGE_BAND',
  'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:DAYS_ACTIVE',
  'prod_overlap_analysis:SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS:REGION_CODE']);
```

### Share with consumers

Only consumers invited by the provider can access the clean room. Consumers can’t share a clean room with other consumers. Designated
consumers can’t access the clean room until it is published. Invitations to join a clean room are at the account level, not at the user
level.

The following example shows how to share a clean room with two consumers. The procedure takes two parallel, comma-delimited lists of
consumer account locators and [consumer data sharing account IDs](/user-guide/admin-account-identifier#label-account-name-data-sharing).

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_consumers(
  $cleanroom_name,
  'CONSUMER_LOCATOR1,CONSUMER_LOCATOR2',
  'CONSUMER_DATA_SHARING_ACCOUNT_ID1,CONSUMER_DATA_SHARING_ACCOUNT_ID2');
```

#### Sharing with consumers in other cloud hosting regions

If a consumer and provider are in different cloud regions, the provider and consumer must enable
[cross-cloud auto-fulfillment](/user-guide/cleanrooms/v1/enabling-laf) before the consumer can be added to the clean room. You can see
your own cloud region by running `SELECT CURRENT_REGION();`. You typically can’t see the consumer’s region, but if you try to add a
consumer in another region, `provider.add_consumers` fails with a message indicating the problem. When this failure occurs, you should
call `provider.remove_consumers` to remove the accounts that are in a different region, then enable cross-cloud auto-fulfillment, and
then add the cross-region accounts again.

### Set the default version

Clean rooms are versioned native applications. Certain actions, such as adding code to a clean room, generate a new patch version of the
application. Consumers must install the clean room in their account. The version that they install is based on the default version number
that you specify. If you later publish a new version of the clean room and increment the default version number, any versions installed by
consumers will automatically update, and new installations will default to the new version.
[Read more about clean room versioning.](/user-guide/cleanrooms/dcr-versions)

The following example shows how to set the default version of a clean room to V1.0.0, which is the initial version of a clean room,
if you haven’t uploaded any code:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.set_default_release_directive(
  $cleanroom_name,
  'V1_0',          -- Version number: Never changes.
  '0'              -- Patch number: Can change.
  );
```

### Publish the clean room

Publish or republish the clean room as shown in the following example. The first time this procedure is called, it makes the clean room
visible and installable by any consumers that you shared it with. You should call this procedure whenever you make significant changes,
such as when you update the default version or make changes specific to the clean room UI.

Copy code

```
CALL samooha_By_snowflake_local_db.provider.create_or_update_cleanroom_listing(
  $cleanroom_name);
```

Now the consumer can install the clean room, link in data, set policies, and run templates, as described next.

Tip

When you no longer need a clean room, you should delete the clean room on the provider and consumer accounts
(`provider.drop_cleanroom` and `consumer.uninstall_cleanroom`). There is a limit to the number of clean rooms and
collaborators per account. When you leave many unused clean rooms in your account, you can reach your quota.

## Consumer steps

After a provider publishes a clean room, all consumers who were added as collaborators can see and install the clean room using either
the UI or the API. This section shows how a consumer can install a clean room and run an analysis using the API.

Here is a quick overview of the steps the consumer takes to install a clean room and run an analysis:

- [Set up the environment](#set-up-the-environment-1)
- [Install the clean room](#install-the-clean-room)
- [Add data and set policies](#add-data-and-set-policies)
- [Run the analysis](#run-the-analysis)

### Set up the environment

Like the provider, the consumer must use a
[warehouse that SAMOOHA\_APP\_ROLE can access](/user-guide/cleanrooms/v1/installation-details#label-cleanrooms-installation-details-warehouses). However, unlike the provider, the
consumer can either use the SAMOOHA\_APP\_ROLE role directly for full API access, or a clean room administrator in that account can grant a
more limited role that gives privileges to run a subset of the API for consumers. This limited role, sometimes generically called a
“run role,” is granted by a user with full clean room privileges.
[Learn how to grant limited API access.](/user-guide/cleanrooms/manage-dcr-users#label-dcr-grant-limited-access)

A run role doesn’t allow you to install a clean room, so you must use SAMOOHA\_APP\_ROLE, as shown in the following example:

Copy code

```
USE WAREHOUSE app_wh;
USE ROLE SAMOOHA_APP_ROLE;
```

### Install the clean room

The following snippet shows how to list all clean rooms that are installed you have been invited to install:

Copy code

```
-- See all clean rooms, installed and not.
CALL samooha_by_snowflake_local_db.consumer.view_cleanrooms();

-- See only clean rooms that aren't installed.
CALL samooha_by_snowflake_local_db.consumer.view_cleanrooms() ->>
  SELECT * FROM $1
    WHERE IS_ALREADY_INSTALLED = false;
```

Install the clean room that the provider shared with you, as shown in the following example. You must specify the provider’s account locator
when you install a clean room.

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.install_cleanroom(
  $cleanroom_name,
  '<PROVIDER_ACCOUNT_LOCATOR>');
```

Tip

Clean rooms have both a name and an ID. For clean rooms created by using the API, use the clean room name wherever an API procedure needs
a clean room name. For clean rooms created in the UI, use the clean room ID rather than the name wherever an API procedure needs a clean
room name.

The clean room UI labels clean rooms created using the API as **Supported with Developer APIs**.

### Add data and set policies

If the clean room templates allow the consumer to include their own data in a query, the consumer registers data, links data, and sets
policies like the provider does. Be sure to use the `consumer` versions of the procedures, as shown in the following example:

Copy code

```
-- You must use a role with MANAGE GRANTS privilege on an object to register it.
USE ROLE ACCOUNTADMIN;
CALL samooha_by_snowflake_local_db.consumer.register_db('MY_DATABASE');

-- Link some tables.
CALL samooha_by_snowflake_local_db.consumer.link_datasets(
  $cleanroom_name,
  [
    'SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS',
    'MY_DATABASE.PUBLIC.EXPOSURES'
  ]);
```

The provider’s join policy shows which provider columns can be joined on. This example shows how to check which provider
columns you can join on:

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.view_provider_join_policy($cleanroom_name);
```

A provider needs the consumer’s approval to run a template in the clean room. As a result, most consumers don’t bother setting policies on
the tables that they link in. Nevertheless, we recommend that you consider adding policies in case a provider asks to run a template later,
because you might forget to add appropriate policies at that time.

If you do set policies, they are enforced only if the template includes a `join_policy` or `column_policy`
filter to the column in the template, so make sure that the templates you add to a clean room include these filters to enforce your
policies. To examine the templates in a clean room, call `consumer.view_added_templates`. For more information about policies,
see [Understanding Snowflake Data Clean Room policies](/user-guide/cleanrooms/v1/policies).

### Run the analysis

Before you run a template, you typically examine it to see what it does and what variables it accepts, then you examine what provider
tables are available in the clean room.

#### Examine the templates

You can list the templates in a clean room and examine the code of each (unless the provider has explicitly
[obfuscated the code](#dcr-provider-add-custom-sql-template)). This can be useful to help you understand the query better. You can
also ask the clean room to parse the template and show which variables you can pass in when you run the code.

You can pass in a list of tables to use in the query, subject to the design of the template. Any table linked in to the clean room can be
passed to the template.

Many templates also support variables that you can specify at run time; for example, to match a particular value or to specify which
columns to show. Ideally, the provider should let you know what the template does and what arguments it accepts. But typically, you also
want to examine a template to see the code. The following snippet lists the templates added to the clean room by any collaborator, and gets
the arguments supported for a specific template:

Copy code

```
-- View the list of templates available in this clean room,
-- and the source code for each template.
CALL samooha_by_snowflake_local_db.consumer.view_added_templates($cleanroom_name);

-- Show which variables can be passed in when running the specified template.
CALL samooha_by_snowflake_local_db.consumer.get_arguments_from_template(
  $cleanroom_name,
  $template_name
);
```

Tip

If you see the `my_table` array variable used in a template, this holds the list of consumer table names that you pass in when you run
the template. If you see the `source_table` array variable, this holds the list of provider table names that you pass in when you run
the template.

#### See what data is available

You can list the datasets that you and the provider have linked into a clean room, as shown in the following example:

Copy code

```
-- See which datasets you have linked into the clean room.
CALL samooha_by_snowflake_local_db.consumer.view_consumer_datasets($cleanroom_name);

-- See which datasets the provider has linked into the clean room.
CALL samooha_by_snowflake_local_db.consumer.view_provider_datasets($cleanroom_name);
```

When you pass in a table name, use the table name, not the view name, from the results of these procedures.

#### Run the template

In the previous two steps, you learned what data you have and what variables you can pass in. You’re now ready to run the analysis.

Depending on the query and the size of the data, you might want to change the warehouse size to
[something more appropriate](/user-guide/cleanrooms/v1/installation-details#label-cleanrooms-installation-details-warehouses).

The following example shows how a user might call a template that takes both consumer and provider tables, and two variables:
`dimensions`, which is used as a grouping column, and an optional `where_clause`, which is used in a WHERE clause in the query.

The template runs a query against a single provider table, so the request will omit consumer tables.

In the following example, notice how the `dimensions` value is a column name prefixed by *p*. The *p* indicates that this column comes
from the provider table that is passed in. Column names typically require that you add a *p* or *c* to indicate which table they come from,
provider or consumer, to disambiguate the column names. However, this requirement is very template-specific. You need to communicate with
the template provider or examine the template code to understand when these prefixes are required.

Copy code

```
CALL samooha_by_snowflake_local_db.consumer.run_analysis(
$cleanroom_name,
$template_name,
[],                                              -- This template doesn't accept consumer tables.
['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],      -- Provider tables.
object_construct(                                -- Template-specific arguments.
  'dimensions', ['p.STATUS'],                    -- Template takes a variable named 'dimensions'.
  'where_clause', 'p.REGION_CODE=$$REGION_10$$'  -- Template allows you to pass in a WHERE clause.
                                                 -- $$ is used to wrap string literals
  )
);
```

## Example code

The following worksheet files demonstrate how to create, share, and run a clean room analysis.

Download the following examples, and then upload them as worksheet files in your Snowflake account. You need separate accounts for
the provider and consumer, each with the clean rooms API installed.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Provider example code](/static/samples/clean-rooms/c-run-analysis-p.sql)
- [Consumer example code](/static/samples/clean-rooms/c-run-analysis-c.sql)
