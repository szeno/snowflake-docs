# ALTER APPLICATION ROLE

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Modifies the properties for an existing application role.

See also:
:   [CREATE APPLICATION ROLE](/sql-reference/sql/create-application-role), [GRANT APPLICATION ROLE](/sql-reference/sql/grant-application-role),
    [REVOKE APPLICATION ROLE](/sql-reference/sql/revoke-application-role), [SHOW APPLICATION ROLES](/sql-reference/sql/show-application-roles)

## Syntax

Copy code

```
ALTER APPLICATION ROLE [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER APPLICATION ROLE [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER APPLICATION ROLE [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the application role. If the identifier contains spaces or
    special characters, the entire string must be enclosed in double quotes. Identifiers enclosed
    in double quotes are also case-sensitive.

`RENAME TO new_name`
:   Specifies the new identifier for the application role. The identifier must be unique
    for within the application.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

    Note that when specifying the fully-qualified name of the application role, you cannot specify a
    different application. The name of the application, `application_name`, must remain the same.
    Only the `application_role_name` can change during a rename operation.

`SET ...`
:   Specifies the properties to set for the application role:

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites an existing comment for the application role.

`UNSET ...`
:   Specifies the properties to unset for the application role, which resets them to the defaults.

    - `COMMENT`

## Usage notes

- This command can only be run in the context of an application created using the Native
  Apps Framework.
- Only the application role owner (i.e. the role with the OWNERSHIP privilege on the application
  role), or a higher role, can run this command.
- Renaming an application role is only allowed within the same application.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Copy code

```
ALTER APPLICATION ROLE app_role RENAME TO new_app_role;
```

Copy code

```
ALTER APPLICATION ROLE app_role SET
  COMMENT = 'Application role for the Hello Snowflake application.';
```

Copy code

```
ALTER APPLICATION ROLE app_role UNSET COMMENT;
```
