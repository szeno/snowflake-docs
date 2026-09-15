# Request Access in Workspaces

[Preview Feature — Open](/release-notes/preview-features)

Available to all accounts. Requires enablement.

To opt in to this public preview, after you
[enable preview features for your account](/sql-reference/functions/system_enable_preview_access), use the
[ALTER ACCOUNT](/sql-reference/sql/alter-account) command. For example:

Copy code

```
ALTER ACCOUNT SET FEATURE_ENABLE_REQUEST_ACCESS_FOR_WORKSPACES = 'ENABLED';
```

The Request Access workflow in Workspaces helps users resolve access-related SQL errors by submitting access
requests directly from Snowsight. It also gives administrators a dedicated experience in
Snowsight, with insights to review and resolve user access requests.

When a user runs a query and it fails with an access error, Snowflake first checks whether the issue can be
resolved through self-service, such as switching to another role the user already has. If self-resolution isn’t
possible, or if the user cancels the self-resolution analysis, the user can submit an access request for review.
The ACCOUNTADMIN and SECURITYADMIN roles always receive email and in-app notifications about the access request.
If an `ACCESS_APPROVAL` contact is configured, that contact is also notified. Users with the ACCOUNTADMIN or
SECURITYADMIN role can review the request, get insights about roles in the account that can resolve the request,
and take action.

## Why use Request Access in Workspaces

- **Simpler requester experience with actionable next steps**, rather than requiring the user to understand
  complex error messages and identify how to resolve the issue.
- **Minimized context switching with a consolidated experience to submit, review, and track** all access
  requests. The user submits the request at the point of error with relevant information automatically included.
  This eliminates the overhead of gathering details, finding a point of contact for resolution, or filing a
  ticket in an ITSM system.
- **Faster resolution through automated analysis and insights** for the approver, along with a dedicated
  experience in Snowsight to help quickly resolve a request.

## Key personas

### Requester

The user who ran a query and got an access control error. After Snowflake checks that self-resolution isn’t
possible, or after the user cancels that analysis, the requester submits an access request from the
**Resolve Access Error** dialog, providing a mandatory reason and optionally specifying a role they believe
will resolve the issue. This suggestion is advisory only; the approver determines what access, if any, is
granted. The requester can view, track, and cancel their own pending requests at any time in
Snowsight.

### Approver

The ACCOUNTADMIN or SECURITYADMIN who reviews and resolves incoming requests. These roles receive email and
in-app notifications. If an `ACCESS_APPROVAL` contact is configured for the relevant object, that contact also
receives email and in-app notifications. For information about associating an `ACCESS_APPROVAL` contact with
an object, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).
The approver can:

- Grant access by selecting a role and granting it to the user, or to one of the user’s existing roles
- Mark the request as approved if approved in an external system
- Reject the request, providing a reason visible to the requester

Warning

Granting access to one of the user’s existing roles also grants that access to every user who holds that
role. To limit access only to the requester, grant a role directly to the user instead.

## Request states

An access request moves through the following states. You can view and filter requests by state on the
Snowsight **Requests & Approvals** page.

| State | Description |
| --- | --- |
| **Pending** | The request has been submitted and is awaiting approver action. |
| **Approved** | The approver granted access directly in Snowflake or approved it externally. The requester is notified and can rerun their query. |
| **Rejected** | The approver rejected the request. The requester is notified along with the reason for rejection. |
| **Cancelled** | The requester withdrew the request before it was approved or rejected. |
| **Expired** | The approver didn’t act on the request before it expired. The request is no longer actionable. |

Expand

Show lessSee more

## How Request Access works

### Step 1: A user runs a query and it fails

A user runs a query in Workspaces and receives an access control error, such as *Insufficient privileges*,
along with the **Resolve Access Error** option.

### Step 2: Snowflake checks for self-resolution

Before presenting the request flow, Snowflake checks whether the user can resolve the problem with one of their
existing roles. If the user has a role that works, Snowflake guides the user to switch roles instead of
immediately creating a request.

The user can cancel this self-resolution analysis. If they cancel, they can still submit an access request even
when a switchable role exists. In that case, the approver can still see insights about roles that can satisfy
the request, including roles the requester could have switched to.

### Step 3: The user submits a request if needed

If self-resolution isn’t possible, or if the user cancels the self-resolution analysis, a request dialog opens.
The user provides a mandatory reason for submitting the request and can optionally request a specific role if
they already know which one they need. This suggestion is advisory only; the approver determines what access,
if any, is granted.

### Step 4: Administrators review the request

After the request is submitted, it appears in Snowsight under **Governance & security** »
**Requests & Approvals**. Users with the ACCOUNTADMIN or SECURITYADMIN role receive email and in-app
notifications and can review the request details, roles in the account that can satisfy the request, and choose
to:

- Grant access by selecting a role and granting it to the user, or to one of the user’s existing roles
- Mark the request as approved if they approved it in an external system
- Reject the request

### Step 5: Access is resolved and the user retries the query

If the administrator grants access in Snowflake or externally, the requester receives a notification and can
rerun the query successfully. If the administrator rejected the request, the requester receives a notification
along with the reason for rejection.

## Manage requests

### View requests you created

1. Sign in to Snowsight.
2. Select **Governance & security**.
3. Select **Requests & Approvals**.
4. Select **Pending**.
5. Select **Created by me**.
6. Select the request you want to view.
7. Review your submitted request, or cancel the request if it is no longer applicable.

### Review requests sent to you

1. Sign in to Snowsight.
2. Select **Governance & security**.
3. Select **Requests & Approvals**.
4. Select **Pending**.
5. Select **Sent to me**.
6. Select the request you want to review.
7. Select **Grant access**, **Mark as approved**, or **Reject**.

### View request history

1. Sign in to Snowsight.
2. Select **Governance & security**.
3. Select **Requests & Approvals**.
4. Select **History**.
5. Select **Sent to me** or **Created by me**.
6. Optionally, filter by Status, Requested by, or Time.
7. Select the request you want to view.

## Considerations

- A request is created when self-resolution isn’t possible, or when the user cancels the self-resolution
  analysis. Canceling the analysis can still produce a request even if a switchable role exists, and the
  approver can still suggest those roles.
- The requester role picker supports account roles only. It lists all account roles, not only the roles the
  requester currently holds.
- The requester-facing flow doesn’t display detailed missing privileges.
- In this preview, configured `ACCESS_APPROVAL` contacts receive notifications but don’t have a dedicated
  review experience in Snowsight unless they hold the ACCOUNTADMIN or SECURITYADMIN role.
