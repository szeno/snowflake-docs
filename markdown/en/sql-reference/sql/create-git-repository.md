# CREATE GIT REPOSITORY

Creates a Snowflake Git repository clone in the schema or replaces an existing Git repository clone.

For an overview, see [Using a Git repository in Snowflake](/developer-guide/git/git-overview).

See also:
:   [ALTER GIT REPOSITORY](/sql-reference/sql/alter-git-repository), [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository), [DROP GIT REPOSITORY](/sql-reference/sql/drop-git-repository),
    [SHOW GIT BRANCHES](/sql-reference/sql/show-git-branches), [SHOW GIT REPOSITORIES](/sql-reference/sql/show-git-repositories), [SHOW GIT TAGS](/sql-reference/sql/show-git-tags)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] GIT REPOSITORY [ IF NOT EXISTS ] <name>
  ORIGIN = '<repository_url>'
  API_INTEGRATION = <integration_name>
  [ GIT_CREDENTIALS = <secret_name> ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' , ... ] ) ]
```

## Required parameters

`name`
:   Specifies the identifier for the Git repository clone to create.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ORIGIN = 'repository_url'`
:   Specifies the origin URL of the remote Git repository that this Git repository clone represents. The URL must use HTTPS.

    Snowflake supports any HTTPS Git repository URL. For example, you can specify a custom URL to a corporate Git server within your own
    domain.

    From the command line, you can use the `git config` command from within your local repository to get the value to use for the
    ORIGIN parameter, as shown in the following example:

    Copy code

    ```
    $ git config --get remote.origin.url
    https://github.com/mycompany/My-Repo.git
    ```

`API_INTEGRATION = integration_name`
:   Specifies the [API INTEGRATION](/sql-reference/sql/create-api-integration) that contains information about the remote Git
    repository such as allowed credentials and prefixes for target URLs.

    The API integration you specify here must have an API\_PROVIDER parameter whose value is set to `git_https_api`.

    For reference information about API integrations, see [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration).

## Optional parameters

`GIT_CREDENTIALS = secret_name`
:   Specifies the Snowflake [secret](/sql-reference/sql/create-secret) containing the credentials to use for authenticating with the
    remote Git repository. Omit this parameter to use the default secret specified by the API integration or if this integration does not require
    authentication.

    As a best practice, use a personal access token for the secret’s PASSWORD value. For information about creating a personal access token
    in GitHub, see [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
    in the GitHub documentation.

    The secret you specify here must be a secret specified by the ALLOWED\_AUTHENTICATION\_SECRETS parameter of the API integration you specify
    with this command’s API\_INTEGRATION parameter.

    Default: No value

    For reference information about secrets, see [CREATE SECRET](/sql-reference/sql/create-secret).

`COMMENT = 'string_literal'`
:   Specifies a comment for the Git repository clone.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE GIT REPOSITORY | Schema |  |
| USAGE | API integration | The integration specified by this command’s API INTEGRATION parameter |
| USAGE | Secret | The secret specified by this command’s GIT\_CREDENTIALS parameter |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Git repositories larger than 2 GB aren’t supported. For a complete list of limitations, see
  [Git in Snowflake limitations](/developer-guide/git/git-limitations).

## Examples

Code in the following example creates a Git repository clone called `snowflake_extensions`, where the remote repository’s origin URL
is `https://github.com/my-account/snowflake-extensions.git`. The example uses an API integration called `git_api_integration`.
It also uses a secret called `git_secret` to store credentials for authenticating with the remote repository.

For details about setting up integration with a remote Git repository, see [Setting up Snowflake to use Git](/developer-guide/git/git-setting-up).

Copy code

```
CREATE OR REPLACE GIT REPOSITORY snowflake_extensions
  API_INTEGRATION = git_api_integration
  GIT_CREDENTIALS = git_secret
  ORIGIN = 'https://github.com/my-account/snowflake-extensions.git';
```
