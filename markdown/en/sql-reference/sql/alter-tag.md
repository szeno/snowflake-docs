# ALTER TAG

Modifies the properties for an existing tag, including renaming the tag and setting a masking policy on a tag.

Any changes made to the tag go into effect when the next SQL query that uses the tag runs.

See also:
:   [CREATE TAG](/sql-reference/sql/create-tag), [DROP TAG](/sql-reference/sql/drop-tag), [SHOW TAGS](/sql-reference/sql/show-tags), [UNDROP TAG](/sql-reference/sql/undrop-tag), [Multi-value tags](/user-guide/object-tagging/multi-value-tags)

## Syntax

Copy code

```
ALTER TAG [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER TAG [ IF EXISTS ] <name> { ADD | DROP } ALLOWED_VALUES '<val_1>' [ , '<val_2>' [ , ... ] ]

ALTER TAG [ IF EXISTS ] <name> SET
  [ ALLOWED_VALUES '<val_1>' [ , '<val_2>' [ , ... ] ] ]
  [ MULTI_VALUE = TRUE ]
  [ PROPAGATE = { ON_DEPENDENCY_AND_DATA_MOVEMENT | ON_DEPENDENCY | ON_DATA_MOVEMENT }
    [ ON_CONFLICT = { '<string>' | ALLOWED_VALUES_SEQUENCE | MERGE } ] ]
  [ COMMENT = '<string_literal>' ]

ALTER TAG [ IF EXISTS ] <name> UNSET { ALLOWED_VALUES | PROPAGATE | ON_CONFLICT | COMMENT }

ALTER TAG [ IF EXISTS ] <name> SET DATA MOVEMENT POLICY <data_movement_policy_name> [ FORCE ]

ALTER TAG [ IF EXISTS ] <name> UNSET DATA MOVEMENT POLICY

ALTER TAG [ IF EXISTS ] <name> SET MASKING POLICY
  <masking_policy_name> [ , MASKING POLICY <masking_policy_2_name> , ... ] [ FORCE ]

ALTER TAG [ IF EXISTS ] <name> UNSET MASKING POLICY <masking_policy_name> [ , MASKING POLICY <masking_policy_2_name> , ... ]

ALTER TAG [ IF EXISTS ] <name> UNSET DCM PROJECT
```

## Parameters

`name`
:   Identifier for the tag. Assign the tag string value on an [object](/user-guide/object-tagging/introduction#label-object-tag-supported-objects) using either a
    [CREATE <object>](/sql-reference/sql/create) statement or an [ALTER <object>](/sql-reference/sql/alter) statement.

    The identifier value must start with an alphabetic character and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes (e.g. “My object”). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax)

`RENAME TO new_name`
:   Specifies the new identifier for the tag; must be unique for your schema. The new identifier cannot be used if the identifier is already
    in place for a different tag.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`ALLOWED_VALUES 'val_1' [ , 'val_2' [ , ... ] ]`
