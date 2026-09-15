Schema:
:   [DATA\_SHARING\_USAGE](/sql-reference/data-sharing-usage)

# PAID\_LISTING\_ACCESS\_AND\_CHANGE\_LOG view

Note

The CURRENT\_PRICING\_PLAN column includes new fields, indicated with an asterisk (\*), that are available only for the Offers preview.

Providers can use this view in the [Data Sharing Usage](/sql-reference/data-sharing-usage) schema to query a consumer’s paid listing change log to determine the status of a pricing plan and when consumers will lose access to paid or trial listings.

This view is updated when a consumer changes their pricing plan, starts or ends a trial listing, or when they cancel a subscription.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| EVENT\_DATE | DATETIME | The date and time the row was created. |
| LISTING\_NAME | VARCHAR | The name of the listing associated with the pricing plan. |
| LISTING\_DISPLAY\_NAME | VARCHAR | The listing display name. |
| LISTING\_GLOBAL\_NAME | VARCHAR | The Unique Listing Locator (ULL) for the listing. |
| CONSUMER\_ACCOUNT\_NAME | VARCHAR | The consumer account name. |
| CONSUMER\_ACCOUNT\_LOCATOR | VARCHAR | The Snowflake consumer account locator. |
| CONSUMER\_ORGANIZATION\_NAME | VARCHAR | The consumer organization name. |
| CONSUMER\_SNOWFLAKE\_REGION | VARCHAR | The Snowflake region that corresponds to the consumer’s organization billing and shipping addresses. |
| CURRENT\_PRICING\_PLAN | VARIANT | Information in JSON format about the pricing plan that was active on the date and time specified in the EVENT\_DATE column. The following information can be returned:   - PLAN\_TYPE: Type of Pricing Plan. Values can be: (SUBSCRIPTION, USAGE) - PLAN\_SUB\_TYPE: One of:    - If PLAN\_TYPE is SUBSCRIPTION: One of INSTALLMENTS or FIXED.   - If PLAN\_TYPE is USAGE: One of PER\_QUERY, COMPUTE\_POOL\_SURCHARGE, or CUSTOM\_BILLING. - FREE\_QUERIES\_LIMIT: The number of free queries a consumer is allowed before a usage price applies. - PER\_QUERY\_PRICE: The cost per query for usage based plans. - BASE\_PRICE: The base monthly usage fee. - MAX\_MONTHLY\_PRICE\_LIMIT: The maximum monthly usage fee. - MAX\_TRIAL\_DAYS\_LIMIT: The time limit for consumer trials. - MAX\_TRIAL\_QUERIES\_LIMIT: The usage limit for consumer trials. - BILLING\_DURATION\_MONTHS: The contract duration in months. - CUSTOM\_BILLING\_EVENTS: A list of existing custom billing events. One of:    - CLASS\_NAME: Billing event class name.   - DISPLAY\_NAME: The name of the billing event.   - UNIT\_PRICE: Price per billable unit. - DESCRIPTION: The pricing plan description. - IS\_AUTO\_RENEWAL\_ALLOWED: Indicates if the consumer can automatically renew the listing: `true` or `false`. - INSTALLMENT\_SCHEDULE: The installment plan schedule.    - INSTALLMENT\_DURATION\_MONTHS: The number of months installments are due.   - DEFAULT\_INSTALLMENT\_PRICE: The usual dollar amount of each installment payment, excluding exceptions like prorated or upfront payments.   - INSTALLMENT\_OVERRIDES: A list of overridden installments. One of:     - INSTALLMENT\_NUMBER: Installment number being overridden.     - INSTALLMENT\_PRICE: The installment price. - IS\_EARLY\_ACCESS\_ALLOWED: Consumers can access data before payment. - COMPUTE\_POOL\_SURCHARGES: A list of the defined Snowpark Container Services (SPCS) compute pool surcharges. One of:    - COMPUTE\_POOL\_NAME: Compute pool name.   - UNIT\_PRICE: Price per credit or per hour for compute pool usage. - CURRENCY: Pricing plan currency in United States dollars. - \*CONTRACT\_TYPE: For a flat-fee plan, this can be for a limited time or recurring (subscription). For a usage-based plan, this is always “pay as you go.” - \*COMPUTE\_POOL\_SURCHARGE\_TYPE: The unit on which the surcharge would be applicable. This can be `HOUR` or `CREDIT`. - \*CONTRACT\_DURATION\_MONTHS: The length of the contract in months. - \*INVOICE\_START\_PREFERENCE: Indicates whether the first invoice is sent when the offer is accepted or on a specified date. Can be one of `OFFER_ACCEPTED_DATE`, `SPECIFIED_DATE`, or `FIRST_DAY_NEXT_MONTH`. If `SPECIFIED_DATE` is selected, then see `INVOICE_START_TIME`. - \*INVOICE\_START\_TIME: The date of the first invoice. - \*IS\_DEFAULT: This field is always present. If `true`, it indicates that this is a default offer attached to a pricing plan. If `false`, it indicates that this is a private offer targeted to a specific consumer. - \*OFFER\_DISPLAY\_NAME: The name of the offer as shown to consumers. - \*PRICING\_PLAN\_DISPLAY\_NAME: The name of the pricing plan as shown to consumers. - \*PAYMENT\_TERMS: The payment terms. - \*PAYMENT\_TYPE: The payment type. This can be `FULL` for paid in full or `INSTALLMENT` for a payment made in installments. - \*ALLOWED\_PAYMENT\_METHODS: The allowed payment methods. - \*ACCESS\_START\_PREFERENCE: The preference of access start. This can be one of `OFFER_ACCEPTED_DATE` or `SPECIFIC_DATE`. - \*ACCESS\_START\_TIME: The time when access starts. - \*ACCESS\_END\_TIME: The date and time when access ends. - \*TARGET\_CONSUMER: The consumer targeted by this offer. - \*STATE: The offer state. - \*PRODUCT\_SKU: The SKU linked to a pricing plan that’s tied to an offer. - \*PRICING\_MODEL: Specifies whether the pricing plan tied to the offer is a flat fee or a usage model. |
| NEXT\_PRICING\_PLAN | VARIANT | Information in JSON format about the pricing plan that becomes active on the date and time specified in the `CURRENT_PRICING_PLAN_END_ON` column. The JSON format for this column is identical to that of `CURRENT_PRICING_PLAN`. |
| IS\_CONSUMER\_AUTO\_RENEWAL\_ENABLED | BOOLEAN | The consumer enabled auto-renewal. This is applicable only to subscription listings. |
| PURCHASE\_STATE | VARCHAR | The listing state. The state can be one of:   - TRIAL - EXPIRED - DELETED - PURCHASED |
| CURRENT\_PRICING\_PLAN\_START\_ON | DATETIME | The date and time a pricing plan became active. |
| CURRENT\_PRICING\_PLAN\_END\_ON | DATETIME | The date and time the current pricing plan ends. |
| TRIAL\_END\_ON | DATETIME | The end date of the listing trial. |
| ACCESS\_END\_ON | DATETIME | The date and time the current subscription term ends. NULL indicates that the current plan is not a subscription, but a usage based plan instead. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to two days.
- The data is retained up to one year.
- A row is created when any column changes. For example, when a consumer changes their pricing plan, starts or ends a trial, cancels a subscription, or deletes the data.
- The data includes all consumers who have accessed the listing at least once, including those who have canceled their listing subscription or trial.
- The view contains data for paid Snowflake listings that have one or more consumers.
- This report contains one row per listing per consumer. For example, if a consumer purchased two listings from a provider and each purchase was updated three times, then the view contains six entries. An individual column represents the state of a single, specific purchase.
- The following data is not included in the view:
  - Limited trial listings
  - Free listings - provided without charge on or off the Snowflake platform
  - Free listings - provided without charge on-platform, but paid off-platform directly to the provider
  - Listings that have never been accessed by consumers

