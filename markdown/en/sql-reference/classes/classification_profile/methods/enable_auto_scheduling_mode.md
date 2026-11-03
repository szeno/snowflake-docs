# <classification\_profile\_name>!ENABLE\_AUTO\_SCHEDULING\_MODE

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

[Preview Feature](/release-notes/preview-features) — Open

Available to Enterprise Edition or higher.

Enables [Autopilot](/user-guide/classify-intro#label-classify-autopilot) for the instance of the CLASSIFICATION\_PROFILE class. Autopilot
corresponds to `scheduling_mode` set to `AUTO`.

If you set `minimum_object_age_for_classification_days` or `maximum_classification_validity_days` on the profile, Snowflake sets
`scheduling_mode` to `CUSTOM` and turns Autopilot off. Call this method to turn Autopilot back on.

## Syntax

Copy code

```
<classification_profile_name>!ENABLE_AUTO_SCHEDULING_MODE()
```

## Arguments

None.

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

Enable Autopilot for the classification profile:

Copy code

```
CALL my_classification_profile!ENABLE_AUTO_SCHEDULING_MODE();
```
