Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# LISTINGS view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view returns the listings owned by the accounts in your organization, including dropped listings.

Each row in this view corresponds to a different listing.

This view is available only in the [organization account](/user-guide/organization-accounts). Users with the GLOBALORGADMIN role, or users granted the SNOWFLAKE.ORGANIZATION\_SECURITY\_VIEWER application role, can access it. For details, see [Accessing the ORGANIZATION\_USAGE schema](/sql-reference/organization-usage#label-org-usage-access-org-account).

## Columns

**Organization-level columns**

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | Name of the organization. |
| ACCOUNT\_LOCATOR | VARCHAR | System-generated identifier for the account. |
| ACCOUNT\_NAME | VARCHAR | User-defined identifier for the account. |

Expand

Show lessSee more

**Additional columns**

| Column Name | Data Type | Description |
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

## Usage notes

- Latency for the view may be up to 24 hours.