## Examples

Show a change log for a specified listing and consumer:

Copy code

```
SELECT
  event_date,
  listing_name,
  listing_global_name,
  consumer_account_name,
  consumer_account_locator,
  consumer_organization_name,
  current_pricing_plan,
  next_pricing_plan,
  is_consumer_auto_renewal_enabled,
  purchase_state,
  current_pricing_plan_start_on,
  current_pricing_plan_end_on,
  trial_end_on,
  access_end_on
FROM snowflake.data_sharing_usage.paid_listing_access_and_change_log
WHERE TRUE
  AND consumer_organization_name = 'specific_organization_name'
  AND listing_display_name = 'specific_listing_display_name'
ORDER BY event_date DESC;
```

Show listings and consumers with pricing plans ending in the next billing period:

Copy code

```
SELECT
  event_date,
  listing_name,
  listing_global_name,
  consumer_account_name,
  consumer_account_locator,
  consumer_organization_name,
  current_pricing_plan,
  next_pricing_plan,
  is_consumer_auto_renewal_enabled,
  purchase_state,
  current_pricing_plan_start_on,
  current_pricing_plan_end_on,
  trial_end_on,
  access_end_on
FROM snowflake.data_sharing_usage.paid_listing_access_and_change_log
WHERE TRUE
  AND consumer_organization_name = 'specific_organization_name'
  AND listing_display_name = 'specific_listing_display_name'
QUALIFY TRUE
  AND ROW_NUMBER() OVER (
   PARTITION BY
    consumer_organization_name,
    consumer_snowflake_region,
    consumer_account_name,
    listing_display_name
ORDER BY event_date DESC ) = 1;
```
