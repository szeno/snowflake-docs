Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# CATALOG\_LINKED\_DATABASE\_USAGE\_HISTORY view

Use this Account Usage view to view the credit usage for your
[catalog-linked databases](/user-guide/tables-iceberg-catalog-linked-database)
within the last 12 months.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the catalog-linked database operation took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the catalog-linked database operation took place. |
| DATABASE\_ID | NUMBER | Internal identifier for the catalog-linked database that consumed credits. |
| DATABASE\_NAME | VARCHAR | Name of the catalog-linked database that consumed credits. |
| CREDITS\_USED\_COMPUTE | NUMBER(38,9) | Number of credits used by the catalog-linked database for table creation operations between the START\_TIME and END\_TIME. The cost for this usage is described in Table 5 of the [Snowflake service consumption table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) on the Snowflake website. See the Snowflake-managed compute column for the Automated Refresh and Data Registration row. |
| CREDITS\_USED\_CLOUD\_SERVICES | NUMBER(38,9) | Number of credits used by the catalog-linked database for automatic table discovery, schema creation or deletion, and table deletion between the START\_TIME and END\_TIME. Usage for cloud services is charged only if the daily consumption of cloud services exceeds 10% of the daily usage of virtual warehouses. For more information, see [Understanding billing for cloud services usage](/user-guide/cost-understanding-compute#label-understanding-billing-for-cloud-services-usage). |
| CREDITS\_USED | NUMBER(38,9) | Number of credits billed for this catalog-linked database between the START\_TIME and END\_TIME. |

Expand

Show lessSee more
