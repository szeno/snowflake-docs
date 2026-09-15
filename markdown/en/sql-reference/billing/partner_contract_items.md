Schema:
:   [BILLING](/sql-reference/billing)

# PARTNER\_CONTRACT\_ITEMS view

The PARTNER\_CONTRACT\_ITEMS view in the BILLING schema provides contract information for the reseller’s customers.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the reseller’s organization. |
| SOLD\_TO\_ORGANIZATION\_NAME | VARCHAR | Name of the organization of the reseller’s customer. |
| SOLD\_TO\_CUSTOMER\_NAME | VARCHAR | Name of the reseller’s customer. |
| SOLD\_TO\_PO\_NUMBER | VARCHAR | Purchase order number associated with the reseller’s sale to the customer. |
| SOLD\_TO\_CONTRACT\_NUMBER | VARCHAR | Number associated with the customer’s contract with the reseller. |
| START\_DATE | DATE | Start date for the customer’s contract with the reseller, or the date the CONTRACT\_ITEM goes into effect. |
| END\_DATE | DATE | End date of the customer’s contract with the reseller. |
| EXPIRATION\_DATE | DATE | Expiration date of the customer’s contract with the reseller. |
| CONTRACT\_ITEM | VARCHAR | One of capacity, additional capacity, or free usage. |
| CURRENCY | VARCHAR | Currency for the CONTRACT\_ITEM. |
| AMOUNT | NUMBER(26,4) | Amount for the CONTRACT\_ITEM. |
| CONTRACT\_MODIFIED\_DATE | DATE | Date (in UTC) the CONTRACT\_ITEM was last modified. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 24 hours.
