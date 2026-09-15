# ALTER SECURITY INTEGRATION (SCIM)

Modifies the properties of an existing SCIM security integration. For information about modifying other types of
security integrations (e.g. SAML2), see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration).

See also:
:   [CREATE SECURITY INTEGRATION (SCIM)](/sql-reference/sql/create-security-integration-scim) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)

## Syntax

Copy code

```
ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> SET
    [ ENABLED = { TRUE | FALSE } ]
    [ NETWORK_POLICY = '<network_policy>' ]
    [ REJECT_TOKENS_ISSUED_BEFORE = '<datetime_string>' ]
    [ SYNC_PASSWORD = { TRUE | FALSE } ]
    [ COMMENT = '<string_literal>' ]

ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name>  UNSET {
                                                            NETWORK_POLICY |
                                                            [ , ... ]
                                                            }
ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>'
    [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   Identifier for the integration to alter. If the identifier contains spaces or special characters, the entire string must be enclosed in
    double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies one or more properties/parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `ENABLED = TRUE | FALSE`
    :   Specifies whether the security integration is enabled. To disable the integration, set `ENABLED = FALSE`.

    `NETWORK_POLICY = 'network_policy'`
    :   Specifies an existing [network policy](/user-guide/network-policies) that controls SCIM network traffic.

        If there are also network policies set for the account or user, see [Network policy precedence](/user-guide/network-policies#label-network-policy-precedence).

    `REJECT_TOKENS_ISSUED_BEFORE = 'datetime_string'`
    :   If this parameter is set, tokens issued before the date specified are rejected. This can mitigate security risks associated with long-lived or
        potentially compromised tokens. When this parameter is unset or not specified, tokens have no expiration date, and tokens that were previously rejected because of this
        mechanism will be considered valid. Tokens issued before this date that have already been approved are not invalidated, but new
        requests to validate tokens issued before this date will fail.

        This parameter cannot be assigned in the CREATE SECURITY INTEGRATION statement; it can be added only after the integration is created.

        The format is any [valid Snowflake timestamp format](/sql-reference/date-time-input-output#label-date-time-input-output-timestamp-formats), with an optional time zone. If the
        time zone is not provided, it is inferred from the current user settings. For example:

        - ‘Tue, 30 Sep 2025 12:30:00 -0700’
        - ‘Tue, 30 Sep 2025 12:30:00’
        - ’2025-09-30 12:30:00’

        Default: No earliest issue date.

    `SYNC_PASSWORD = TRUE | FALSE`
    :   Specifies whether to enable or disable the synchronization of a user password from an Okta SCIM client as part of the API request to
        Snowflake.

        - `TRUE` enables password synchronization.
        - `FALSE` disables password synchronization.

        Default `FALSE`. If a security integration is created without setting this parameter, Snowflake sets this parameter to `FALSE`.

        If user passwords should not be synchronized from the client to Snowflake, ensure this property value is set to `FALSE` and
        disable password synchronization in the Okta client.

        Note that this property is only supported for Okta SCIM integrations. Microsoft Entra ID SCIM integrations are not supported because
        Microsoft Entra ID does not support password synchronization. To request support, please contact Microsoft.

        For details, see [Snowflake SCIM support](/user-guide/scim-intro).

    `COMMENT`
    :   String (literal) that specifies a comment for the integration.

        Default: No value

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the security integration, which resets them back to their defaults:

    - `NETWORK_POLICY`
    - `REJECT_TOKENS_ISSUED_BEFORE`
    - `SYNC_PASSWORD`
    - `COMMENT`
    - `TAG tag_name [ , tag_name ... ]`

## Usage notes

Regarding metadata:

> Attention
>
> Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example initiates operation of a suspended integration:

Copy code

```
ALTER SECURITY INTEGRATION myint SET ENABLED = TRUE;
```

The following code adds a token age limit to the SCIM integration; tokens issued before noon on September 30, 2025, are considered invalid.

Copy code

```
ALTER SECURITY INTEGRATION 'example_integration'
  SET REJECT_TOKENS_ISSUED_BEFORE = '2025-09-30 12:00:00';
```
