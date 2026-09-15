# DROP CLASSIFICATION\_PROFILE

*Fully qualified name:* SNOWFLAKE.DATA\_PRIVACY.CLASSIFICATION\_PROFILE

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Drops a classification profile instance in the current or specified schema.

## Syntax

Copy code

```
DROP SNOWFLAKE.DATA_PRIVACY.CLASSIFICATION_PROFILE
  [ IF EXISTS ] <classification_profile_name>
```

## Parameters

`classification_profile_name`
:   Specifies the identifier of the instance of the CLASSIFICATION\_PROFILE class.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| OWNERSHIP | SNOWFLAKE.DATA\_PRIVACY.CLASSIFICATION\_PROFILE instance |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Dropped instances cannot be recovered; they must be recreated.

## Examples

Drop the classification profile instance:

Copy code

```
DROP SNOWFLAKE.DATA_PRIVACY.CLASSIFICATION_PROFILE my_classification_profile;
```
