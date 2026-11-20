# DROP CODE BUNDLE

Removes the specified [Code Bundle](/developer-guide/code-bundles/code-bundles) from the current or specified schema, including all of its
versions.

See also:
:   [CREATE CODE BUNDLE](/sql-reference/sql/create-code-bundle), [ALTER CODE BUNDLE](/sql-reference/sql/alter-code-bundle), [DESCRIBE CODE BUNDLE](/sql-reference/sql/desc-code-bundle),
    [SHOW CODE BUNDLES](/sql-reference/sql/show-code-bundles)

## Syntax

Copy code

```
DROP CODE BUNDLE [ IF EXISTS ] <name>
```

## Parameters

`name`
:   Specifies the identifier of the Code Bundle to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`IF EXISTS`
:   Doesn’t return an error if the Code Bundle doesn’t exist.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Code Bundle | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Tasks and other code that run the dropped Code Bundle by name fail after it’s dropped. Drop or update those tasks first.
- Dropping a Code Bundle doesn’t delete the stage or workspace that it was created from.

## Examples

Drop a Code Bundle:

Copy code

```
DROP CODE BUNDLE my_db.my_schema.my_bundle;
```

Drop a Code Bundle without an error if it doesn’t exist:

Copy code

```
DROP CODE BUNDLE IF EXISTS my_db.my_schema.my_bundle;
```
