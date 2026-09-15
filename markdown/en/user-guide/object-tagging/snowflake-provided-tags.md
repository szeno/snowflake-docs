# Snowflake-provided tags

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Snowflake-provided tags are out of the box tags for common governance use cases, such as tracking cost centers, identifying sensitive data,
certifying trusted data assets, and pausing tag propagation. These tags give you a consistent tagging vocabulary across accounts,
databases, teams, and use cases.

## Overview

Organizations commonly create similar governance tags in every Snowflake account. Defining and maintaining those tags requires decisions
about tag names, allowed values, privileges, and comments. Over time, inconsistent definitions make tags difficult to understand and
maintain, which contributes to tag sprawl.

Snowflake-provided tags offer predefined, opinionated defaults for day-one tagging. Snowflake creates these tags in the
`SNOWFLAKE.TAGS` schema in every account. You can use them immediately without creating and maintaining equivalent tags in each
account.

Because the tags have the same fully qualified names and intended uses across accounts, they help you:

- Establish a consistent tagging vocabulary.
- Reduce duplicate and overlapping tags.
- Avoid maintaining separate tag definitions in each account.
- Make tag usage easier to understand across databases, teams, and accounts.
- Build governance and AI workflows that rely on well-known tag names and values.

Users can’t create tags in the `SNOWFLAKE.TAGS` schema. Access is granted through application roles. For more information, see
[Access control](#label-snowflake-provided-tags-access-control).

You can assign Snowflake-provided tags to the same [supported objects](/user-guide/object-tagging/introduction#supported-objects) as
other object tags.

## Available Snowflake-provided tags

The following Snowflake-provided tags are available:

| Tag | Purpose |
| --- | --- |
| `SNOWFLAKE.TAGS.COST_CENTER` | Identifies the cost center associated with an object for cost tracking and budget control. |
| `SNOWFLAKE.TAGS.CERTIFICATION_STATUS` | Identifies whether a data asset is ready and is trusted for use. |
| `SNOWFLAKE.TAGS.SENSITIVITY` | Assigns a standardized sensitivity level to a data object. |
| `SNOWFLAKE.TAGS.ENVIRONMENT` | Identifies the deployment environment an object belongs to. |
| `SNOWFLAKE.TAGS.PROJECT` | Associates an object with a project for organization and cost tracking. |
| `SNOWFLAKE.TAGS.SKIP_TAG_PROPAGATION` | Prevents future automatic tag propagation to an object. Requires Enterprise Edition or higher. |

Expand

Show lessSee more

### COST\_CENTER

Use `SNOWFLAKE.TAGS.COST_CENTER` to identify the cost center associated with an object for cost tracking and budget control.

### CERTIFICATION\_STATUS

Use `SNOWFLAKE.TAGS.CERTIFICATION_STATUS` to identify whether a data asset is ready and is trusted for use.

The tag supports the following values:

- `'DRAFT'`
- `'TO BE REVIEWED'`
- `'IN REVIEW'`
- `'CERTIFIED'`
- `'REJECTED'`
- `'DEPRECATED'`

`CERTIFIED` indicates that the asset has been verified and is ready for production use. `DEPRECATED` indicates that the asset should
no longer be used in production.

Unlike the other Snowflake-provided tags, account administrators can’t modify the definition or allowed values of
`CERTIFICATION_STATUS`. The fixed values let governance and AI workflows interpret certification status consistently.

Note

The `SNOWFLAKE.CORE.CERTIFICATION_STATUS` tag is still supported but will be deprecated in a future release. Snowflake
recommends that you use `SNOWFLAKE.TAGS.CERTIFICATION_STATUS` instead.

### SENSITIVITY

Use `SNOWFLAKE.TAGS.SENSITIVITY` to assign a standardized sensitivity level to a data object.

The predefined values are:

- `'RESTRICTED'`
- `'CONFIDENTIAL'`
- `'INTERNAL'`
- `'PUBLIC'`

A role that is granted the `OOB_TAG_ADMIN` application role can change these allowed values.

Note

`SNOWFLAKE.TAGS.SENSITIVITY` is different from the `SNOWFLAKE.CORE.PRIVACY_CATEGORY` system-defined tag used by
[sensitive data classification](/user-guide/classify-intro#label-classify-classification-tags).

### ENVIRONMENT

Use `SNOWFLAKE.TAGS.ENVIRONMENT` to identify the deployment environment an object belongs to.

The allowed values are:

- `'PRODUCTION'`
- `'STAGING'`
- `'TEST'`
- `'DEVELOPMENT'`

### PROJECT

Use `SNOWFLAKE.TAGS.PROJECT` to associate an object with a project for organization and cost tracking.

### SKIP\_TAG\_PROPAGATION

[Enterprise Edition Feature](/user-guide/intro-editions)

This tag requires Enterprise Edition or higher. To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Use `SNOWFLAKE.TAGS.SKIP_TAG_PROPAGATION` when [automatic tag propagation](/user-guide/object-tagging/propagation) is working as
intended, but a downstream object, such as a transformed or hash-key target, shouldn’t continue receiving propagated tags.

Set the tag with an empty string value:

Copy code

```
ALTER TABLE target_table SET TAG SNOWFLAKE.TAGS.SKIP_TAG_PROPAGATION = '';
```

Setting this tag on an object has the following effects:

- Pauses all future tag propagation to the object.
- Doesn’t remove tags that were previously propagated to the object.

To resume tag propagation to the object, unset the tag.

A user-defined tag with the same name in another schema doesn’t pause tag propagation. Only
`SNOWFLAKE.TAGS.SKIP_TAG_PROPAGATION` activates this behavior.

## Access control

Snowflake creates and owns the tags in the `SNOWFLAKE.TAGS` schema. Users can’t create additional tags in this schema, and you
don’t grant object privileges on these tags directly.

Instead, Snowflake provides application roles. By default, these roles are granted to ACCOUNTADMIN. ACCOUNTADMIN can grant them to other
roles as needed.

| Application role | What it allows |
| --- | --- |
| `OOB_TAG_READ` | USAGE on the `SNOWFLAKE.TAGS` schema so roles can see the tags. This role is also granted to PUBLIC. |
| `OOB_TAG_APPLY` | APPLY on Snowflake-provided tags so a role can assign the tags to objects. |
| `OOB_TAG_ADMIN` | MODIFY on Snowflake-provided tags so a role can change allowed values, comments, and propagate settings. This role doesn’t apply to `CERTIFICATION_STATUS`. |

Expand

Show lessSee more

To let a custom role apply Snowflake-provided tags, grant the apply application role:

Copy code

```
GRANT APPLICATION ROLE SNOWFLAKE.OOB_TAG_APPLY TO ROLE data_steward;
```

## Limitations and considerations

- Snowflake-provided tags are predefined and can’t be dropped.
- You can’t create additional tags in the `SNOWFLAKE.TAGS` schema.
- The allowed values of `CERTIFICATION_STATUS` can’t be modified.
- `SKIP_TAG_PROPAGATION` requires Enterprise Edition or higher.
- `SKIP_TAG_PROPAGATION` pauses all future tag propagation to an object.
- Setting `SKIP_TAG_PROPAGATION` doesn’t remove tags that were previously propagated.
- A user-defined tag with the same name as a Snowflake-provided tag doesn’t activate Snowflake-provided behavior.
