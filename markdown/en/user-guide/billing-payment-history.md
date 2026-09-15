# Access payment history

Snowflake provides a consolidated view of payment activity for On Demand customers. Account and organization administrators can use the payment history to reconcile payments with internal records, track spending, or investigate a specific charge or refund. The payment history covers transaction events from January 1, 2025 onwards.

To access the payment history in Snowsight, either of the following must be true:

- You have been granted the GLOBALORGADMIN role, and you are in the [organization account](/user-guide/organization-accounts).
- You have been granted the ACCOUNTADMIN and ORGADMIN roles, and you are in an account that has the ORGADMIN role enabled.

To access the payment history:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Admin** » **Billing**.
3. On the **Snowflake billing** tab, select **Payment history**.

## Transactions

By default, transactions are listed with the most recent first in a period of the last 12 months. Each entry represents a distinct payment event of one of the following types:

- **Charges**: payments collected for services. Charges include invoice charges for usage-based billing and threshold charges, which are triggered automatically when cumulative account spending reaches a preset limit.
- **Refunds**: amounts returned to the payment method on file, corresponding to a prior charge.
- **Authorization holds**: temporary holds placed on the payment method for verification purposes.

## Transaction details

Each row shows the date, transaction type, amount, current status, and payment method. The possible statuses are:

- **Successful**: the transaction completed as expected.
- **Failed**: the transaction didn’t go through.
- **Released**: an authorization hold was lifted without collecting funds.
- **Other**: the transaction outcome doesn’t fall into one of the previous categories. Contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support) if you see this status for a charge that you don’t recognize.

Invoice charges always include a downloadable document, regardless of whether the charge succeeded or failed. Threshold charges include a downloadable document only when the charge was successful. Refunds and authorization holds don’t have associated documents.

## Filter transactions

You can filter the list of transactions by any of the following criteria:

- Transaction type
- Payment status
- Amount, by specifying a value that the amount must be greater than, less than, or equal to
- A date range
