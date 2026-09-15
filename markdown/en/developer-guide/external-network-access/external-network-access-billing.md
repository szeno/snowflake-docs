# Costs of external network access

Using external network access incurs normal costs associated with:

- [Snowflake warehouse usage.](/user-guide/cost-understanding-compute#label-virtual-warehouse-credit-usage)
- [Data transfer.](/user-guide/cost-understanding-data-transfer)

Data transfer charges will appear as a TRANSFER\_TYPE of EXTERNAL\_ACCESS in the [DATA\_TRANSFER\_HISTORY view](/sql-reference/account-usage/data_transfer_history).
Any data egress traffic associated with a “bring-your-own-IP” (BYOIP) destination will be charged at cross-cloud or Internet traffic rates.

Calling to an external network location from a handler will result in payload egress. As data egress, this call results in data
transfer cost.

In addition, you might need to pay indirect or third-party charges, including charges by the provider of the remote service. Charges can
vary from vendor to vendor.
