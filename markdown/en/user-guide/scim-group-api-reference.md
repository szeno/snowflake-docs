# SCIM group API reference

You can use the SCIM group API to access, create, and modify roles.

Snowflake uses SCIM to import roles from Okta, Azure AD and custom-built applications. The roles in these identity providers map one-to-one
with Snowflake roles.

Roles, sometimes called groups, are a collection of access privileges. To access securable objects in Snowflake, privileges must be assigned
to roles, and roles are assigned to other roles or users.

Access permissions and rights that are granted to the role are automatically inherited by every member, such as a user, of the role. For
more information, see [Overview of Access Control](/user-guide/security-access-control-overview).

A user’s access requirements to Snowflake can change. For example, a user can change from being an individual contributor to a manager in
their organization, which may require their role in Snowflake to change, or they may require access to data sets only available to managers.

As the user’s role changes in the identity provider, their access to Snowflake automatically changes when their organization role maps to the
corresponding Snowflake role.

## HTTP headers

The Snowflake SCIM API uses bearer tokens for HTTP authentication.

Each HTTP request to the Snowflake SCIM API allows the following HTTP headers:

| Header | Value |
| --- | --- |
| `Authorization` (Required) | `Bearer <access_token>`. Snowflake accepts different types of tokens. See [Authenticating SCIM API requests](/user-guide/scim-authentication). |
| `Content-Type` | `application/scim+json` |
| `Accept-Encoding` | `utf-8` |
| `Accept-Charset` | `utf-8` |

Expand

Show lessSee more

## Base URL

If you are authenticating with External OAuth or programmatic access tokens, specify which SCIM security integration
to use by including its UUID in the URL:

Copy code

```
/scim/v2/<integration_uuid>/
```

To obtain the `integration_uuid`, run a [DESCRIBE SECURITY INTEGRATION](/sql-reference/sql/desc-integration) command
and copy the value of the `SCIM_ENDPOINT_ID` property. For example:

Copy code

```
DESC SECURITY INTEGRATION OKTA_PROVISIONING;
```

If your account has only one enabled SCIM security integration, you can omit the UUID:

Copy code

```
/scim/v2/
```

