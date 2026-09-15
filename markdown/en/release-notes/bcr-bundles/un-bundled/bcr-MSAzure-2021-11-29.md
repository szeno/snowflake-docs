# Microsoft Azure subnet expansion (Pending for selected accounts)

As of **November 2021**, this change has been implemented for the following Azure regions:

- US East 2
- Canada Central

The change for the remaining regions has been scheduled for January 2022; however the date is subject to change.
For the most up-to-date details about the date on which it will be enabled, as well as other release-related details, refer to
[Behavior change announcements](/release-notes/behavior-changes).

In the 5.23 Behavior Change Release Notes, we announced the implementation of additional subnets in
the Microsoft Azure virtual network for all Snowflake accounts. The additional subnets provide scalability improvements, but can impact the
following access:

- Access to external stages and tables that reference Azure cloud storage.
- Azure storage queue access for Snowpipe auto-ingest.

- Customer-managed key access to tables for [Tri-Secret Secure](/user-guide/security-encryption-tss) with firewall-enabled Azure Key Vault.

If one or more of your accounts was identified as being impacted by this change, we deactivated the additional subnets for those accounts
while Snowflake Support contacted your internal Azure administrator about making the required network and firewall updates to allow
uninterrupted access.

The additional subnets have been activated for accounts in the East US 2 and Canada Central regions, with the remaining regions to
follow in **January 2022**. If your internal Azure administrator has not yet made the required updates when the subnets are activated,
your accounts may be impacted as described above.

This article provides additional information and resources to facilitate completing the required tasks before the scheduled date:

- [Update the Azure Key Vault Allow List (for Tri-Secret Secure with Key Vault Firewall enabled)](https://community.snowflake.com/s/article/Microsoft-Azure-Subnet-Expansion?r=398&ui-knowledge-components-aura-actions.KnowledgeArticleVersionCreateDraftFromOnlineAction.createDraftFromOnlineArticle=1#update-key-vault)

- [Identify the Azure Subnets](https://community.snowflake.com/s/article/Microsoft-Azure-Subnet-Expansion?r=398&ui-knowledge-components-aura-actions.KnowledgeArticleVersionCreateDraftFromOnlineAction.createDraftFromOnlineArticle=1#identify-subnets)
- [Update the Azure Storage Allow List (for External Stages/Tables and Snowpipe Auto-ingest)](https://community.snowflake.com/s/article/Microsoft-Azure-Subnet-Expansion?r=398&ui-knowledge-components-aura-actions.KnowledgeArticleVersionCreateDraftFromOnlineAction.createDraftFromOnlineArticle=1#update-storage)
  - Note: All of these tasks can and should be completed before the scheduled date to prevent any disruptions.

Identify the Azure Subnets:

To obtain a list of all the Azure subnet IDs for your Snowflake account(s), log into each account that will be impacted by the change and
execute the [SYSTEM$GET\_SNOWFLAKE\_PLATFORM\_INFO](/sql-reference/functions/system_get_snowflake_platform_info) function.

Example JSON output for an account (line breaks added for readability):

Copy code

```
{"snowflake-vnet-subnet-id":[
"/subscriptions/ae0c1e4e-d49e-4115-b3ba-888d77ea97a3/resourceGroups/azure-prod/providers/Microsoft.Network/virtualNetworks/azure-prod/subnets/xp",
"/subscriptions/ae0c1e4e-d49e-4115-b3ba-888d77ea97a3/resourceGroups/azure-prod/providers/Microsoft.Network/virtualNetworks/azure-prod/subnets/gs",
"/subscriptions/37265438-aa4f-49f6-adc4-46271ae19193/resourceGroups/deployment-infra-rg2/providers/Microsoft.Network/virtualNetworks/deployment-vnet2/subnets/xp",
"/subscriptions/37265438-aa4f-49f6-adc4-46271ae19193/resourceGroups/deployment-infra-rg2/providers/Microsoft.Network/virtualNetworks/deployment-vnet2/subnets/gs",
"/subscriptions/63c9e19b-5cf1-4dcf-ace5-bf0f416f2ff7/resourceGroups/deployment-infra-rg3/providers/Microsoft.Network/virtualNetworks/deployment-vnet3/subnets/xp",
"/subscriptions/63c9e19b-5cf1-4dcf-ace5-bf0f416f2ff7/resourceGroups/deployment-infra-rg3/providers/Microsoft.Network/virtualNetworks/deployment-vnet3/subnets/gs"
]}
```

Update the Azure Key Vault Allow List (for Tri-Secret Secure with Key Vault Firewall enabled):

If you are using Tri-Secret Secure with Key Vault firewall enabled, you must update the Azure VNet allow list for Key Vault to include the additional subnets.

To update the allow list for Key Vault, complete the instructions in the this [Community article](https://community.snowflake.com/s/article/Azure-Tri-Secret-Secure-Firewall-enabled-Azure-KeyVault.html).

Note: The required subnets for Key Vault are appended with /gs. You must add each /gs subnet individually.

Update the Azure Storage Allow List (for External Stages/Tables and Snowpipe Auto-ingest):

If you are using Azure Storage for external stages/tables or Snowpipe auto-ingest, you must update the Azure VNet allow list for Azure Storage to include the additional subnets.

To update the allow list for Azure Storage, complete the instructions in [Allow the VNet subnet IDs](/user-guide/data-load-azure-allow).
:   - Note: Azure Storage requires adding all subnets appended with /gs and /xp to the allow list. You must add each /gs and /xp subnet individually.

Ref: n/a
