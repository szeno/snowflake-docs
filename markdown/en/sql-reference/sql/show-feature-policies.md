# SHOW FEATURE POLICIES

Lists the [feature policies](/user-guide/feature-policies) for which you have access privileges.

See also:
:   [CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy) , [ALTER FEATURE POLICY](/sql-reference/sql/alter-feature-policy), [DESCRIBE FEATURE POLICY](/sql-reference/sql/desc-feature-policy), [DROP FEATURE POLICY](/sql-reference/sql/drop-feature-policy)

## Syntax

Copy code

```
SHOW FEATURE POLICIES
  [ IN
    {
      ACCOUNT                                        |
      APPLICATION {app_name}                         |
      APPLICATION PACKAGE {app_package_name}         |
      DATABASE {database_name}                       |
      SCHEMA {schema_name}                           |
    }
  ]

SHOW FEATURE POLICIES ON ACCOUNT

SHOW FEATURE POLICIES ON APPLICATION <application_name>

SHOW FEATURE POLICIES ON DATABASE <database_name>
```

## Parameters

`[ IN ... ]`
:   Optionally specifies the scope of the command. Specify one of the following:

    `ACCOUNT`
    :   Returns information about feature policies created in the specified account.

    `APPLICATION app_name`
    :   Returns information about feature policies created in the specified app.

    `APPLICATION PACKAGE app_package_name`
    :   Returns information about feature policies created in the specified application package.

    `DATABASE database_name`
    :   Returns information about feature policies created in the specified database.

    `SCHEMA schema_name`
    :   Returns information about feature policies created in the specified schema.

`ON ACCOUNT`
:   Shows the feature policies that have been applied to the current account.

`ON APPLICATION app_name`
:   Shows the feature policies that have been applied on the specified app. This command also
    displays feature policies that are inherited from those applied on the account.

`ON DATABASE database_name`
:   Shows the feature policies that have been applied directly to the specified database.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Feature policy | This privilege is required to use this command. |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

| Column | Description |
| --- | --- |
| `created_on` | The timestamp when the policy was created. |
| `name` | The name of the policy. |
| `database_name` | The name of the database containing the policy. |
| `schema_name` | The name of the schema containing the policy. |
| `kind` | The type of feature policy. Currently, only `FEATURE_POLICY` is supported. |
| `owner` | The role that owns the feature policy. |
| `comment` | A comment containing information about the policy. |
| `owner_role_type` | The type of the role that owns the feature policy. |
| `options` | Currently, always NULL. |

Expand

Show lessSee more

## Examples

The following example lists the feature policies that you have the privileges to view
in the current account:

Copy code

```
SHOW FEATURE POLICIES;
```

The following example lists the feature policies that you have the privileges to view
in an app named `hello_snowflake_app`:

Copy code

```
SHOW FEATURE POLICIES IN APPLICATION hello_snowflake_app;
```

The following example lists the feature policies that have been applied on the current account:

Copy code

```
SHOW FEATURE POLICIES ON ACCOUNT
```

The following example lists the feature policies that have been applied directly to a database
named `my_db`:

Copy code

```
SHOW FEATURE POLICIES ON DATABASE my_db;
```
