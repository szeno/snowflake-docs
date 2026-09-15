Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views) , [READER\_ACCOUNT\_USAGE](/sql-reference/account-usage#label-reader-account-usage-views)

# RESOURCE\_MONITORS view

This Account Usage view displays the resource monitors that have been created in the account.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| READER\_ACCOUNT\_NAME | VARCHAR | Name of the reader account where the resource monitor was created. Column only included in view in READER\_ACCOUNT\_USAGE schema. |
| NAME | VARCHAR | Name of the resource monitor. |
| CREATED | TIMESTAMP\_LTZ | Date and time when the resource monitor was created. |
| CREDIT\_QUOTA | VARIANT | Monthly credit quota for the resource monitor. |
| USED\_CREDITS | VARIANT | Number of credits used in the current monthly billing cycle by all the warehouses associated with the resource monitor. |
| REMAINING\_CREDITS | FLOAT | Number of credits still available to use in the current monthly billing cycle. |
| OWNER | VARCHAR | Name of the role that owns the resource monitor. |
| WAREHOUSES | VARCHAR | Names of the warehouses that are associate with the resource monitor. |
| NOTIFY | NUMBER | Percentage of the credit quota. When consumption reaches this threshold, notifications are sent. |
| SUSPEND | NUMBER | Percentage of the credit quota. When consumption reaches this threshold, assigned warehouses are suspended but currently running queries are allowed to complete. |
| SUSPEND\_IMMEDIATE | NUMBER | Percentage of the credit quota. When consumption reaches this threshold, all assigned warehouses are suspended immediately, including those running queries. |
| LEVEL | VARCHAR | Indicates whether it is an account-level or a warehouse-level resource monitor. |
| READER\_ACCOUNT\_DELETED\_ON | TIMESTAMP\_LTZ | Time and date (in the UTC time zone) when the reader account is deleted. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The view only displays objects for which the current role for the session has been granted access privileges.
