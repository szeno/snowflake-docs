# Package Versions in Declarative Sharing in the Native Application Framework

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

## Versioning Application Packages in Declarative Sharing

With Declarative Sharing, versioning of your Declarative Native App is handled automatically, so providers and consumers don’t need to manually track version numbers. This simplifies the development and release process.

As a provider, you can iterate on your application in a live development environment and release new versions.

This topic describes how versioning works in the Snowflake Native App Framework for Declarative Native Apps and how new versions are made available to consumers.

### Make new versions of the application package

With Declarative Native Apps, versioning is handled automatically.

Providers can make changes to the new live version of the app, update the contents, and re-release the application package.

Shortly after releasing a new version, it appears both for existing consumers and for new consumers in the Snowflake Marketplace.

Neither providers nor consumers can revert to a previous version of the app.

Workspaces and notebooks are embedded in the application package and versioned along with the manifest.

Notebook versioning commands, such as `ALTER NOTEBOOK CREATE LIVE VERSION FROM LAST`, aren’t supported for these notebooks.
