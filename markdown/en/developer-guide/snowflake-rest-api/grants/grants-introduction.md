# Manage grants

The SNOWFLAKE REST [Grant API](/developer-guide/snowflake-rest-api/reference/grant.html) provides the following endpoints to manage Snowflake grants:

**Snowflake Grant API endpoints**

| Endpoint | Description |
| --- | --- |
| `POST /api/v2/grants/granteeType/granteeName/securableType/securableName/privileges` | Grants privileges listed in the request body. |
| `POST /api/v2/grants/granteeType/granteeName/bulkGrantType/securableTypePlural/scopeType/scopeName/privileges` | Grants privileges listed in the request body to all securables of the specified type in the given scope. |
| `DELETE /api/v2/grants/granteeType/granteeName/securableType/securableName/privileges/privilege` | Revokes privileges listed in the path parameters. |
| `DELETE /api/v2/grants/granteeType/granteeName/securableType/securableName/privileges/privilege/grant-option` | Revokes the grant option for the privileges listed in the path parameters. |
| `DELETE /api/v2/grants/granteeType/granteeName/bulkGrantType/securableTypePlural/scopeType/scopeName/privileges/privilege` | Revokes the privilege listed on the group securable in the specified scope. |
| `DELETE /api/v2/grants/granteeType/granteeName/bulkGrantType/securableTypePlural/scopeType/scopeName/privileges/privilege/grant-option` | Revokes the grant option for the privilege listed on the group securable in the given scope. |
| `GET /api/v2/grants/granteeType/granteeName` | Lists the roles and privileges granted to the specified grantee using the output of SHOW GRANTS TO. |

Expand

Show lessSee more

For reference documentation, see [Snowflake Grant API reference](/developer-guide/snowflake-rest-api/reference/grant.html).
