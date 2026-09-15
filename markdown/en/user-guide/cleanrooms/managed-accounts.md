# Clean room managed accounts

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

Managed Account Terms termination

The [Snowflake Data Clean Room Managed Account Terms](https://www.snowflake.com/en/legal/other/data-clean-rooms/managed-account-terms/)
are being terminated effective **2027-06-01**. Prior to that date, your ability to create new managed accounts
is limited as described in the end-of-life notice above. Snowflake will contact affected managed account
users separately with additional details.

## Overview

A clean room provider must have a Snowflake account. However, a provider can collaborate with consumers who do not have Snowflake
accounts by inviting them to collaborate using a *clean room managed account*. To begin collaborating in a clean room, the consumer simply
accepts the provider’s invitation to use the managed account.

If you want to invite new managed account users to your clean rooms, contact your clean rooms account representative.

A managed account can be converted to a Snowflake account in the consumer’s organization if the managed account user wants to become a
Snowflake Service customer.

[See the usage terms](https://www.snowflake.com/en/legal/other/data-clean-rooms/managed-account/) that apply to managed accounts
in Snowflake Data Clean Rooms.

Important

The consumer who accepts a provider’s invitation to use a managed account pays for the use of the clean room. When accepting the
invitation, the consumer must enter billing details before accessing the clean room environment.

## Requirements and limitations

A managed account has the following requirements and limitations:

- It requires the use of external tables for the managed account user to import data. As a result, the provider must explicitly
  [allow the use of external tables in the clean room](/user-guide/cleanrooms/register-data).
- It does not behave the same as a Snowflake [reader account](/user-guide/data-sharing-reader-create). The
  consumer does not access the managed account outside the context of the clean room environment.
- It can be used only as a clean rooms consumer, not a clean rooms provider.
- It does not support the use of [identity connectors](/user-guide/cleanrooms/connector-identity) in an analysis.
- An underlying Snowflake instance is created in the same cloud region as the provider but the managed account consumer can
  link their data from any cloud region. The managed account user can access the underlying data only by using the clean rooms UI.
- A managed account user cannot use the clean rooms APIs.
- Providers using a trial Snowflake account cannot invite managed account users as collaborators.

## Provider tasks

Follow these steps to add a managed account user as a collaborator:

- [1. Enable external tables for your account (and clean room)](#enable-external-tables-for-your-account-and-clean-room)
- [2. Invite a consumer to collaborate using a managed account](#invite-a-consumer-to-collaborate-using-a-managed-account)
- [3. Find the account identifier of a managed account](#find-the-account-identifier-of-a-managed-account)
- [4. Share a clean room with a managed account](#share-a-clean-room-with-a-managed-account)

### 1. Enable external tables for your account (and clean room)

The provider must ensure that [external tables are enabled for the account](/user-guide/cleanrooms/register-data#label-cleanrooms-external-iceberg-tables) (and, if the
provider is using the API, the specific clean room). The consumer links data using an external table connector appropriate for their cloud
platform. The consumer does not need to enable external tables.

### 2. Invite a consumer to collaborate using a managed account

When a provider wants to collaborate with a consumer who does not have a Snowflake account, they can invite them to
collaborate using a managed account.

Important

Contact your clean rooms account representative to request the ability to add new managed account users to your account.

To send a consumer an invitation for a managed account:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Collaborators**.
3. Select **Managed Accounts** » **+ Managed Account**.
4. In the **Company Name** field, enter the name of the consumer you are inviting to use the managed account.
5. In the **Account Admin Email**, enter the email of the consumer’s administrator. The invitation to use the managed account is sent to
   this email.
6. Select **Invite**.

   An email is sent to the consumer inviting them to use the managed account to access a clean room environment.

### 3. Find the account identifier of a managed account

Clean room managed accounts have account identifiers just like fully capable Snowflake accounts. You might need an identifier
for tasks like using the developer API to share a clean room with a consumer.

To find the account locator or account name for a managed account:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Collaborators**.
3. Find the name of the managed account, and do one of the following:
   1. If you need the [account locator](/user-guide/admin-account-identifier#label-account-locator) format of the account identifier, copy the value under
      **Account Locator**.
   2. If you need the [account name](/user-guide/admin-account-identifier#label-account-name) format of the account identifier, copy the value under
      **Account Identifier**.

### 4. Share a clean room with a managed account

The consumer is limited to using the UI from a managed account, so you can share only clean rooms that have an analysis that is runnable in
the UI. This means either an analysis created in the UI, or a custom template that has a
[user input form](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-define-user-form).

You cannot share a clean room with a consumer until they accept your invitation to collaborate using the managed account. To
determine whether the consumer has accepted the invitation and signed in to the clean room environment:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Collaborators**.
3. Find the name of the managed account. If the consumer has accepted the invitation, the status of the account is **Active**. You have
   the option of resending the invite if the consumer did not respond to the original email.

After the consumer accepts the invitation to use the managed account, you can create a clean room to share with the consumer. Simply select
them as a collaborator during the Share portion of the creation process.

## Consumer (managed account user) tasks

Working with managed accounts as a consumer consists of the following tasks:

- [Get started with the managed account](#get-started-with-the-managed-account)
- [Access your data in a clean room](#access-your-data-in-a-clean-room)
- [Join a clean room](#join-a-clean-room)
- [Monitor and manage the cost of your managed account](#monitor-and-manage-the-cost-of-your-managed-account)
- [Become a Snowflake Service customer](#become-a-snowflake-service-customer)

### Get started with the managed account

When a provider invites a consumer to collaborate using a managed account, the consumer administrator receives an email that lets them sign
up for the clean room environment. The provider cannot share a clean room with the consumer until the administrator uses the link in the
email to complete
the sign up process.

Because the consumer pays for their use of the managed account, the first person to sign in to the clean room environment is prompted to
enter billing information. If you want to change this billing information after the initial sign in, contact [accounts.receivable@snowflake.com](mailto:accounts.receivable@snowflake.com).

### Access your data in a clean room

You can join your data with the provider’s data to gain valuable insights. Clean room external data connectors let you
link your data into a clean room.

Follow the steps in one of the following topics, depending on your cloud hosting platform, to link your data into a clean room:

- [Snowflake Data Clean Room: External data from an Amazon S3 bucket](/user-guide/cleanrooms/external-data-aws)
- [Snowflake Data Clean Room: External data from Azure Blob Storage](/user-guide/cleanrooms/external-data-azure)
- [Snowflake Data Clean Room: External data from Google Cloud Platform](/user-guide/cleanrooms/external-data-gcp)

These topics also include information about revoking access to your data, which you can do at any time.

### Join a clean room

After a provider creates and shares a clean room with you, you can sign in to the clean room environment and join the clean room to start
running analyses. To join a clean room:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Clean Rooms**.
3. Select the **Invited** tab.
4. Find the tile for the clean room, and select **Join**.

### Monitor and manage the cost of your managed account

As a consumer, you pay for the use of the clean room managed account that the provider created for you. Snowflake Data Clean Rooms lets you:

- Monitor how many credits have been consumed by your clean room activities during the current month.
- Set a limit on how much you spend on clean rooms in a given month. After a limit has been set, users cannot sign in to the clean rooms UI
  if the total credit consumption is within 10 credits of the limit.

To monitor and manage the cost of your managed account:

1. [Sign in to the clean rooms UI.](/user-guide/cleanrooms/web-app-introduction#label-cleanroom-web-app-sign-in)
2. In the left navigation, select **Admin** » **My Account**.
3. Use the **Credit Limit & Usage** section to set a monthly spending limit and view the current number of credits consumed. A blank
   limit allows unlimited spending.

### Become a Snowflake Service customer

If you want to start using a managed account for more than clean rooms, you can convert it to a fully capable
Snowflake account. To convert a managed account, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).
