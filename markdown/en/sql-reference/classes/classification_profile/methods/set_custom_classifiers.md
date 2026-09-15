# <classification\_profile\_name>!SET\_CUSTOM\_CLASSIFIERS

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Adds [custom classifiers](/user-guide/classify-custom) to an existing classification profile so sensitive data can be automatically
classified with custom classification semantic and privacy categories.

## Syntax

Copy code

```
<classification_profile_name>!SET_CUSTOM_CLASSIFIERS( <object> )
```

## Arguments

`object`
:   An [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) value that specifies the custom classifiers to add to the classification profile.

    Each key in the object specifies the name of an instance of the [CUSTOM\_CLASSIFIER class](/sql-reference/classes/custom_classifier).

    The value of each key specifies the [<code className=”samp”><em>custom\_classifier</em></code>!LIST](/sql-reference/classes/custom_classifier/methods/list) method of the custom classifier instance.

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

Copy code

```
CALL my_classification_profile!SET_CUSTOM_CLASSIFIERS(
  {
    'medical_codes': medical_codes!list(),
    'finance_codes': finance_codes!list()
  });
```
