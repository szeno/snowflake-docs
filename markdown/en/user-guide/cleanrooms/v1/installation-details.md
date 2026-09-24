# Snowflake Data Clean Rooms: Installed objects

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This topic provides information about the objects created in your account when you install a clean room environment.

## High-level overview

The following diagram shows a high-level view of the main objects installed in provider and consumer accounts:

[![High-level diagram of clean room components](/static/images/cleanrooms/DCR-system-diagram.svg)](/static/images/cleanrooms/DCR-system-diagram.svg)

- **Clean rooms UI:** Users accessing a clean room using the clean rooms UI go through a service user account, configured once per account
  by the clean room installer, to the clean rooms API.
- **API user:** API users and the clean rooms UI both use the same clean rooms API. This API is defined by the local DB in your account.
- **Local DB:** Defines the clean rooms API. There is one local DB per account (not per clean room). The actual name of this object is
  [SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB](#label-samooha-by-snowflake-local-db).
- **Clean room application package:** Created on the provider’s account when the provider creates a clean room. There is one package per
  clean room, named `SAMOOHA_CLEANROOM_{cleanroom name}`. This package produces the clean room app installed by the consumer.
- **Back shares:** Back shares must be mounted by the provider to get messages and data from the consumer to the provider.
  Native apps support data flows only from the provider to the consumer, so a back share must be mounted to enable data to flow from the
  consumer to the provider. Two back shares are mounted in the provider’s account: a governance back share, which stores provider-run and
  provider activation data; and a request log back share, which stores messaging and responses from the consumer to the provider, such as
  consumer custom template requests, or consumer approvals of provider run requests. (The share itself lives in the consumer’s account.)
- **Installed app:** Created by an application package, the installed app defines a clean room on the consumer side. The installed app
  follows the naming convention `SAMOOHA_CLEANROOM_APP_cleanroom_name`.
- **Consumer DB:** Contains read-only views of the datasets registered in the consumer’s account. The consumer creates these views when they
  link datasets into the clean room. The consumer’s account contains one consumer DB per clean room, named `SAMOOHA_CLEANROOM_CONSUMER_{clean room ID}`.
- **Clean room:** A clean room at a high level can be considered as comprising the application package and back shares on the provider side,
  plus the installed app and consumer DB on the consumer side.

## Application packages

The following application packages can be installed in your account:

`SAMOOHA_CLEANROOM_{cleanroom name}`
:   Installed in the provider’s account, one application package per clean room created. It contains all the core
    application logic of a clean room created by the provider. It also contains the secure views used to
    share data with the clean room and several tables that store the clean room state. These include tables
    that record the current differential privacy budget of consumers, the column and join policy, and names of
    tables linked to the clean room.

## Applications

The following applications can be installed in your account:

`SAMOOHA_CLEANROOM_APP_cleanroom_name`
:   Installed in the consumer’s account when they install (join) a clean room.

## Databases

Snowflake Data Clean Rooms installs the following databases:

- [SAMOOHA\_BY\_SNOWFLAKE](#samooha-by-snowflake)
- [SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB](#samooha-by-snowflake-local-db)
- [`SAMOOHA_CLEANROOM_{cleanroom ID}`](#samooha-cleanroom-cleanroom-id)
- [`SAMOOHA_CLEANROOM_REQUESTS_{clean room ID}`](#samooha-cleanroom-requests-clean-room-id)
- [`SAMOOHA_CLEANROOM_CONSUMER_{clean room ID}`](#samooha-cleanroom-consumer-clean-room-id)
- [SAMOOHA\_SAMPLE\_DATABASE](#samooha-sample-database)

### SAMOOHA\_BY\_SNOWFLAKE

This database contains all of the core functionality and application logic used to create and manage clean rooms.
This database has the following schemas:

ADMIN schema
:   This schema contains app-level details such as the following:

    - Patches applied (version, commands).
    - Version information (number).

APP\_SCHEMA schema
:   This schema contains functions and procedures that are necessary to facilitate all the clean room flows. Key details include:

    - Encrypt and decrypt functions.
    - Clean room procedures that you use with the developer APIs and clean rooms UI to create, install, and work with clean rooms.

TEMPLATES schema
:   This schema contains the Snowflake-provided SQL Jinja templates.

    These pre-built templates offer ready-to-use SQL queries for secure data collaboration within Snowflake Data Clean Rooms. They leverage
    Jinja templating for customization, allowing you to tailor queries to specific data sharing scenarios.

### SAMOOHA\_BY\_SNOWFLAKE\_LOCAL\_DB

This database is created by the clean rooms UI during the Snowflake installation process. It is local to your account. It is not
an application, but does contain application logic.

This database has two types of data:

- The developer APIs that you and the clean rooms UI use to create and manage clean rooms.
- Intermediate datasets owned by you that get saved to the PUBLIC schema during flows such as identity resolution. For example,
  the output tables from LiveRamp’s resolution and transcoding process are saved to the PUBLIC schema and joined to the view
  that gets linked to the clean room by the clean rooms UI.

The database has the following schemas:

ADMIN schema
:   This schema contains information necessary to operate certain clean room features associated with the account, such as:

    - Using Cross-Cloud Auto-Fulfillment to collaborate across regions or cloud platforms.
    - Clean room metadata updates needed to register clean rooms from developer APIs to the clean rooms UI.
    - Versioning of the current procedures associated with the functioning of the clean rooms UI with the Snowflake account.
    - Tasks and streams that listen to changes in the set of clean room shares that are shared back from collaborators, and to enable/disable
      clean rooms as needed based on the changes.

CONSUMER schema
:   This schema contains the definitions of the [consumer API procedures](/user-guide/cleanrooms/consumer) as well as some common
    consumer tasks.

INFORMATION\_SCHEMA schema
:   Like all Snowflake databases, this database contains the INFORMATION\_SCHEMA schema (“Data dictionary”), which consists of a set of
    system-defined views and table functions that provide extensive metadata information about the objects created in your account.

LIBRARY schema
:   This schema contains the definitions of the `library` namespace API procedures as well as some common tasks and procedures used by both
    providers and consumers.

PROVIDER schema
:   This schema contains the definitions of the [provider API procedures](/user-guide/cleanrooms/provider) as well as some common
    provider tasks.

PUBLIC schema
:   This schema contains the developer APIs that you and the clean rooms UI use to create and manage clean rooms. It also contains
    intermediate datasets owned entirely by you that get saved to the PUBLIC schema during flows such as identity resolution. For example,
    the output tables from LiveRamp’s resolution and transcoding process are saved to the PUBLIC schema and joined to the view that gets
    linked to the clean room by the clean rooms UI.

    This schema has the following tables:

    - **CLEANROOM\_RECORD**: This table includes the status of a clean room (created, deleted) along with the user and timestamp of the last
      update. If the update was done in the clean rooms UI, the user is the service account user. If the update was done in
      Snowsight using
      the developer APIs, the user is the actual user who called the API. The clean room database name can be customized in this table.
    - **CONNECTOR\_CONFIGURATION**: This table is the list of configured connectors in the account.
    - **REPORTS**: This table includes the list of reports saved by the consumer in the clean rooms UI. Top-level results from standard
      reports are saved in the table.
    - **HORIZONTAL\_ANALYSIS\_<report ID>**: Output of analyses executed with the SQL Query template and custom templates executed in the clean
      rooms UI.
    - **CONSUMER\_ACTIVATION\_SUMMARY**: Consumer activation results.
    - **PROVIDER\_ACTIVATION\_SUMMARY**: Provider activation results.

This database has three shares that get created from it:

- **SAMOOHA\_INTERNAL\_GOVERNANCE\_SUMMARY\_SHARE\_NAV2**: This share contains views on the (CONSUMER\_/PROVIDER\_)GOVERNANCE\_SUMMARY and
  (CONSUMER\_/PROVIDER\_)ACTIVATION\_SUMMARY tables in the
  PUBLIC schema. This gets shared with any providers who have created clean rooms installed by this account, and is used to share
  governance information and provider activations back.
- **SAMOOHA\_INTERNAL\_LOGS\_SHARE\_NAV2**: This share is on the LOG\_EVENTS table and is primarily used to share logs on how ID
  resolution procedures are progressing back to Snowflake, given they use third-party native apps. No PII or data is ever shared back,
  only the success/failure of the third-party app APIs used for transcoding/resolution.
- **SAMOOHA\_INTERNAL\_PROVIDER\_METADATA\_NAV2**: This share is on two tables, ADMIN.METADATA\_UPDATE\_REQUESTS, which is used to send registration
  requests from the API to the UI, and ADMIN.RESOURCE\_MONITOR\_USAGE, which is only used by managed accounts to log usage.

### `SAMOOHA_CLEANROOM_{cleanroom ID}`

Each clean room published (as a creator) or installed (as a consumer) has an associated database that includes all the details of that
clean room, including any templates installed, request logs, LAF status, and much more. This database includes the following schemas:

> - **Admin**: Cryptographic keys, privacy budget, request logs, requests for provider analyses, and more.
> - **Shared\_schema**: Join policy, LAF status, linked tables, and versions.
> - **Templates**: List of activation templates, custom templates, and template chains in this clean room.

### `SAMOOHA_CLEANROOM_REQUESTS_{clean room ID}`

This is a database on the provider side and a share on the consumer side. It corresponds to the share that gets sent back from a consumer
to the provider of a clean room as part of the consumer clean room installation process. This database contains information on all the
requests raised by the consumer against the clean room and is used to keep track of the differential privacy budget usage by the consumer.

### `SAMOOHA_CLEANROOM_CONSUMER_{clean room ID}`

This database is installed in consumer accounts only. It is used to share objects such as the secure view of the consumer data to the
clean room, and consumer column/join policies if applied. It has the following table:

- `SAMOOHA_CLEANROOM_CONSUMER_{clean room ID}.SHARED.REQUESTS`. This table shows the consumer exactly which query was attempting to
  run, where PROPOSED\_QUERY is the query rendered from the consumer’s template.

### SAMOOHA\_SAMPLE\_DATABASE

This database contains sample datasets named DEMO.CUSTOMERS and DEMO.CUSTOMERS\_2 that you can use as test data.

Note

The CUSTOMERS\_2 table was added in September 2025. If you installed your clean rooms environment before then, you might not have this
sample table installed. To see whether you have CUSTOMERS\_2 installed, you can run the following SQL code:

Copy code

```
SHOW TABLES LIKE 'CUSTOMERS_2' IN SCHEMA SAMOOHA_SAMPLE_DATABASE.DEMO;
```

If the response contains no rows, then you, or someone with ACCOUNTADMIN role, must run the following command to install the sample table:

Copy code

```
USE ROLE ACCOUNTADMIN;
EXECUTE IMMEDIATE FROM @SAMOOHA_BY_SNOWFLAKE.APP_SCHEMA.MOUNT_CODE_STAGE/dcr_loader.sql;
```

## Tasks

Here are some tasks used by clean rooms that you might see running in your environment.

You can find more information about a given task by running the following procedure:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.DCR_HEALTH.DCR_TASKS_HEALTH_CHECK();
```

[Learn how to view your task and warehouse usage costs.](/user-guide/cleanrooms/v1/cleanroom-cost#label-dcr-v1-view-your-costs)

**Clean room tasks**

| Task name | Description | Warehouse | Entity level |
| --- | --- | --- | --- |
| `AUTO_RUN_warehouse` | Runs the scheduled reports for each warehouse. Uses the warehouse it reports on.  Default schedule: 1 day. | `DCR_WH_warehouse` | Per clean room report |
| `AUTO_RUN_TASK` | Runs the reports set to auto-run.  Default schedule: 1 day. | The warehouse chosen by the user. | Per account |
| `COMPUTE_DATA_STATS_​FOR_ACCOUNT_{consumer locator}` | Computes baseline metrics for joined clean rooms.  Default schedule: 3 hours. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `COMPUTE_DATA_STATS_​FOR_ACCOUNT_{provider locator}` | Computes baseline metrics for created clean rooms.  Default schedule: 3 hours. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `DISTINCT_COLUMN_VALUES​_TASK` | Computes distinct values for datasets linked in a clean room to enable filter dropdowns.  Default schedule: 1 day. | SAMOOHA\_TASK\_WAREHOUSE | Per clean room |
| `EXPECTED_VERSION_TASK` | Automatically upgrades the native app as new versions are released.  Default schedule: Triggered by request. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `LISTEN_TO_REQUESTS` | Mount, repair, and validate incoming shares from collaborators when differential privacy is enabled on the account. The same task at higher a frequency is added to prevent over-running of analysis when DP is enabled. This task costs approximately 6 credits per day.  Default schedule: 1 minute. | \*Serverless\* | Per account |
| `LISTEN_TO_REQUESTS_NODP` | Mount, repair, and validate incoming shares from collaborators.  Default schedule: 30 minutes. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `LISTEN_TO_REQUESTS​_1_COLLABORATOR` | Sets up listeners for the return requests streamed back from the consumer to the provider. Determines whether a clean room has been enabled.  Default schedule: Triggered by request. | SAMOOHA\_TASK\_WAREHOUSE | Per collaborator |
| `MONITORING_SUMMARY_CRON_TASK` | Internal usage.  Default schedule: 30 minutes. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `MOUNT_PROVIDER_ACTIVATIONS_TASK` | Mounts the incoming share for activations for each consumer.  Default schedule: 15 minutes. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `PRIVACY_AND_SECURITY_SCANNER` | Scans each template in each provider’s clean room for privacy and security issues.  Default schedule: 30 minutes. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `PROCESS_ACTIVATIONS` | Decrypts the activation data sent back by the consumer.  Default schedule: Triggered by request. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| PROCESS\_PROVIDER\_ANALYSIS\_REQUESTS | Runs the actual provider analysis.  Default schedule: Triggered by request. | `PROVIDER_RUN_UUID` | Per clean room |
| `PROCESS_REQUESTS_​BUDGET_COLLABORATOR_1` | Processes the differential privacy budget for a clean room.  Default schedule: Triggered by request. | SAMOOHA\_TASK\_WAREHOUSE | Per collaborator |
| `PROCESS_TEMPLATE_REQUESTS​_COLLABORATOR` | Processes the template requests for a clean room.  Default schedule: Triggered by request. | SAMOOHA\_TASK\_WAREHOUSE | Per collaborator |
| `RESET_PRIVACY_BUDGET` | Resets the privacy budget for all clean rooms.  Default schedule: 1 day. | SAMOOHA\_TASK\_WAREHOUSE | Per clean room |
| `SAMOOHA_INTERNAL_UID_​OUTPUT_TABLE_REFRESH_TABLE_DATA_TASK` | Created once per table.  Default schedule: 1 day. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `SETUP_AUTO_RUN` | Sets up auto-run reports.  Default schedule: 60 minutes. | SAMOOHA\_TASK\_WAREHOUSE | Per account |
| `SETUP_PROVIDER_ANALYSIS​_REQUESTS` | Sets up provider analysis infrastructure and processes the requests for provider analysis.  Default schedule: Triggered by request. | SAMOOHA\_TASK\_WAREHOUSE | Per clean room |
| `TRIGGER_REFRESH_FOR_LAF_CLEANROOMS` | Triggers data refresh for Cross-Cloud Auto-Fulfillment enabled clean rooms.  Default schedule: 30 minutes. | SAMOOHA\_TASK\_WAREHOUSE | Per account |

Expand

Show lessSee more

## Warehouses

Snowflake Data Clean Rooms installs the following warehouses in your account. You can change the size of any warehouse
as needed. We recommend that you use XS warehouses for general clean room editing, creation, or deletion commands. Consider using larger warehouses, or Snowpark-optimized warehouses, when running large analyses, such as machine learning workloads.

[Learn how to view your warehouse usage costs.](/user-guide/cleanrooms/v1/cleanroom-cost#label-dcr-v1-view-your-costs)

| Warehouse name | Notes |
| --- | --- |
| APP\_WH | XSMALL warehouse has access to the API, sets up new clean rooms, manages permissions and data sharing. |
| DCR\_WH\_SMALL | Regular, SMALL warehouse |
| DCR\_WH\_Medium | Regular, MEDIUM warehouse |
| DCR\_WH\_Large | Regular, LARGE warehouse |
| DCR\_WH\_XLarge | Regular, XLARGE warehouse |
| DCR\_WH\_2XLARGE | Regular, XXLARGE warehouse |
| DCR\_WH\_4XLarge | Regular, X4LARGE warehouse |
| DCR\_WH\_OPT\_XLarge | Snowpark-Optimized, XLARGE warehouse |
| DCR\_WH\_OPT\_2XLarge | Snowpark-Optimized, XXLARGE warehouse |
| DCR\_WH\_OPT\_4XLarge | Snowpark-Optimized, X4LARGE warehouse |
| PROVIDER\_RUN\_<cleanroom\_identifier> | Warehouse in consumer’s account that executes analyses run by the provider. |
| SAMOOHA\_TASK\_WAREHOUSE | XSMALL warehouse used for many things, such as privacy and security scans, processing auto-run reports, computing data stats, and processing consumer template requests. |
| DCR\_ACTIVATION\_WAREHOUSE | Used to decrypt activation results sent to the provider. Default size is XL, but size can be modified by calling `provider.update_activation_warehouse`. |

Expand

Show lessSee more

## Other objects

Snowflake Data Clean Room installs the following additional objects:

- SAMOOHA\_SERVICE\_ACCOUNT\_USER\_ACCESS: A user-level network policy used by the service user to
  [enable the clean room UI](/user-guide/cleanrooms/v1/enable-clean-rooms-ui#label-dcr-install-clean-rooms-ui-step).
