# Creating a Listing using Declarative Sharing

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

After you have created and tested your Declarative Native App, you can make it available to consumers by creating a listing. A listing makes your app discoverable and accessible to other Snowflake accounts, either privately to specific accounts or publicly on the Snowflake Marketplace. This topic provides an overview of the requirements and steps to create a listing for your Declarative Native App.

## Create a listing

To publish to consumers, a provider can share a Declarative Native App with consumers by publishing a [listing](https://other-docs.snowflake.com/collaboration/collaboration-listings-about).

The process is the same as with Snowflake Native Apps. For more information, see [Native Apps workflow:publish](/developer-guide/native-apps/native-apps-workflow#label-native-apps-workflow-publishing).

Note

Organizational listings are currently only supported when the provider and consumer are in different Snowflake accounts.

For same-account testing, perform the installation directly from the package rather than through the organizational listing mechanism.

### Access control requirements

To create a listing, the provider requires additional privileges, including:

- **OWNERSHIP** on the application package
- Global **CREATE LISTING** privilege

For additional requirements to create a listing, see [Use listings as a provider](https://other-docs.snowflake.com/en/collaboration/provider-becoming).

## Consumers install and use the app

After you create a listing for your app, consumers can install the app from the Snowflake Marketplace. For more information, see [Install a Declarative Native App](/developer-guide/declarative-sharing/consumer/install).
