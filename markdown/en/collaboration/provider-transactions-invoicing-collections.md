# Snowflake Marketplace Provider Expectations for Transactions, Invoicing, and Collections

This page explains the respective responsibilities of Marketplace Providers and Snowflake for invoicing,
taxes, collections, payouts, and transaction reporting for monetized Snowflake Marketplace transactions.

## Seller of record

The **Provider is the Seller of Record** for their Product(s) (not Snowflake) and is fully responsible for their
Product(s), the applicable listing terms, and the commercial terms offered to the customer.

The Provider remains responsible for dispute and refund discussions, as well as customer communication related to
its products, invoices, and listing terms. Providers may communicate directly with customers regarding their
products, transactions, and invoices, subject to the Snowflake Provider and Consumer Terms and the Provider’s
privacy policy.

For more information on disputes and enforcement, refer to
[Dispute resolution, enforcement, and appeals](/collaboration/dispute-resolution-enforcement-appeal).

## Invoicing and taxes

For monetized transactions, **Snowflake** invoices customers on the Provider’s behalf in USD.

**Snowflake Marketplace acts as a marketplace facilitator** and, where required by law, calculates,
collects, and remits applicable taxes and issues tax-compliant invoices as applicable.

In jurisdictions where Snowflake is not registered or authorized to collect a transaction tax, the **provider**
may need to assess, invoice, collect, remit, and report that tax directly. Providers should consult their own
tax advisors.

For additional tax information, refer to the
[Snowflake Marketplace taxes overview for consumers](https://www.snowflake.com/marketplace-taxes-overview-for-consumers/).

## Collections

**Snowflake** makes a best-effort attempt to collect payment on the Provider’s behalf for monetized
Marketplace transactions, including automated payment reminders for overdue invoices. Snowflake
provides support to customers with billing-related questions.

**Providers** are ultimately responsible for collecting payment and taking any necessary action in the event
of consumer nonpayment.

Snowflake provides reporting tools to help Providers monitor invoices, payments, payouts, and usage, including:

1. UI path: **Marketplace –> Provider Studio –> Invoices**
2. SQL views: [DATA\_SHARING\_USAGE schema](/sql-reference/data-sharing-usage)

## Payouts, Net Terms and fees

**Snowflake Marketplace uses Stripe to process Provider payouts.** To receive payouts, Providers must create a Stripe Express
connected account as their payout method through Snowflake Marketplace. If eligible, Providers can reuse verified information
from an existing Stripe account instead of completing verification again.

There is no additional cost to Providers for using the Stripe connected account. As part of the setup process,
Providers must accept the [Stripe Connected Account Agreement](https://stripe.com/legal/connect-account).
This agreement is between the Provider and Stripe; Snowflake is not a party to it.

**Net terms,** the amount of time a customer has to pay an invoice, are determined by the Provider and should be
specified in the order form and Marketplace Offer.

**Provider payouts** occur only after Snowflake collects the applicable product charges from the customer, net of
Snowflake fees, applicable taxes, and any permitted adjustments. If a customer pays with Marketplace Capacity
Drawdown (MCD), the related capacity invoice must be paid in full before payout is issued. Provider payouts are
made 30 days after payment is received in full.

Snowflake Marketplace charges a **transaction fee**, which is deducted from the Provider’s payout. Find the fee
schedule by navigating in Snowsight: **Admin –> Billing & Terms –> Fee**.
