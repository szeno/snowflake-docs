# SNOWFLAKE database

Snowflake provides a system-defined, read-only shared database named SNOWFLAKE that contains metadata and historical usage data
about the objects in your organization and accounts.
The SNOWFLAKE database is an example of [Secure Data Sharing](/guides-overview-sharing) and provides object metadata and other usage metrics for your organization and accounts.

In each account, the SNOWFLAKE database contains the following schemas (also read-only):

ACCOUNT\_USAGE:
:   Views that display object metadata and usage metrics for your account.

ALERT:
:   Functions that are intended for use in [alert objects](/user-guide/alerts).

BILLING:
:   Views that contain billing information for the customers of Snowflake resellers and distributors, as well as FOCUS-compliant cost and
    usage data for org-enabled accounts. See [BILLING](/sql-reference/billing).

CORE:
:   Contains views and other schema objects to support select Snowflake features, such as the
    [system tags](/user-guide/classify-intro#label-classify-classification-tags) used to classify data and the
    [system data metric functions](/user-guide/data-quality-system-dmfs) used to measure data quality.

DATA\_PRIVACY:
:   Contains functions and stored procedures related to data privacy. Also contains the
    [custom\_classifier class](/user-guide/classify-custom).

DATA\_SHARING\_USAGE:
:   Views that display object metadata and usage metrics related to listings published in the Snowflake Marketplace or
    a data exchange.

EXTERNAL\_ACCESS:
:   Schema that contains built-in network rules specific to connections for network traffic outbound from Snowflake.
    For information about egress network rules, see [Snowflake-managed egress network rules](/user-guide/network-rules#label-snowflake-managed-egress-network-rules).

INFORMATION\_SCHEMA:
:   This schema is automatically created in all databases. In a shared database, such as SNOWFLAKE, this schema doesn’t
    serve a purpose and can be disregarded.

LOCAL:
:   This schema is used by some account-level Snowflake features for logging to [telemetry event tables](/developer-guide/logging-tracing/event-table-setting-up#label-logging-event-table-definition).
    For more information about this schema, see [LOCAL](/sql-reference/local).

ML:
:   Contains [ML functions](/guides-overview-ml-functions), which are a suite of analysis tools built by Snowflake.

MONITORING:
:   Views that provide historical information for objects in your account. In the
    [Information Schema](/sql-reference/info-schema), the views and table functions that return historical information will eventually be
    migrated to the MONITORING schema.

NETWORK\_SECURITY:
:   Schema that contains built-in network rules that define the set of allowed IP addresses that a frequently used, third-party
    partner application uses to connect with Snowflake. For more information about Snowflake-managed network rules, see [Snowflake-managed network rules](/user-guide/network-rules#label-snowflake-managed-network-rules). This schema also contains stored procedures for the
    [Network Policy Advisor](/user-guide/network-policy-advisor), including
    [RECOMMEND\_NETWORK\_POLICY](/sql-reference/stored-procedures/recommend_network_policy) and
    [EVALUATE\_CANDIDATE\_NETWORK\_POLICY](/sql-reference/stored-procedures/evaluate_candidate_network_policy).

NOTIFICATION:
:   Stored procedures and functions for [sending notifications](/user-guide/notifications/snowflake-notifications).

ORGANIZATION\_USAGE:
:   Views that display historical usage data across all the accounts in your organization.

READER\_ACCOUNT\_USAGE:
:   Similar to ACCOUNT\_USAGE, but only contains views relevant to the reader accounts (if any) provisioned for the
    account.

SPCS:
:   Functions for use with [Snowpark Container Services](/developer-guide/snowpark-container-services/working-with-services).

TAGS:
:   Contains [Snowflake-provided tags](/user-guide/object-tagging/snowflake-provided-tags) for common governance use cases.

TELEMETRY:
:   Tables, views, and stored procedures to support [collecting telemetry data](/developer-guide/logging-tracing/logging-tracing-overview)
    such as log messages, trace event data, and metrics data.

TRUST\_CENTER:
:   Views that display data about the [Trust Center extensions](/user-guide/trust-center/trust-center-extensions).

Some SNOWFLAKE schemas include classes. A class is an extensible object type that encapsulates object data and code. For more information,
see [Snowflake classes](/sql-reference/snowflake-db-classes).

Important

By default, the SNOWFLAKE database is visible to all users. This does not mean all objects within the SNOWFLAKE database are accessible
to all users.

Objects that are not meant to be accessible by default remain inaccessible unless access is explicitly granted by a user with the
ACCOUNTADMIN role, including access to the ACCOUNT\_USAGE, READER\_ACCOUNT\_USAGE, ORGANIZATION\_USAGE, and DATA\_SHARING\_USAGE schemas.

Privileges to perform other actions on these views can be granted to other roles in your account. For more information, see
[Enabling other roles to use schemas in the SNOWFLAKE database](/sql-reference/account-usage#label-enabling-usage-for-other-roles).
