# Using auto-fulfillment

When you configure a listing and make it available in a region other than your local region, or when you share a private listing with consumer
accounts in another region, you can enable auto-fulfillment. See [Region availability](/collaboration/provider-listings-reference#label-listings-set-up-region-avail).

## Enable auto-fulfillment for your account

Note

Auto-fulfillment isn’t available on trial accounts.

To enable auto-fulfillment for your account, use the [SYSTEM$ENABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_enable_global_data_sharing_for_account) system function.

You must use the [ORGADMIN](/user-guide/organization-administrators) role to call this system function.

Copy code

```
SELECT SYSTEM$ENABLE_GLOBAL_DATA_SHARING_FOR_ACCOUNT(
  '<account_name>'
  );
```

Where:

`account_name`
:   Specifies the name of the account in which to enable users with the ACCOUNTADMIN role to manage Cross-Cloud Auto-Fulfillment. For more information, see [Finding the organization and account name for an account](/user-guide/admin-account-identifier#label-account-name-find).

Note

To disable auto-fulfillment for an account, use the [SYSTEM$DISABLE\_GLOBAL\_DATA\_SHARING\_FOR\_ACCOUNT](/sql-reference/functions/system_disable_global_data_sharing_for_account) system function. To check whether auto-fulfillment is enabled for an account, use the [SYSTEM$IS\_GLOBAL\_DATA\_SHARING\_ENABLED\_FOR\_ACCOUNT](/sql-reference/functions/system_is_global_data_sharing_enabled_for_account) system function.

## Required privileges to perform auto-fulfillment tasks

Before continuing with either Snowsight or SQL, ensure that you have the required privileges to set up auto-fulfillment.

To perform auto-fulfillment tasks, use one of the following roles:

- The ORGADMIN role.
- The ACCOUNTADMIN role after auto-fulfillment is enabled on an account.
- A custom role that has been granted the MANAGE LISTING AUTO FULFILLMENT privilege by a user with the
  [ACCOUNTADMIN role with delegated privileges](/collaboration/provider-listings-auto-fulfillment-manage-privileges#label-delegate-laf-privileges).

Any role that you use must also have OWNERSHIP or MODIFY privileges on the listing.

Now that you understand the required privileges, you can configure auto-fulfillment for your listing. See [Set up auto-fulfillment](/collaboration/provider-listings-auto-fulfillment-setup-steps) for more information. Keep in mind that you must add a data product to your listing before you can set up auto-fulfillment. Also, the steps to set up auto-fulfillment differ depending on the data product you offer and how you make your listing available.
