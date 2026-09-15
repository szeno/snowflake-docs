# SHOW AVAILABLE OFFERS

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Lists the [offers](/user-guide/collaboration/listings/pricing-plans-offers/pricing-plans-and-offers#label-listings-offers) that are available to the user who runs the command.

## Syntax

Copy code

```
SHOW AVAILABLE OFFERS [ LIKE '<pattern>' ] IN LISTING <listing>
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`IN LISTING listing`
:   The listing associated with the offer you want shown.

## Output

The command output provides offer properties and metadata in the following columns:

| Column | Description |
| --- | --- |
| `name` | The offer name. |
| `state` | Offer status, one of:   - DRAFT - PUBLISHED - WITHDRAWN |
| `state_updated_on` | The date and time the offer state was last updated. |
| `access_start_date_preference` | The preferred date for consumer listing access, one of:   - OFFER\_ACCEPTED\_DATE - SPECIFIC\_DATE |
| `contract_value` | The total contract value. |
| `contract_type` | The contract type, one of:   - SUBSCRIPTION - LIMITED\_TIME - PAY\_AS\_YOU\_GO |
| `contract_duration_months` | The contract duration in months. |
| `invoice_start_date_preference` | The preferred invoicing start date, one of:   - OFFER\_ACCEPTED\_DATE - SPECIFIC\_DATE - FIRST\_DAY\_NEXT\_MONTH |
| `invoice_start_time` | The date and time invoicing started. |
| `is_default` | Specifies a default offer is included with the pricing plan, one of:   - TRUE - FALSE (default) |
| `display_name` | The offer name visible to consumers. |
| `expiration_time` | The date and time the offer expires. |
| `payment_terms` | Additional pricing plan parameters, one of:   - PAYMENT\_TYPE - INSTALLMENT\_SCHEDULE - ALLOWED\_PAYMENT\_METHODS |
| `access_end_time` | The date and time consumers lose access to the listing. |
| `access_start_time` | The date and time consumers can access the listing. |
| `discount` | The offer discount. |
| `target_consumer` | The consumer the offer targets. |
| `terms_of_service` | The terms of service associated with the offer. |
| `additional_information` | Additional offer information. |
| `pricing_plan` | The pricing plan associated with the offer. |
| `updated_on` | The date and time the offer was last updated. |
| `attachments` | PDF attachments included with the offer. Each entry contains a download link valid for 5 minutes. Returns an empty array if no attachments are included. |

Expand

Show lessSee more

## Access control requirements

| Privilege | Object | Notes |
| --- | --- | --- |
| PURCHASE DATA EXCHANGE LISTING | Global | This privilege grants the ability to purchase a paid listing. If you don’t have a role with this privilege, contact your account administrator. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Show all available offers with names that start with `myoffer` in `mylisting`:

Copy code

```
SHOW AVAILABLE OFFERS LIKE 'MYOFFER%' IN LISTING MYLISTING;
```
