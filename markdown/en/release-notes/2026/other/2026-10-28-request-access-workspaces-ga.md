# Oct 28, 2026: Request Access in Workspaces (*General availability*)

Request Access in Workspaces is now generally available and is no longer in [Preview](/release-notes/preview-features).

When a query fails because of missing privileges and the user can’t self-resolve the issue by switching roles, the user can submit an access request with a reason directly from Snowsight. Users with the ACCOUNTADMIN or SECURITYADMIN role receive notifications and can review, approve, reject, or mark requests as approved externally on the **Requests & Approvals** page.

To enable the feature for your account, use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) command. For example:

Copy code

```
ALTER ACCOUNT SET FEATURE_ENABLE_REQUEST_ACCESS_FOR_WORKSPACES = 'ENABLED';
```

For more information, see [Request Access in Workspaces](/user-guide/access-requests-workspaces).
