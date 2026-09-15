[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# OBJECT\_ACCESS\_REQUEST\_HISTORY view

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view allows consumers to access audit logs that track the submission, rejection, and approval of object access requests through the Internal Marketplace to maintain security and compliance.

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
| TIMESTAMP | TIMESTAMP\_LTZ | The state transition event. |
| USER\_REGION | VARCHAR | The region of the requester or approver. |
| USER\_ACCOUNT\_NAME | VARCHAR | The account name of the requester or approver. |
| USER\_NAME | VARCHAR | The username of the requester or approver. |
| USER\_EMAIL | VARCHAR | The email of the requester or approver. |
| USER\_COMMENT | VARCHAR | For CREATE\_REQUEST and CANCEL REQUEST, this shows the reason for access provided by the requester.  For APPROVE\_REQUEST, DENY\_REQUEST, and AUTO\_APPROVE\_REQUEST, this is the comment for approval/denial provided by the approver. |
| ACTION | VARCHAR | The requester or approver action. This can be one of the following:   - CREATE\_REQUEST - CANCEL\_REQUEST - APPROVE\_REQUEST - DENY\_REQUEST - AUTO\_APPROVE\_REQUEST |
| REQUEST\_ID | VARCHAR | The UUID of the request. This can be used to track the history of the request. |
| OBJECT\_DOMAIN | VARCHAR | The requested object domain. Currently, this can only be DATA\_EXCHANGE\_LISTING. |
| OBJECT\_REGION | VARCHAR | The snowflake region name where the requested object is located. |
| OBJECT\_ACCOUNT\_NAME | VARCHAR | The account where the requested object is located. |
| OBJECT\_NAME | VARCHAR | The name of the requested object. |
| GRANTEE\_TO\_AUTHORIZE | VARCHAR | For CREATE\_REQUEST and CANCEL REQUEST, this shows the role provided by the requester.  For APPROVE\_REQUEST, DENY\_REQUEST, and AUTO\_APPROVE\_REQUEST, this is the role granted or denied by the approver. |
| GRANTEE\_TYPE | VARCHAR | The type of the grantee. Currently, this can only be ROLE. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 5 hours.
