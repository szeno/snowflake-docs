# ALTER GIT REPOSITORY

Modifies the properties of a Snowflake [Git repository clone](/developer-guide/git/git-overview).

See also:
:   [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository), [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository), [DROP GIT REPOSITORY](/sql-reference/sql/drop-git-repository), [SHOW GIT BRANCHES](/sql-reference/sql/show-git-branches),
    [SHOW GIT REPOSITORIES](/sql-reference/sql/show-git-repositories), [SHOW GIT TAGS](/sql-reference/sql/show-git-tags)

## Syntax

Copy code

```
ALTER GIT REPOSITORY [ IF EXISTS ] <name> SET
  [ GIT_CREDENTIALS = <secret_name> ]
  [ API_INTEGRATION = <integration_name> ]
  [ COMMENT = '<string_literal>' ]

ALTER GIT REPOSITORY [ IF EXISTS ] <name> SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER GIT REPOSITORY [ IF EXISTS ] <name> UNSET TAG <tag_name> [ , <tag_name> ... ]

ALTER GIT REPOSITORY [ IF EXISTS ] <name> UNSET {
  GIT_CREDENTIALS |
  COMMENT }
  [ , ... ]

ALTER GIT REPOSITORY [ IF EXISTS ] <name> FETCH
```

## Parameters

`name`
:   Specifies the identifier for the Git repository clone to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET ...`
:   Specifies the properties to set for the integration:

    `GIT_CREDENTIALS = secret_name`
    :   Specifies the secret object containing credentials for authenticating with the remote Git repository.

        The secret you specify here must be a secret specified by the ALLOWED\_AUTHENTICATION\_SECRETS parameter of the API integration specified
        for this Git repository.

        For reference information about secrets, see [CREATE SECRET](/sql-reference/sql/create-secret).

    `API_INTEGRATION = integration_name`
    :   Specifies the API integration containing details about how Snowflake should interact with the repository API.

        For reference information about API integrations, see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration).

    `TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
    :   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

        The tag value is always a string, and the maximum number of characters for the tag value is 256.

        For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

    `COMMENT = 'string_literal'`
    :   Specifies a comment.

        Default: No value

`UNSET ...`
:   Specifies the property to unset for the integration, which resets it to the default value:

    - `GIT_CREDENTIALS`
    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

`FETCH`
:   Fetches content from the remote Git repository to the Git repository clone.

    The content fetched is a full clone that fetches all branches, tags, and commits from the remote repository. The command also prunes
    branches and commits that were fetched earlier but no longer exist in the remote repository.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP or WRITE | Git repository | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Note

If the secret specified in `GIT_CREDENTIALS` is in a different database or schema than the Git repository, the executing role must also have USAGE on that secret’s parent database and schema. This allows Snowflake to resolve the secret’s fully qualified name and match it against the API integration’s `ALLOWED_AUTHENTICATION_SECRETS` list. USAGE on the secret object itself is not required.

## Examples

The following example refreshes the `snowflake_extensions` [Git repository clone](/developer-guide/git/git-overview) with
data from its remote Git origin:

Copy code

```
ALTER GIT REPOSITORY snowflake_extensions FETCH;
```
