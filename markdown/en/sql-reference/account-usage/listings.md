Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# LISTINGS view

This Account Usage view returns all the listings owned by the current account, including dropped listings. The information in this view has a latency of up to 3 hours.

## Columns

The following table provides definitions for the LISTINGS view columns.

| Column | Data type | Description |
| --- | --- | --- |
| GLOBAL\_NAME | VARCHAR | The global name of the listing. |
| NAME | VARCHAR | The object name of the listing. |
| OWNER | VARCHAR | The name of the role that owns the listing. |
| CREATED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was created. |
| UPDATED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was last updated. |
| PUBLISHED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was published. |
| DELETED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was deleted. This value is NULL if the listing hasn’t been deleted. |
| TITLE | VARCHAR | The title of the listing. |
| SUBTITLE | VARCHAR | The subtitle of the listing. |
| DESCRIPTION | VARCHAR | The description of the listing. |
| LISTING\_TERMS | OBJECT | The terms of service associated with the listing. |
| STATE | VARCHAR | The current state of the listing. |
| SHARE | VARCHAR | The name of the share associated with the listing. |
| APPLICATION\_PACKAGE | VARCHAR | The name of the application package associated with the listing. This is only populated if `IS_APPLICATION` is true. |
| DATA\_ATTRIBUTES | OBJECT | Data attributes associated with the listing. |
| CATEGORIES | VARCHAR | Categories associated with the listing. |
| PROFILE | VARCHAR | The profile attached to the external listing. |
| CUSTOMIZED\_CONTACT\_INFO | VARCHAR | Customized contact information associated with the listing. |
| COMMENT | VARCHAR | Comment associated with the listing, if any. |
| TARGETS | OBJECT | Targets consolidating external/organizational listings with regions. |
| AUTO\_FULFILLMENT | OBJECT | Auto-fulfillment information associated with the listing. |
| IS\_SHARE | BOOLEAN | Indicates whether this is a data share listing. |
| IS\_APPLICATION | BOOLEAN | Indicates whether this is an application listing. |
| DISTRIBUTION | VARCHAR | The distribution of the listing. Possible values are `EXTERNAL` and `ORGANIZATION`. |
| ORGANIZATION\_PROFILE\_NAME | VARCHAR | The organization profile attached to the listing. |
| UNIFORM\_LISTING\_LOCATOR | VARCHAR | The uniform listing locator (ULL) of the listing. |
| APPROVER\_CONTACT | VARCHAR | The approver contact information associated with the listing. |
| SUPPORT\_CONTACT | VARCHAR | The support contact information associated with the listing. |
| RESHARING | OBJECT | Resharing configuration of the listing. |

Expand

Show lessSee more
