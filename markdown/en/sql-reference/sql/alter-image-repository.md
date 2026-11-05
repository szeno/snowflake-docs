# ALTER IMAGE REPOSITORY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Modifies the properties of an existing [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository).

See also:
:   [CREATE IMAGE REPOSITORY](/sql-reference/sql/create-image-repository) , [DROP IMAGE REPOSITORY](/sql-reference/sql/drop-image-repository) , [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories)

## Syntax

Copy code

```
ALTER IMAGE REPOSITORY [ IF EXISTS ] <name> SET
  [ COMMENT = '<string_literal>' ]

ALTER IMAGE REPOSITORY [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER IMAGE REPOSITORY [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER IMAGE REPOSITORY [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the image repository to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies the properties to set for the image repository:

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   Specifies a comment for the image repository.

        Default: No value

`UNSET ...`
:   Specifies the property to unset for the image repository, which resets it to the default value:

    - `TAG tag_name [ , tag_name ... ]`
    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Image repository |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Examples

The following example sets a comment on the repository named `tutorial_repository`:

Copy code

```
ALTER IMAGE REPOSITORY tutorial_repository SET COMMENT = 'Images for the tutorial services';
```

The following example removes the comment:

Copy code

```
ALTER IMAGE REPOSITORY tutorial_repository UNSET COMMENT;
```
