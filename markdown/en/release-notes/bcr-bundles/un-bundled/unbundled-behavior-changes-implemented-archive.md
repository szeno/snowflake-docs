# Archived implemented unbundled behavior changes

Archived implemented unbundled behavior changes are unbundled behavior changes with an implementation date older than two years.
Snowflake periodically moves older but still relevant implemented unbundled behavior changes to this page.

For more information about unarchived BCRs, see:

- [Recently implemented changes](/release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes#label-unbundled-changes-recently-implemented-changes) that were previously pending/disabled, were not part of a behavior change bundle, and cannot be disabled.
- [Upcoming pending changes](/release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes#label-unbundled-changes-upcoming-pending-changes) that will not be part of a behavior change bundle and cannot be enabled in advance.
- [Canceled behavior changes](/release-notes/bcr-bundles/un-bundled/unbundled-cancelled-behavior-changes#label-unbundled-changes-canceled-changes) that have been removed from BCR bundles and will not be implemented.

If you have questions about any of these behavior changes, please feel free to contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Archived implemented behavior changes

The following table lists behavior changes that were implemented but archived after a certain period of time, typically two years.

| Release Date | Functional Area | Implemented Behavior Change | Additional Notes |
| --- | --- | --- | --- |
| **Nov 30, 2023** | Snowflake Native App Framework | [Snowflake Native App Framework: Need to recreate or update some APPLICATION objects](/release-notes/bcr-bundles/un-bundled/bcr-update-app-dev-mode) |  |
| **Nov 14, 2023** | Snowflake Native App Framework | [Snowflake Native App Framework: Providers must accept terms of service to set the DISTRIBUTION property to EXTERNAL](/release-notes/bcr-bundles/un-bundled/bcr-enforce-provider-tos) |  |
| **Nov 14, 2023** | Snowflake Native App Framework | [Snowflake Native App Framework Changes to the version output for the SHOW APPLICATIONS and DESC APPLICATION commands](/release-notes/bcr-bundles/un-bundled/bcr-add-unversioned-status) |  |
| **Nov 7, 2023** | Snowflake Native App Framework | [Snowflake Native App Framework Cannot use “UNVERSIONED” as the prefix of a version label](/release-notes/bcr-bundles/un-bundled/bcr-prevent-unversioned-in-version-name) |  |
| **October 23, 2023** | SQL Changes — Usage Views & Information Schema Views / Table Functions | [WAREHOUSE\_EVENTS\_HISTORY view: Change to the CLUSTER\_NUMBER column output](/release-notes/bcr-bundles/un-bundled/bcr-warehouse-events-history-cluster-number) |  |
| **Sep 28, 2023** | Data Loading and Unloading | [Stronger UTF-8 validation for external files](/release-notes/bcr-bundles/un-bundled/bcr-1013-1014) |  |
| **Sep 19, 2023** | SQL Changes — Commands & Functions | [SHOW APPLICATIONS command: Changes to the LABEL column output](/release-notes/bcr-bundles/un-bundled/bcr-show-applications-output-change) | This change is enabled by default and cannot be disabled. |
| **Aug 23, 2023** | SQL Changes — Security | [CREATE USER command: NETWORK\_POLICY parameter must specify a valid network policy](/release-notes/bcr-bundles/un-bundled/bcr-non-existing-network-policy) |  |
| **Sep 27, 2022** | Snowflake CLI, Connectors, Drivers, and SQL API Changes | [Snowflake Connector for Python: Empty results of fetch\_arrow and fetch\_pandas are typed](/release-notes/bcr-bundles/un-bundled/bcr-812) |  |
| **Aug 24, 2022** | Snowflake CLI, Connectors, Drivers, and SQL API Changes | [Snowflake .NET driver update - August 2022](/release-notes/bcr-bundles/un-bundled/dot-net-driver-relnotes) | Snowflake .NET driver 2.0.16: Replaces .NET Standard 2.0 with .NET 6.0 |
| **2021 and 2022** | Infrastructure Changes | [Microsoft Azure subnet expansion (Pending for selected accounts)](/release-notes/bcr-bundles/un-bundled/bcr-MSAzure-2021-11-29) | This change only impacts accounts hosted on Azure that are using the functionality documented in the provided article. |

Expand

Show lessSee more
