Schemas:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# OPENFLOW\_USAGE\_HISTORY view

This Account Usage view returns the hourly [Openflow](/user-guide/data-integration/openflow/about) runtime credit usage for an account within the last 365 days (1 year).

Note

This view returns records only for Openflow BYOC deployments. It doesn’t return records for Openflow Snowflake
Deployments, which are billed under the *OPENFLOW\_COMPUTE\_SNOWFLAKE* service type. To track the cost of an Openflow
Snowflake Deployment, see [Openflow Snowflake Deployment cost and scaling considerations](/user-guide/data-integration/openflow/cost-spcs).

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| START\_TIME | TIMESTAMP\_LTZ | The date and beginning of the hour (in the local time zone) in which the usage took place. |
| END\_TIME | TIMESTAMP\_LTZ | The date and end of the hour (in the local time zone) in which the usage took place. |
| DATA\_PLANE\_ID | VARCHAR | ID of the data plane which incurred the credit usage. |
| DATA\_PLANE\_TYPE | VARCHAR | Type of the data plane. The only value currently returned is *BYOC*. |
| DATA\_PLANE\_CREDITS\_USED | NUMBER | Number of compute credits the data plane used in the hour. This value is always 0, because *BYOC* data planes run on infrastructure you manage and incur no Snowflake compute credits. For *BYOC*, you’re charged credits only for runtime usage. |
| RUNTIME\_KEY | VARCHAR | Key identifying the runtime which incurred the credit usage. |
| RUNTIME\_NAME | VARCHAR | Name of the runtime which incurred the credit usage. |
| ENTITY\_ID | NUMBER | ID of the Openflow object that incurred the credit usage. For gen 2 runtimes, this is the ID of the runtime. For gen 1 runtimes, this is the ID of the runtime’s integration. Contains a NULL value when Snowflake doesn’t know the entity, such as for usage recorded before entity attribution was turned on for your account. |
| ENTITY\_TYPE | VARCHAR | Type of the object identified by `ENTITY_ID`. One of:   - `OPENFLOW RUNTIME` for gen 2 runtimes. - `INTEGRATION` for gen 1 runtimes.   When `ENTITY_ID` is NULL, this column returns `OPENFLOW_RUNTIME`. This value doesn’t identify a specific object. |
| RUNTIME\_CREDITS\_USED | NUMBER | Number of compute credits the runtime used in the hour. This does not include the credits used by the data plane or the credits used to ingest the data in Snowflake. |

Expand

Show lessSee more

## Usage notes

- `ENTITY_ID` and `ENTITY_TYPE` are populated only for usage recorded after entity attribution was turned on for your
  account. Earlier usage has a NULL `ENTITY_ID`.
- Runtime and integration IDs can overlap. Always use `ENTITY_TYPE` together with `ENTITY_ID` to identify the object.
- A runtime can have more than one row for the same hour. This happens when the hour spans the point where entity
  attribution was turned on, because usage processed before that point has a NULL `ENTITY_ID`. Usage can also have a
  NULL `ENTITY_ID` when Openflow doesn’t know the entity for it.
