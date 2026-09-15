# LISTINGS view

This Information Schema view displays all listings for which the current role has been granted access privileges. This view provides real time information with no latency of data.

## Columns

| Column | Data type | Description |
| --- | --- | --- |
| GLOBAL\_NAME | VARCHAR | The global name of the listing. |
| NAME | VARCHAR | The name of the listing. |
| OWNER | VARCHAR | The name of the role that owns the listing. |
| CREATED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was created. |
| UPDATED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was last updated. |
| PUBLISHED\_ON | TIMESTAMP\_LTZ | The timestamp when the listing was published. |
| TITLE | VARCHAR | The title of the listing. |
| SUBTITLE | VARCHAR | The subtitle of the listing. |
| DESCRIPTION | VARCHAR | The description of the listing. |
| LISTING\_TERMS | VARCHAR | The terms of service associated with the listing. |
| STATE | VARCHAR | The current state of the listing. |
| SHARE | VARCHAR | The name of the share associated with the listing. |
| APPLICATION\_PACKAGE | VARCHAR | The name of the application package associated with the listing. |
| DATA\_ATTRIBUTES | VARCHAR | Data attributes associated with the listing. |
| CATEGORIES | VARCHAR | Categories associated with the listing. |
| PROFILE | VARCHAR | The profile attached to the external listing. |
| CUSTOMIZED\_CONTACT\_INFO | VARCHAR | Customized contact information associated with the listing. |
| COMMENT | VARCHAR | Comment associated with the listing, if any. |
| TARGETS | VARCHAR | The targets consolidating external/organization listings with regions. |
| AUTO\_FULFILLMENT | VARCHAR | Auto-fulfillment information associated with the listing. |
| IS\_SHARE | BOOLEAN | Indicates whether this is a data share listing. |
| IS\_APPLICATION | BOOLEAN | Indicates whether this is an application listing. |
| DISTRIBUTION | VARCHAR | The distribution of the listing. Possible values are `EXTERNAL` and `ORGANIZATION`. |
| IS\_MOUNTLESS\_QUERYABLE | BOOLEAN | Indicates whether the listing is mountless queryable. |
| ORGANIZATION\_PROFILE\_NAME | VARCHAR | The organization profile attached to the listing, if any. |
| UNIFORM\_LISTING\_LOCATOR | VARCHAR | The uniform listing locator (ULL) of the listing. |
| APPROVER\_CONTACT | VARCHAR | The approver contact information associated with the listing. |
| SUPPORT\_CONTACT | VARCHAR | The support contact information associated with the listing. |
| RESHARING | VARCHAR | Resharing configuration of the listing. |

Expand

Show lessSee more

## Usage notes

The view doesn’t capture deleted listings.

## Examples

Retrieve all listings in the current account:

Copy code

```
SELECT * FROM <any_database>.INFORMATION_SCHEMA.LISTINGS;
```
