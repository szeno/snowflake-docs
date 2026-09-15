# Managing Cross-Cloud Auto-Fulfillment in Collaboration Data Clean Rooms

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About Cross-Cloud Auto-Fulfillment

Collaborators can seamlessly share data with collaborators in different cloud regions. In order to do so, they must enable
[Cross-Cloud Auto-Fulfillment](/collaboration/provider-listings-auto-fulfillment) on their account. Only collaborators sharing or activating data must enable this on their account.

When Cross-Cloud Auto-Fulfillment is used in a collaboration:

- Data is replicated into the cloud region of each collaborator that can access that data.
- Data is also replicated into the owner’s region for orchestration purposes via the Secure Collaboration Orchestrator (SCO). However, the collaboration owner’s ability to
  access the data is determined by the data offering’s sharing rules.
- Collaborators in a different cloud region experience some data lag due to the
  [replication frequency](#label-dcr-laf-collab-refresh-rates).

## Enabling Cross-Cloud Auto-Fulfillment

Cross-Cloud Auto-Fulfillment must be enabled in the account of any collaborator that needs to share data with an account in another cloud hosting region. If this feature isn’t enabled for an account or role in an account, follow the below steps:

1. Enable Cross-Cloud Auto-Fulfillment for an account

   - **To check if Cross-Cloud Auto-Fulfillment is enabled on an account,** an organization administrator must call [SYSTEM$IS\_GLOBAL\_DATA\_SHARING\_ENABLED\_FOR\_ACCOUNT](/sql-reference/functions/system_is_global_data_sharing_enabled_for_account).
   - **To enable Cross-Cloud Auto-Fulfillment on an account,** an organization administrator must call [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account).
2. Enable Cross-Cloud Auto-Fulfillment for a role in an account

   - **To delegate privileges to another role in an account,** an ACCOUNTADMIN role can grant the MANAGE LISTING AUTO FULFILLMENT privilege to other roles in the account. For more information, see [Manage privileges for auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-manage-privileges).

Note

Each user who will call REVIEW or JOIN must have a first and last name set with a validated email address on
their Snowflake user profile. See [Verify the email addresses of the email notification recipients](https://docs.snowflake.com/en/user-guide/notifications/email-notifications#label-email-notification-verify-address)
for instructions.

## Refresh frequency for cross-region accounts

Update requests and shared data between collaborators in different cloud regions are subject to a 10-minute refresh schedule. This schedule is not configurable.

## Costs associated with cross-region collaboration

Additional costs are incurred when collaborators are in different cloud regions. For more information
about how these costs are incurred, see [Auto-fulfillment costs](/collaboration/provider-understand-cost-auto-fulfillment).

## Limitations on cross-region collaboration

The following limitations exist on cross-region collaboration:

- Data offerings that reference external or Apache Iceberg™ tables can’t be shared with collaborators in a different
  cloud or region than the collaboration owner.
- Every collaborator must have a different [account locator](/user-guide/admin-account-identifier#label-account-locator).
- See [additional considerations when enabling cross-region collaboration](/collaboration/provider-listings-auto-fulfillment#label-listings-auto-fulfill-considerations).
