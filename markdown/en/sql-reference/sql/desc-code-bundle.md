# DESCRIBE CODE BUNDLE

Describes the properties of a [Code Bundle](/developer-guide/code-bundles/code-bundles), including its versions and the source that backs
it.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle), [ALTER CODE BUNDLE](/sql-reference/sql/alter-code-bundle), [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles),
    [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle)

## Syntax

Copy code

```
{ DESC | DESCRIBE } CODE BUNDLE <name>
```

## Parameters

`name`
:   Specifies the identifier of the Code Bundle to describe.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Output

The output of the command includes the following columns, which describe the properties and metadata of the object:

| Column | Description |
| --- | --- |
| `name` | Name of the Code Bundle. |
| `comment` | Comment for the Code Bundle. |
| `default_version` | The version that runs use when they call the Code Bundle by name, for example `LAST`. |
| `default_version_name` | Name of the default version. |
| `default_version_alias` | Alias of the default version. |
| `default_version_location_uri` | Location of the default version’s files, in the form `snow://code bundle/...`. |
| `default_version_source_location_uri` | Stage or workspace path that the default version was created from. |
| `default_version_git_commit_hash` | Git commit hash of the default version, if its source is backed by a Git repository. |
| `last_version_name` | Name of the most recently added version. |
| `last_version_alias` | Alias of the most recently added version. |
| `last_version_location_uri` | Location of the most recently added version’s files. |
| `last_version_source_location_uri` | Stage or workspace path that the most recently added version was created from. |
| `last_version_git_commit_hash` | Git commit hash of the most recently added version, if its source is backed by a Git repository. |
| `live_version_location_uri` | Location of the live version, if the Code Bundle has one. |
| `created_on` | Date and time when the Code Bundle was created. |
| `owner_role` | Role that owns the Code Bundle. |
| `owner_role_type` | Type of role that owns the Code Bundle. |
| `container_type` | Type of the object that holds the Code Bundle’s source, for example `Stage`. |
| `container_database` | Database of the object that holds the Code Bundle’s source. |
| `container_schema` | Schema of the object that holds the Code Bundle’s source. |
| `container_name` | Name of the object that holds the Code Bundle’s source. |

Expand

Show lessSee more

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| USAGE or OWNERSHIP | Code Bundle |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Examples

Describe a Code Bundle:

Copy code

```
DESCRIBE CODE BUNDLE my_db.my_schema.my_bundle;
```

Find the source location of the version that runs use:

Copy code

```
DESCRIBE CODE BUNDLE my_db.my_schema.my_bundle;

SELECT "default_version", "default_version_source_location_uri"
  FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
```
