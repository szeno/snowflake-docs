# ALTER CODE BUNDLE

Modifies an existing [Code Bundle](/developer-guide/code-bundles/code-bundles). Use this command to add a new version of the bundle’s
source files, or to set or unset its comment.

See also:
:   [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle), [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle), [DESCRIBE CODE BUNDLE](/sql-reference/sql/desc-code-bundle),
    [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles), [DROP CODE BUNDLE](/sql-reference/sql/drop-code-bundle)

## Syntax

Copy code

```
ALTER CODE BUNDLE <name> ADD VERSION FROM '<source>'

ALTER CODE BUNDLE <name> SET COMMENT = '<string_literal>'

ALTER CODE BUNDLE <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier of the Code Bundle to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`ADD VERSION FROM 'source'`
:   Adds a new version of the Code Bundle from the specified source. Snowflake copies the files from the source into the new version, which is
    an immutable snapshot. The source can be an internal or temporary stage path (for example, `'@my_db.my_schema.my_stage/project'`) or a
    workspace path (for example, `'snow://workspace/USER$.PUBLIC."my_workspace"/versions/live'`). External stages aren’t supported.

    Include a `code_bundle.yml` file in the root of the source. If the version doesn’t have one, every run needs a complete
    specification in `WITH SPECIFICATION`. For the file’s fields, see the
    [`code_bundle.yml` reference](/developer-guide/code-bundles/code-bundle-yml-reference).

`SET COMMENT = 'string_literal'`
:   Sets a comment for the Code Bundle. Comments are stored as object metadata; avoid including sensitive data in comments.

`UNSET COMMENT`
:   Removes the comment from the Code Bundle.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Code Bundle | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |
| READ | Stage | Required to add a version from a stage. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A Code Bundle’s default version is `LAST`, so after you add a version, runs that use the Code Bundle by name use the new version. To see
  the default and last versions, use [DESCRIBE CODE BUNDLE](/sql-reference/sql/desc-code-bundle).
- Renaming a Code Bundle isn’t supported. To use a different name, create a Code Bundle with the new name and drop the old one. Update any
  tasks that run the old name.
- To run the `ALTER CODE BUNDLE` command, execute it from a SQL file or SQL worksheet, not from within a notebook cell.

## Examples

Add a version from a workspace:

Copy code

```
ALTER CODE BUNDLE my_db.my_schema.my_bundle
  ADD VERSION FROM 'snow://workspace/USER$.PUBLIC."my_workspace"/versions/live';
```

Add a version from a stage:

Copy code

```
ALTER CODE BUNDLE my_db.my_schema.my_bundle
  ADD VERSION FROM '@my_db.my_schema.my_stage/project';
```

Set and remove the comment:

Copy code

```
ALTER CODE BUNDLE my_db.my_schema.my_bundle SET COMMENT = 'Nightly sales aggregation';

ALTER CODE BUNDLE my_db.my_schema.my_bundle UNSET COMMENT;
```
