# Declarative Native App command reference

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

The following commands include new parameters to support creating and publishing application packages:

- [CREATE APPLICATION PACKAGE](#label-dsna-create-application-package)
- [ALTER APPLICATION PACKAGE](#label-dsna-alter-application-package)
- [GRANT IMPORTED PRIVILEGES ON APPLICATION](/developer-guide/declarative-sharing/consumer/install#label-dsna-share-access-to-all-data)

## CREATE APPLICATION PACKAGE

The [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package)
command supports a new optional parameter, `TYPE = DATA`, which specifies that the app will be a Declarative Native App.

### Syntax

Copy code

```
CREATE APPLICATION PACKAGE [ IF NOT EXISTS ] <name> TYPE = DATA
```

New optional parameter:

`TYPE = [ DATA | NATIVE ]`
:   Specifies which type of application package to create:

    - `DATA`: indicates that the application package will contain a Declarative Native App.
    - `NATIVE`: indicates that the application package will contain a Snowflake Native App. This is the default value.

    After you specify an application package type, you cannot use ALTER APPLICATION PACKAGE to change the type later.

    When `TYPE = DATA` is specified, the other parameters in this command, such as DATA\_RETENTION\_TIME\_IN\_DAYS and COMMENT, are not supported.

    This parameter requires a [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) with the CREATE APPLICATION PACKAGE and CREATE DATABASE [privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges).

    The creator of the application package is automatically granted the OWNERSHIP privilege on that application package.

## ALTER APPLICATION PACKAGE

The [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package) command
supports the following new optional parameters to support creating and publishing Declarative Native Apps. These new parameters are not supported for Snowflake Native Apps.

### Syntax

Copy code

```
ALTER APPLICATION PACKAGE <name>
[ ADD LIVE VERSION
| ADD VERSION FROM @<STAGE>/<path>
| BUILD
| COMMIT
| RELEASE [LIVE VERSION]
| ABORT LIVE VERSION ]
[COMMENT = 'string_literal']
```

### New optional parameters

`ADD LIVE VERSION`
:   Create a live version of the application package that can be edited. This live version is used to add or update files, such as the manifest file and workspace files.

`ADD VERSION FROM @<STAGE>/<path>`
:   Creates a live version of the application package based on files from a [stage](/user-guide/data-load-local-file-system-stage). This method is useful if you have a set of files that you want to include in the application package, and you want to add them all at once.

Note

If you iterate on the files after creating the live version, you’ll need to make the same changes to the files on the stage to keep future versions consistent.

`BUILD`
:   Builds the app, but doesn’t commit it. Use this command to validate the manifest
    file and to continue working on the application package.

`COMMIT`
:   Builds the app, commits it for publishing, but doesn’t release it.

    The commit process prepares the application package for publishing by adding an
    internal version number, and makes the application package immutable.

`RELEASE`
:   Releases a committed version of the app to the Snowflake Marketplace.

`RELEASE LIVE VERSION`
:   Builds the app, commits it for publishing, and releases it to the Snowflake Marketplace.

    Equivalent to running the BUILD, COMMIT, and RELEASE commands in sequence.

`ABORT LIVE VERSION`
:   Removes the LIVE version of the application package. Restores the application package to the last committed version.

### Existing parameters

These parameters are supported for both Declarative Native Apps and Snowflake Native Apps.

`<name>`
:   Specifies the identifier for the application package.

    If the identifier contains spaces, special characters, or mixed-case characters,
    the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`COMMENT = 'string_literal'`
:   Optional: Adds a comment or overwrites an existing comment for the app version. This comment is displayed in SHOW APPLICATION PACKAGES.

### Access control requirements

This command requires a role with the OWNERSHIP privilege for the application package.

### Examples

- Create a new application package:

  Copy code

  ```
  CREATE APPLICATION PACKAGE market_data_app TYPE = DATA;
  ```
- Create a live version of the application package that can be edited:

  Copy code

  ```
  ALTER APPLICATION PACKAGE market_data_app
    ADD LIVE VERSION
    COMMENT = 'Market views for Northern region';
  ```
- Create a new version of the application package from an existing staged application package:

  Copy code

  ```
  ALTER APPLICATION PACKAGE market_data_app
    ADD VERSION FROM @my_stage/market_data_app_v1;
  ```
- Build the application package, but don’t commit it:

  Copy code

  ```
  ALTER APPLICATION PACKAGE market_data_app BUILD;
  ```
- Build and commit the application package for publishing, but don’t release it:

  Copy code

  ```
  ALTER APPLICATION PACKAGE market_data_app
    COMMIT
    COMMENT = 'Market views for North and East regions';
  ```
- Release the application package to the Snowflake Marketplace:

  Copy code

  ```
  ALTER APPLICATION PACKAGE market_data_app RELEASE;
  ```
- Build, commit, and release the live version of the application package to the Snowflake Marketplace:

  Copy code

  ```
  ALTER APPLICATION PACKAGE market_data_app RELEASE LIVE VERSION
    COMMENT = 'Market views for North, East, and West regions';
  ```
- After adding a live version of the app and editing it, stop editing and restore to the last committed version:

  Copy code

  ```
  ALTER APPLICATION PACKAGE market_data_app ABORT LIVE VERSION;
  ```

## GRANT IMPORTED PRIVILEGES ON APPLICATION

The [GRANT IMPORTED PRIVILEGES](/sql-reference/sql/grant-privilege) command supports a new optional parameter, `ON APPLICATION <name>`.

This command allows consumers to grant access to all of the data and views in a Declarative Native App to other members of their organization.

This command can be used on any Declarative Native App, and does not require app roles to be defined for the application package.

### Access control requirements

This command requires a role with the OWNERSHIP privilege for the installed app.

### Syntax

Copy code

```
GRANT IMPORTED PRIVILEGES ON APPLICATION <name> TO ROLE <role_name>;
```

### Example

Copy code

```
GRANT IMPORTED PRIVILEGES ON APPLICATION market_data_app TO ROLE marketing_team_east;
```