If you are authenticating with a [SCIM access token](/user-guide/scim-authentication#label-scim-auth-long-lived-token), use the shorter base
URL `/scim/v2/`.

For more information about authentication and base URLs, see [Send SCIM requests](/user-guide/scim-authentication#label-scim-auth-send-requests).

## Group attributes

You can specify group (that is, a role) attributes in the body of the API requests as key-value pairs in JSON format. These pairs contain
information about the group, such as the group’s display name. Identity providers can specify their own key names for each attribute.

Snowflake supports the following SCIM attributes for role lifecycle management. Attributes are writable unless otherwise noted.

| SCIM Group Attribute | Snowflake Group Attribute | Type | Description |
| --- | --- | --- | --- |
| `id` | `id` | String | The immutable, unique identifier (GUID) of the role in Snowflake.  Snowflake does not return this value.  You can find this value by calling the Information Schema table function [REST\_EVENT\_HISTORY](/sql-reference/functions/rest_event_history). Check the IdP logs to ensure the values match. |
| `displayName` | `name` | String | The text shown in the user interface when referring to the group. |
| `members.value` | N/A | String | The `id` of the user who is a member of the role. |
| `schemas` | N/A | String | An array of strings to indicate the namespace URIs. For example, `urn:ietf:params:scim:schemas:core:2.0:Group`. |

Expand

Show lessSee more

## Get details about a group by displayName

Method and endpoint:
:   `GET /scim/v2/Groups?filter=displayName eq "{{group_name}}"`

Description:
:   Returns details about a group associated with the `displayName` query parameter.

    If the `MONITOR ROLE` privilege is granted to the [SCIM provisioner](/user-guide/scim-okta), then the SCIM provisioner can see
    all groups in a Snowflake account, instead of only seeing groups owned by the SCIM provisioner.

    For example, to grant the `MONITOR ROLE` privilege to a SCIM provisioner, you can use the GRANT command:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;
    GRANT MONITOR ROLE ON ACCOUNT TO ROLE example_okta_provisioner_role;
    ```

    Returns the HTTP response status code `200` if the HTTP request successfully completed.

## Get details about a group by groupId

Method and endpoint:
:   `GET /scim/v2/Groups/{{group_id}}`

Description:
:   Returns details about a group associated with the `group_id` path parameter.

    Returns the HTTP response status code `200` if the HTTP request successfully completed.

## List groups

Method and endpoint:
:   `GET /scim/v2/Groups`

Description:
:   Returns a paginated list of groups (roles) in the account, optionally matching a filter.

    If the `MONITOR ROLE` privilege is granted to the [SCIM provisioner](/user-guide/scim-okta), then the SCIM provisioner can see
    all groups in a Snowflake account, instead of only seeing groups owned by the SCIM provisioner.

    For example, to grant the `MONITOR ROLE` privilege to a SCIM provisioner, you can use the GRANT command:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;
    GRANT MONITOR ROLE ON ACCOUNT TO ROLE example_okta_provisioner_role;
    ```

    Returns the HTTP response status code `200` if the HTTP request successfully completed.

    Note

    This endpoint’s behavior is controlled by the 2026\_03 behavior change bundle. For rollout details, see
    [SCIM: List API returns paginated results; unsupported filters rejected](/release-notes/bcr-bundles/2026_03/bcr-2276).

Optional query parameters:
:   `filter=displayName { eq | sw } "{displayName}"`

    > eq:
    > :   Searches for a group with a name that matches the provided `displayName` value. The search matches both the exact value and its fully uppercased equivalent.
    >
    >     Pagination query parameters, such as `startIndex` and `count`, are ignored when using `eq`.
    >
    >     **Example**: the following request finds a role named `ABC`:
    >
    >     Copy code
    >
    >     ```
    >     GET /scim/v2/Groups?filter=displayName eq "abc"
    >     ```
    >
    > sw:
    > :   Searches for group names that start with the value provided for `displayName`. The search is case-sensitive.
    >
    >     **Example**: the following request finds roles starting with `ABC`, such as `ABC_ADMIN` or `ABC_READER`.
    >     Note that `sw "abc"` would not match a role named `ABC_ADMIN`.
    >
    >     Copy code
    >
    >     ```
    >     GET /scim/v2/Groups?filter=displayName sw "ABC"
    >     ```

    `startIndex`

    > The 1-based index of the first result to return. Values less than 1 are treated as 1.
    > Non-numeric values return HTTP `400`.
    >
    > Default: `1`.
    >
    > **Example**: the following request returns a list of groups, skipping the first group:
    >
    > Copy code
    >
    > ```
    > GET /scim/v2/Groups?startIndex=2
    > ```

    `count`

    > The maximum number of groups returned per page. Negative values are treated as 0 (returns an empty
    > `Resources` array). Values above 1000 are treated as 1000. Non-numeric values return HTTP `400`.
    >
    > Default: `100`.
    >
    > Max: `1000`.
    >
    > **Example**: the following request returns a list of groups, skipping the first group, with a maximum of 10 groups per page:
    >
    > Copy code
    >
    > ```
    > GET /scim/v2/Groups?startIndex=2&count=10
    > ```

    `excludedAttributes`

    > Excludes the specified attributes from the response. Only `members` is supported, which omits the list
    > of users that belong to each group. Other values are ignored.
    >
    > **Example**: the following request returns the first page of groups without their members returned:
    >
    > Copy code
    >
    > ```
    > GET /scim/v2/Groups?excludedAttributes=members
    > ```

    Note

    For accounts with large numbers of groups, specifying `excludedAttributes` can significantly reduce response
    size and latency.

Limitations:
:   - Only the `displayName` attribute is supported for filtering. Filtering on other attributes returns an empty
      result set.
    - Only the `eq` and `sw` operators are supported. Using an unsupported operator returns HTTP `400` with
      SCIM error type `invalidFilter`.
    - Compound filters using logical operators (`and`, `or`) are not supported and return HTTP `400` with
      SCIM error type `invalidFilter`.
    - The `sw` operator is case-sensitive for groups.
    - The `members` attribute for groups includes only users directly granted the role. Users who inherit the role
      through the role hierarchy are not included.

Response body objects:
:   `itemsPerPage` equals the `count` value used for the query.

    `totalResults` equals `startIndex` + `count` when more pages are available, or the total number of
    matching items when no more pages are available.

    Clients should check that the sum of `startIndex` and `itemsPerPage` is less than or equal to `totalCount`.

    Clients should continue making requests until the sum of `startIndex` and `itemsPerPage` is greater than `totalCount`.

    See [Group attributes](#label-scim-group-attributes) for group attribute details.

Examples:
:   An example response that returns a paginated list of groups, excluding their `members` attribute from the results:

    Copy code

    ```
    {
        "schemas": [
            "urn:ietf:params:scim:api:messages:2.0:ListResponse"
        ],
        "Resources": [
            {
                "schemas": [
                    "urn:ietf:params:scim:schemas:core:2.0:Group"
                ],
                "id": "81_2",
                "meta": {
                    "resourceType": "Group",
                    "created": "2024-08-01T03:37:04Z",
                    "lastModified": "2024-08-01T03:37:04Z"
                },
                "displayName": "okta_role1"
            },
            {
                "schemas": [
                    "urn:ietf:params:scim:schemas:core:2.0:Group"
                ],
                "id": "82_2",
                "meta": {
                    "resourceType": "Group",
                    "created": "2024-08-02T03:37:04Z",
                    "lastModified": "2024-08-02T03:37:04Z"
                },
                "displayName": "okta_role2"
            }
        ],
        "totalResults": 2,
        "startIndex": 1,
        "itemsPerPage": 100
    }
    ```

## Create a group

Method and endpoint:
:   `POST /scim/v2/Groups`

Description:
:   Creates a new group in Snowflake.

    Returns the HTTP response status code `201` if the HTTP request successfully completed.

Examples:
:   Create a group with the `displayName` `scim_test_group2`:

    Copy code

    ```
    {
      "schemas": ["urn:ietf:params:scim:schemas:core:2.0:Group"],
      "displayName":"scim_test_group2"
    }
    ```

## Update a group

Method and endpoint:
:   `PATCH /scim/v2/Groups/{{group_id}}`

Description:
:   Updates the display name attribute or group membership of the group associated with the `group_id` path parameter.

    You must set `op` to `add` or `replace` to perform this HTTP request.

    Returns a `200` or `204` HTTP response status code if the HTTP request successfully completed. A `200` status code indicates the
    SCIM client is Okta.

Examples:
:   Update a group `displayName`, remove a member and add a member:

    Copy code

    ```
    {
      "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
      "Operations": [{
        "op": "replace",
        "value": { "displayName": "updated_name" }
      },
      {
        "op" : "remove",
        "path": "members[value eq \"user_id_1\"]"
      },
      {
        "op": "add",
        "value": [{ "value": "user_id_2" }]
      }]
    }
    ```

## Delete a group

Method and endpoint:
:   `DELETE /scim/v2/Groups/{{group_id}}`

Description:
:   Deletes the group associated with the `group_id` path parameter.
