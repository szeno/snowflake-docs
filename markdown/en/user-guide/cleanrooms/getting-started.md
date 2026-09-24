# Overview of Provider and Consumer Clean Rooms

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This page provides an overview of how Snowflake Data Clean Rooms work. If you are a Snowflake administrator and want to install clean
rooms in your account, read [Installing the Snowflake Data Clean Rooms environment](/user-guide/cleanrooms/installing-dcr).

New!

Snowflake Data Clean Room has a new collaboration experience Generally Available. [Read about and try out our new Collaboration Clean Rooms experience.](/user-guide/cleanrooms/about)

## Overview of Snowflake Data Clean Rooms

Data clean rooms are configurable, isolated Snowflake environments where collaborators can import data, specify what queries can be run
against that data, and configure data protection settings such as differential privacy and specifying joinable and projectable columns. Access
to a clean room is by invitation only.

Clean rooms don’t support monetization features. Providers are billed for various background processes required to enable clean rooms;
the account running a query is billed standard Snowflake costs for the data and compute usage. For more information about costs, see
[Understanding cost](/user-guide/cleanrooms/cleanroom-cost).

You must be invited by a clean room provider to be able to access a clean room. If you want to open up your clean room to a larger
audience, you must provide a way for potential collaborators to contact you to provide their Snowflake account for you to invite (or an
email address for [non-Snowflake users](/user-guide/cleanrooms/managed-accounts)).

Here is a high-level overview of how Snowflake Data Clean Rooms work:

### Clean Room environment installation

The Snowflake Data Clean Room environment is installed once for an entire Snowflake account (not once per user or per clean
room) by someone with ACCOUNTADMIN privileges on the Snowflake account.

The administrator configures the environment to specify which users in the account can create clean rooms and run queries, which users have
API access, which accounts can be invited to collaborate in a clean room, what data a clean room creator can import into the clean room,
and which (if any) third-party services can be used to export query results from any clean room created in this account.

If a clean room environment has already been installed for your account, reach out to your clean rooms administrator for access. If a clean
room environment has not been installed for your account, [learn how to install the environment](/user-guide/cleanrooms/installing-dcr).

After installing and configuring the environment, the administrator grants permission to other Snowflake users to use the clean
rooms UI, API, or both.

Learn more

- Learn how to [install and configure the Clean Room environment](/user-guide/cleanrooms/installing-dcr).
- By default, you can share clean rooms only with accounts in the same web hosting region. The administrator can
  [enable sharing with accounts in other regions](/user-guide/cleanrooms/v1/enabling-laf).
- See [other tasks that clean rooms administrators perform](/user-guide/cleanrooms/admin-tasks).

Note

- **If you were emailed an invitation to join a clean room,** you already have clean rooms installed in your Snowflake account. You can
  read the rest of this page to learn more about clean room usage, but you don’t need to install anything, only to join the clean room.
- **If you are an account administrator** and the clean room environment is not installed in your Snowflake account, [learn how to install the clean room environment for your Snowflake account](/user-guide/cleanrooms/installing-dcr).
- **If you are not an account administrator,** ask an account administrator whether Snowflake Data Clean Rooms is installed for your
  account. If not, ask them to install it and grant you access. If it is, ask them to grant you permission to access clean rooms.
- **If you are a developer and want API access,** ask a clean rooms administrator to
  [grant you access to the API](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-add-developers).

### Creating a clean room

A Snowflake account administrator grants permission to users in their Snowflake account to be able to create clean rooms. The account
that creates a clean room is called a *provider* for that clean room. Providers can configure and share clean rooms with users in other
Snowflake accounts (or even non-Snowflake users). When a clean room is shared with you, you are called a *consumer* for that clean room.

After creating a clean room, the provider *links* (imports) tables or views into it, specifies what queries can be run against their data,
which columns in their data can be joined or appear in the results, and what can be done with the results.

The provider then invites consumers to join the clean room, link their own tables and views, and run one of the queries specified by the
provider. Consumers must be pre-approved by a clean rooms administrator before they can be invited to a clean room.

Learn more

- Clean rooms can be created either in code or using the clean rooms UI. Permission to create a clean room is granted differently for
  [web users](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-get-started-add-users) and [coders](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-add-developers).
- Tables can be imported from both Snowflake accounts and [non-Snowflake Iceberg tables](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables) on
  [AWS](/user-guide/cleanrooms/external-data-aws), [Azure](/user-guide/cleanrooms/external-data-azure), and
  [Google](/user-guide/cleanrooms/external-data-gcp).
- Before data can be imported into a clean room, it must be [registered](/user-guide/cleanrooms/register-data) by a user with admin
  privileges on the source data.
