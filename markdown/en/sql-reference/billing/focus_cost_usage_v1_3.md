Schema:
:   [BILLING](/sql-reference/billing)

# FOCUS\_COST\_USAGE\_V1\_3 view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

The FOCUS\_COST\_USAGE\_V1\_3 view in the BILLING schema exposes cost and usage data formatted to the
[FinOps Open Cost and Usage Specification (FOCUS) v1.3](https://focus.finops.org). It provides daily
granular charge line items covering Snowflake credit consumption across all sub-accounts within a billing account.

This view is the primary source for FOCUS-compliant cost analytics, enabling practitioners to perform
invoice reconciliation, cost allocation, rate optimization, and FinOps reporting using a standardized schema.

## Access

| Requirement | Details |
| --- | --- |
| Database | `SNOWFLAKE` |
| Schema | `BILLING` |
| Account requirement | Must be an org-enabled account |
| Database role | `SNOWFLAKE.ORGANIZATION_BILLING_VIEWER` |

Expand

Show lessSee more

Access is restricted to org-enabled accounts and requires the `ORGANIZATION_BILLING_VIEWER` database role
on the `SNOWFLAKE` shared database.

Copy code

```
-- Grant the database role to a user role
GRANT DATABASE ROLE SNOWFLAKE.ORGANIZATION_BILLING_VIEWER TO ROLE <role_name>;

-- Query the view
USE ROLE <role_name>;
SELECT * FROM SNOWFLAKE.BILLING.FOCUS_COST_USAGE_V1_3 LIMIT 10;
```

## Grain

- One row per daily charge line item per sub-account, service, and charge type.
- `ChargePeriodStart` and `ChargePeriodEnd` represent inclusive start / exclusive end of a 24-hour period.
- `BillingPeriodStart` and `BillingPeriodEnd` represent the calendar month billing period (inclusive start / exclusive end).

## Columns

### FOCUS standard columns

| Column | Type | Description |
| --- | --- | --- |
| BillingPeriodStart | TIMESTAMP\_TZ | Inclusive start of the billing period (first day of month, UTC midnight). |
| BillingPeriodEnd | TIMESTAMP\_TZ | Exclusive end of the billing period (first day of next month, UTC midnight). |
| ChargePeriodStart | TIMESTAMP\_TZ | Inclusive start of the charge period (daily granularity). |
| ChargePeriodEnd | TIMESTAMP\_TZ | Exclusive end of the charge period (daily granularity). |
| BillingAccountName | TEXT | The Organization responsible for paying for the line of usage. This will always refer to the Snowflake organization that owns the billing relationship. |
| BillingAccountId | TEXT | Unique identifier of the Snowflake organization billing account. |
| SubAccountId | TEXT | Unique identifier of the Snowflake account (sub-account within the org). |
| SubAccountName | TEXT | Display name of the Snowflake account. |
| SubAccountType | TEXT | Type of sub-account. Values: `Regular`, `Reader`. |
| ChargeCategory | TEXT | Highest-level charge classification. Values: `Usage`, `Purchase`, `Adjustment`. |
| ChargeClass | TEXT | Indicates correction rows. Value: `Correction` when applicable; otherwise null. |
| ChargeFrequency | TEXT | How often the charge recurs. Value: `Usage-Based`. |
| ServiceCategory | TEXT | High-level category of the Snowflake service (for example, `Compute`, `Storage`, `AI and Machine Learning`). |
| ServiceName | TEXT | Specific Snowflake service type. See [Service Types](/sql-reference/service-types) for the full list of possible values. |
| ChargeDescription | TEXT | Human-readable description of the charge (for example, `OVERAGE-COMPUTE`). |
| ConsumedQuantity | NUMBER(38,9) | How the underlying resource was metered (up to 9 decimal places). May differ in unit from PricingQuantity (for example, storage is metered in TiB-Days but priced in TiB-Months). |
| ConsumedUnit | TEXT | Unit of metered consumption (for example, `Credits`, `TiB-Days`, `TiB-Months`). |
| PricingQuantity | NUMBER(38,9) | How Snowflake prices the consumption for billing (rounded to 3 decimal places). This is the quantity used in cost calculations. |
| PricingUnit | TEXT | Unit corresponding to PricingQuantity (for example, `Credits`, `TiB-Months`). |
| ListUnitPrice | NUMBER(38,9) | Published list price per unit before any discounts. |
| ListCost | NUMBER(38,9) | Cost at list price: ListUnitPrice × PricingQuantity. |
| ContractedUnitPrice | NUMBER(38,9) | Negotiated/contracted price per unit, inclusive of discounts if applicable. Rounded to 2 decimal places. |
| ContractedCost | NUMBER(38,9) | Precise calculated cost: ContractedUnitPrice × PricingQuantity (up to 9 decimal places). This is not the amount actually billed to the customer. |
| EffectiveCost | NUMBER(38,9) | Amortized cost accounting for commitment drawdowns. Rounded to 2 decimal places. This is the amount actually drawn from the customer balance. |
| BilledCost | NUMBER(38,9) | Actual cost drawn from the customer’s capacity balance. Rounded to 2 decimal places. Matches the usage statement. |
| BillingCurrency | TEXT | Currency of all cost columns. Value: `USD`. |
| PricingCategory | TEXT | Pricing model applied. Value: `Standard`. |
| CapacityReservationId | NUMBER | Identifier of the capacity reservation associated with this charge. |
| CapacityReservationStatus | TEXT | Status of the capacity reservation. Value: `Unused` when capacity is not fully utilized. |
| RegionId | TEXT | Cloud provider region identifier (for example, `AWS_US_WEST_2`). |
| RegionName | TEXT | Cloud provider region display name (for example, `AWS_US_WEST_2`). |
| HostProviderName | TEXT | Name of the underlying cloud infrastructure provider (for example, `Aws`, `Azure`, `Gcp`). |
| InvoiceIssuerName | TEXT | Entity issuing the invoice. Value: `Snowflake`. |
| InvoiceId | TEXT | Invoice identifier. See [Known limitations](#known-limitations). |
| ContractApplied | JSON Object | JSON object containing contract metadata applied to this charge. |

Expand

Show lessSee more

### Snowflake custom columns

Custom columns are Snowflake-specific extensions to the FOCUS schema. Per FOCUS spec, custom columns use
the `x_` prefix to distinguish them from standard FOCUS columns.

| Column | Type | Description |
| --- | --- | --- |
| x\_UpdatedAt | TIMESTAMP\_TZ | Timestamp when this row was last updated in the billing system. |
| x\_OrganizationName | TEXT | The Organization responsible for the line of usage. This will always refer to the Snowflake organization that owns the sub-account generating the usage. |
| x\_ServiceLevel | TEXT | Snowflake edition/service level of the sub-account (for example, `Enterprise`, `Business Critical`, `Standard`). |
| ContractApplied.x\_BalanceSource | TEXT | The balance source where usage is drawn down from (for example, `capacity`, `rollover`, `free usage`, `overage`). |
| ContractApplied.x\_ContractCommitCostBalance | NUMBER | The resultant balance left for the corresponding bucket of usage after draw down. |

Expand

Show lessSee more

## Cost and quantity relationships

### Quantity columns

`ConsumedQuantity` and `PricingQuantity` may differ in both value and unit:

- **ConsumedQuantity** (up to 9 decimals): How the underlying resource was metered.
- **PricingQuantity** (rounded to 3 decimals): How Snowflake prices the consumption for billing.

For example, storage is metered in **TiB-Days** (`ConsumedQuantity`) but priced in **TiB-Months** (`PricingQuantity` = TiB-Days ÷ days in month). For compute, both are in Credits and typically equal.

### Cost columns

Copy code

```
ListCost           = ListUnitPrice × PricingQuantity              (rack rate, up to 9 decimals)
ContractedCost     = ContractedUnitPrice (2dp) × PricingQuantity  (precise mathematical product, up to 9 decimals)
BilledCost         = rounded to 2 decimals — what is actually billed after rounding
EffectiveCost      = rounded to 2 decimals — same as BilledCost
```

**Savings analysis:** `ListCost - ContractedCost` shows savings from negotiated discounts.

## Sample queries

For additional use cases and sample queries, see the
[FOCUS Use Cases library](https://focus.finops.org/use-cases/?version=v1-3&use_case=analyze-costs-by-service-name).

### Total monthly spend by service

Copy code

```
SELECT
    DATE_TRUNC('month', "ChargePeriodStart")::DATE AS month,
    "ServiceName",
    SUM("BilledCost") AS total_billed_cost
FROM SNOWFLAKE.BILLING.FOCUS_COST_USAGE_V1_3
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC;
```

### Daily spend by sub-account

Copy code

```
SELECT
    "ChargePeriodStart"::DATE AS charge_date,
    "SubAccountName",
    "x_ServiceLevel",
    SUM("BilledCost") AS daily_cost
FROM SNOWFLAKE.BILLING.FOCUS_COST_USAGE_V1_3
GROUP BY 1, 2, 3
ORDER BY 1 DESC, 4 DESC;
```

### Spend by cloud provider region

Copy code

```
SELECT
    "HostProviderName",
    "RegionName",
    SUM("BilledCost") AS total_cost
FROM SNOWFLAKE.BILLING.FOCUS_COST_USAGE_V1_3
GROUP BY 1, 2
ORDER BY 3 DESC;
```

### Current billing period summary

Copy code

```
SELECT
    "BillingPeriodStart"::DATE AS billing_period,
    COUNT(*) AS line_items,
    SUM("BilledCost") AS total_billed,
    SUM("EffectiveCost") AS total_effective,
    SUM("ListCost") AS total_list
FROM SNOWFLAKE.BILLING.FOCUS_COST_USAGE_V1_3
WHERE "BillingPeriodStart"::DATE = DATE_TRUNC('month', CURRENT_DATE)
GROUP BY 1;
```

## Known limitations

| Limitation | Detail |
| --- | --- |
| InvoiceId may be empty | For Contract (capacity) customers, InvoiceId may be empty, as usage is not tied directly to the invoice for capacity purchases. For On-Demand customers, InvoiceId will only be populated after month end. |
| Missing conditional columns | `CommitmentDiscount*`, `Sku*`, `PricingCurrency*`, `ResourceId/Name/Type`, `AllocatedTags`, `AllocatedMethodDetails` columns are not populated. |

Expand

Show lessSee more

## Usage notes

- The view refreshes hourly, but latent usage activity may take up to 72 hours before it is reflected in the data.
- Until month close, data for a given day in a month can change to account for any end-of-month adjustments, mid-month contract amendments, latent usage, or Snowflake account transfers from one organization to another.
- Historical data is available from January 1, 2026 onwards.

## Related views

| View | Description |
| --- | --- |
| [USAGE\_IN\_CURRENCY\_DAILY](/sql-reference/organization-usage/usage_in_currency_daily) | Org-level daily spend in billing currency. Requires ORGADMIN role. |
| [RATE\_SHEET\_DAILY](/sql-reference/organization-usage/rate_sheet_daily) | Daily rate sheet with contracted pricing per service. Requires ORGADMIN role. |
| [REMAINING\_BALANCE\_DAILY](/sql-reference/organization-usage/remaining_balance_daily) | Daily capacity balance remaining. Requires ORGADMIN role. |

Expand

Show lessSee more
