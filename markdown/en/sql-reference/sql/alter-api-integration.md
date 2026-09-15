# ALTER API INTEGRATION

Modifies the properties of an existing API integration.

See also:
:   [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) ,
    [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

Copy code

```
ALTER [ API ] INTEGRATION [ IF EXISTS ] <name> SET
  [ API_AWS_ROLE_ARN = '<iam_role>' ]
  [ AZURE_AD_APPLICATION_ID = '<azure_application_id>' ]
  [ API_KEY = '<api_key>' ]
  [ ENABLED = { TRUE | FALSE } ]
  [ API_ALLOWED_PREFIXES = ('<...>') ]
  [ API_BLOCKED_PREFIXES = ('<...>') ]
  [ ALLOWED_AUTHENTICATION_SECRETS = ( { <secret_name> [, <secret_name>, ... ] } ) | all | none ]
  [ COMMENT = '<string_literal>' ]

ALTER [ API ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ API ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER [ API ] INTEGRATION [ IF EXISTS ] <name>  UNSET {
                                                      API_KEY              |
                                                      ENABLED              |
                                                      API_BLOCKED_PREFIXES |
                                                      COMMENT
                                                      }
                                                      [ , ... ]
```

## Parameters

`name`
:   The identifier of the integration to alter. If the identifier contains spaces or special characters, the entire
    string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`SET ...`
:   Specifies one or more properties/parameters to set for API integration (separated by blank spaces, commas, or new lines):

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether to initiate operation of the integration or suspend it.

        - `TRUE` allows the integration to run.
        - `FALSE` suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

    `ALLOWED_AUTHENTICATION_SECRETS = { <secret_name> [, <secret_name> ... ] | all | none }`
    :   Specifies the secrets that UDF or procedure handler code can use when accessing the Git repository at the API\_ALLOWED\_PREFIXES value. You
        specify a secret from this list when specifying Git credentials with the [GIT\_CREDENTIALS parameter](/sql-reference/sql/create-git-repository#label-create-git-repository-optional-parameters).

        This parameter’s value must be one of the following:

        - One or more fully-qualified Snowflake secret names to allow any of the listed secrets.
        - (Default) `all` to allow any secret.
        - `none` to allow no secrets.

        For reference information about secrets, refer to [CREATE SECRET](/sql-reference/sql/create-secret).

    `API_AWS_ROLE_ARN = '<iam_role>'`
    :   The `iam_role` is the ARN (Amazon resource name) of a cloud platform role.

        This parameter applies only if the API\_PROVIDER is set to `aws_api_gateway`.

    `AZURE_AD_APPLICATION_ID = '<azure_application_id>'`
    :   The “Application (client) id” of the Azure AD (Active Directory) app for your remote service.

        This parameter applies only if the API\_PROVIDER is set to `azure_api_management`.

    `API_KEY = '<api_key>'`
    :   The [API key](/sql-reference/external-functions-security#label-external-functions-api-key) (also called a “subscription key”).

    `API_ALLOWED_PREFIXES = ('<...>')`
    :   Explicitly limits external functions that use the integration to reference one or more HTTPS proxy
        service endpoints (e.g. Amazon AWS API Gateway) and resources within those proxies. Supports a comma-separated
        list of URLs, which are treated as prefixes (for details, see below).

        Each URL in `API_ALLOWED_PREFIXES = (...)` is treated as a prefix. For example, if you specify:

        `https://xyz.amazonaws.com/production/`

        that means all resources under

        `https://xyz.amazonaws.com/production/`

        are allowed. For example the following is allowed:

        `https://xyz.amazonaws.com/production/ml1`

        To maximize security, you should restrict allowed locations as narrowly as practical.

    `API_BLOCKED_PREFIXES = ('<...>')`
    :   Lists the endpoints and resources in the HTTPS proxy service that are not allowed to be called from Snowflake.

        The possible values for locations follow the same rules as for `API_ALLOWED_PREFIXES` above.

        API\_BLOCKED\_PREFIXES takes precedence over API\_ALLOWED\_PREFIXES. If a prefix matches both, then it is blocked.
        In other words, Snowflake allows all values that match API\_ALLOWED\_PREFIXES except values that also
        match API\_BLOCKED\_PREFIXES.

        If a value is outside API\_ALLOWED\_PREFIXES, you do not need to explicitly block it.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    > String (literal) that specifies a comment for the integration.

`UNSET ...`
:   Specifies one or more properties/parameters to unset for the API integration, which resets them back to their defaults:

    - `ENABLED`
    - `API_BLOCKED_PREFIXES`
    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

## Usage notes

- The API\_PROVIDER cannot be changed.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

The following example initiates operation of a suspended integration:

Copy code

```
ALTER API INTEGRATION myint SET ENABLED = TRUE;
```
