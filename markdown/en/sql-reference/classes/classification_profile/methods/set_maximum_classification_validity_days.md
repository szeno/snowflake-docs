# <classification\_profile\_name>!SET\_MAXIMUM\_CLASSIFICATION\_VALIDITY\_DAYS

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Specifies the maximum number of days to wait before a table is eligible to be automatically classified for an instance of the
CLASSIFICATION\_PROFILE class.

## Syntax

Copy code

```
<classification_profile_name>!SET_MAXIMUM_CLASSIFICATION_VALIDITY_DAYS( <days> )
```

## Arguments

`days`
:   Specifies the number of days since the last classification event before a table can be classified again using automatic classification.

    The value must be greater than `0`.

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

Set the minimum number of days to be `5` before a table can be automatically classified again:

Copy code

```
CALL my_classification_profile!SET_MAXIMUM_CLASSIFICATION_VALIDITY_DAYS(5);
```
