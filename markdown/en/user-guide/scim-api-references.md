# SCIM API requests

Identity providers can use a SCIM client to make RESTful API requests to the Snowflake SCIM server. After validating the API request,
Snowflake performs actions requested by the identity providers on users or groups. For information about authenticating
SCIM API requests, see [Authenticating SCIM API requests](/user-guide/scim-authentication).

Note

The Snowflake SCIM API lets you manage users and groups in Snowflake from your identity provider. If you make
changes to users and groups in Snowflake directly, the changes don’t synchronize with your identity provider.

Snowflake provides the following SCIM APIs:

- [User API](/user-guide/scim-user-api-reference): Allows identity providers to do the following actions:

  - Check whether users exist.
  - Get details about users.
  - List users.
  - Create and activate users.
  - Update user attributes.
  - Deactivate users.
- [Group API](/user-guide/scim-group-api-reference): Allows identity providers to do the following actions:

  - Get details about groups.
  - List groups.
  - Create groups.
  - Update groups.
  - Delete groups.

For additional examples, see the [Postman collection](https://documenter.getpostman.com/view/5462540/S1Lzx6gY?version=latest#intro).

## Auditing SCIM API requests

You can query Snowflake to find information about SCIM API requests that were made over a span of time. You can use this information to see
whether your organization’s active users match the users provisioned into Snowflake.

For example, to determine which SCIM API requests were made in the last five minutes, with a maximum of 200 requests to be returned, you can
use the Information Schema table function [REST\_EVENT\_HISTORY](/sql-reference/functions/rest_event_history):

Copy code

```
USE ROLE ACCOUNTADMIN;
USE DATABASE demo_db;
USE SCHEMA information_schema;
SELECT *
  FROM TABLE(rest_event_history(
      'scim',
      dateadd('minutes',-5,current_timestamp()),
      current_timestamp(),
      200))
  ORDER BY event_timestamp;
```

For more information on how to modify this query, see [DATEADD](/sql-reference/functions/dateadd) and
[CURRENT\_TIMESTAMP](/sql-reference/functions/current_timestamp).
