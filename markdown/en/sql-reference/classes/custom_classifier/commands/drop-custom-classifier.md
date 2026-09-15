# DROP CUSTOM\_CLASSIFIER

*Fully qualified name:* SNOWFLAKE.DATA\_PRIVACY.CUSTOM\_CLASSIFIER

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Drops a custom classification instance in the current or specified schema.

See also:
:   [Using custom classifiers to implement custom semantic categories](/user-guide/classify-custom-using)

## Syntax

Copy code

```
DROP SNOWFLAKE.DATA_PRIVACY.CUSTOM_CLASSIFIER
[ IF EXISTS ] <custom_classifier_name>
```

## Parameters

`custom_classifier_name`
:   Specifies the identifier (name) for the instance.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Arguments

None.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object |
| --- | --- |
| OWNERSHIP | SNOWFLAKE.DATA\_PRIVACY.CUSTOM\_CLASSIFIER instance |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Dropped instances cannot be recovered; they must be recreated.

## Examples

Copy code

```
DROP SNOWFLAKE.DATA_PRIVACY.CUSTOM_CLASSIFIER data.classifiers.internal_ids;
```
