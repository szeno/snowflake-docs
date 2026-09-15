# ALTER MODEL

Modifies the properties for an existing model, including its name, tags, default version, or comment.

Three other variants of this command exist, namely:

- [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version) adds a new version of a model.
- [ALTER MODEL … DROP VERSION](/sql-reference/sql/alter-model-drop-version) removes a version of a model.
- [ALTER MODEL … MODIFY VERSION](/sql-reference/sql/alter-model-modify-version) sets a model version’s comment or metadata.

## Syntax

Copy code

```
ALTER MODEL [ IF EXISTS ] <name> SET
  [ COMMENT = '<string_literal>' ]
  [ DEFAULT_VERSION = '<version_name>']

ALTER MODEL [ IF EXISTS ] <model_name> SET TAG <tag_name> = '<tag_value>'

ALTER MODEL [ IF EXISTS ] <model_name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER MODEL [ IF EXISTS ] <model_name> VERSION <version_name> SET ALIAS = <alias_name>

ALTER MODEL [ IF EXISTS ] <model_name> VERSION <version_or_alias_name> UNSET ALIAS

ALTER MODEL <model_name> RENAME TO <new_name>
```

## Parameters

`name`
:   Specifies the identifier (i.e. name) of the model.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies one or more model properties to be set.

    `COMMENT = 'string_literal'`
    :   Sets the comment of the model. This can also be done using the [COMMENT](/sql-reference/sql/comment) command.

    `DEFAULT_VERSION = 'version_name'`
    :   Sets the default version of the model (the version that methods are invoked on when calling a method directly on the
        model). The version name is an [identifier](/sql-reference/identifiers-syntax).

        The system alias DEFAULT refers to the default version.

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `ALIAS = alias_name`
    :   Sets `alias_name` as an alias of the version. An alias is an alternative name that can be easily reassigned.
        The alias can be used most places where the version name can be used. A version can have at most one alias.

        The alias name is an [identifier](/sql-reference/identifiers-syntax). It must be unique in the model and may
        not duplicate the system alias names, which are:

        - `DEFAULT` refers to the default version of the model.
        - `FIRST` refers to the oldest version of the model by creation time.
        - `LAST` refers to the newest version of the model by creation time.

`UNSET TAG tag_name [ , tag_name ... ]`
:   Specifies one or more tags to be unset on the model.

`UNSET ALIAS`
:   Removes the alias from this model version, if it has one. The system aliases DEFAULT, FIRST, and LAST cannot be removed.
    You may specify the version by its name or by alias.

`RENAME TO new_name`
:   Renames the specified model with a new identifier that is not currently used by any other models in the schema.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When a model is renamed, other objects that reference it must be updated with the new name.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Model | A role must be granted or inherit the OWNERSHIP privilege on the object to create a temporary object that has the same name as the object that already exists in the schema. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).
