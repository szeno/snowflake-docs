# Data Clean Rooms Developer Guide

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

This topic provides guidelines for users who want to create or manage Snowflake Data Clean Rooms collaborations programmatically.

## Development tools

These are the main developer tools for Snowflake Data Clean Rooms collaborations:

- **Coding environment:** Any coding environment that can run stored procedures in your Snowflake account will work. Most developers use
  worksheets in Snowsight (the browser-based tool) or the [Snowflake CLI](/developer-guide/snowflake-cli/index).
- **Cortex Code:** Data Clean Room procedures are also available in an agentic experience via
  [Cortex Code](/user-guide/cortex-code/cortex-code).

## Setting up your environment

Here are some tips for setting up your coding environment to use the Snowflake Data Clean Rooms API effectively.

- [Using the Collaboration API](#using-the-collaboration-api)
- [Choosing a warehouse](#choosing-a-warehouse)
- [Setting up testing accounts](#setting-up-testing-accounts)

### Using the Collaboration API

Snowflake provides the Data Clean Rooms Collaboration API to create and manage collaborations. This API consists of stored procedures that can be run
in any environment that can access your Snowflake account. This includes Snowsight notebooks, workspaces, worksheets and the
[Snowflake CLI](/developer-guide/snowflake-cli/index).

The documentation here shows SQL usage, but you can also use Python or
[any other supported Snowflake language](/developer-guide/stored-procedure/stored-procedures-overview#label-stored-procedures-handler-languages).

You can grant users access to the complete API or a subset of it through
specific [DCR privileges](/user-guide/cleanrooms/manage-access#label-dcr-collab-list-of-required-privileges).

Note

You need proper [DCR privileges](/user-guide/cleanrooms/manage-access#label-dcr-collab-about-rbac-roles) to use the Collaboration API. You can grant limited access to specific procedures for sub-groups of users through [fine-grained role-based access control](/user-guide/cleanrooms/manage-access).

The SAMOOHA\_APP\_ROLE has pre-configured access to the entire API.

### Choosing a warehouse

You must use the Collaboration API in a warehouse that your role has the USAGE privilege on. `APP_WH` is one of a
[number of warehouses](/user-guide/cleanrooms/v1/installation-details#label-cleanrooms-installation-details-warehouses) that you can use. Choose the appropriate
warehouse for your needs.

Any standard warehouse works for general collaboration editing, creation, or deletion commands. Consider
using larger warehouses, or Snowpark-optimized warehouses, when running large analyses, such as machine learning workloads. If you use a
Snowpark-optimized warehouse for reviewing or joining a collaboration, make sure [MAX\_CONCURRENCY\_LEVEL](/sql-reference/parameters#label-max-concurrency-level) is set to a value equal to or greater than 2.

### Setting up testing accounts

You should have at least two separate accounts in which you have full coding access, to be able to develop and test multi-party
collaborations.

Depending on your use case, you might also want a Snowflake test account in a different cloud hosting region to test
[cross-cloud behavior](/user-guide/cleanrooms/laf).

Name your test Snowflake accounts meaningfully to indicate their typical usage: for example, “Cross-cloud account” or “Standard Edition
account.” This can help when you have multiple test accounts and must choose an account on the clean
rooms login page.

## References and resources

The following topics are useful for Snowflake Data Clean Room developers.

- **Reference topics:**

  - [Snowflake Data Clean Rooms Collaboration API](/user-guide/cleanrooms/collaboration-api-reference)
  - [Data Clean Rooms Schema Reference](/user-guide/cleanrooms/spec-reference)
  - [Design custom templates](/user-guide/cleanrooms/custom-templates)
  - [Items installed with the Snowflake Data Clean Room environment](/user-guide/cleanrooms/installed-artifacts): What objects are installed with the SDCR environment.
- **Sample data:**

  - The Snowflake DCR environment installs [a few sample datasets](/user-guide/cleanrooms/installed-artifacts#label-dcr-samooha-sample-database-new) that you can use.
  - You can also [generate synthetic test data](/user-guide/synthetic-data) using Snowflake.
- **Troubleshooting:** See the [data clean room troubleshooting guide](/user-guide/cleanrooms/v2/troubleshooting) for tips.
- **Useful collaboration metadata:** See the [metadata cheat sheet](/user-guide/cleanrooms/collaboration-api-reference#label-dcr-collab-metadata-cheat-sheet) to learn how to get
  useful metadata about a collaboration, such as whether a collaborator (including yourself) has installed a given collaboration.
- **See your API query history:** To see a history of Collaboration API (or other) calls that you’ve made:

  1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
  2. In the navigation menu, select **Monitoring** » **Query History**.
  3. Use the filters to find the query associated with the analysis, and select the query or analysis.
- **Feature examples:** To help you understand how to use various features of the Collaboration API, you can refer to the examples in the
  **Use cases** and **Key concepts & features** sections of the Snowflake DCR documentation.
- **Additional examples and videos:** For additional code examples, tutorials, and videos, see
  [Sample Worksheets and Videos](/user-guide/cleanrooms/tutorials-and-samples).