- You can invite both Snowflake and [non-Snowflake users](/user-guide/cleanrooms/managed-accounts) to join a clean room.
- Learn more about the [provider role in clean rooms](#label-dcr-provider-role).
- During development, you can [use the same account for both provider and consumer roles](/user-guide/cleanrooms/v1/developer-introduction#label-dcr-self-share-for-developers),
  though with only a subset of clean room functionality.

### Joining a clean room

After creating and configuring a clean room, the provider sends invitations to users in other accounts to join the clean room. These
invited users are called *consumers*, or sometimes *collaborators*. Consumers invited through the clean rooms UI
receive an emailed invitation to join the clean room. Snowflake users must have the Clean Room environment installed in order to be
invited to join a clean room, but you can [invite non-Snowflake users](/user-guide/cleanrooms/managed-accounts) to join a clean room.
A Snowflake account must be allowlisted by a clean rooms administrator before a clean room creator can invite users in that account.

(In the clean rooms UI, both “join” and “install” are used to describe when a consumer accepts a clean room invitation. This is because a
clean room must literally be installed in the consumer’s clean room environment.)

After joining a clean room, a consumer imports (links) any data needed for the templates in that clean room, specifies how their data can
be accessed, such as which columns can be joined or projected, provides any template-specific filters or other parameters, then runs the
template. Consumers can specify a repeating run of the template, if desired. Results can be viewed in the browser, or downloaded. If the
provider has enabled activation and the consumer approves, the consumer can export the results to the approved locations (their own
Snowflake account, or a third-party activation connector designated by the provider).

Data imported into a clean room cannot be queried or viewed directly by either party — either the provider or the consumer — but can
only be accessed through a template in the clean room. A template is a SQL query installed in the clean room by the provider or consumer,
and permission must be given by the other party to use it in the clean room.

Each party also sets access rules on their own data, including which columns can be joined, projected, or exported, and which
templates can be run in the clean room. Each party can delete their data from the clean room at any time.

By default, only a consumer can run templates in a clean room, but the provider can ask permission from the consumer to run a specified
template in the clean room.

Learn more

- Clean rooms support [differential privacy](/user-guide/cleanrooms/differential-privacy). Differential privacy can be enabled and
  configured by either the provider or consumer.
- Learn more about the [consumer role in Snowflake Data Clean Rooms](#label-dcr-consumer-role).

### Templates

Every clean room has one or more *templates* installed. A template is a JinjaSQL query that typically includes run-time parameters provided by the
template runner. These parameters enable users to specify column or table names or WHERE clause filters. You cannot simply run
arbitrary SQL queries in a clean room (unless a provider [grants that ability](/user-guide/cleanrooms/v1/web-app-sql-template)); most
clean room usage is limited to templates submitted by the provider or consumer and approved by the other party.

Snowflake provides a few stock templates for common use cases such as audience overlap and reach and frequency templates. You can also
create custom templates to use in your clean room. Snowflake Data Clean Rooms supports any valid JinjaSQL template.

Templates can be run in the clean rooms UI or in code. Template results can be viewed or downloaded, or can be shared to the provider, the
consumer, or an approved third-party if *activation* is allowed in that clean room.

Learn more

- By default, only consumers can run a template in a clean room. However, a provider can
  [ask permission of the consumer to run a template](/user-guide/cleanrooms/demo-flows/provider-run-analysis) in a clean room.
- The template and clean room configuration define what can be done with the query results. If the query results are exported outside the
  clean room, this is called [activation](/user-guide/cleanrooms/v1/activation). Results can be activated to a
  Snowflake account of the provider or consumer, or to a [Snowflake-approved third party](/user-guide/cleanrooms/connector-activation).

### Clean room variations

The most common clean room, as described above, is one where a provider imports data and specifies one or more specific queries that can
be run against the data and how the results can be shared, and the consumer imports their own data and runs the permitted queries against
the combined data. However, a provider can permit several variations on the standard clean room:

- [Allow the provider to run their own queries against consumer data.](/user-guide/cleanrooms/demo-flows/provider-run-analysis). By
  default, only the consumer can run queries in a clean room. If enabled for a clean room, a provider can request permission from the
  consumer to run a specific query in the clean room.
- Allow the query results to be exported [(activated)](/user-guide/cleanrooms/v1/activation) to the Snowflake account
  of the person running the query or to a Snowflake-approved third-party account, such as Google Ads or Meta Ads Manager. Exporting
  data outside the clean room is always subject to approval by all parties who shared the data being queried.
- Allow either party to [include custom Python code](/user-guide/cleanrooms/demo-flows/custom-code) that can be called by
  the query they run. This code typically filters or manipulates the data in some way as the query is being run; it cannot take external
  actions such as saving a file, exporting data, or performing other actions.
- Allow the query to [access data in other clean rooms](/user-guide/cleanrooms/overview), subject to approval by the
  providers of all the clean rooms being accessed.
- [Chain multiple queries together.](/user-guide/cleanrooms/developer-template-chains)

### About providers and consumers

Clean room collaborators are classified as either a *provider* or a *consumer* for a given clean room. A provider is the account that
creates a clean room; a consumer is the account with whom a clean room is shared. You cannot invite someone in the same account where you
created a clean room to act as a consumer for that clean room. All users in the same Snowflake account have the same clean room role
(provider or consumer) for the same clean rooms in that account.

The provider and consumer roles apply at the Snowflake account level, not the individual user level. That is, if
you create clean room `cleanroom1` using Snowflake account ABC, then share `cleanroom1` with account XYZ, all ABC users with access
to `cleanroom1` are providers, and all XYZ users with access to `cleanroom1` are consumers.

Whether you are a provider or consumer is determined solely by whether you created or were shared a clean room, not by any Snowflake roles
or other permissions.

Here is more information about the provider and consumer roles.

Tip

Sometimes the word *collaborator* is used to mean a consumer or anyone with access to a given clean room.

#### Providers

A *provider* is defined as the account that created a clean room. Anyone accessing the clean room from that account is considered to be a
provider for that clean room.

Providers perform the following clean room actions:

- Create, share, and delete clean rooms
- Specify who can use a clean room as a consumer
- Import data into a clean room
- Define which templates can be run in a clean room
- Specify whether consumers can run a custom template in a clean room
- Specify which templates are used in a clean room, and create custom templates for the clean room
- Run queries on consumer data, if the consumer consents
- Permit chained templates
- Load python script into a clean room to use in a template
- Permit provider data from this clean room to be queried with data from other specified clean rooms in a consumer query
- Enable or disable differential privacy for the clean room or consumer
- Manage versioning of the clean room
- Set column and join policies on their own data

#### Consumers

A *consumer* is defined as an account that was extended an invitation by a provider to join (install) a clean room.

Consumers perform the following clean room actions (according to the clean room configuration):

- Join (install) a clean room for their account
- Import data into the clean room
- Run any queries supported by the clean room
- Export query results as enabled by the clean room
- Request permission to use their own template in a clean room
- Specify whether providers can run a template in the clean room (by default, only consumers can run a template)
- Allow the clean room provider to run queries against the consumer’s data
- Run a query that spans their data and provider data from multiple clean rooms, if the providers in all the affected clean rooms agree.
- Load python script into the clean room (with the permission of the provider)
- Set column and join policies on their own data
- Set differential privacy settings for provider-run queries

## Ways to access Snowflake Data Clean Rooms

Snowflake Data Clean Rooms provide both a no-code browser-based application (the clean rooms UI) and an API to create and manage clean
rooms. Currently the clean rooms UI and API are not exactly equivalent in capabilities. Here is a summary of the differences:

| UI-only features | API-only features |
| --- | --- |
| - Environment management tasks, such as clean room logo, name, and description, the list of available activation or identity   connectors. - Managing the list of administrator, provider, and (potential) consumer accounts. - Scheduling repeating runs of a template. (You can schedule runs using other scripting tools such as cron jobs.) - Using identity providers. | - Creating custom templates, either provider or consumer - Creating template chains - Multi-provider analysis - Consumer-level access control on tables and templates (`restrict_table_options_to_consumers` and `restrict_template_options_to_consumers`). |

Expand

Show lessSee more

Note that you can create a clean room using the clean rooms UI and then use or manage it in the API, and vice versa.

### Clean rooms UI

Snowflake data clean rooms can be managed and run in a browser. You can use the clean rooms UI to create, manage, and use clean rooms as
a provider or consumer, or to configure various account-level features, such as managed accounts, third-party connectors, and features
for UI users.

The clean rooms UI is accessed at a separate URL from Snowsight. You can [find the login URL here](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in).

**Permissions and access:** You must be [granted access to use the clean room UI](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-get-started-add-users) by a clean
room administrator. The clean rooms UI uses your Snowflake credentials.

[Try out the clean rooms UI tutorial](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-tutorial) or
[read more about the clean rooms UI](/user-guide/cleanrooms/v1/web-app-introduction).

### API

Snowflake provides a number of stored procedures to create, manage, and run clean rooms. These procedures can be called through Snowsight
notebooks or worksheets or any interface where you can run stored procedures in your Snowflake account.
The API doesn’t enable clean room account administration; to administer a clean room account you must use the clean rooms UI.

**Permissions and access:** To use the API, you must be
[granted access to use the SAMOOHA\_APP\_ROLE](/user-guide/cleanrooms/manage-dcr-users#label-cleanrooms-add-developers) by a clean rooms administrator for your Snowflake
account.

[Read about the Clean Room API](/user-guide/cleanrooms/v1/developer-introduction) or
[try out the API tutorial](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic).

### Is the clean rooms environment installed in your Snowflake account?

Here is how to tell whether the clean rooms UI or API is installed in your account:

SnowsightClean rooms API

To see whether Snowflake Data Clean Rooms is installed:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Catalog** » **Apps** » **Installed Apps**.
3. Look to see whether **Snowflake Data Clean Rooms** appears in your **Installed Apps** list.

- Run `SHOW ROLES LIKE 'SAMOOHA_APP_ROLE';` to see if the API is installed in your account. If the role appears, the clean rooms
  environment is probably installed.
- Run `SELECT IS_ROLE_IN_SESSION('SAMOOHA_APP_ROLE');` to see whether you have access to the API.
- Run `SHOW GRANTS ON ROLE SAMOOHA_APP_ROLE;` to see what roles can grant SAMOOHA\_APP\_ROLE, which is required to use the API.
