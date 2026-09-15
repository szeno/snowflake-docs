# SCIM user API reference

You can use the SCIM user API to access, create, and modify user data.

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

## User attributes

You can specify user attributes in the body of the API requests as key-value pairs in JSON format. These pairs contain information about the
user, such as the user’s display name or their email address. Identity providers can specify their own key names for each attribute. For
example, identity providers can use the key `lastName`, instead of `familyName`, to represent the user’s last name. Snowflake
does not support multi-value user attributes.

Important

In the table below, the attributes `userName` and `loginName` both refer to the attribute `userName`. Snowflake
supports specifying different values for the `userName` and `loginName` attributes by setting the
[MAP\_SCIM\_USERNAME\_TO\_ENTERPRISE\_ATTR](/sql-reference/parameters#label-map-scim-username-to-enterprise-attr) account parameter to `TRUE`.
When this parameter is enabled, `userName` maps to `LOGIN_NAME` and the `snowflakeUserName` enterprise extension
attribute maps to `NAME`.

Snowflake supports the following attributes for user lifecycle management:

| SCIM User Attribute | Snowflake User Attribute | Type | Description |
| --- | --- | --- | --- |
| `id` | `ID` | string | The immutable, unique identifier (GUID) of the user in Snowflake.  Snowflake does not return this value in the [DESCRIBE USER](/sql-reference/sql/desc-user) or [SHOW USERS](/sql-reference/sql/show-users) output.  For requests on endpoints that require this attribute, such as `PATCH scim/v2/Users/{{id}}`, the `id` attribute can be found using the [REST\_EVENT\_HISTORY](/sql-reference/functions/rest_event_history) function. Check the IdP logs to ensure the values match. |
| `userName` | `NAME`, `LOGIN_NAME` | string | The identifier used to log in to Snowflake. For more information about these attributes, see [CREATE USER](/sql-reference/sql/create-user). |
| `name.givenName` | `FIRST_NAME` | string | The first name of the user. |
| `name.familyName` | `LAST_NAME` | string | The last name of the user. |
| `emails` | `EMAIL` | string | The email address of the user. |
| `displayName` | `DISPLAY_NAME` | string | The text shown in the user interface when referring to the user. |
| `externalID` | N/A | string | The unique identifier set by the provisioning client (for example, Azure or Okta). |
| `password` | `PASSWORD` | string | The password for the user.  This value is not returned in the JSON response.  If the `SYNC_PASSWORD` property in the SCIM security integration is set to `FALSE`, and the SCIM API request specifies the `password` attribute, Snowflake ignores the value for the `password` attribute. All other attributes in the API request are processed normally. |
| `active` | `DISABLED` | boolean | Disables the user when set to `false`. |
| `groups` | N/A | string | A list of groups to which the user belongs. The group `displayName` is required.  The user’s groups are immutable and their membership must be updated using the [SCIM groups API](/user-guide/scim-group-api-reference#label-scim-update-a-group). |
| `meta.created` | `CREATED_ON` | string | The time the user was added to Snowflake. |
| `meta.lastModified` | `UPDATED_ON` | string | The time the user was last modified in Snowflake. |
| `meta.resourceType` | N/A | string | The type of resource for the user. You should use `user` as a value for this attribute. |
| `schemas` | N/A | string | A comma-separated array of strings specifying the namespace URIs. Snowflake supports the following values:   - `urn:ietf:params:scim:schemas:core:2.0:User` - `urn:ietf:params:scim:schemas:extension:enterprise:2.0:User` - `urn:ietf:params:scim:schemas:extension:2.0:User` |

Expand

Show lessSee more

## Custom attributes

You can set custom attributes that are not defined by [RFC 7643](https://datatracker.ietf.org/doc/html/rfc7643), such as
`defaultRole`.

You can use the following namespaces to set custom attributes when making POST, PUT, and PATCH requests:

`urn:ietf:params:scim:schemas:extension:enterprise:2.0:User`
:   This namespace was part of the original SCIM implementation in Snowflake. Use this namespace for [Okta SCIM security integrations](/user-guide/scim-okta).

    For [Microsoft Azure SCIM security integrations](/user-guide/scim-azure) or [custom SCIM integrations](/user-guide/scim-custom), use `urn:ietf:params:scim:schemas:extension:2.0:User` instead.

`urn:ietf:params:scim:schemas:extension:2.0:User`
:   Use this namespace for [Microsoft Azure SCIM security integrations](/user-guide/scim-azure) or
    [custom SCIM integrations](/user-guide/scim-custom).

    For [Okta SCIM security integrations](/user-guide/scim-okta), use `urn:ietf:params:scim:schemas:extension:enterprise:2.0:User` instead.

Snowflake supports the following custom attributes:

| SCIM User Custom Attribute | Snowflake User Attribute | Type | Description |
| --- | --- | --- | --- |
| `allowedInterfaces` | `ALLOWED_INTERFACES` | string | Defines which Snowflake interfaces the user can access. Specified as a comma-delimited list of interfaces. For a list of possible interfaces, see [CREATE USER](/sql-reference/sql/create-user#label-create-user-allowed-interfaces). If a value other than `ALL` is specified, then users can only access the interface specified and can’t interact with any Snowflake data outside of the interface specified. |
| `defaultWarehouse` | `DEFAULT_WAREHOUSE` | string | The virtual warehouse that is active by default for the user’s session upon login. |
| `defaultRole` | `DEFAULT_ROLE` | string | The primary role that is active by default for the user’s session upon login. |
| `defaultSecondaryRoles` | `DEFAULT_SECONDARY_ROLES` | string | The list of secondary roles that are active for the user’s session upon login. You can set this attribute to `ALL` as an alias for `('ALL')`, or you can set this attribute to `NONE` or `""` as an alias for `()`. |
| `type` | `TYPE` | string | The type of user. Default: `person`. You can set this attribute to `person`, `service`, `service_agent`, `legacy_service`, or `null`. For more information about types of users, see [Types of users](/user-guide/admin-user-management#label-user-management-types). |
| `snowflakeTags` | `SNOWFLAKE_TAGS` | array of string | Assign or update [tag values](/user-guide/object-tagging/introduction) associated with a user. Each element is a tag assignment in the format `{database name}.{schema name}.{tag name}:{tag value}`. These tags must already exist in the account and the integration must be properly provisioned. Each element must point to a different tag. Here is an example of assigning values to two tags:  `["cost_management.tags.cost_center:finance", "cost_management.tags.type:PowerUser"]` |

Expand

Show lessSee more

### Usage notes for TYPE attribute

Note

The LEGACY\_SERVICE type is being deprecated. Use the SERVICE type for services and applications. For a timeline of the deprecation of
LEGACY\_SERVICE, see [Planning for the deprecation of single-factor password sign-ins](/user-guide/security-mfa-rollout).

This list describes the effects of setting the TYPE attribute in the following SCIM requests:

- `POST` request to create a user, and the `type` attribute is unspecified or `NULL`, the `TYPE` property is set to
  `PERSON`.
- `PATCH` request with a replace operation that specifies the `type` attribute as `NULL`, `TYPE` property doesn’t
  change.
- `PUT` request with a replace operation, and the `type` attribute is unspecified or `NULL`, the `TYPE` property is set to
  `PERSON`.
- `PATCH` request with a remove operation that unsets the `type` attribute, the `TYPE` property doesn’t change.

## Check if a user exists

Method and endpoint:
:   `GET /scim/v2/Users?filter=userName eq "{{user_name}}"`

Description:
:   Returns details about a user associated with the `userName` query parameter.

    If the `MONITOR USER` privilege is granted to the [SCIM provisioner](/user-guide/scim-okta), then the SCIM provisioner can see
    all users in the Snowflake account, instead of only seeing users owned by the SCIM provisioner.

    For example, to grant the `MONITOR USER` privilege to a SCIM provisioner, you can use the GRANT command:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;
    GRANT MONITOR USER ON ACCOUNT TO ROLE example_okta_provisioner_role;
    ```

    Returns the HTTP response status code `200` if the HTTP request successfully completed.

## Get details about a user

Method and endpoint:
:   `GET /scim/v2/Users/{{user_id}}`

Description:
:   Returns details about a user associated with the `user_id` path parameter.

    Returns the HTTP response status code `200` if the HTTP request successfully completed.

## List users

Method and endpoint:
:   `GET /scim/v2/Users`

Description:
:   Returns a paginated list of users in the account, optionally matching a filter.

    If the `MONITOR USER` privilege is granted to the [SCIM provisioner](/user-guide/scim-okta), then the SCIM provisioner can see
    all users in the Snowflake account, instead of only seeing users owned by the SCIM provisioner.

    For example, to grant the `MONITOR USER` privilege to a SCIM provisioner, you can use the GRANT command:

    Copy code

    ```
    USE ROLE ACCOUNTADMIN;
    GRANT MONITOR USER ON ACCOUNT TO ROLE example_okta_provisioner_role;
    ```

    Returns the HTTP response status code `200` if the HTTP request successfully completed.

    Note

    This endpoint’s behavior is controlled by the 2026\_03 behavior change bundle. For rollout details, see
    [SCIM: List API returns paginated results; unsupported filters rejected](/release-notes/bcr-bundles/2026_03/bcr-2276).

Optional query parameters:
:   `filter=userName { eq | sw } "{name}"`

    > eq:
    > :   Searches for a user with a Snowflake `LOGIN_NAME` that matches `name`. The search is case-insensitive.
    >
    >     Pagination query parameters, such as `startIndex` and `count`, are ignored when using `eq`.
    >
    >     **Example**: the following request finds a user with `LOGIN_NAME` equal to `ABC`:
    >
    >     Copy code
    >
    >     ```
    >     GET /scim/v2/Users?filter=userName eq "abc"
    >     ```
    >
    > sw:
    > :   Searches for users with a Snowflake `LOGIN_NAME` that starts with the value provided for `name`. The search is case-insensitive.
    >
    >     **Example**: the following request matches users with a `LOGIN_NAME` that starts with `AL`, such as `ALBERT` or `ALICE`:
    >
    >     Copy code
    >
    >     ```
    >     GET /scim/v2/Users?filter=userName sw "al"
    >     ```

    `startIndex`

    > The 1-based index of the first result to return. Values less than 1 are treated as 1.
    > Non-numeric values return HTTP `400`.
    >
    > Default: `1`.
    >
    > **Example**: the following request returns a list of users, skipping the first user:
    >
    > Copy code
    >
    > ```
    > GET /scim/v2/Users?startIndex=2
    > ```

    `count`

    > The maximum number of users returned per page. Negative values are treated as 0 (returns an empty
    > `Resources` array). Values above 1000 are treated as 1000. Non-numeric values return HTTP `400`.
    >
    > Default: `100`.
    >
    > Max: `1000`.
    >
    > **Example**: the following request returns a list of users, skipping the first user, with a maximum of 10 users per page:
    >
    > Copy code
    >
    > ```
    > GET /scim/v2/Users?startIndex=2&count=10
    > ```

    `excludedAttributes`

    > Excludes the specified attributes from the response. Only `groups` is supported, which omits the list
    > of roles that each user belongs to. Other values are ignored.
    >
    > **Example**: the following request returns the first page of users without their groups returned:
    >
    > Copy code
    >
    > ```
    > GET /scim/v2/Users?excludedAttributes=groups
    > ```

    Note

    For accounts with large numbers of users, specifying `excludedAttributes` can significantly reduce response
    size and latency.

Limitations:
:   - Only the `userName` attribute is supported for filtering. Filtering on other attributes (for example,
      `externalId`) returns an empty result set.
    - Only the `eq` and `sw` operators are supported. Using an unsupported operator returns HTTP `400` with
      SCIM error type `invalidFilter`.
    - Compound filters using logical operators (`and`, `or`) are not supported and return HTTP `400` with
      SCIM error type `invalidFilter`.

Response body objects:
:   `itemsPerPage` equals the `count` value used for the query.

    `totalResults` equals `startIndex` + `count` when more pages are available, or the total number of
    matching items when no more pages are available.

    Clients should check that the sum of `startIndex` and `itemsPerPage` is less than or equal to `totalCount`.

    Clients should continue making requests until the sum of `startIndex` and `itemsPerPage` is greater than `totalCount`.

    See the following user attributes references:

    - [User attributes](#label-scim-intro-user-attributes)
    - [Custom attributes](#label-scim-custom-attributes)

Examples:
:   An example response that returns a paginated list of users, excluding their `groups` attribute from the results:

    Copy code

    ```
    {
        "schemas": [
            "urn:ietf:params:scim:api:messages:2.0:ListResponse"
        ],
        "Resources": [
            {
                "schemas": [
                    "urn:ietf:params:scim:schemas:core:2.0:User",
                    "urn:ietf:params:scim:schemas:extension:2.0:User",
                    "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
                ],
                "id": "32_1",
                "meta": {
                    "resourceType": "User",
                    "created": "2024-08-01T18:20:29Z",
                    "lastModified": "2024-08-01T18:20:29Z"
                },
                "userName": "SHERRY_J",
                "displayName": "sherry_j",
                "name": {
                    "givenName": "sherry_j",
                    "familyName": "xyz"
                },
                "emails": [
                    {
                        "primary": true,
                        "value": "sherry_j.xyz@example.com"
                    }
                ],
                "active": true
            },
            {
                "schemas": [
                    "urn:ietf:params:scim:schemas:core:2.0:User",
                    "urn:ietf:params:scim:schemas:extension:2.0:User",
                    "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
                ],
                "id": "61_1",
                "meta": {
                    "resourceType": "User",
                    "created": "2024-08-02T18:20:29Z",
                    "lastModified": "2024-08-02T18:20:29Z"
                },
                "userName": "ALICE_ADMIN",
                "displayName": "alice_admin",
                "name": {
                    "givenName": "alice_admin",
                    "familyName": "xyz"
                },
                "emails": [
                    {
                        "primary": true,
                        "value": "alice_admin.xyz@example.com"
                    }
                ],
                "active": true
            }
        ],
        "totalResults": 2,
        "startIndex": 1,
        "itemsPerPage": 100
    }
    ```

## Create a user

Method and endpoint:
:   `POST /scim/v2/Users`

Description:
:   Creates a user in Snowflake.

    Returns the HTTP response status code `201` if the HTTP request successfully completed.

    If the user already exists or the HTTP request failed for a different reason, then Snowflake returns the HTTP response status code
    `409`.

Examples:
:   Create a user with `userName` and `loginName` mapped to the same value:

    Copy code

    ```
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:2.0:User"
      ],
      "userName": "test_user_1",
      "password": "test",
      "name": {
        "givenName": "test",
        "familyName": "user"
      },
      "emails": [
        {"value": "test.user@example.com"}
      ],
      "displayName": "test user",
      "active": true
    }
    ```

    Create a user with `userName` and `loginName` mapped to different values:

    Note

    This example requires the [MAP\_SCIM\_USERNAME\_TO\_ENTERPRISE\_ATTR](/sql-reference/parameters#label-map-scim-username-to-enterprise-attr) account
    parameter to be set to `TRUE`. Both the `userName` attribute and the `snowflakeUserName` enterprise extension
    attribute must be specified.

    If you use Okta as your identity provider, see the [Okta procedure](/user-guide/scim-okta#label-okta-separate-attributes) for additional IdP configuration steps.

    Copy code

    ```
    {
      "active": true,
      "displayName": "test user",
      "emails": [
        {"value": "test.user@example.com"}
      ],
      "name": {
        "familyName": "test_last_name",
        "givenName": "test_first_name"
      },
      "password": "test_password",
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
      ],
      "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
        "snowflakeUserName": "TEST_USER"
      },
      "userName": "test.user@example.com"
    }
    ```

    Create a user and assign two tags: `cost_center = finance` and `type = PowerUser`:

    Copy code

    ```
    {
      "active": true,
      "displayName": "test user",
      "emails": [
        {"value": "test.user@snowflake.com"}
      ],
      "name": {
        "familyName": "test_last_name",
        "givenName": "test_first_name"
      },
      "password": "test_password",
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
      ],
      "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
        "snowflakeUserName": "USER5",
        "snowflakeTags": ["cost_management.tags.cost_center:finance", "cost_management.tags.type:PowerUser"]
      },
      "userName": "USER5"
    }
    ```

## Replace user attributes

Method and endpoint:
:   `PATCH /scim/v2/Users/{{id}}`

Description:
:   Replaces attributes of the user associated with the `id` path parameter.

    You must set `op` to `replace` to perform this HTTP request.

    `active` allows the following values:

    - `false`: deactivates the user.
    - `true`: activates the user.

    Returns the HTTP response status code `200` if the HTTP request was successfully completed.

    If unsuccessful, returns the HTTP response code `204`.

Examples:
:   Deactivate a user and update their `givenName` to `deactivated_user`:

    Copy code

    ```
    {
      "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
      "Operations": [
        {"op": "replace", "value": { "active": false }},
        {"op": "replace", "value": { "givenName": "deactivated_user" }}
      ]
    }
    ```

    Update a user with `userName` and `loginName` mapped to the same value:

    Copy code

    ```
    {
      "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"],
      "Operations": [
        {"op": "replace", "value": { "active": false }}
      ]
    }
    ```

    Update a user with `userName` and `loginName` mapped to different values.
    This requires the [MAP\_SCIM\_USERNAME\_TO\_ENTERPRISE\_ATTR](/sql-reference/parameters#label-map-scim-username-to-enterprise-attr) account parameter
    to be set to `TRUE`. If you use Okta as your identity provider, see the [Okta procedure](/user-guide/scim-okta#label-okta-separate-attributes)
    for additional IdP configuration steps.

    Copy code

    ```
    {
      "Operations": [
        {
          "op": "replace",
          "path": "userName",
          "value": "test_updated_name"
        },
        {
          "op": "replace",
          "path": "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User.snowflakeUserName",
          "value": "USER5"
        }
      ],
      "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"]
    }
    ```

    Update tag values assigned to a user:

    Copy code

    ```
    {
      "Operations": [
        {
          "op": "replace",
          "path": "userName",
          "value": "test_updated_name"
        },
        {
          "op": "replace",
          "path": "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User.snowflakeTags",
          "value": ["cost_management.tags.cost_center:finance", "cost_management.tags.type:PowerUser"]
        }
      ],
      "schemas": ["urn:ietf:params:scim:api:messages:2.0:PatchOp"]
    }
    ```

## Update a user

Method and endpoint:
:   `PUT /scim/v2/Users/{{id}}`

Description:
:   Updates the attributes of the user associated with the `id` path parameter.

    If unsuccessful, returns the HTTP response code `400`. The HTTP request is unsuccessful if the request tries to change immutable
    attributes or if the attributes being changed do not exist in Snowflake.

Examples:
:   Update a user and their `"defaultRole"`, `"defaultSecondaryRoles"`, and `"defaultWarehouse"` attributes.

    To specify the `"defaultRole"`, `"defaultSecondaryRoles"`, and `"defaultWarehouse"` attributes, you must use one of the
    `extension` [schemas](#label-scim-intro-user-attributes). The `defaultSecondaryRoles` attribute only accepts `"ALL"` as
    a value.

    Note

    The PUT method is more expensive than the PATCH method. Use the PATCH operation instead.

    Copy code

    ```
    {
      "schemas": [
       "urn:ietf:params:scim:schemas:core:2.0:User",
       "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
      ],
      "userName": "test_user_1",
      "password": "test",
      "name": {
        "givenName": "test",
        "familyName": "user"
      },
      "emails": [{
        "primary": true,
        "value": "test.user@example.com",
        "type": "work"
      }
      ],
      "displayName": "test user",
      "active": true,
      "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
        "defaultRole" : "test_role",
        "defaultSecondaryRoles" : "ALL",
        "defaultWarehouse" : "test_warehouse"
      }
    }
    ```

    Update a user and their tag values. Omitting a tag value or omitting the tag entirely from the request will remove the tag from the user.

    Copy code

    ```
    {
      "schemas": [
       "urn:ietf:params:scim:schemas:core:2.0:User",
       "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
      ],
      "userName": "test_user_1",
      "password": "test",
      "name": {
        "givenName": "test",
        "familyName": "user"
      },
      "emails": [{
        "primary": true,
        "value": "test.user@snowflake.com",
        "type": "work"
      }
      ],
      "displayName": "test user",
      "active": true,
      "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
        "defaultRole" : "test_role",
        "defaultSecondaryRoles" : "ALL",
        "defaultWarehouse" : "test_warehouse",
        "snowflakeTags": ["cost_management.tags.cost_center:finance", "cost_management.tags.type:PowerUser"]
      }
    }
    ```

    Update a user with `userName` and `loginName` mapped to different values.
    This requires the [MAP\_SCIM\_USERNAME\_TO\_ENTERPRISE\_ATTR](/sql-reference/parameters#label-map-scim-username-to-enterprise-attr) account parameter
    to be set to `TRUE`. If you use Okta as your identity provider, see the [Okta procedure](/user-guide/scim-okta#label-okta-separate-attributes)
    for additional IdP configuration steps.

    Copy code

    ```
    {
      "schemas": [
        "urn:ietf:params:scim:schemas:core:2.0:User",
        "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User"
      ],
      "userName": "test.user@example.com",
      "password": "test_password",
      "name": {
        "givenName": "test_first_name",
        "familyName": "test_last_name"
      },
      "emails": [
        {"value": "test.user@example.com"}
      ],
      "displayName": "test user",
      "active": true,
      "urn:ietf:params:scim:schemas:extension:enterprise:2.0:User": {
        "snowflakeUserName": "TEST_USER"
      }
    }
    ```

## Delete a user

Method and endpoint:
:   `DELETE /scim/v2/Users/{{id}}`

Description:
:   Deletes the user associated with the `id` path parameter.
