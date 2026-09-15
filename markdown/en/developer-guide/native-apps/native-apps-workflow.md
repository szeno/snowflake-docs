# Snowflake Native App Framework workflow

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes the workflows for developing, publishing, and installing a Snowflake Native App.

## Development workflow

The following workflow outlines the general tasks for developing and testing Snowflake Native App:

Note

Developing an app is an iterative process. You might perform many of these tasks multiple
times or in a different order depending on the requirements of your app and environment.

1. Set up your development environment.

   To develop a Snowflake Native App, you need to set up your development environment. This includes:

   - Install the Snowflake CLI. See [Set up the Snowflake CLI to develop an app](/developer-guide/native-apps/installing-snow-cli-na).
   - Create a stage to upload your application files.

     Note

     If you are using Snowflake CLI you do not need to create a stage manually because Snowflake CLI
     automatically creates a temporary stage to upload your application files during development.

     For information on creating a stage using SQL, see [CREATE STAGE](/sql-reference/sql/create-stage). For information on creating a stage using Snowsight, see
     [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui).
2. [Create an application package](/developer-guide/native-apps/creating-app-package).

   An application package is a container that encapsulates the data content, application logic,
   metadata, and setup script required by an app.
3. [Create the setup script](/developer-guide/native-apps/creating-setup-script) for your
   app.

   The setup script contains the SQL statements that define the components created
   when a consumer installs your app.
4. [Create the manifest file](/developer-guide/native-apps/manifest-overview) for your
   app.

   The manifest file defines the configuration and setup properties required by the app,
   including the location of the setup script and versions.
5. Upload the application files to a stage.

   The setup script, the manifest file, and other resources that your app requires
   must be uploaded to a named stage so that these files are available as you develop your app.
6. Add versions and patches for your app.

   See [About release channels, versions, and patches](/developer-guide/native-apps/release-channels-versions) for more information.
7. Add shared data content to your app.

   You can securely share your data content with consumers as part of your app. For more information,
   see [Share data content in a Snowflake Native App](/developer-guide/native-apps/preparing-data-content)
8. Add features to your app.

   You can add various features to your app to provide additional functionality, including the following
   features:

   - [Add application logic to an application package](/developer-guide/native-apps/adding-application-logic)
   - [Extending Snowflake with Functions and Procedures](/developer-guide/extensibility).
   - [Snowpark API](/developer-guide/snowpark/index).
   - [Introduction to external functions](/sql-reference/external-functions-introduction).
9. [Set up logging and event handling to troubleshoot your app.](/developer-guide/native-apps/event-about)

   To troubleshoot an app, you can set up logging and event handling.
   Consumers can set up logging and event handling in their account and share them with providers.
10. Set the release directive for your app.

A release directive determines which version and patch level are available to consumers. You can set the release directive for each release channel of your application package. For more information, see
[Set the release directive using a release channel](/developer-guide/native-apps/release-channels#label-native-apps-relchan-release-directive).

11. Test your app.

You can test an app in your account before publishing it to consumers. For more information, see
[Install and test an app locally](/developer-guide/native-apps/installing-testing-application).

Snowflake provides [development mode](/developer-guide/native-apps/installing-testing-application#label-native-apps-dev-mode) and
[debug mode](/developer-guide/native-apps/installing-testing-application#label-native-apps-testing-debug-mode) to test different aspects of your app.

12. [Run the automated security scan](/developer-guide/native-apps/security-overview).

Before you can share an app with consumers outside your organization, the app must pass an
automated security scan to ensure that it is secure and stable.

## Publishing workflow

After developing and testing your app, providers can publish the app to share it
with consumers.

1. [Become a provider](/collaboration/provider-becoming).

   Becoming a provider allows you to create and manage listings to share your app with consumers.
2. Create a listing.

   You can create a private listing or a Snowflake Marketplace listing to share your app with consumers.
   For more information, see [Create a listing for an app](/developer-guide/native-apps/ui-provider-publishing-app-package#label-nativeapps-provider-listings-create).
3. Submit your listing for approval.

   Before you can publish a listing to the Snowflake Marketplace, you must submit the listing to
   Snowflake for approval. For more information, see [Submit a listing for approval](/developer-guide/native-apps/ui-provider-publishing-app-package#label-nativeapps-provider-listings-submit-approval)
4. Publish your listing.

   After your listing is approved, you can publish the listing to make it available to consumers.
   For more information, see [Publish a listing for an app](/developer-guide/native-apps/ui-provider-publishing-app-package#label-nativeapps-provider-listings-publish).

## Consumer workflow

Consumers can discover the app and install it from a listing. After installing the
app, consumers can configure, use, and monitor the app. See
[Working with apps as a consumer](https://other-docs.snowflake.com/en/native-apps/consumer-about).

1. [Become a Snowflake consumer](/collaboration/consumer-becoming).

   Becoming a Snowflake consumer allows you to access listings shared privately or on the
   Snowflake Marketplace. You can also access data shared as part of direct shares or data exchanges, which
   offer more limited data sharing capabilities.
2. [Install the app](https://other-docs.snowflake.com/en/native-apps/consumer-installing).

   Consumers can install an app from a listing.
3. [Grant the privileges required by the app](https://other-docs.snowflake.com/en/native-apps/consumer-granting-privs).

   Some apps might ask the consumer to grant global and object-level privileges to
   the app.
4. [Enable logging and event sharing to troubleshoot the app](https://other-docs.snowflake.com/en/native-apps/consumer-enable-logging).

   A provider can set up an app to emit logging and event data. A consumer can set up an events table
   to share this data with providers. Logs and event data are useful when troubleshooting an app.
5. [Manage an app](https://other-docs.snowflake.com/en/native-apps/consumer-managing-applications).

   After installing and configuring the app, a consumer can perform additional tasks to
   use and monitor the app.
