Schema:
:   [ORGANIZATION\_USAGE](/sql-reference/organization-usage)

    For guidance on query performance when using organization-wide usage views, see [Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance).

# MULTI\_PARTY\_APPROVAL\_REQUESTS view

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Enterprise Edition Feature](/user-guide/intro-editions)

Available in the organization account, which requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Important

This view is only available in the organization account. For more information, see [Premium views in the organization account](/user-guide/organization-accounts-premium-views).

Organization Usage performance

When you query a specific view in the `SNOWFLAKE.ORGANIZATION_USAGE` schema, follow the organization-wide guidance in
[Performance (Organization Usage)](/sql-reference/organization-usage#label-org-usage-performance): bound every scan on history views, list
columns explicitly, and use the time filter column table plus worked SQL and anti-patterns there.

This Organization Usage view returns one row for each [Multi-party Approval](/user-guide/multi-party-approval)
request in your organization.

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
| REQUEST\_ID | VARCHAR | Unique identifier for the approval request. |
| REQUESTER\_USER\_NAME | VARCHAR | Name of the user who triggered the request. |
| STATUS | VARCHAR | Status of the request, such as PENDING, APPROVED, REJECTED, CANCELLED, or EXPIRED. |
| OPERATION | VARCHAR | The protected operation that triggered the request, such as MODIFY\_MULTI\_PARTY\_APPROVAL, DISABLE\_MULTI\_FACTOR\_AUTHENTICATION, or MODIFY\_NETWORK\_POLICY. |
| JOB\_UUID | VARCHAR | UUID of the job that triggered the request. |
| CREATED\_TIME | TIMESTAMP\_LTZ | Date and time when the request was created. |
| RESOLVED\_TIME | TIMESTAMP\_LTZ | Date and time when the request was resolved. NULL if the request is still pending. |
| EXPIRED\_AT | TIMESTAMP\_LTZ | Date and time when the request expires or expired. NULL if the request has not yet expired. |
| REQUEST\_JUSTIFICATION | VARCHAR | Business justification provided by the requester. |
| JUSTIFICATION\_TIME | TIMESTAMP\_LTZ | Date and time when the justification was submitted. NULL if no justification was provided. |
| REQUIRED\_APPROVALS\_COUNT | NUMBER | Number of approvals required for this request. |
| APPROVERS | ARRAY | An array of objects, one per approver, each with the following keys: `approver_user_name`, `vote`, `assigned_time`, `voted_time`, and `comment`. |
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the Multi-party Approval policy that governs the request. |
| POLICY\_NAME | VARCHAR | Fully qualified name (database.schema.policy) of the Multi-party Approval policy. NULL if the policy was dropped. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 24 hours.
