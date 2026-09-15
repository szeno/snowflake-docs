Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# MULTI\_PARTY\_APPROVAL\_REQUESTS view

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides the [Multi-party Approval](/user-guide/multi-party-approval)
requests in your account, including who requested each protected operation, who approved
or rejected it, and when.

Each row in this view corresponds to a different Multi-party Approval request.

## Columns

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

- Latency for the view may be up to 120 minutes (2 hours).
