# ALTER EXTERNAL ACCESS INTEGRATION

Modifies the properties of an existing [external access integration](/developer-guide/external-network-access/creating-using-external-network-access).

See also:
:   [CREATE EXTERNAL ACCESS INTEGRATION](/sql-reference/sql/create-external-access-integration), [DROP INTEGRATION](/sql-reference/sql/drop-integration),
    [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations), [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
ALTER EXTERNAL ACCESS INTEGRATION [ IF EXISTS ] <name> SET
  [ ALLOWED_NETWORK_RULES = (<rule_name> [ , <rule_name> ... ]) ]
  [ ALLOWED_API_AUTHENTICATION_INTEGRATIONS = { ( <integration_name_1> [, <integration_name_2>, ... ] ) | none } ]
  [ ALLOWED_AUTHENTICATION_SECRETS = { ( <secret_name> [ , <secret_name> ... ] ) | all | none } ]
  [ ENABLED = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]
  [ TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ] ]

ALTER EXTERNAL ACCESS INTEGRATION [ IF EXISTS ] <name> UNSET {
  ALLOWED_NETWORK_RULES |
  ALLOWED_API_AUTHENTICATION_INTEGRATIONS |
  ALLOWED_AUTHENTICATION_SECRETS |
  COMMENT |
  TAG <tag_name> }
  [ , ... ]
```

## Parameters

`name`
:   Identifier for the external access integration to alter. If the identifier contains spaces or special characters, the entire string
    must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies the properties to set for the integration:

    `ALLOWED_NETWORK_RULES = (rule_name [ , rule_name ... ])`
    :   Specifies the allowed network rules. Only egress rules may be specified.

        For reference information about network rules, refer to [CREATE NETWORK RULE](/sql-reference/sql/create-network-rule).

    `ALLOWED_API_AUTHENTICATION_INTEGRATIONS = ( integration_name_1 [, integration_name_2, ... ] ) | none`
    :   Specifies the security integrations whose OAuth authorization server issued the secret used by the UDF or procedure. The security
        integration must be the type used for external API integration.

        For reference information about security integrations, refer to [CREATE SECURITY INTEGRATION (External API Authentication)](/sql-reference/sql/create-security-integration-api-auth).

    `ALLOWED_AUTHENTICATION_SECRETS = ( secret_name [ , secret_name ... ] ) | all | none`
    :   Specifies the secrets that a UDF or procedure can use when referring to this integration.

        For reference information about secrets, refer to [CREATE SECRET](/sql-reference/sql/create-secret).

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether this integration is enabled or disabled. If the integration is disabled, any handler code that relies
        on it will be unable to reach the external endpoint.

        The value is case-insensitive.

        The default is `TRUE`.

    `COMMENT = 'string_literal'`
    :   Specifies a comment for the external access integration.

        Default: No value

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies the property to unset for the integration, which resets it to the default:

    - `ALLOWED_NETWORK_RULES`
    - `ALLOWED_API_AUTHENTICATION_INTEGRATIONS`
    - `ALLOWED_AUTHENTICATION_SECRETS`
    - `COMMENT`
    - `TAG tag_name`

    You can reset multiple properties/parameters with a single ALTER statement; however, each property/parameter must be separated by a
    comma. When resetting a property/parameter, specify only the name; specifying a value for the property will return an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Integration | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Set the allowed secrets to the `my_new_secret` secret:

Copy code

```
ALTER EXTERNAL ACCESS INTEGRATION IF EXISTS dev_integration
  SET ALLOWED_AUTHENTICATION_SECRETS = (my_new_secret);
```

Disable the integration `dev_integration_disabled`:

Copy code

```
ALTER EXTERNAL ACCESS INTEGRATION IF EXISTS dev_integration_disabled
  SET ENABLED = FALSE;

ALTER EXTERNAL ACCESS INTEGRATION IF EXISTS dev_integration_disabled
  SET COMMENT = 'Disabled until the end of the Q1.';
```