:   Specifies a comma-separated list of the possible string values that can be assigned to the tag when the tag is set on an
    [object](/user-guide/object-tagging/introduction#label-object-tag-supported-objects) using the corresponding [CREATE <object>](/sql-reference/sql/create) or
    [ALTER <object>](/sql-reference/sql/alter) command.

    The maximum number of tag values in this list is 5,000.

    If you use the SET ALLOWED\_VALUES clause, the specified values *replace* previously specified values, which allows you to adjust the
    sequence of values atomically.

    Using the DROP ALLOWED\_VALUES clause to remove all values prevents someone from setting the tag to a value. If your intention is to let
    users set the tag to any value, use UNSET ALLOWED\_VALUES instead.

    Changing or removing allowed values doesn’t affect values already assigned to objects. For more information, see
    [Set a list of allowed tag values](/user-guide/object-tagging/work#label-object-tagging-specify-tag-values).

    If a tag is configured to automatically propagate to target objects, the order of values in the allowed list can affect how conflicts are
    resolved. For more information, see [Tag propagation conflicts](/user-guide/object-tagging/propagation#label-tag-propagation-conflicts).

    Default: NULL (all string values are allowed, including an empty string value (that is, `' '`)).

`MULTI_VALUE = TRUE`
:   Converts the tag so it can store more than one string value on the same object or column. After you set this property, you
    can’t unset it or set it to FALSE. For more information, see [Multi-value tags](/user-guide/object-tagging/multi-value-tags).

`PROPAGATE = { ON_DEPENDENCY_AND_DATA_MOVEMENT | ON_DEPENDENCY | ON_DATA_MOVEMENT }`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Enterprise Edition Feature](/user-guide/intro-editions)

    This parameter requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

    Specifies that the tag will be [automatically propagated](/user-guide/object-tagging/propagation) from source objects to target
    objects. You can configure the tag to propagate when there is an [object dependency](/user-guide/object-tagging/propagation#label-tag-propagation-dependency),
    [data movement](/user-guide/object-tagging/propagation#label-tag-propagation-lineage), or both.

    Changes to this parameter do not automatically propagate to target objects. These changes have no effect on tags that were previously
    applied to target objects as part of tag propagation.

    Possible values are:

    `ON_DEPENDENCY_AND_DATA_MOVEMENT`
    :   Propagates the tag when there is an object dependency or data movement.

    `ON_DEPENDENCY`
    :   Propagates the tag for object dependencies, but not for data movement.

    `ON_DATA_MOVEMENT`
    :   Propagates the tag when there is data movement, but not for object dependencies.

`ON_CONFLICT = { 'string' | ALLOWED_VALUES_SEQUENCE | MERGE }`
:   [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Enterprise Edition Feature](/user-guide/intro-editions)

    This parameter requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

    Specifies what happens when there is a conflict between the values of [propagated tags](/user-guide/object-tagging/propagation).

    If you don’t set this parameter and there is a conflict, the value of the tag is set to the string `CONFLICT`.

    Changes to this parameter do not automatically propagate to target objects. These changes have no effect on tags that were previously
    applied to target objects as part of tag propagation.

    Possible values are:

    `'string'`
    :   When there is a conflict, the value of the tag is set to the specified string.

    `ALLOWED_VALUES_SEQUENCE`
    :   The order of the values in the ALLOWED\_VALUES property of the tag determines which value is used when there is a conflict.
        For example, suppose you created a tag with the following statement:

        Copy code

        ```
        CREATE TAG my_tag ALLOWED_VALUES 'blue', 'red' PROPAGATE = ON_DEPENDENCY;
        ```

        If there is a conflict, then the value of `my_tag` will be `blue` because it comes before `red` in the allowed values list.

    `MERGE`
    :   Combines conflicting tag values into multiple values on the target object. You can set `ON_CONFLICT = MERGE` only when
        `MULTI_VALUE = TRUE`. For more information, see [Multi-value tags](/user-guide/object-tagging/multi-value-tags).

    Default: Set the value of the tag to `CONFLICT`.

`SET DATA MOVEMENT POLICY data_movement_policy_name [ FORCE ]`
:   Attaches a [data movement policy](/user-guide/data-movement-policies) to the tag. When this tag is set on a column, table,
    schema, or database, the data movement policy governs data movement operations on the tagged object.

    If a data movement policy is already set on the tag, use FORCE to replace it without having to unset the existing policy
    first.

`UNSET DATA MOVEMENT POLICY`
:   Removes the data movement policy from the tag.

`MASKING POLICY masking_policy_name [ , MASKING POLICY masking_policy_2_name , ... ]`
:   Specifies a comma-separated list of [masking policies](/user-guide/security-column-intro) that can be assigned to the tag.

`FORCE`
:   Replaces a masking policy that is currently set on a tag with a different masking policy in a single statement.

    Note that using the FORCE keyword replaces the masking policy when a policy of the same [data type](/sql-reference-data-types) is
    already set on the tag.

    If a masking policy is not currently set on the tag, specifying this keyword has no effect.

    For details, see [Replace a masking policy on a tag](/user-guide/tag-based-masking-policies#label-tag-based-masking-replace-masking-policy).

`COMMENT = 'string_literal'`
:   Specifies a comment for the tag.

    Default: No value

`UNSET`
:   Specifies one (or more) properties and/or parameters to unset for the tag, which resets them to the defaults:

    - `ALLOWED_VALUES`
    - `PROPAGATE`
    - `ON_CONFLICT`
    - `COMMENT`

`UNSET DCM PROJECT`

> Detaches the tag from the [DCM project](/user-guide/dcm-projects/dcm-projects-overview) that currently manages it.
> The command removes the association between the tag and the DCM project without dropping the tag. See [Detach objects from a DCM project](/user-guide/dcm-projects/dcm-projects-use#label-dcm-projects-detach-object) for more information.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Tag | This privilege is required to modify tag properties (e.g. comment, allowed values).  OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| APPLY DATA MOVEMENT POLICY | Account | Assigning and replacing a data movement policy on a tag requires the global APPLY DATA MOVEMENT POLICY privilege. |
| APPLY MASKING POLICY | Account | Assigning and replacing a masking policy on a tag requires the global APPLY MASKING POLICY privilege. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For additional details on tag DDL and privileges, see [Access control privileges](/user-guide/object-tagging/work#label-object-tags-privileges).

## Usage notes

- For more information on tag DDL authorization, see [required privileges](/user-guide/object-tagging/work#label-object-tags-ddl-privilege-summary).
- Regarding assigning one or more masking policies to a tag:

  - A tag can have only one masking policy per data type.

    For example, a tag can have one policy for the STRING data type, one policy for the NUMBER data type, and so on.
  - If a masking policy already protects a column and the tag with a masking policy is set on the same column, the masking policy
    directly assigned to the column takes precedence over the masking policy assigned to the tag.
  - A tag cannot be [dropped](/sql-reference/sql/drop-tag) if a masking policy is assigned to the tag, nor can the masking policy be
    dropped if the masking policy is assigned to a tag.
- Regarding replication, particularly with tag-based masking policies, see
  [policy replication considerations](/user-guide/database-replication-considerations#label-database-replication-considerations-masking-row-policies).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Rename the `cost_center` tag to `cost_center_na`, where `na` specifies North America.

> Copy code
>
> ```
> ALTER TAG cost_center RENAME TO cost_center_na;
> ```
