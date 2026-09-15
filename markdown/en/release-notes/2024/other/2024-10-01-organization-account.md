# October 02, 2024 — Organization accounts — *Preview*

With this release, we are pleased to announce the preview of the organization account, which is a new type of account that organization
administrators use to perform their tasks. During this preview, organization administrators can continue to use an ORGADMIN-enabled account
to perform their tasks, but eventually all organization-level tasks for multi-account organizations will be performed using the organization
account.

The ORGANIZATION\_USAGE schema in the organization account contains premium views that aggregate account usage across accounts. These premium
views are not found in the ORGANIZATION\_USAGE schema of a regular account, and incur additional storage and compute costs. For example, the
organization account allows you to use a single view to track access history across the organization, something you can’t do in a regular
account.

For more information, see [Organization accounts](/user-guide/organization-accounts).
