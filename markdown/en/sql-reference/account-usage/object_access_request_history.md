Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# OBJECT\_ACCESS\_REQUEST\_HISTORY view

This Account Usage view allows consumers to access audit logs that track the submission, rejection, and approval of object access requests through the Internal Marketplace to maintain security and compliance.

## Columns

The following table provides a description of each column in the view.

| Column Name | Data Type | Description |
| --- | --- | --- |
| ORGANIZATION\_NAME | VARCHAR | The organization name of current account. |
| ACCOUNT\_NAME | VARCHAR | The account name of the current account. |
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

For approver-initiated actions, such as APPROVE\_REQUEST, DENY\_REQUEST, and AUTO\_APPROVE\_REQUEST, the requester can’t see the approver’s USER\_ACCOUNT\_NAME, USER\_NAME, USER\_EMAIL, and OBJECT\_ACCOUNT\_NAME.
