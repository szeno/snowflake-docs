# <classification\_profile\_name>!SET\_ENABLE\_TAG\_BASED\_SENSITIVE\_DATA\_EXCLUSION

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Enables or disables the ability to exclude certain data from sensitive data classification. When enabled, all objects tagged with
`SNOWFLAKE.CORE.SKIP_SENSITIVE_DATA_CLASSIFICATION='TRUE'` are skipped during sensitive data classification.

For more information, see [Excluding data from sensitive data classification](/user-guide/classify-auto-exclude).

## Syntax

Copy code

```
<classification_profile_name>!SET_ENABLE_TAG_BASED_SENSITIVE_DATA_EXCLUSION( <boolean_value> )
```

## Arguments

`boolean_value`
:   Determines whether tag-based sensitive data exclusion is enabled for the classification profile.

    When set to TRUE, objects tagged with `SNOWFLAKE.CORE.SKIP_SENSITIVE_DATA_CLASSIFICATION='TRUE'` are excluded from
    sensitive data classification.

    When set to FALSE, all objects are included in sensitive data classification regardless of whether the
    `SKIP_SENSITIVE_DATA_CLASSIFICATION` tag is set on an object.

    Default: FALSE

## Returns

Returns a successful status message or an error message.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Instance role | Object | Notes |
| --- | --- | --- |
| `classification_profile`!PRIVACY\_USER | The classification profile instance. | The account role that calls this method must be granted this instance role on the classification profile. The role used to create the instance is automatically granted this instance role. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

Calling this method does not return the object. Because of this, you can’t use method chaining to call another method on the
return value of this method. Instead, call each method in a separate SQL statement.

## Examples

Enable tag-based sensitive data exclusion for the `my_classification_profile` instance:

Copy code

```
CALL my_classification_profile!SET_ENABLE_TAG_BASED_SENSITIVE_DATA_EXCLUSION(TRUE);
```

Disable tag-based sensitive data exclusion for the `test_profile` instance:

Copy code

```
CALL test_profile!SET_ENABLE_TAG_BASED_SENSITIVE_DATA_EXCLUSION(FALSE);
```
