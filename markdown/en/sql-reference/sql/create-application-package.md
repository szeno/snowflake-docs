# CREATE APPLICATION PACKAGE

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Creates a new application package that contains the data content and application logic of
Snowflake Native App. An application package contains the following information about an app:

- The version and patch number of the app.
- The data content that is available to the application.
- The setup script of the app.
- The manifest file of the app.

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package), [DROP APPLICATION PACKAGE](/sql-reference/sql/drop-application-package), [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages)

## Syntax

Copy code

```
CREATE APPLICATION PACKAGE [ IF NOT EXISTS ] <name>
  [ DATA_RETENTION_TIME_IN_DAYS = <integer> ]
  [ MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer> ]
  [ DEFAULT_DDL_COLLATION = '<collation_specification>' ]
  [ COMMENT = '<string_literal>' ]
  [ [ WITH ] TAG ( <tag_name> = '<tag_value>' [ , ... ] ) ]
  [ DISTRIBUTION = { INTERNAL | EXTERNAL } ]
  [ LISTING_AUTO_REFRESH = { TRUE | FALSE } ]
  [ MULTIPLE_INSTANCES = TRUE ]
  [ ENABLE_RELEASE_CHANNELS = { TRUE | FALSE } ]
```

## Required parameters

`name`
:   Specifies the identifier for the application package; must be unique for your account.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the entire identifier
    string is enclosed in double quotes (e.g. `"My object"`). Identifiers enclosed in double quotes are also case-sensitive.

    For more details, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`DATA_RETENTION_TIME_IN_DAYS = integer`
:   Specifies the default Time Travel retention time for all schemas created in the application package.

    Note

    CLONE and UNDROP are not supported for APPLICATION PACKAGE objects. Despite these operations being listed in the parameter description for consistency with other database objects, neither operation can be performed on an application package.

    For more details, see [Understanding & using Time Travel](/user-guide/data-time-travel).

    For a detailed description of this object-level parameter, as well as more information about object parameters, see [Parameters](/sql-reference/parameters).

    Values:

    > - Standard Edition: `0` or `1`
    > - Enterprise Edition:
    >   - `0` to `90` for permanent databases

    Default:

    > - Standard Edition: `1`
    > - Enterprise Edition (or higher): `1` (unless a different default value was specified at the account level)

    Note

    A value of `0` disables Time Travel for the database.

`MAX_DATA_EXTENSION_TIME_IN_DAYS = integer`
:   Object parameter that specifies the maximum number of days for which Snowflake can extend the data retention period for tables in the application package to prevent streams on the tables from becoming stale.

    For a detailed description of this parameter, see [MAX\_DATA\_EXTENSION\_TIME\_IN\_DAYS](/sql-reference/parameters#label-max-data-extension-time-in-days).

`DEFAULT_DDL_COLLATION = 'collation_specification'`
:   Specifies a default [collation specification](/sql-reference/collation#label-collation-specification) for all schemas and tables added to the application package. The default
    can be overridden at the schema and individual table level.

    For more details about the parameter, see [DEFAULT\_DDL\_COLLATION](/sql-reference/parameters#label-default-ddl-collation).

`COMMENT = 'string_literal'`
:   Specifies a comment for the application package.

    Default: No value

`TAG ( tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ] )`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

`DISTRIBUTION = { INTERNAL | EXTERNAL }`
:   Specifies the type of listing a provider can create when using the application package as the data product of a listing.

    - `INTERNAL` indicates that a provider can only create a private listing within the same organization
      where the application package was created. The automated security scan is not performed
      when the DISTRIBUTION property is set to INTERNAL.
    - `EXTERNAL` indicates that a provider can create listings outside the same organization where
      the application package was created.

    See [Run the automated security scan](/developer-guide/native-apps/security-run-scan) for information on setting the DISTRIBUTION property and
    the automated security scan.

    Note

    Setting the `DISTRIBUTION` parameter to `EXTERNAL` triggers an automated security review for each
    active version and patch defined in the application package.

    The following restrictions apply until the automated security review has a status of `APPROVED`:

    - You cannot set a release directive for a version or patch.
    - You cannot publish a listing for the application package.

`LISTING_AUTO_REFRESH = { TRUE | FALSE}`
:   When set to TRUE, initiates replication to all remote regions when there is a change to the release directive of the application package. When a release directive changes, the application package does not wait for the Cross-Cloud Auto-Fulfillment schedule.

`MULTIPLE_INSTANCES = TRUE`
:   Enables the consumer to install multiple instances of an app from the application package. This property cannot be
    set for applications packages that are included in a trial or paid listing.

    When multiple instances are allowed, consumers can install a maximum of 30 instances of an app in their account.

    Caution

    After this property is set to `TRUE`, it cannot be set to `FALSE` or unset later.

`ENABLE_RELEASE_CHANNELS = { TRUE | FALSE }`
:   Enables or disables [release channels](/developer-guide/native-apps/release-channels) for the application package.

    - `TRUE` enables release channels. This is the default. You can also omit this parameter; release channels are enabled automatically.
    - `FALSE` disables release channels. Specify this value at create time to opt out of release channels and use the legacy version and patch management workflow instead.

    Caution

    After this property is set to `TRUE`, it cannot be set to `FALSE` or unset later.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE APPLICATION PACKAGE | Account | Only the ACCOUNTADMIN role has this privilege by default. The privilege can be granted to other roles as needed. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To create an application package, the caller must have the CREATE APPLICATION PACKAGE privilege on the account.
- There are no restrictions on the types of objects that may reside in the application package or what roles (database or account level)
  that may own those objects.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Copy code

```
CREATE APPLICATION PACKAGE hello_snowflake_package;
```

```
+-----------------------------------------------------------------------+
| status                                                                |
|-----------------------------------------------------------------------|
| Application Package 'hello_snowflake_package' created successfully.   |
+-----------------------------------------------------------------------+
```
