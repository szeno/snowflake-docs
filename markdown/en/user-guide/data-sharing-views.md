# Share data in non-secured views

To take full advantage of the performance gains of query
optimizations on the views that you share, you can
create a share that lets you share non-secure views with other accounts.

Note

When possible, use secure views to enforce the security of your data.
See [Use secure objects to control data access](/user-guide/data-sharing-secure-views).

## Create a share that allows non-secure objects

To share non-secure views,
create a share that allows non-secure objects.

For example, run the following:

Copy code

```
CREATE OR REPLACE SHARE allow_non_secure_views
 SECURE_OBJECTS_ONLY=FALSE
 COMMENT="Share views that require query optimization";
```

Note

For full syntax, see [Syntax for sharing non-secure views](#label-sharing-non-secure-view-syntax)
in this topic.

After you create a share that allows sharing views,
use the [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share) command to
grant a view to a share. For example, to grant a view named
`non_secure_view` to the share, run the following:

Copy code

```
GRANT SELECT ON VIEW non_secure_view TO SHARE allow_non_secure_views;
```

Alternatively, you can grant the SELECT privilege on the view to a
database role, and then grant that database role to the share.
For example, to grant SELECT privileges on the view `non_secure_view`
to the database role `performance_engineer` and then
grant the role to the share, run the following:

Copy code

```
GRANT SELECT ON VIEW non_secure_view TO DATABASE ROLE performance_engineer;
GRANT DATABASE ROLE performance_engineer TO SHARE allow_non_secure_views;
```

## Convert an existing share to allow sharing non-secure views

You can convert an existing share with secure views into a share that
supports sharing non-secure views.

For example, to convert an existing share `secure_views_only` into
one that supports sharing non-secure views, do the following:

1. Use the [SHOW GRANTS](/sql-reference/sql/show-grants) command to determine
   which objects are granted to the share, and which accounts
   have access to the share, respectively:

   Copy code

   ```
   SHOW GRANTS TO SHARE secure_views_only;
   SHOW GRANTS OF SHARE secure_views_only;
   ```
2. Convert the existing share with one that allows sharing views:

   Copy code

   ```
   ALTER SHARE secure_views_only
    SET SECURE_OBJECTS_ONLY = FALSE,
    COMMENT = "Convert to allow sharing non-secure views that require
    query optimization";
   ```
3. Optionally convert an existing secure view into a view. In this example,
   alter `secure_view2` into a non-secure view:

   Copy code

   ```
   ALTER VIEW secure_view2 UNSET SECURE;
   ```

> For more details, see [Convert a secure view in a share to a non-secure view](#label-sharing-non-secure-view-alter).

## Convert a secure view in a share to a non-secure view

If you want to convert an existing secure view into a view, you can do
that before or after granting the view to a share.

To convert an existing secure view in a share to a view, the following
must be true:

- The secure view must only be granted to shares that are
  [configured to allow sharing non-secure objects](#label-sharing-non-secure-objects-create).
- The secure view cannot be granted to:
  - Database roles granted to shares that do not allow sharing non-secure
    objects.
  - Shares that do not allow sharing non-secure objects.

For example, for an existing secure view named `high_performance_view`,
unset the SECURE property:

Copy code

```
ALTER VIEW high_performance_view UNSET SECURE;
```

Alternatively, you can recreate the secure view as a view:

Copy code

```
CREATE OR REPLACE VIEW high_performance_view WITH COPY GRANTS;
```

## Limitations of sharing non-secure objects

If you plan to share objects, consider the following:

- After you create a share with the SECURE\_OBJECTS\_ONLY property set to FALSE, you cannot unset this property or set this property to TRUE.
- You can only add non-secure views to shares that have been explicitly configured to allow non-secure objects.

## Syntax for sharing non-secure views

Copy code

```
CREATE [ OR REPLACE ] SHARE <name>
[ SECURE_OBJECTS_ONLY = <boolean> ]
[ COMMENT = '<string_literal>' ]
```

### Required Parameters

`name`
:   Specifies the identifier for the share;
    must be unique for the account in which the share is created.

    In addition, the identifier must start with an alphabetic character
    and cannot contain spaces or special characters unless the entire
    identifier string is enclosed in double quotes. For example, `"My object"`.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information about identifier requirements, see [Identifier requirements](/sql-reference/identifiers-syntax).

### Optional Parameters

`SECURE_OBJECTS_ONLY = boolean`
:   Specifies whether allow granting only secure objects,
    or also allow granting non-secure objects to the share.

    Default: true

`COMMENT = 'string_literal'`
:   Specifies a comment for the share.

    Default: No value

### Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE SHARE | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to additional roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

For more information about access control requirements for Snowflake
Secure Data Sharing specifically, see
[Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

### Usage notes

- You cannot see the value of the SECURE\_OBJECTS\_ONLY property when you
  run [SHOW SHARES](/sql-reference/sql/show-shares). Use the COMMENT property to note the
  value of the SECURE\_OBJECTS\_ONLY property.
- The existing notes for [CREATE SHARE](/sql-reference/sql/create-share) also apply.

### Examples

For an example on how to create a share with non-secure views, see [Create a share that allows non-secure objects](#label-sharing-non-secure-objects-create).

For an example using ALTER SHARE,
see [Convert an existing share to allow sharing non-secure views](#label-sharing-non-secure-objects-alter).
