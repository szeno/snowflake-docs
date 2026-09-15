# DESCRIBE APPLICATION PACKAGE

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

Displays information about an application package.

DESCRIBE can be abbreviated to DESC.

See also:
:   [ALTER APPLICATION PACKAGE](/sql-reference/sql/alter-application-package),
    [CREATE APPLICATION PACKAGE](/sql-reference/sql/create-application-package),
    [DROP APPLICATION PACKAGE](/sql-reference/sql/drop-application-package),
    [SHOW APPLICATION PACKAGES](/sql-reference/sql/show-application-packages)

## Syntax

Copy code

```
DESC[RIBE] APPLICATION PACKAGE <name>
```

## Parameters

`name`
:   Specifies the [identifier](/sql-reference/identifiers) of the application package to
    describe.

## Output

The command displays properties of an application package in the following columns:

| Column | Description |
| --- | --- |
| `property` | The name of the property of the application package. This column can include the properties listed in the following table. |
| `value` | The value assigned to the property of the application package. |

Expand

Show lessSee more

The `property` column can include the following properties of an application package:

| Property | Description |
| --- | --- |
| `name` | The name of the application package. |
| `created_on` | The timestamp when the application package was created. |
| `distribution` | The distribution method of the application package. Valid values are `INTERNAL` and `EXTERNAL`. |
| `multiple_instances` | Indicates whether multiple instances of the application package can be installed in a single account. Valid values are `TRUE` and `FALSE`. |
| `uses_container_services` | Indicates whether the application package uses Snowpark Container Services. Valid values are `TRUE` and `FALSE`. |
| `comment` | A description of the application package. |
| `owner` | The owner of the application package. |
| `release-channels` | Indicates whether release channels are enabled for the application package. Valid values are `ENABLED` and `DISABLED`. |
| `listing_auto_refresh` | Indicates whether Cross-Cloud Auto-Fulfillment is enabled for the application package. Valid values are `TRUE` and `FALSE`. |

Expand

Show lessSee more

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

Describe the properties of an application package:

Copy code

```
DESC APPLICATION PACKAGE hello_snowflake_app;
```

```
+------------------------------------+-------------------------------+
| property                           | value                         |
|------------------------------------+-------------------------------|
| name                               | hello_snowflake_app_package   |
| created_on                         | 2025-07-14 14:29:56.927 -0700 |
| distribution                       | INTERNAL                      |
| multiple_instances                 | FALSE                         |
| uses_container_services            | FALSE                         |
| comment                            | My awesome app                |
| owner                              | APP_DEV_ROLE                  |
| release_channels                   | ENABLED                       |
| listing_auto_refresh               | DISABLED                      |
+------------------------------------+-------------------------------+
```
