# Publishing a Snowflake Native App to customers

## Prerequisites

- You must have an existing connection in your `config.toml` file.
- You must have a `snowflake.yml` file in your Snowflake Native App project.
- You must have an existing listing if you are publishing a Snowflake Native App to the [Snowflake Marketplace](/collaboration/collaboration-marketplace-about).

## How to publish a Snowflake Native App to customers

In Snowflake, publishing a Snowflake Native App to customers is done by setting release directives.
Release directives are a set of rules that determine which version and patch of the Snowflake Native App is available to which customers.

Release channels provide a way to manage separate release processes for different types of customers. For example, early access customers can use the ALPHA channel, the internal QA team can use the QA channel, and general customers can use the DEFAULT channel.

If release channels are enabled for an application package, the release directives are tied to the release channels; otherwise, the release directives are tied directly to the application package.

Note

The release channels feature might not be available in all regions. Please contact Snowflake Support for more information.

### Process with release channels enabled

To explicitly enable release channels, add `enable_release_channels=true` to the [application package definition](/developer-guide/snowflake-cli/native-apps/project-definitions#label-cli-app-pkg-entity-props) in your `snowflake.yml` file. You need to update or recreate your application package after enabling release channels.

Note

After enabling, release channels cannot be disabled

To confirm that release channels have been enabled, run the [snow app release-channel list](/developer-guide/snowflake-cli/command-reference/native-apps-commands/release-channel/list) command. A list of release channels in the application package is then displayed:

Copy code

```
snow app release-channel list
```

The simplest way to publish an existing version and patch to all customers on the default release channel is to use the [snow app publish](/developer-guide/snowflake-cli/command-reference/native-apps-commands/publish-app) command with the `--version` and `--patch` options:

Copy code

```
snow app publish --version v1 --patch 1
```

To automatically create a new version and patch, use the `--create-version` option:

Copy code

```
snow app publish --version v1 --create-version
```

To publish a Snowflake Native App to a non-default release channel, use the `--channel` option:

Copy code

```
snow app publish --version v1 --patch 1 --channel ALPHA
```

To publish a Snowflake Native App to a custom release directive targeting specific customers, use the `--directive` option:

Copy code

```
snow app publish --version v1 --patch 1 --channel ALPHA --directive customers_group_1
```

The `snow app publish` command adds the version to the release channel. If the release channel already has the maximum number of versions allowed, this command first attempts to remove from the channel one of the versions not referenced by any release directive.

After adding the version to the release channel, the command sets the default release directive of that release channel to the specified version and patch.

For more control over what is happening, replace the previous command with the following commands:

Copy code

```
snow app release-channel add-version --version v1 ALPHA
snow app release-directive set customers_group_1 --version v1 --patch 1
```

For more information on managing release channels and release directives, see the [snow app release-channel](/developer-guide/snowflake-cli/command-reference/native-apps-commands/release-channel/overview) and [snow app release-directive](/developer-guide/snowflake-cli/command-reference/native-apps-commands/release-directive/overview) command references.

### Process with release channels disabled

If release channels are not enabled for an application package, the release directives are tied directly to the application package.

The simplest way to publish an existing version and patch to all customers is to use the [snow app publish](/developer-guide/snowflake-cli/command-reference/native-apps-commands/publish-app) command with the `--version` and `--patch` options.

Copy code

```
snow app publish --version v1 --patch 1
```

This command sets the default release directive of the application package to the specified version and patch. In this case, release channels are not enabled, so no release channel is involved in this process.

If you want the publish command to automatically create a new version and patch, use the `--create-version` option:

Copy code

```
snow app publish --version v1 --create-version
```

To publish a Snowflake Native App to a custom release directive targeting specific customers, use the `--directive` option:

Copy code

```
snow app publish --version v1 --patch 1 --directive customers_group_1
```

These *snow app publish* commands continue to work even if release channels are enabled in the future. When release channels are enabled, the command starts using the default release channel.
