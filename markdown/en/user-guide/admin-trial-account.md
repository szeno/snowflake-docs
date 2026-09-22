# Trial accounts

A Snowflake trial account lets you evaluate/test Snowflake’s full range of innovative and powerful features with no cost or contractual obligations. To sign
up for a trial account, all you need is a valid email address; no payment information or other qualifying information is required.

Note

AI features are disabled by default on self-service trial accounts until you
add a credit card to the account. For more information, see [current limitations for trial accounts](#label-trial-account-ai-features).

## Signing up for a trial account

You can sign up for a free trial using the [self-service form](https://signup.snowflake.com/) (on the Snowflake website).

When you sign up for a trial account, you select your [cloud platform](/user-guide/intro-cloud-platforms), [region](/user-guide/intro-regions),
and [Snowflake Edition](/user-guide/intro-editions). These selections can affect how quickly you exhaust your free usage balance. For example, some features available in the Enterprise Edition consume additional [credits](/user-guide/cost-understanding-compute#label-what-are-credits).

The balance of your free usage decreases as you consume credits to use [compute resources](/user-guide/cost-understanding-compute) and accrue costs associated with [storage](/user-guide/cost-understanding-data-storage). You can [track your remaining balance](#label-trial-account-track-balance) at any time.

The trial continues for 30 days (from the sign-up date) or until you’ve depleted your free usage balance, whichever occurs first. At any time during the trial, you can [cancel the trial](#label-trial-account-cancel) or [upgrade the account to a paid account](#label-trial-account-convert).

At the end of the trial, the account is suspended. You can still log into a suspended account, but you cannot use any features, such as running a virtual warehouse,
loading data, or performing queries.

To reactivate a suspended trial account, add a credit card if one isn’t already on file, and then upgrade to a paid account.

## Using compute resources

[Virtual warehouses](/user-guide/warehouses) provide the compute power to [load data](/guides-overview-loading-data) and
[perform queries](/guides-overview-queries). These warehouses consume credits, which reduces your free usage balance. To begin, simply start a warehouse; any credits consumed by the warehouse will be deducted from your balance. If your credit consumption fully depletes your free usage balance, you must upgrade to a paid account to continue using Snowflake.

Free credits are consumed by the virtual warehouses you create in your account while they’re running. Serverless features,
including AI features, also consume free credits when you use them.

Tip

To prevent unintentional usage of your free credits:

- Verify the size of your virtual warehouses before you start/resume them. The larger the warehouse, the more credits it consumes while running.
  In many situations, Small or Medium size warehouses are sufficient for evaluating Snowflake’s loading and querying capabilities.
- Do not disable [auto-suspend](/user-guide/warehouses-overview#label-auto-suspension-and-auto-resumption) when creating a warehouse. Choosing a short auto-suspend time period (e.g. 5 minutes or less) can reduce credit consumption.

For additional tips on using your trial account:

1. In the left navigation bar, find the tile showing your remaining balance.
2. Select **…** » **Using your trial credits**.

## Using storage

As you load data into your trial account, the cost of that storage is subtracted from your free usage balance based on the standard On-Demand cost of a TB in your cloud platform and region. In addition to the cost of storage, loading data also consumes credits as it uses the compute resources of a warehouse.

## Tutorials for trial accounts

The following tutorials are available for trial accounts:

- [Load and query sample data using SQL](/user-guide/tutorials/tasty-bytes-sql-load)
- [Load data from cloud storage: Amazon S3](/user-guide/tutorials/load-from-cloud-tutorial)
- [Load data from cloud storage: Microsoft Azure](/user-guide/tutorials/load-from-cloud-tutorial-azure)
- [Load data from cloud storage: Google Cloud Storage](/user-guide/tutorials/load-from-cloud-tutorial-gcs)
- [Create users and grant roles](/user-guide/tutorials/users-and-roles-tutorial)

## Tracking your remaining balance

Users with the ACCOUNTADMIN role can track the remaining balance of their trial using a tile in the left navigation bar of
Snowsight.

From this tile you can also:

- Select **Upgrade** to [upgrade the trial account to a paid account](#label-trial-account-convert).
- Select **…** » **see organization usage details** to access the **Usage** page, which allows you to drill down into your credit
  consumption and storage costs.
- Select the **…** button to access resources that help you get the most out of your trial account.

## Upgrading to a paid account

To upgrade a trial account to a paid account, first add a credit card to the account:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Billing**.
3. Click the **Snowflake billing** tab.
4. In the **Payment method** pane, click **+ Credit Card**.
5. Enter the required information, and then select **Add Card**.

Adding a credit card doesn’t upgrade your trial account to a paid account. After adding a credit card, you can select **Upgrade** in the left navigation at any time to upgrade the account.

Snowflake knows trial account subscribers who upgrade to paid
accounts as on-demand, self-service (ODSS) customers. ODSS customers can edit the billing contact information for a self-service account using
Snowsight. For more information, see [Update billing contact information](/user-guide/billing-contacts).

Note that you can also change the credit card for a trial account, at any time, using the same interface in which you added the card.

Note

Upgrading to a paid account ends the free trial and moves the account to on-demand billing, where you’re charged only for what you use. Any remaining free trial credits still apply.

**Threshold billing:** Depending on your usage after your free credits are exhausted, you may be automatically billed one or more times before the end of each calendar month if your consumption reaches certain thresholds (threshold payments). Threshold payments can vary in amount and may occur multiple times in a single month. You will receive an email notification each time a threshold payment is charged. Any threshold payments successfully charged during a calendar month are credited toward that month’s total consumption.

If you don’t upgrade before the trial period ends, the account is suspended and any unused free usage balance expires.

For pricing details, see the [pricing page](https://www.snowflake.com/pricing/) (on the Snowflake website).

Warning

If a threshold payment fails, your account may be suspended. If you receive a payment failure notification, take action promptly to update your payment method.

## Canceling a trial account

You can cancel a trial account at any time by contacting [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support)
and requesting the account to be canceled.

Note

Currently, trial accounts cannot be canceled through the web interface. To cancel an account, you must contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

## Current limitations for trial accounts

The following features are not available for trial accounts:

- [External network access](/developer-guide/external-network-access/external-network-access-overview)
- [Hybrid tables](/user-guide/tables-hybrid)
- [Outbound private connectivity](/user-guide/private-connectivity-outbound)
- [Snowflake Openflow](/user-guide/data-integration/openflow/about)
- Using Duo for multi-factor authentication (MFA)

AI features are disabled by default on self-service trial accounts. To enable them, add a credit card to the account. Adding a credit card doesn’t upgrade the trial to a paid account or end the trial period.
