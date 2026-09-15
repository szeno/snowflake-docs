# CREATE SECURITY INTEGRATION (SCIM)

Attention

Mentions of Microsoft Azure Active Directory refer to Microsoft Entra ID.

Creates a new SCIM security integration in the account or replaces an existing integration. A SCIM security integration allows the
automated management of user identities and groups (i.e. roles) by creating an interface between Snowflake and a third-party Identity
Provider (IdP).

For information about creating other types of security integrations (e.g. SAML2), see [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration).

See also:
:   [ALTER SECURITY INTEGRATION (SCIM)](/sql-reference/sql/alter-security-integration-scim) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] SECURITY INTEGRATION [ IF NOT EXISTS ]
    <name>
    TYPE = SCIM
    ENABLED = { TRUE | FALSE }
    SCIM_CLIENT = { 'OKTA' | 'AZURE' | 'GENERIC' }
    RUN_AS_ROLE = { 'OKTA_PROVISIONER' | 'AAD_PROVISIONER' | 'GENERIC_SCIM_PROVISIONER' | '<custom_role>' }
    [ NETWORK_POLICY = '<network_policy>' ]
    [ SYNC_PASSWORD = { TRUE | FALSE } ]
    [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the integration; must be unique in your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

`TYPE = SCIM`
:   Specify the type of integration:

    - `SCIM`: Creates a security interface between Snowflake and a client that supports SCIM.

`ENABLED = { TRUE | FALSE }`
:   Specify whether the security integration is enabled. To create a security integration that is disabled, set `ENABLED = FALSE`.

    A SCIM security integration cannot be disabled. If you execute a `SHOW SECURITY INTEGRATIONS` command, the value of the `enabled`
    property might be `false`, but this property of the SCIM integration has no effect on functionality at this time.

    The value is case-insensitive.

    Default: `TRUE`

`SCIM_CLIENT = { 'OKTA' | 'AZURE' | 'GENERIC' }`
:   Specify the SCIM client.

`RUN_AS_ROLE = { 'OKTA_PROVISIONER' | 'AAD_PROVISIONER' | 'GENERIC_SCIM_PROVISIONER' | 'custom_role' }`
:   Specify the SCIM role in Snowflake that owns any users and roles that are imported from the identity provider into Snowflake using SCIM.

    The values `OKTA_PROVISIONER`, `AAD_PROVISIONER`, and `GENERIC_SCIM_PROVISIONER` are case-sensitive and must
    always be capitalized. You can also specify a custom role.

## Optional parameters

`NETWORK_POLICY = 'network_policy'`
:   Specifies an existing [network policy](/user-guide/network-policies) that controls SCIM network traffic.

    If there are also network policies set for the account or user, see [Network policy precedence](/user-guide/network-policies#label-network-policy-precedence).

`SYNC_PASSWORD = { TRUE | FALSE }`
:   Specifies whether to enable or disable the synchronization of a user password from an Okta SCIM client as part of the API request to
    Snowflake.

    - `TRUE` enables password synchronization.
    - `FALSE` disables password synchronization.

    Default `FALSE`. If a security integration is created without setting this parameter, Snowflake sets this parameter to `FALSE`.

    If user passwords should not be synchronized from the client to Snowflake, ensure this property value is set to `FALSE` and
    disable password synchronization in the client.

    Note that this property is supported for Okta and Custom SCIM integrations. Microsoft Entra ID SCIM integrations are not supported because
    Microsoft Entra ID does not support password synchronization. To request support, please contact Microsoft.

    For more information, see [Snowflake SCIM support](/user-guide/scim-intro).

`COMMENT = 'string_literal'`
:   Specifies a comment for the integration.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INTEGRATION | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

### Microsoft Entra ID example

The following example creates a Microsoft Entra ID SCIM integration with the default settings:

Copy code

```
CREATE OR REPLACE SECURITY INTEGRATION aad_provisioning
    TYPE = scim
    SCIM_CLIENT = 'AZURE'
    RUN_AS_ROLE = 'AAD_PROVISIONER';
```

View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

Copy code

```
DESC SECURITY INTEGRATION aad_provisioning;
```

The output includes a `SCIM_ENDPOINT_ID` property, which is the UUID used in SCIM API request URLs.
For more information, see [Send SCIM requests](/user-guide/scim-authentication#label-scim-auth-send-requests).

### Okta example

The following example creates an Okta SCIM integration with the default settings:

Copy code

```
CREATE OR REPLACE SECURITY INTEGRATION okta_provisioning
    TYPE = scim
    SCIM_CLIENT = 'OKTA'
    RUN_AS_ROLE = 'OKTA_PROVISIONER';
```

View the integration settings using [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration):

> Copy code
>
> ```
> DESC SECURITY INTEGRATION okta_provisioning;
> ```

The output includes a `SCIM_ENDPOINT_ID` property, which is the UUID used in SCIM API request URLs.
For more information, see [Send SCIM requests](/user-guide/scim-authentication#label-scim-auth-send-requests).
