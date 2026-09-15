# <classification\_profile\_name>!SET\_AI\_MODE

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Specifies whether to enable [AI mode](/user-guide/classify-intro#label-classify-ai-mode) for the instance of the CLASSIFICATION\_PROFILE
class.

## Syntax

Copy code

```
<classification_profile_name>!SET_AI_MODE( <boolean_value> )
```

## Arguments

`boolean_value`
:   Specifies whether to enable AI mode for the instance of the CLASSIFICATION\_PROFILE class.

    TRUE enables AI mode.

    FALSE disables AI mode.

    Default: FALSE

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

When AI mode is enabled, LLM usage is billed under the `AI_SENSITIVE_DATA_CLASSIFICATION` [service type](/sql-reference/service-types).
Serverless compute for classification continues to be billed under `SENSITIVE_DATA_CLASSIFICATION`.

## Examples

Enable AI mode for the classification profile:

Copy code

```
CALL my_ai_profile!SET_AI_MODE(true);
```

Disable AI mode for the classification profile:

Copy code

```
CALL my_ai_profile!SET_AI_MODE(false);
```
