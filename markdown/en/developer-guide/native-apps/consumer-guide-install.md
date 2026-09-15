# Install a Native App

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

## From the Snowflake Marketplace

The Snowflake Marketplace is the primary channel for discovering and installing apps. From
[Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in), navigate to the Marketplace, find the listing, and follow the installation
prompts. The listing page includes the provider’s description, pricing, and contact information.

For full step-by-step instructions, see [Install an app from a listing](/developer-guide/native-apps/ui-consumer-installing).

## From a private listing

Some apps are distributed via private listings shared directly with your account rather than
published on the public Snowflake Marketplace. The installation steps are the same, but note the
following: private listings may not have gone through the same Marketplace-level review that public
listings require. Apply the same security evaluation process described in
[Evaluate a Native App before installing](/developer-guide/native-apps/consumer-guide-evaluate) regardless of how the listing is
distributed.

In either case, you can install from the `default` channel (typically for production-quality
versions) or, where available, from the `alpha` channel for previews or User Acceptance Testing
(UAT) prior to production use. See [About release channels, versions, and patches](/developer-guide/native-apps/release-channels-versions) for
details.

## Installation overview

Installing a Snowflake Native App creates an APPLICATION object in your account and runs the app’s setup
script, which creates the objects the app needs inside its boundary. The app is not fully
operational at this point: you will need to approve any App Specs and configure the explicit data
access grants the app needs before it can deliver its intended value. Plan for this post-install
configuration step with sufficient privileges so that you can approve or decline what the app asks
and let app users get a fully functional app.

At installation time, the app presents:

- Its Category 1 privilege requests (the operational resources it needs to create). These are
  automatically granted to the app if you agree and proceed with the installation.
- Any initial App Specs requiring your approval.

Review these before clicking through. If something in the list is unexpected (a privilege or App
Spec you were not told about during procurement), pause and ask the provider to clarify before
proceeding.

## Apps with containers (SPCS)

Apps with containers have the same installation flow with one prerequisite: your account must have
Snowpark Container Services enabled. The app may create a compute pool automatically if it has
requested the `CREATE COMPUTE POOL` privilege. Compute pools cannot be shared across apps or
between an app and your non-app workloads.

For full step-by-step instructions, see
[Install and manage an app with containers](/developer-guide/native-apps/ui-consumer-installing-container).

## Using the Snowflake CLI

Developers and administrators who prefer a command-line workflow can install and manage Native Apps
using the Snowflake CLI. They can also perform the necessary app configuration and grants via SQL
after successful installation.

For full instructions, see [Set up the Snowflake CLI to develop an app](/developer-guide/native-apps/installing-snow-cli-na).
