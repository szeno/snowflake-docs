Schema:
:   [BILLING](/sql-reference/billing)

# BILLING\_SUBSCRIPTIONS\_HISTORY view

The BILLING\_SUBSCRIPTIONS\_HISTORY view in the BILLING schema provides a current snapshot of your existing subscriptions and relevant billing information for subscription products.

The view includes:

- Subscription product information.
- Subscription lifecycle dates and status.
- Organization and account metadata.
- Subscription phase information, when applicable.
- Billed or pending installments.
- Subscription quantity, amount, currency, and auto-renewal information.

The view does not include:

- Marketplace subscriptions.
- Overage or usage charges.
- Oracle BYOL products.
- Invoice activity.
- Subscriptions without at least one qualifying installment.

## Access

| Requirement | Detail |
| --- | --- |
| Database | SNOWFLAKE |
| Schema | BILLING |
| Account requirement | Must be an org-enabled account |
| Database role | SNOWFLAKE.ORGANIZATION\_BILLING\_VIEWER |

Expand

Show lessSee more

Access is restricted to org-enabled accounts and requires the ORGANIZATION\_BILLING\_VIEWER database role on the SNOWFLAKE shared database.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| SUBSCRIPTION\_ID | VARCHAR | Identifier of the subscription. |
| FEATURE | VARCHAR | Subscription product, such as `CORTEX-CODE-CLI`. |
| PRODUCT\_TYPE | VARCHAR | Product line represented by the row. |
| SUBSCRIPTION\_NAME | VARCHAR | Display name of the subscription. |
| STATUS | VARCHAR | Lifecycle status of the subscription. For the possible values, see [STATUS values](#status-values). |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |
| REGION | VARCHAR | Name of the region where the account is located. |
| TRIAL\_START\_DATE | TIMESTAMP\_NTZ | Start timestamp of the first Trial phase. NULL when the subscription has no configured Trial phase. |
| TRIAL\_END\_DATE | TIMESTAMP\_NTZ | End timestamp (exclusive) of the first Trial phase. NULL when the subscription has no configured Trial phase or the phase is open-ended. |
| START\_DATE | TIMESTAMP\_NTZ | Subscription start timestamp. |
| END\_DATE | TIMESTAMP\_NTZ | Subscription end timestamp. NULL when the subscription is open-ended. |
| CANCELLATION\_DATE | TIMESTAMP\_NTZ | Timestamp when the cancellation takes effect. A future value means the subscription is marked for cancellation and remains in its current term until that time. NULL if the subscription is not canceled. |
| CANCELLATION\_REASON | VARCHAR | Reason the subscription was canceled. NULL if the subscription is not canceled. |
| RENEWAL\_DATE | DATE | Date the subscription renews. NULL if the subscription does not renew automatically. |
| NEXT\_BILLING\_DATE | DATE | Date of the next scheduled charge for the subscription. NULL when no charge is scheduled. |
| PHASE\_NAME | VARCHAR | Name of the current phase. |
| IS\_BILLABLE | BOOLEAN | Indicates whether the current phase is billable. |
| PHASE\_DURATION | NUMBER | Configured duration of the current phase. |
| PHASE\_DURATION\_TYPE | VARCHAR | Unit for PHASE\_DURATION, such as `DAY` or `MONTH`. |
| PHASE\_START\_DATE | TIMESTAMP\_NTZ | Start timestamp of the current phase. |
| PHASE\_END\_DATE | TIMESTAMP\_NTZ | End timestamp (exclusive) of the current phase. |
| QUANTITY | NUMBER | Number of subscribed units. The value can include a fraction. |
| UNIT\_PRICE | NUMBER | Price of one subscribed unit on one qualifying installment, based on the most recent qualifying installment available from the source. This is not calculated as TOTAL\_AMOUNT / QUANTITY and is not a lifetime average. |
| TOTAL\_AMOUNT | NUMBER | Amount billed so far. This does not include usage or overage charges. The value is 0 if nothing has been billed. |
| CURRENCY | VARCHAR | Currency of the amount, represented as an ISO 4217 code. The default is USD. |
| INSTALLMENTS\_BILLED | NUMBER | Number of subscription payments that have been billed. The value is 0 if none have been billed. |
| INSTALLMENTS\_SCHEDULED\_COUNT | NUMBER | Number of subscription payments that are still scheduled. The value is 0 if none are scheduled. |
| IS\_AUTO\_RENEW | BOOLEAN | TRUE if the subscription renews automatically. |
| CREATED\_DATE | TIMESTAMP\_NTZ | Timestamp when the subscription was created. |
| LAST\_MODIFIED\_DATE | TIMESTAMP\_NTZ | Timestamp when the subscription was last updated. |

Expand

Show lessSee more

### STATUS values

The STATUS column is derived from the subscription lifecycle dates and the current subscription phase.

| Value | Description |
| --- | --- |
| `CANCELED` | The subscription is canceled or marked for cancellation. CANCELLATION\_DATE is when the termination takes effect. A CANCELLATION\_DATE in the future means the subscription is marked for cancellation and remains in its current term until that timestamp. END\_DATE is the subscription end and is not the cancellation effective date. |
| `TRIAL` | The current timestamp falls within a non-billable Trial phase interval. |
| `EXPIRED` | The subscription end timestamp has passed. |
| `ACTIVE` | The subscription is not canceled, is not currently in a Trial phase, and has not passed its end date. |

Expand

Show lessSee more

For trial and phase intervals, the start timestamp is inclusive and the end timestamp is exclusive. An interval with a NULL end timestamp has no defined end.

## Usage notes

- The view is available to all customers and returns the subscriptions for your organization.
- Latency for the view may be up to 4 hours.

## Example queries

### Query active and trial subscriptions

Copy code

```
SELECT
    SUBSCRIPTION_ID,
    FEATURE,
    PRODUCT_TYPE,
    STATUS,
    START_DATE,
    END_DATE,
    NEXT_BILLING_DATE
  FROM SNOWFLAKE.BILLING.BILLING_SUBSCRIPTIONS_HISTORY
  WHERE STATUS IN ('ACTIVE', 'TRIAL');
```

### Query a feature, including future-dated cancellations

Copy code

```
SELECT
    SUBSCRIPTION_ID,
    FEATURE,
    STATUS,
    CANCELLATION_DATE,
    END_DATE
  FROM SNOWFLAKE.BILLING.BILLING_SUBSCRIPTIONS_HISTORY
  WHERE FEATURE = 'CORTEX-CODE-CLI'
    AND (
          STATUS IN ('ACTIVE', 'TRIAL')
          OR (
              STATUS = 'CANCELED'
              AND CANCELLATION_DATE >= CURRENT_TIMESTAMP()
          )
        );
```
