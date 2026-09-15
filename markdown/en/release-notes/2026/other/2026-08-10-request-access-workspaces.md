# Aug 10, 2026: Request Access in Workspaces (*Preview*)

With this preview release, you can resolve access-related SQL errors in Workspaces by submitting access
requests directly from Snowsight. When a query fails because of missing privileges and the user can’t
self-resolve the issue by switching roles, the user can submit a request with a reason. Users with the
ACCOUNTADMIN or SECURITYADMIN role receive notifications and can review, approve, reject, or mark requests as
approved externally on the **Requests & Approvals** page.

To enable the preview for your account, after you
[enable preview features for your account](/sql-reference/functions/system_enable_preview_access), use the
[ALTER ACCOUNT](/sql-reference/sql/alter-account) command. For example:

Copy code

```
ALTER ACCOUNT SET FEATURE_ENABLE_REQUEST_ACCESS_FOR_WORKSPACES = 'ENABLED';
```

For more information, see [Request Access in Workspaces](/user-guide/access-requests-workspaces).
