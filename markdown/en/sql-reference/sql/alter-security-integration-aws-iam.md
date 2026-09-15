# ALTER SECURITY INTEGRATION (AWS IAM Authentication)

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Modifies the properties of an existing security integration created for authenticating with AWS IAM.

For information about modifying other types of security integrations (such as Snowflake OAuth), see [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration).

See also:
:   [CREATE SECURITY INTEGRATION (AWS IAM Authentication)](/sql-reference/sql/create-security-integration-aws-iam) , [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration) , [DROP INTEGRATION](/sql-reference/sql/drop-integration) , [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

## Syntax

Copy code

```
ALTER [ SECURITY ] INTEGRATION [ IF EXISTS ] <name> SET
  [ TYPE = AWS_IAM ]
  [ AWS_ROLE_ARN = '<iam_role_arn>' ]
  [ ENABLED = { TRUE | FALSE } ]
  [ COMMENT = '<string_literal>' ]

ALTER [ SECURITY ] INTEGRATION <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER [ SECURITY ] INTEGRATION <name> UNSET TAG <tag_name> [ , <tag_name> ... ]
```

## Parameters

`name`
:   String that specifies the identifier (such as the name) for the integration.

`SET ...`
:   Specifies one or more properties/parameters to set for the integration (separated by blank spaces, commas, or new lines):

    `TYPE = AWS_IAM`
    :   Specifies that the integration uses AWS IAM to authenticate to the external service.

    `ENABLED = { TRUE | FALSE }`
    :   Specifies whether to enable or disable this security integration.

        `TRUE`
        :   Allows the integration to run based on the parameters specified in the integration definition.

        `FALSE`
        :   Suspends the integration for maintenance. Any integration between Snowflake and a third-party service fails to work.

`AWS_ROLE_ARN = 'iam_role_arn'`
:   Specifies the Amazon Resource Name (ARN) of the AWS identity and access management (IAM) role that grants privileges for AWS resources.

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

The following example initiates operation of a suspended integration:

> Copy code
>
> ```
> ALTER SECURITY INTEGRATION myint SET ENABLED = TRUE;
> ```
